from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import ContentSchedule, GeneratedContent, ContentStatus, PublishFrequency, BlogCategory
from app.services.content_scheduler_service import ContentSchedulerService
from datetime import datetime

auto_content = Blueprint('auto_content', __name__, url_prefix='/admin/auto-content')

@auto_content.route('/')
@login_required
def index():
    """Отображает главную страницу управления автоматическим контентом"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем все расписания
    schedules = ContentSchedule.query.order_by(ContentSchedule.created_at.desc()).all()
    
    # Статистика
    total_posts = GeneratedContent.query.filter_by(status=ContentStatus.PUBLISHED).count()
    failed_generations = GeneratedContent.query.filter_by(status=ContentStatus.FAILED).count()
    pending_generations = GeneratedContent.query.filter_by(status=ContentStatus.PLANNED).count()
    
    return render_template('admin/auto_content/index.html',
                          schedules=schedules,
                          total_posts=total_posts,
                          failed_generations=failed_generations,
                          pending_generations=pending_generations)

@auto_content.route('/schedules/create', methods=['GET', 'POST'])
@login_required
def create_schedule():
    """Создает новое расписание для генерации контента"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем все категории для выбора
    categories = BlogCategory.query.all()
    
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        topic_area = request.form.get('topic_area')
        description = request.form.get('description')
        keywords = request.form.get('keywords')
        frequency = request.form.get('frequency')
        category_id = request.form.get('category_id', type=int)
        
        # Создаем новое расписание
        schedule = ContentSchedule(
            name=name,
            topic_area=topic_area,
            description=description,
            keywords=keywords,
            frequency=PublishFrequency(frequency),
            category_id=category_id,
            author_id=current_user.id,
            next_generation_date=datetime.utcnow()  # Установим текущую дату, чтобы первая генерация произошла сразу
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        flash('Расписание успешно создано', 'success')
        return redirect(url_for('auto_content.index'))
    
    return render_template('admin/auto_content/create_schedule.html',
                          categories=categories,
                          frequencies=[f.value for f in PublishFrequency])

@auto_content.route('/schedules/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_schedule(id):
    """Редактирует существующее расписание"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем расписание
    schedule = ContentSchedule.query.get_or_404(id)
    
    # Получаем все категории для выбора
    categories = BlogCategory.query.all()
    
    if request.method == 'POST':
        # Получаем данные из формы
        schedule.name = request.form.get('name')
        schedule.topic_area = request.form.get('topic_area')
        schedule.description = request.form.get('description')
        schedule.keywords = request.form.get('keywords')
        schedule.frequency = PublishFrequency(request.form.get('frequency'))
        schedule.category_id = request.form.get('category_id', type=int)
        schedule.enabled = 'enabled' in request.form
        
        db.session.commit()
        
        flash('Расписание успешно обновлено', 'success')
        return redirect(url_for('auto_content.index'))
    
    return render_template('admin/auto_content/edit_schedule.html',
                          schedule=schedule,
                          categories=categories,
                          frequencies=[f.value for f in PublishFrequency])

@auto_content.route('/schedules/<int:id>/delete', methods=['POST'])
@login_required
def delete_schedule(id):
    """Удаляет расписание"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем расписание
    schedule = ContentSchedule.query.get_or_404(id)
    
    db.session.delete(schedule)
    db.session.commit()
    
    flash('Расписание успешно удалено', 'success')
    return redirect(url_for('auto_content.index'))

@auto_content.route('/schedules/<int:id>/generate', methods=['POST'])
@login_required
def generate_now(id):
    """Немедленно генерирует контент для выбранного расписания"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем расписание
    schedule = ContentSchedule.query.get_or_404(id)
    
    # Генерируем контент
    generated_content = ContentSchedulerService.generate_content(schedule)
    
    if generated_content and generated_content.status == ContentStatus.PUBLISHED:
        # Публикуем сгенерированный контент
        en_post, de_post = ContentSchedulerService.publish_content(generated_content)
        
        if en_post and de_post:
            flash('Контент успешно сгенерирован и опубликован', 'success')
        else:
            flash('Контент сгенерирован, но возникла ошибка при публикации', 'warning')
    else:
        flash('Произошла ошибка при генерации контента', 'danger')
    
    return redirect(url_for('auto_content.index'))

@auto_content.route('/content')
@login_required
def generated_content():
    """Отображает список сгенерированного контента"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем весь сгенерированный контент
    content = GeneratedContent.query.order_by(GeneratedContent.created_at.desc()).all()
    
    return render_template('admin/auto_content/generated_content.html', content=content)

@auto_content.route('/content/<int:id>')
@login_required
def view_content(id):
    """Просмотр сгенерированного контента"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем контент
    content = GeneratedContent.query.get_or_404(id)
    
    return render_template('admin/auto_content/view_content.html', content=content)

@auto_content.route('/content/<int:id>/publish', methods=['POST'])
@login_required
def publish_content(id):
    """Публикует сгенерированный контент"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем контент
    content = GeneratedContent.query.get_or_404(id)
    
    # Публикуем контент
    en_post, de_post = ContentSchedulerService.publish_content(content)
    
    if en_post and de_post:
        flash('Контент успешно опубликован', 'success')
    else:
        flash('Произошла ошибка при публикации контента', 'danger')
    
    return redirect(url_for('auto_content.generated_content'))
