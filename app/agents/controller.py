from typing import Optional, Dict, List
import json
import re
from . import get_agent, choose_agent_by_metadata, InteractiveButton, InteractiveResponse, list_domain_options
from .site_knowledge import get_site_info
from .prompts import get_greeter_prompt, get_project_consultant_prompt, get_technical_advisor_prompt
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
    """Special handler for the greeter agent that offers domain options"""
    options = list_domain_options()
    
    # Определяем язык пользователя (по умолчанию немецкий)
    user_lang = metadata.get('language', 'de')
    
    # Приветственные тексты на разных языках
    welcome_texts = {
        'de': "👋 Guten Tag! Ich bin der KI-Assistent von Rozoom-KI.\n\n"
              "Ich kann Ihnen helfen, eine technische Spezifikation für Ihr Projekt zu erstellen. "
              "In welchem Bereich benötigen Sie Unterstützung? Sie können eine der unten stehenden Optionen wählen oder Ihre Frage stellen.",
        
        'ru': "👋 Привет! Я AI-ассистент Rozoom-KI.\n\n"
              "Я могу помочь вам составить техническое задание для вашего проекта. "
              "В каком направлении вам нужна помощь? Вы можете выбрать одну из опций ниже или задать свой вопрос.",
        
        'en': "👋 Hello! I'm the AI assistant of Rozoom-KI.\n\n"
              "I can help you create a technical specification for your project. "
              "In which area do you need assistance? You can choose one of the options below or ask your question."
    }
    
    # Используем приветствие на указанном языке или по умолчанию на немецком
    welcome_text = welcome_texts.get(user_lang, welcome_texts['de'])
    
    # Convert options to buttons
    buttons = []
    for option in options:
        buttons.append(InteractiveButton(
            key=option['key'],
            label=option['label'],
            icon=option.get('icon', 'code')
        ))
    
    return {
        'agent': 'greeter',
        'answer': welcome_text,
        'interactive': {
            'text': welcome_text,
            'buttons': [b.__dict__ for b in buttons],
            'requires_input': True,  # Всегда разрешаем ввод
            'show_restart': False,
            'meta': {'action': 'select_domain'}
        }
    }


def handle_domain_selection(message: str, metadata: Dict) -> Dict:
    """Handle when user selects a domain from the greeter options"""
    selected_domain = metadata.get('selected_domain')
    if not selected_domain:
        return route_to_default_agent(message, metadata)
    
    domain_agent = get_agent(selected_domain)
    if not domain_agent:
        return route_to_default_agent(message, metadata)
    
    # Update metadata to start requirements gathering flow
    metadata['gathering_requirements'] = True
    
    # Определяем язык пользователя (по умолчанию немецкий)
    user_lang = metadata.get('language', 'de')
    
    # Создаем промпт на соответствующем языке
    prompts = {
        'de': (
            f"Der Benutzer hat {domain_agent.description} ausgewählt. "
            f"Stellen Sie sich als spezialisierter Assistent für diesen Bereich vor und beginnen Sie, Informationen für die technische Spezifikation zu sammeln. "
            f"Stellen Sie jeweils eine Frage, um wichtige Informationen zu sammeln. "
            f"Nachdem Sie ausreichend Informationen gesammelt haben, schlagen Sie vor, eine technische Spezifikation zu erstellen. "
            f"Beginnen Sie mit einer Begrüßung und stellen Sie sich vor."
        ),
        'ru': (
            f"Пользователь выбрал {domain_agent.description}. "
            f"Представься как специализированный ассистент для этой области, и начни собирать информацию для технического задания. "
            f"Задавай по одному вопросу за раз, чтобы собрать ключевую информацию. "
            f"После сбора достаточной информации, предложи опцию составить техническое задание. "
            f"Начни с приветствия и представления себя."
        ),
        'en': (
            f"The user has selected {domain_agent.description}. "
            f"Introduce yourself as a specialized assistant for this area and begin collecting information for the technical specification. "
            f"Ask one question at a time to gather key information. "
            f"After collecting sufficient information, suggest the option to create a technical specification. "
            f"Start with a greeting and introduce yourself."
        )
    }
    
    prompt_text = prompts.get(user_lang, prompts['de'])
    
    # Create a special first-time message from this agent
    return call_openai(prompt_text, metadata, domain_agent)


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

    # Определяем язык пользователя (по умолчанию немецкий)
    user_lang = metadata.get('language', 'de')
    
    # Получаем знания о сайте на выбранном языке
    site_info = get_site_info(user_lang)
    
    # Выбираем соответствующий промпт в зависимости от роли агента
    system_prompt = agent.system_prompt
    if agent.name == 'greeter':
        system_prompt = get_greeter_prompt(user_lang)
    elif agent.name in ['requirements', 'project_consultant']:
        system_prompt = get_project_consultant_prompt(user_lang)
    elif agent.name in ['technical', 'tech_support']:
        system_prompt = get_technical_advisor_prompt(user_lang)
    
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
    
    # Если язык не указан, устанавливаем по умолчанию немецкий
    if not user_lang:
        metadata['language'] = 'de'
    
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
    
    # Check if this is a domain selection from the greeter
    if metadata.get('selected_domain') and not metadata.get('gathering_requirements'):
        return handle_domain_selection(message, metadata)
    
    # Otherwise, route based on agent selection logic
    agent = choose_agent_by_metadata(metadata)
    if not agent:
        agent = get_agent('general')
    
    # Handle special agents
    if agent.special_handler:
        if agent.name == 'greeter':
            return handle_greeter(metadata)
    
    # Regular agent handling through OpenAI
    return call_openai(message, metadata, agent)
