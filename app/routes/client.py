from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.project import Project, ProjectTask, ProjectUpdate
from app.models.tech_spec_submission import TechSpecSubmission
from app import db

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.before_request
def check_authentication():
    """Проверка авторизации для всех маршрутов клиентской панели"""
    if not current_user.is_authenticated:
        flash('Please log in to access your client dashboard.', 'warning')
        return redirect(url_for('pages.login', next=request.url))

@client_bp.route('/')
@client_bp.route('/dashboard')
@login_required
def dashboard():
    """Личный кабинет клиента"""
    # Получаем все проекты клиента
    projects = Project.query.filter_by(client_id=current_user.id).all()
    
    # Добавляем вспомогательные свойства для отображения бейджей статуса
    status_map = {
        'planning': 'bg-info',
        'development': 'bg-primary',
        'testing': 'bg-warning',
        'review': 'bg-secondary',
        'completed': 'bg-success',
        'on_hold': 'bg-danger',
        'new': 'bg-info',
        'in_progress': 'bg-primary',
        'blocked': 'bg-danger',
        'archived': 'bg-secondary'
    }
    status_display = {
        'planning': 'Planning',
        'development': 'Development',
        'testing': 'Testing',
        'review': 'Review',
        'completed': 'Completed',
        'on_hold': 'On Hold',
        'new': 'New',
        'in_progress': 'In Progress',
        'blocked': 'Blocked',
        'archived': 'Archived'
    }
    for p in projects:
        p.status_badge_class = status_map.get(p.status, 'bg-secondary')
        p.status_display = status_display.get(p.status, p.status.title() if p.status else '—')
    
    # Получаем все заявки клиента
    submissions = TechSpecSubmission.query.filter_by(client_id=current_user.id).all()
    
    # Получаем последние обновления всех проектов
    project_ids = [project.id for project in projects]
    recent_updates = []
    if project_ids:
        recent_updates = ProjectUpdate.query.filter(
            ProjectUpdate.project_id.in_(project_ids)
        ).order_by(ProjectUpdate.created_at.desc()).limit(5).all()
    
    return render_template('client/dashboard.html', 
                          projects=projects, 
                          submissions=submissions,
                          recent_updates=recent_updates)

@client_bp.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    """Просмотр проекта клиентом"""
    project = Project.query.get_or_404(project_id)
    
    # Проверяем, что проект принадлежит текущему пользователю
    if project.client_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('client.dashboard'))
    
    tasks = ProjectTask.query.filter_by(project_id=project_id).all()
    updates = ProjectUpdate.query.filter_by(project_id=project_id).order_by(ProjectUpdate.created_at.desc()).all()
    
    # Добавляем вспомогательные свойства для отображения в шаблоне
    status_map = {
        'planning': 'bg-info',
        'development': 'bg-primary',
        'testing': 'bg-warning',
        'review': 'bg-secondary',
        'completed': 'bg-success',
        'on_hold': 'bg-danger'
    }
    project.status_badge_class = status_map.get(project.status, 'bg-secondary')
    
    status_display = {
        'planning': 'Planning',
        'development': 'Development',
        'testing': 'Testing',
        'review': 'Review',
        'completed': 'Completed',
        'on_hold': 'On Hold'
    }
    project.status_display = status_display.get(project.status, project.status.title())
    
    # Для задач
    for task in tasks:
        task_status_map = {
            'not_started': 'bg-secondary',
            'in_progress': 'bg-primary',
            'completed': 'bg-success',
            'blocked': 'bg-danger'
        }
        task.status_badge_class = task_status_map.get(task.status, 'bg-secondary')
        
        task_status_display = {
            'not_started': 'Not Started',
            'in_progress': 'In Progress',
            'completed': 'Completed',
            'blocked': 'Blocked'
        }
        task.status_display = task_status_display.get(task.status, task.status.title())
        
        # Порядок для сортировки
        status_order = {
            'not_started': 1,
            'in_progress': 0, 
            'blocked': 2,
            'completed': 3
        }
        task.status_order = status_order.get(task.status, 99)
    
    return render_template('client/project_detail.html', 
                          project=project, 
                          tasks=tasks, 
                          updates=updates)

@client_bp.route('/submission/<int:submission_id>')
@login_required
def view_submission(submission_id):
    """Просмотр заявки клиентом"""
    submission = TechSpecSubmission.query.get_or_404(submission_id)
    
    # Проверяем, что заявка принадлежит текущему пользователю
    if submission.client_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('client.dashboard'))
    
    return render_template('client/submission.html', submission=submission)

@client_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Профиль клиента с возможностью обновления"""
    if request.method == 'POST':
        # Обновляем профиль
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        current_user.company = request.form.get('company')
        
        # Обновляем пароль, если указан новый
        password = request.form.get('password')
        if password and len(password) >= 8:
            current_user.set_password(password)
        
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('client.profile'))
    
    return render_template('client/profile.html')

@client_bp.route('/api/projects')
@login_required
def api_get_projects():
    """API для получения списка проектов для PM агента"""
    projects = Project.query.filter_by(client_id=current_user.id).all()
    
    projects_data = []
    for project in projects:
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'status': project.status,
            'progress': project.progress,
            'description': project.description,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'estimated_completion': project.estimated_completion_date.strftime('%Y-%m-%d') if project.estimated_completion_date else None
        })
    
    return jsonify({
        'projects': projects_data
    })

@client_bp.route('/api/project/<int:project_id>/updates')
@login_required
def api_get_project_updates(project_id):
    """API для получения обновлений проекта для PM агента"""
    project = Project.query.get_or_404(project_id)
    
    # Проверяем, что проект принадлежит текущему пользователю
    if project.client_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    updates = ProjectUpdate.query.filter_by(project_id=project_id).order_by(ProjectUpdate.created_at.desc()).all()
    
    updates_data = []
    for update in updates:
        updates_data.append({
            'id': update.id,
            'title': update.title,
            'message': update.message,
            'created_at': update.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'project': {
            'id': project.id,
            'title': project.title
        },
        'updates': updates_data
    })
