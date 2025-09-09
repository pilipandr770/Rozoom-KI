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
        
        # Определяем автора - если это AdminUser, найдем соответствующего User
        from app.auth import AdminUser
        from app.models import User
        
        if isinstance(current_user, AdminUser):
            # Ищем User с таким же email как у AdminUser
            author = User.query.filter_by(email=current_user.email).first()
            if not author:
                # Создаем User на основе AdminUser
                author = User(
                    email=current_user.email,
                    name=current_user.username,
                    is_admin=True
                )
                db.session.add(author)
                db.session.flush()  # Получаем ID без коммита
        else:
            author = current_user
        
        # Создаем новое расписание
        schedule = ContentSchedule(
            name=name,
            topic_area=topic_area,
            description=description,
            keywords=keywords,
            frequency=PublishFrequency(frequency),
            category_id=category_id,
            author_id=author.id,
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

@auto_content.route('/test-openai', methods=['GET'])
@login_required
def test_openai():
    """Тестирует подключение к OpenAI API"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))

    from app.services.openai_service import OpenAIService
    import logging

    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting OpenAI API test from web interface")

        # Создаем сервис
        openai_service = OpenAIService()
        logger.info("OpenAI service created successfully")

        # Тестируем подключение
        connection_ok, message = openai_service.test_connection()
        logger.info(f"OpenAI connection test result: {connection_ok}, message: {message}")

        if connection_ok:
            flash(f'✅ {message}', 'success')
        else:
            flash(f'❌ {message}', 'danger')

    except Exception as e:
        logger.error(f"Error testing OpenAI API: {str(e)}")
        flash(f'❌ Ошибка при тестировании OpenAI API: {str(e)}', 'danger')

    return redirect(url_for('auto_content.index'))

@auto_content.route('/system-status', methods=['GET'])
@login_required
def system_status():
    """Показывает статус системы и переменных окружения"""
    # Проверяем, является ли пользователь администратором
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице', 'danger')
        return redirect(url_for('main.index'))

    import os
    from app.services.openai_service import OpenAIService

    status_info = {
        'environment': {},
        'database': {},
        'openai': {},
        'mail': {},
        'app_config': {}
    }

    # Переменные окружения
    status_info['environment'] = {
        'FLASK_ENV': os.getenv('FLASK_ENV', 'не установлена'),
        'FLASK_APP': os.getenv('FLASK_APP', 'не установлена'),
    }

    # База данных
    database_url = os.getenv('DATABASE_URL', 'не установлена')
    status_info['database'] = {
        'DATABASE_URL': database_url[:50] + '...' if database_url != 'не установлена' else database_url,
        'SSL_MODE': 'sslmode' in database_url if database_url != 'не установлена' else False
    }

    # OpenAI
    openai_key = os.getenv('OPENAI_API_KEY', 'не установлена')
    status_info['openai'] = {
        'API_KEY_SET': openai_key != 'не установлена',
        'API_KEY_LENGTH': len(openai_key) if openai_key != 'не установлена' else 0,
        'API_KEY_FORMAT': 'sk-proj-' if openai_key.startswith('sk-proj-') else 'sk-' if openai_key.startswith('sk-') else 'неизвестный' if openai_key != 'не установлена' else 'не установлен',
        'FALLBACK_ENABLED': os.getenv('OPENAI_FALLBACK_ENABLED', 'true').lower() in ('true', 'yes', '1')
    }

    # Почта
    status_info['mail'] = {
        'MAIL_SERVER': 'установлен' if os.getenv('MAIL_SERVER') else 'не установлен',
        'MAIL_PORT': os.getenv('MAIL_PORT', 'не установлен'),
        'MAIL_USERNAME': 'установлен' if os.getenv('MAIL_USERNAME') else 'не установлен',
    }

    # Конфигурация приложения
    status_info['app_config'] = {
        'SECRET_KEY': 'установлен' if current_app.config.get('SECRET_KEY') else 'не установлен',
        'DATABASE_URI': 'установлен' if current_app.config.get('SQLALCHEMY_DATABASE_URI') else 'не установлен',
        'OPENAI_API_KEY': 'установлен' if current_app.config.get('OPENAI_API_KEY') else 'не установлен'
    }

    # Тест OpenAI
    openai_test = {'success': False, 'message': 'API ключ не доступен'}
    if current_app.config.get('OPENAI_API_KEY'):
        try:
            service = OpenAIService()
            success, message = service.test_connection()
            openai_test = {'success': success, 'message': message}
        except Exception as e:
            openai_test = {'success': False, 'message': f'Ошибка: {str(e)}'}

    return render_template('admin/auto_content/system_status.html',
                          status_info=status_info,
                          openai_test=openai_test)
