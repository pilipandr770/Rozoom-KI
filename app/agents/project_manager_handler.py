from flask import current_app
from app import db
from app.models.project import Project, ProjectTask, ProjectUpdate
from app.models.base import User
from app.models.tech_spec_submission import TechSpecSubmission
from typing import Dict, List

def handle_pm_request(message: str, metadata: Dict) -> Dict:
    """
    Обрабатывает запросы к агенту ПМ
    """
    if 'user_id' not in metadata or not metadata['user_id']:
        return {
            'answer': _get_not_logged_in_message(metadata.get('language', 'en')),
            'agent': 'pm'
        }
    
    user_id = metadata['user_id']
    user = db.session.get(User, user_id)
    
    if not user:
        return {
            'answer': _get_not_logged_in_message(metadata.get('language', 'en')),
            'agent': 'pm'
        }
    
    # Обрабатываем сообщение от клиента
    lowered_message = message.lower()
    
    # Запрос на просмотр проектов
    if any(keyword in lowered_message for keyword in ['project', 'projects', 'status', 'progress', 'проект', 'проекты', 'статус', 'прогресс']):
        return _handle_project_status_request(user, metadata)
    
    # Запрос на последние обновления
    if any(keyword in lowered_message for keyword in ['update', 'updates', 'latest', 'new', 'обновление', 'обновления', 'последнее', 'новое']):
        return _handle_project_updates_request(user, metadata)
    
    # Запрос конкретного проекта (если в сообщении упоминается название проекта)
    user_projects = Project.query.filter_by(client_id=user.id).all()
    for project in user_projects:
        if project.title.lower() in lowered_message:
            return _get_specific_project_info(project, metadata)
    
    # По умолчанию общая информация
    return {
        'answer': _get_general_welcome_message(user, metadata.get('language', 'en')),
        'agent': 'pm'
    }

def _get_not_logged_in_message(language: str) -> str:
    """Сообщение для неавторизованных пользователей"""
    messages = {
        'en': "I can help you track your project status, but it looks like you're not logged in. Please log in to access your project information.",
        'ru': "Я могу помочь вам отслеживать статус проекта, но похоже, вы не вошли в систему. Пожалуйста, войдите, чтобы получить доступ к информации о вашем проекте.",
        'de': "Ich kann Ihnen helfen, Ihren Projektstatus zu verfolgen, aber es sieht so aus, als wären Sie nicht angemeldet. Bitte melden Sie sich an, um auf Ihre Projektinformationen zuzugreifen.",
        'uk': "Я можу допомогти вам відстежувати статус проекту, але схоже, ви не увійшли в систему. Будь ласка, увійдіть, щоб отримати доступ до інформації про ваш проект."
    }
    return messages.get(language, messages['en'])

def _get_general_welcome_message(user: User, language: str) -> str:
    """Приветственное сообщение для авторизованного пользователя с обзором его проектов"""
    projects = Project.query.filter_by(client_id=user.id).all()
    
    if not projects:
        messages = {
            'en': f"Hello, {user.name}! You don't have any active projects yet. If you've submitted a technical specification, our team is reviewing it. If you have any questions, feel free to ask!",
            'ru': f"Здравствуйте, {user.name}! У вас пока нет активных проектов. Если вы отправили техническое задание, наша команда рассматривает его. Если у вас есть вопросы, не стесняйтесь спрашивать!",
            'de': f"Hallo, {user.name}! Sie haben noch keine aktiven Projekte. Wenn Sie eine technische Spezifikation eingereicht haben, prüft unser Team diese gerade. Wenn Sie Fragen haben, fragen Sie gerne!",
            'uk': f"Вітаю, {user.name}! У вас поки немає активних проектів. Якщо ви надіслали технічне завдання, наша команда розглядає його. Якщо у вас є питання, не соромтеся запитувати!"
        }
        return messages.get(language, messages['en'])
    
    # Формируем обзор проектов
    projects_info = []
    for project in projects:
        projects_info.append({
            'title': project.title,
            'status': project.status,
            'progress': project.progress
        })
    
    project_list_str = "\n".join([f"- {p['title']}: {p['status'].upper()} ({p['progress']}% complete)" for p in projects_info])
    
    messages = {
        'en': f"Hello, {user.name}! Here's an overview of your projects:\n\n{project_list_str}\n\nYou can ask me about any specific project or request updates.",
        'ru': f"Здравствуйте, {user.name}! Вот обзор ваших проектов:\n\n{project_list_str}\n\nВы можете спросить меня о любом конкретном проекте или запросить обновления.",
        'de': f"Hallo, {user.name}! Hier ist ein Überblick über Ihre Projekte:\n\n{project_list_str}\n\nSie können mich nach einem bestimmten Projekt fragen oder Updates anfordern.",
        'uk': f"Вітаю, {user.name}! Ось огляд ваших проектів:\n\n{project_list_str}\n\nВи можете запитати мене про будь-який конкретний проект або запросити оновлення."
    }
    return messages.get(language, messages['en'])

def _handle_project_status_request(user: User, metadata: Dict) -> Dict:
    """Обработка запроса о статусе проектов"""
    projects = Project.query.filter_by(client_id=user.id).all()
    language = metadata.get('language', 'en')
    
    if not projects:
        messages = {
            'en': "You don't have any active projects at the moment.",
            'ru': "У вас нет активных проектов на данный момент.",
            'de': "Sie haben derzeit keine aktiven Projekte.",
            'uk': "У вас немає активних проектів на даний момент."
        }
        return {
            'answer': messages.get(language, messages['en']),
            'agent': 'pm'
        }
    
    # Формируем детальный отчет по каждому проекту
    projects_report = []
    for project in projects:
        tasks = ProjectTask.query.filter_by(project_id=project.id).all()
        completed_tasks = sum(1 for task in tasks if task.status == 'completed')
        total_tasks = len(tasks)
        
        latest_update = ProjectUpdate.query.filter_by(project_id=project.id).order_by(ProjectUpdate.created_at.desc()).first()
        
        project_info = {
            'title': project.title,
            'status': project.status,
            'progress': project.progress,
            'tasks_info': f"{completed_tasks}/{total_tasks} tasks completed",
            'latest_update': latest_update.content if latest_update else "No updates yet."
        }
        projects_report.append(project_info)
    
    # Создаем читаемый текстовый отчет
    report_text = ""
    for i, p in enumerate(projects_report, 1):
        report_text += f"Project {i}: {p['title']}\n"
        report_text += f"Status: {p['status'].upper()}\n"
        report_text += f"Progress: {p['progress']}%\n"
        report_text += f"Tasks: {p['tasks_info']}\n"
        report_text += f"Latest update: {p['latest_update']}\n\n"
    
    messages = {
        'en': f"Here's the current status of your projects:\n\n{report_text}",
        'ru': f"Вот текущий статус ваших проектов:\n\n{report_text}",
        'de': f"Hier ist der aktuelle Status Ihrer Projekte:\n\n{report_text}",
        'uk': f"Ось поточний статус ваших проектів:\n\n{report_text}"
    }
    
    return {
        'answer': messages.get(language, messages['en']),
        'agent': 'pm'
    }

def _handle_project_updates_request(user: User, metadata: Dict) -> Dict:
    """Обработка запроса о последних обновлениях проектов"""
    language = metadata.get('language', 'en')
    
    # Получаем ID всех проектов пользователя
    projects = Project.query.filter_by(client_id=user.id).all()
    project_ids = [p.id for p in projects]
    
    if not project_ids:
        messages = {
            'en': "You don't have any active projects yet.",
            'ru': "У вас пока нет активных проектов.",
            'de': "Sie haben noch keine aktiven Projekte.",
            'uk': "У вас поки немає активних проектів."
        }
        return {
            'answer': messages.get(language, messages['en']),
            'agent': 'pm'
        }
    
    # Получаем последние обновления для всех проектов пользователя
    updates = ProjectUpdate.query.filter(
        ProjectUpdate.project_id.in_(project_ids)
    ).order_by(ProjectUpdate.created_at.desc()).limit(5).all()
    
    if not updates:
        messages = {
            'en': "There are no recent updates for your projects.",
            'ru': "Нет недавних обновлений для ваших проектов.",
            'de': "Es gibt keine aktuellen Updates für Ihre Projekte.",
            'uk': "Немає нещодавніх оновлень для ваших проектів."
        }
        return {
            'answer': messages.get(language, messages['en']),
            'agent': 'pm'
        }
    
    # Формируем отчет
    updates_text = ""
    for update in updates:
        project = next((p for p in projects if p.id == update.project_id), None)
        if project:
            updates_text += f"Project: {project.title}\n"
            updates_text += f"Update: {update.title}\n"
            updates_text += f"Details: {update.content}\n"
            updates_text += f"Date: {update.created_at.strftime('%Y-%m-%d')}\n"
            updates_text += f"{'🔔 MILESTONE' if update.is_milestone else ''}\n\n"
    
    messages = {
        'en': f"Here are the recent updates for your projects:\n\n{updates_text}",
        'ru': f"Вот последние обновления для ваших проектов:\n\n{updates_text}",
        'de': f"Hier sind die aktuellen Updates für Ihre Projekte:\n\n{updates_text}",
        'uk': f"Ось останні оновлення для ваших проектів:\n\n{updates_text}"
    }
    
    return {
        'answer': messages.get(language, messages['en']),
        'agent': 'pm'
    }

def _get_specific_project_info(project: Project, metadata: Dict) -> Dict:
    """Получение информации о конкретном проекте"""
    language = metadata.get('language', 'en')
    
    # Получаем задачи проекта
    tasks = ProjectTask.query.filter_by(project_id=project.id).all()
    completed_tasks = sum(1 for task in tasks if task.status == 'completed')
    total_tasks = len(tasks)
    
    # Получаем последние обновления
    updates = ProjectUpdate.query.filter_by(project_id=project.id).order_by(ProjectUpdate.created_at.desc()).limit(3).all()
    
    # Формируем отчет
    project_details = f"Project: {project.title}\n"
    project_details += f"Status: {project.status.upper()}\n"
    project_details += f"Progress: {project.progress}%\n"
    project_details += f"Tasks: {completed_tasks}/{total_tasks} completed\n\n"
    
    if updates:
        project_details += "Recent Updates:\n"
        for update in updates:
            project_details += f"- {update.title}: {update.content}\n"
    else:
        project_details += "No recent updates.\n"
    
    messages = {
        'en': f"Here are the details for project '{project.title}':\n\n{project_details}",
        'ru': f"Вот детали проекта '{project.title}':\n\n{project_details}",
        'de': f"Hier sind die Details für das Projekt '{project.title}':\n\n{project_details}",
        'uk': f"Ось деталі проекту '{project.title}':\n\n{project_details}"
    }
    
    return {
        'answer': messages.get(language, messages['en']),
        'agent': 'pm'
    }
