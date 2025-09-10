from typing import Optional, Dict, List
import json
import re
from . import get_agent, choose_agent_by_metadata, InteractiveButton, InteractiveResponse, list_domain_options
from .site_knowledge import get_site_info
from .prompts import get_greeter_prompt, get_project_consultant_prompt, get_technical_advisor_prompt
from .tech_spec import get_tech_spec_prompt, TechSpecTemplate
from .tech_spec_handler import handle_tech_spec_creation, generate_tech_spec_summary
from flask import current_app, request
import requests


def format_interactive_response(text: str) -> InteractiveResponse:
    """
    Parse LLM output for special interactive formatting directives.
    Supports:
    - [[BUTTON:label:key:icon]] for interactive buttons
    - [[REQUIRE_INPUT:true/false]] to show/hide input field
    - [[RESTART:true/false]] to show restart button
    """
    response = InteractiveResponse(text=text)
    buttons = []
    
    # Extract buttons
    button_pattern = r'\[\[BUTTON:(.*?):(.*?)(?::(.*?))?\]\]'
    for match in re.finditer(button_pattern, response.text):
        label = match.group(1)
        key = match.group(2)
        icon = match.group(3) if match.group(3) else None
        buttons.append(InteractiveButton(key=key, label=label, icon=icon))
        # Remove button markup from text
        response.text = response.text.replace(match.group(0), '')
    
    # Extract input requirement
    input_pattern = r'\[\[REQUIRE_INPUT:(true|false)\]\]'
    input_match = re.search(input_pattern, response.text)
    if input_match:
        # Всегда разрешаем ввод, но храним исходное значение для отображения подсказок
        original_requires = input_match.group(1).lower() == 'true'
        response.requires_input = True  # Всегда разрешаем ввод
        response.text = response.text.replace(input_match.group(0), '')
    
    # Extract restart option
    restart_pattern = r'\[\[RESTART:(true|false)\]\]'
    restart_match = re.search(restart_pattern, response.text)
    if restart_match:
        response.show_restart = restart_match.group(1).lower() == 'true'
        response.text = response.text.replace(restart_match.group(0), '')
    
    # Strip any trailing whitespace
    response.text = response.text.strip()
    
    if buttons:
        response.buttons = buttons
    
    return response


def handle_greeter(metadata: Dict) -> Dict:
    """Special handler for the greeter agent that offers team specialist options"""
    # Определяем язык пользователя (по умолчанию английский)
    user_lang = metadata.get('language', 'en')
    
    # Приветственные тексты на разных языках
    welcome_texts = {
        'de': "👋 Guten Tag! Ich bin der AI-Assistent von Rozoom-KI.\n\n"
              "Ich kann Ihnen helfen, ein technisches Lastenheft für Ihr Projekt zu erstellen - völlig kostenlos und unverbindlich. "
              "Mit welchem unserer Spezialisten möchten Sie sprechen? "
              "Oder möchten Sie direkt mit der Erstellung eines technischen Lastenhefts beginnen?",
        
        'en': "👋 Hello! I'm the AI assistant at Rozoom-KI.\n\n"
              "I can help you create a technical specification for your project - completely free and with no obligations. "
              "Which of our specialists would you like to speak with? "
              "Or would you like to start creating a technical specification right away?"
    }
    
    # Используем приветствие на указанном языке или по умолчанию на английском
    welcome_text = welcome_texts.get(user_lang, welcome_texts['en'])
    
    # Создаем специалистов для команды
    specialists = [
        {
            'key': 'tech_support',
            'label': 'Technical Advisor' if user_lang == 'en' else 'Technischer Berater',
            'icon': 'cogs',
            'description': 'For architecture and technology questions' if user_lang == 'en' else 'Für Architektur- und Technologiefragen'
        },
        {
            'key': 'requirements',
            'label': 'Create Technical Specification' if user_lang == 'en' else 'Technisches Lastenheft erstellen',
            'icon': 'file-alt',
            'description': 'Free assessment of your project' if user_lang == 'en' else 'Kostenlose Bewertung Ihres Projekts'
        },
        {
            'key': 'sales',
            'label': 'Pricing & Timelines' if user_lang == 'en' else 'Preise & Zeitpläne',
            'icon': 'money-bill-wave',
            'description': 'Budget and timeline questions' if user_lang == 'en' else 'Fragen zu Budget und Zeitplan'
        },
        {
            'key': 'general',
            'label': 'General Questions' if user_lang == 'en' else 'Allgemeine Fragen',
            'icon': 'question-circle',
            'description': 'Any other questions about our services' if user_lang == 'en' else 'Weitere Fragen zu unseren Dienstleistungen'
        }
    ]
    
    # Convert specialists to buttons
    buttons = []
    for specialist in specialists:
        buttons.append(InteractiveButton(
            key=specialist['key'],
            label=specialist['label'],
            icon=specialist.get('icon', 'user')
        ))
    
    return {
        'agent': 'greeter',
        'answer': welcome_text,
        'interactive': {
            'text': welcome_text,
            'buttons': [b.__dict__ for b in buttons],
            'requires_input': True,  # Всегда разрешаем ввод
            'show_restart': False,
            'meta': {'action': 'select_specialist', 'language': user_lang}
        }
    }


def handle_specialist_selection(message: str, metadata: Dict) -> Dict:
    """Handle when user selects a specialist from the greeter options"""
    selected_specialist = metadata.get('selected_agent')
    current_app.logger.info(f"Handle specialist selection with: {selected_specialist}")
    
    if not selected_specialist:
        current_app.logger.warning("No selected_agent found in metadata")
        return route_to_default_agent(message, metadata)
    
    # Специальный обработчик для создания технического задания
    if selected_specialist == 'requirements':
        return handle_tech_spec_creation(message, metadata)
    
    # Map specialist keys to actual agent names
    specialist_map = {
        'technical': 'tech_support',
        'development': 'general',
        'sales': 'sales',
        # Добавляем прямое сопоставление, если ключи уже совпадают с именами агентов
        'tech_support': 'tech_support',
        'general': 'general',
        'sales': 'sales',
        'greeter': 'greeter',
        'billing': 'billing'
    }
    
    # Get the appropriate agent
    agent_name = specialist_map.get(selected_specialist, 'general')
    specialist_agent = get_agent(agent_name)
    
    current_app.logger.info(f"Mapped to agent: {agent_name}, found: {specialist_agent is not None}")
    
    if not specialist_agent:
        current_app.logger.warning(f"Could not find agent: {agent_name}")
        return route_to_default_agent(message, metadata)
    
    # Update metadata with the active specialist
    metadata['active_specialist'] = agent_name
    
    # Определяем язык пользователя (по умолчанию английский)
    user_lang = metadata.get('language', 'en')
    
    # Создаем промпт на соответствующем языке
    prompts = {
        'de': (
            f"Der Benutzer möchte mit einem {specialist_agent.description} Spezialisten sprechen. "
            f"Stellen Sie sich als spezialisierter Assistent für diesen Bereich vor und beginnen Sie ein Gespräch, um die Bedürfnisse des Benutzers zu verstehen. "
            f"Verwenden Sie einen herzlichen, professionellen Ton. "
            f"Beginnen Sie mit einer Begrüßung und stellen Sie sich vor. "
            f"Stellen Sie spezifische Fragen zu ihrem Anliegen und geben Sie konkrete Hilfestellung. "
            f"Verwenden Sie die Sprache, die der Benutzer bevorzugt (Sprache: {user_lang})."
        ),
        'en': (
            f"The user wants to speak with a {specialist_agent.description} specialist. "
            f"Introduce yourself as a specialized assistant for this area and begin a conversation to understand the user's needs. "
            f"Use a warm, professional tone. "
            f"Start with a greeting and introduce yourself. "
            f"Ask specific questions about their inquiry and provide concrete assistance. "
            f"Use the language preferred by the user (language: {user_lang})."
        )
    }
    
    prompt_text = prompts.get(user_lang, prompts['en'])
    
    # Create a special first-time message from this agent
    return call_openai(prompt_text, metadata, specialist_agent)


def route_to_default_agent(message: str, metadata: Dict) -> Dict:
    """Route to the general agent when no special handling is needed"""
    agent = get_agent('general')
    return call_openai(message, metadata, agent)


def call_openai(message: str, metadata: Dict, agent) -> Dict:
    """Make the actual API call to OpenAI"""
    openai_key = current_app.config.get('OPENAI_API_KEY')
    model = current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini')
    
    if not openai_key:
        return {'error': 'OpenAI API key not configured'}

    # Определяем язык пользователя (по умолчанию английский)
    user_lang = metadata.get('language', 'en')
    
    # Получаем знания о сайте на выбранном языке
    site_info = get_site_info(user_lang)
    
    # Добавляем информацию о языке в системный промпт
    language_info = f"\nIMPORTANT: The user's preferred language is {user_lang}. Please respond in this language."
    
    # Выбираем соответствующий промпт в зависимости от роли агента
    system_prompt = agent.system_prompt + language_info
    
    if agent.name == 'greeter':
        system_prompt = get_greeter_prompt(user_lang) + language_info
    elif agent.name in ['requirements', 'project_consultant']:
        system_prompt = get_project_consultant_prompt(user_lang) + language_info
    elif agent.name in ['technical', 'tech_support']:
        system_prompt = get_technical_advisor_prompt(user_lang) + language_info
    
    # Добавляем информацию о текущей странице, если она есть
    current_page = metadata.get('page', 'home')
    if current_page in site_info['site_structure']:
        page_info = site_info['site_structure'][current_page]
        page_context = f"\nUser is currently on the {page_info['title']} page: {page_info['description']}"
        system_prompt += page_context

    # Extract conversation history if available
    history = metadata.get('history', [])
    
    # Build messages array with history
    messages = [{'role': 'system', 'content': system_prompt}]
    
    # Add history messages if available (limited to last 10)
    for h in history[-10:]:
        messages.append({'role': h.get('role', 'user'), 'content': h.get('content', '')})
    
    # Add current message if not already in history
    if not history or message != history[-1].get('content', ''):
        messages.append({'role': 'user', 'content': message})

    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': 1000,
    }

    headers = {'Authorization': f'Bearer {openai_key}'}
    resp = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
    
    if resp.status_code != 200:
        # try fallback model if configured
        fallback = current_app.config.get('OPENAI_MODEL_FALLBACK')
        if fallback and fallback != model:
            payload['model'] = fallback
            resp = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
            if resp.status_code != 200:
                return {'error': 'OpenAI error', 'details': resp.text}
        else:
            return {'error': 'OpenAI error', 'details': resp.text}

    data = resp.json()
    try:
        answer = data['choices'][0]['message']['content']
        
        # Parse for interactive elements
        interactive = format_interactive_response(answer)
        
        # Создаем описание опций для включения в текст сообщения
        options_text = ""
        if interactive.buttons and len(interactive.buttons) > 0:
            options_text = "\n\n*Доступные опции:*"
            for button in interactive.buttons:
                options_text += f"\n• {button.label}"
        
        # Добавляем информацию о кнопке перезапуска
        if interactive.show_restart:
            options_text += "\n\n*Вы также можете начать разговор заново.*"
        
        # Полный текст с опциями (для сохранения в истории)
        full_text = interactive.text + options_text
        
        # Add agent information to response
        return {
            'agent': agent.name,
            'answer': full_text,  # Включаем описание опций в текст ответа
            'interactive': {
                'text': interactive.text,
                'buttons': [b.__dict__ for b in (interactive.buttons or [])],
                'requires_input': True,  # Всегда разрешаем ввод
                'show_restart': interactive.show_restart,
                'meta': {'agent': agent.name}
            }
        }
    except Exception as e:
        current_app.logger.error(f"Error parsing OpenAI response: {e}")
        return {'error': 'Failed to parse response', 'agent': agent.name}


def route_and_respond(message: str, metadata: Dict) -> Dict:
    """Main routing function that delegates to appropriate handlers"""
    # Определение языка пользователя
    user_lang = metadata.get('language')
    
    # Если язык не указан, устанавливаем по умолчанию английский
    if not user_lang:
        metadata['language'] = 'en'
    
    # Получаем информацию о текущей странице, если она передана в метаданных
    referer = request.headers.get('Referer', '')
    current_page = 'home'  # По умолчанию
    
    # Определяем текущую страницу на основе URL
    for page, data in get_site_info(metadata['language'])['site_structure'].items():
        path = data['path']
        if path != '/' and path in referer:
            current_page = page
            break
    
    # Добавляем информацию о текущей странице в метаданные
    metadata['page'] = current_page
    
    # For new conversations, use greeter
    if not metadata.get('conversation_id'):
        return handle_greeter(metadata)
    
    # Check if we're handling an agent transition (from button click)
    if metadata.get('selected_agent'):
        # Log detailed info for debugging
        current_app.logger.info(f"Agent transition detected: {metadata.get('selected_agent')}, transition flag: {metadata.get('agent_transition')}")
        
        # Reset transition flag after logging
        metadata['agent_transition'] = False
        
        # Handle the specialist selection
        return handle_specialist_selection(message, metadata)
        
    # Проверяем, находимся ли мы в процессе создания технического задания
    if metadata.get('tech_spec_started'):
        # Проверяем специальные команды
        if message.lower() in ['edit requirements', 'anforderungen bearbeiten']:
            # Начинаем процесс заново
            metadata['tech_spec_section'] = 0
            return handle_tech_spec_creation(message, metadata)
        elif message.lower() in ['send request', 'anfrage senden']:
            # Отправляем запрос
            thank_message = "Thank you for submitting your request! Our team will review your requirements and get back to you shortly."
            if metadata.get('language') == 'de':
                thank_message = "Vielen Dank für Ihre Anfrage! Unser Team wird Ihre Anforderungen prüfen und sich in Kürze bei Ihnen melden."
            
            # Send notification via Telegram
            try:
                # Use the queue system for tech spec notifications
                from app.utils.telegram_queue import queue_telegram_message
                from app.services.telegram_service import send_tech_spec_notification
                
                # Prepare data for notification
                tech_spec_data = {
                    'answers': []
                }
                
                # Format each question-answer pair
                template = TechSpecTemplate(metadata.get('language', 'en'))
                answers = metadata.get('tech_spec_answers', [])
                
                # Extract contact information from the answers
                user_name = None
                user_email = None
                user_phone = None
                
                # Last section should be Contact Information
                contact_section_index = len(template.sections) - 1
                if contact_section_index < len(answers):
                    contact_info = answers[contact_section_index].split('\n')
                    if len(contact_info) >= 2:
                        user_name = contact_info[0].strip()
                        user_email = contact_info[1].strip()
                        if len(contact_info) >= 3:
                            user_phone = contact_info[2].strip()
                
                # Add all sections to the tech spec data
                for i, section in enumerate(template.sections):
                    if i < len(answers):
                        tech_spec_data['answers'].append({
                            'question': section['title'],
                            'answer': answers[i]
                        })
                
                # Add language information for proper template loading
                tech_spec_data['language'] = metadata.get('language', 'en')
                
                # Prepare contact information for the notification
                contact_info = {
                    'name': user_name,
                    'email': user_email,
                    'phone': user_phone
                }
                
                # Generate the message but queue it instead of sending directly
                message_content = send_tech_spec_notification(tech_spec_data, contact_info, return_message_only=True)
                queue_telegram_message(message_content)
                current_app.logger.info(f"Technical specification notification queued for {user_email}")
            except Exception as e:
                current_app.logger.error(f"Failed to send Telegram notification: {str(e)}")
            
            # Очищаем метаданные технического задания
            metadata.pop('tech_spec_started', None)
            metadata.pop('tech_spec_section', None)
            
            return {
                'agent': 'requirements',
                'answer': thank_message,
                'interactive': {
                    'text': thank_message,
                    'buttons': [],
                    'requires_input': True,
                    'show_restart': True,
                    'meta': {'agent': 'requirements'}
                }
            }
        
        # Продолжаем процесс создания технического задания
        return handle_tech_spec_creation(message, metadata)
    
    # Handle when user wants to return to greeter
    if message and message.lower() in ['start over', 'restart', 'начать сначала', 'neu starten']:
        # Clear specialist selection
        metadata.pop('selected_agent', None)
        metadata.pop('active_specialist', None)
        return handle_greeter(metadata)
    
    # Check if we have an active specialist
    if metadata.get('active_specialist'):
        agent = get_agent(metadata.get('active_specialist'))
    else:
        # Otherwise, route based on agent selection logic
        agent = choose_agent_by_metadata(metadata)
    
    # Fallback if no agent found
    if not agent:
        agent = get_agent('general')
    
    # Handle special agents
    if agent.special_handler:
        if agent.name == 'greeter':
            return handle_greeter(metadata)
    
    # Regular agent handling through OpenAI
    return call_openai(message, metadata, agent)
