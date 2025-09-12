# app/agents/controller.py
from __future__ import annotations
import logging
from typing import Dict, Any

from flask import current_app, Blueprint, request
import json
from app.models.language import detect_language, get_text_by_key
from app.models.tech_spec import TechSpecTemplate
from app.services.logger import logger
from app.services.responses_service import respond as responses_respond

# Agents configuration
agent_bp = Blueprint('agent', __name__, url_prefix='/api/agent')

# Available specialists/agents for the chat
SPECIALISTS = {
    'greeter': {
        'name': 'greeter',
        'title': {
            'en': 'Greeter',
            'ru': 'Приветствующий',
            'de': 'Greeter',
            'uk': 'Вітаючий'
        },
        'description': {
            'en': 'I can help you choose the right specialist or service.',
            'ru': 'Я помогу вам выбрать подходящего специалиста или услугу.',
            'de': 'Ich kann Ihnen helfen, den richtigen Spezialisten oder Dienst zu wählen.',
            'uk': 'Я допоможу вам обрати відповідного спеціаліста або послугу.'
        },
        'avatar': '/static/img/agents/greeter.png'
    },
    'design': {
        'name': 'design',
        'title': {
            'en': 'Designer',
            'ru': 'Дизайнер',
            'de': 'Designer',
            'uk': 'Дизайнер'
        },
        'description': {
            'en': 'I can help with web design questions, UI/UX, and graphic design.',
            'ru': 'Я могу помочь с вопросами веб-дизайна, UI/UX и графического дизайна.',
            'de': 'Ich kann bei Fragen zu Webdesign, UI/UX und Grafikdesign helfen.',
            'uk': 'Я можу допомогти з питаннями веб-дизайну, UI/UX та графічного дизайну.'
        },
        'avatar': '/static/img/agents/design.png'
    },
    'development': {
        'name': 'development',
        'title': {
            'en': 'Developer',
            'ru': 'Разработчик',
            'de': 'Entwickler',
            'uk': 'Розробник'
        },
        'description': {
            'en': 'I specialize in web development, programming and technical questions.',
            'ru': 'Я специализируюсь на веб-разработке, программировании и технических вопросах.',
            'de': 'Ich bin spezialisiert auf Webentwicklung, Programmierung und technische Fragen.',
            'uk': 'Я спеціалізуюсь на веб-розробці, програмуванні та технічних питаннях.'
        },
        'avatar': '/static/img/agents/development.png'
    },
    'marketing': {
        'name': 'marketing',
        'title': {
            'en': 'Marketing Expert',
            'ru': 'Маркетолог',
            'de': 'Marketing-Experte',
            'uk': 'Маркетолог'
        },
        'description': {
            'en': 'I can help with digital marketing, SEO, and promotion strategies.',
            'ru': 'Я помогу с цифровым маркетингом, SEO и стратегиями продвижения.',
            'de': 'Ich kann bei digitalem Marketing, SEO und Werbestrategien helfen.',
            'uk': 'Я допоможу з цифровим маркетингом, SEO та стратегіями просування.'
        },
        'avatar': '/static/img/agents/marketing.png'
    },
    'portfolio': {
        'name': 'portfolio',
        'title': {
            'en': 'Portfolio Navigator',
            'ru': 'Навигатор портфолио',
            'de': 'Portfolio-Navigator',
            'uk': 'Навігатор портфоліо'
        },
        'description': {
            'en': 'I can show you our works, projects and case studies.',
            'ru': 'Я могу показать наши работы, проекты и кейсы.',
            'de': 'Ich kann Ihnen unsere Arbeiten, Projekte und Fallstudien zeigen.',
            'uk': 'Я можу показати наші роботи, проекти та кейси.'
        },
        'avatar': '/static/img/agents/portfolio.png'
    },
    'requirements': {
        'name': 'requirements',
        'title': {
            'en': 'Technical Specification Assistant',
            'ru': 'Помощник по техническому заданию',
            'de': 'Technischer Spezifikationsassistent',
            'uk': 'Помічник з технічного завдання'
        },
        'description': {
            'en': 'I can help create a technical specification for your project.',
            'ru': 'Я помогу составить техническое задание для вашего проекта.',
            'de': 'Ich kann bei der Erstellung einer technischen Spezifikation für Ihr Projekt helfen.',
            'uk': 'Я допоможу скласти технічне завдання для вашого проекту.'
        },
        'avatar': '/static/img/agents/requirements.png'
    },
    'quiz': {
        'name': 'quiz',
        'title': {
            'en': 'Website Cost Calculator',
            'ru': 'Калькулятор стоимости сайта',
            'de': 'Website-Kostenrechner',
            'uk': 'Калькулятор вартості веб-сайту'
        },
        'description': {
            'en': 'I can help you calculate an approximate cost of your website.',
            'ru': 'Я помогу рассчитать примерную стоимость вашего сайта.',
            'de': 'Ich kann Ihnen helfen, die ungefähren Kosten Ihrer Website zu berechnen.',
            'uk': 'Я допоможу розрахувати приблизну вартість вашого веб-сайту.'
        },
        'avatar': '/static/img/agents/quiz.png'
    },
    'consultation': {
        'name': 'consultation',
        'title': {
            'en': 'Consultant',
            'ru': 'Консультант',
            'de': 'Berater',
            'uk': 'Консультант'
        },
        'description': {
            'en': 'I can provide consultation on your project requirements.',
            'ru': 'Я могу проконсультировать вас по требованиям к вашему проекту.',
            'de': 'Ich kann Sie zu Ihren Projektanforderungen beraten.',
            'uk': 'Я можу проконсультувати вас щодо вимог вашого проекту.'
        },
        'avatar': '/static/img/agents/consult.png'
    }
}

# Route for incoming agent messages
@agent_bp.route('/message', methods=['POST'])
def agent_message():
    """Handle incoming messages from the user to the agent"""
    message_data = request.json
    user_message = message_data.get('message')
    metadata = message_data.get('metadata', {})
    
    # Detect language of the user message
    if user_message:
        detected_lang = detect_language(user_message)
        if detected_lang:
            metadata['language'] = detected_lang
    
    # If no language is detected or set, default to English
    if 'language' not in metadata:
        metadata['language'] = 'en'
    
    # Process the message and get response
    response = route_and_respond(user_message, metadata)
    
    # Convert to JSON and return
    return json.dumps(response)

"""
Єдиний роутер:
- greeter: привітання, виявлення потреби, пропозиції → може переключити на spec або pm
- spec: допомога у формуванні ТЗ
- pm: статуси поточних проєктів (використовує дані з БД — робимо це в іншому шарі логіки; тут лише діалог)
"""

# Ключі для metadata
META_LANG = "language"
META_CONV = "conversation_id"
META_USER = "user_id"
META_SELECTED = "selected_agent"      # 'greeter' | 'spec' | 'pm'
META_ACTIVE = "active_specialist"     # поточний агент (те саме)
META_SUPPRESS = "suppress_greeting"   # bool

VALID_AGENTS = ("greeter", "spec", "pm")

def _ensure_defaults(metadata: Dict[str, Any]) -> None:
    if META_LANG not in metadata or not metadata[META_LANG]:
        metadata[META_LANG] = "uk"
    if META_SELECTED not in metadata or metadata[META_SELECTED] not in VALID_AGENTS:
        metadata[META_SELECTED] = "greeter"
    if META_ACTIVE not in metadata or metadata[META_ACTIVE] not in VALID_AGENTS:
        metadata[META_ACTIVE] = metadata[META_SELECTED]

def route_and_respond(message, metadata=None):
    """
    Повертає словник з результатами виклику асиста:
    {
        'agent': agent_key,
        'answer': assistant_response,
        'interactive': optional_ui_elements,
        'conversation_id': conversation_id # Unique ID for the conversation
    }
    """
    if metadata is None:
        metadata = {}

    # Determine language early
    language = metadata.get('language') or detect_language(message or '') or 'uk'
    metadata['language'] = language

    # Fast-path to tech-spec intent: switch to requirements/spec agent
    try:
        text = (message or '').lower()
        tech_spec_triggers = (
            'тз', 'тех завдан', 'техзавдан', 'техніч', 'технічне завдан', 'техзадани', 'техзад',
            'техническ', 'техзадан', 'тех задани', 'тех задание', 'техзадание',
            'спец', 'спеціаліст', 'специалист', 'експерт',
            'tech spec', 'technical spec', 'specification', 'requirements'
        )
        if any(k in text for k in tech_spec_triggers):
            metadata['selected_agent'] = 'requirements'
            metadata['active_specialist'] = 'requirements'
    except Exception:
        pass

    # Normalize selected agent to our trio for Responses service
    selected = (metadata.get('selected_agent') or metadata.get('active_specialist') or 'greeter').lower()
    agent = 'spec' if selected in ('requirements', 'spec') else ('pm' if selected == 'pm' else 'greeter')

    conversation_id = metadata.get('conversation_id') or 'anon'
    context = metadata.get('context')
    # If SPEC agent is chosen, enrich context with Services TZ form schema/CTA
    if agent == 'spec':
        try:
            from app.agents.site_knowledge import spec_agent_context
            spec_ctx = spec_agent_context(language)
            if context:
                context = f"{context}\n\n---\n{spec_ctx}"
            else:
                context = spec_ctx
        except Exception:
            pass

    result = responses_respond(
        user_text=message or '',
        agent=agent,
        conversation_id=conversation_id,
        language=language,
        context=context,
        structured=False,
    )

    ui_agent = 'requirements' if result.get('agent') == 'spec' else result.get('agent')
    # Keep UI state coherent
    metadata['active_specialist'] = ui_agent

    return {
        'agent': ui_agent,
        'answer': result.get('answer'),
        'interactive': None,
        'conversation_id': result.get('conversation_id', conversation_id),
    }

def handle_specialist_selection(specialist_key, metadata):
    """Handle when a user selects a specific specialist"""
    # Store the selected agent in the metadata
    metadata['selected_agent'] = specialist_key
    
    # Add a system message to the history indicating a specialist change
    language = metadata.get('language', 'en')
    
    # Get specialist name in the user's language
    specialist_title = SPECIALISTS.get(specialist_key, {}).get('title', {}).get(language, specialist_key)
    
    # Create a transition message to preserve conversation context
    transition_text = {
        'en': f"Switching to {specialist_title} specialist to better assist you.",
        'ru': f"Переключаюсь на специалиста по {specialist_title} для лучшей помощи.",
        'de': f"Wechsle zum {specialist_title}-Spezialisten, um Ihnen besser zu helfen.",
        'uk': f"Перемикаюсь на спеціаліста з {specialist_title} для кращої допомоги."
    }.get(language, f"Switching to {specialist_title} specialist.")
    
    # Add transition message to history if history exists
    if 'history' in metadata and isinstance(metadata['history'], list):
        # Add a system message about the transition
        metadata['history'].append({
            "role": "system",
            "content": transition_text
        })
    
    # Route back to the main handler with the updated metadata
    return route_and_respond(None, metadata)

def handle_generic_agent(message, agent_name, metadata):
    """Handle messages for generic agents (design, development, marketing)"""
    language = metadata.get('language', 'en')
    
    # Create specialized prompt for the agent
    system_prompt = create_system_prompt(language)
    
    # Use a greeting if no message is provided
    if not message:
        user_prompt = get_text_by_key(f"{agent_name}_greeting", language)
    else:
        user_prompt = message
    
    # Prepare messages for the OpenAI API
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Add history if available
    if 'history' in metadata and isinstance(metadata['history'], list):
        # Insert history messages before the current user message
        # but after the system message
        history_messages = metadata['history']
        if history_messages:
            messages = [messages[0]] + history_messages + [messages[-1]]
    
    # Get response from the OpenAI API
    response_text = get_chat_response(messages, language)
    
    # Fallback if API fails
    if not response_text:
        if language == 'ru':
            response_text = f"Я ваш ассистент по {SPECIALISTS[agent_name]['title']['ru']}. Как я могу помочь с вашими вопросами о {agent_name}?"
        elif language == 'de':
            response_text = f"Ich bin Ihr {SPECIALISTS[agent_name]['title']['de']}-Assistent. Wie kann ich Ihnen mit Ihren {agent_name}-Anfragen helfen?"
        elif language == 'uk':
            response_text = f"Я ваш асистент з {SPECIALISTS[agent_name]['title']['uk']}. Як я можу допомогти з вашими питаннями щодо {agent_name}?"
        else:
            response_text = f"I'm your {SPECIALISTS[agent_name]['title']['en']} assistant. How can I help with your {agent_name} needs?"
    
    # Only include a back button
    buttons = [{
        'text': 'Back' if language == 'en' else ('Назад' if language == 'ru' or language == 'uk' else 'Zurück'),
        'value': 'back',
        'description': 'Return to specialist selection' if language == 'en' else 
                      ('Вернуться к выбору специалиста' if language == 'ru' else 
                       ('Повернутися до вибору спеціаліста' if language == 'uk' else
                        'Zurück zur Spezialistenauswahl'))
    }]
    
    return {
        'agent': agent_name,
        'answer': response_text,
        'interactive': {
            'text': response_text,
            'buttons': buttons,
            'requires_input': True,
            'meta': {'agent': agent_name}
        }
    }

def handle_portfolio(message, metadata):
    """Handle messages for the portfolio agent"""
    language = metadata.get('language', 'en')
    
    # Create specialized prompt for the portfolio agent
    system_prompt = create_system_prompt(language)
    user_prompt = create_portfolio_prompt(language)
    
    # Prepare messages for the OpenAI API
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Add history if available - this is crucial for context preservation
    if 'history' in metadata and isinstance(metadata['history'], list):
        history_messages = metadata['history']
        # Take the last 15 messages to maintain context but avoid token limits
        trimmed_history = history_messages[-15:] if len(history_messages) > 15 else history_messages
        if trimmed_history:
            messages.extend(trimmed_history)
    
    # If this is the initial message (no user query yet)
    if not message:
        # Add a prompt message to generate initial greeting
        messages.append({"role": "user", "content": user_prompt})
        
        try:
            # Get response from AI model using our chat service
            greeting = get_chat_response(messages, language)
        except Exception as e:
            current_app.logger.error(f"Error getting AI response for portfolio: {str(e)}")
            # Fallback to hardcoded responses if API call fails
            greeting = "Here's our portfolio of recent projects. What kind of projects are you interested in seeing?"
            if language == 'ru':
                greeting = "Вот наше портфолио недавних проектов. Какие типы проектов вас интересуют?"
            elif language == 'de':
                greeting = "Hier ist unser Portfolio der neuesten Projekte. An welcher Art von Projekten sind Sie interessiert?"
            elif language == 'uk':
                greeting = "Ось наше портфоліо нещодавніх проектів. Які типи проектів вас цікавлять?"
        
        # Sample portfolio categories as buttons
        buttons = [
            {
                'text': 'E-commerce' if language == 'en' else ('Интернет-магазины' if language == 'ru' else 'E-Commerce'),
                'value': 'ecommerce',
                'description': 'Online stores and marketplaces' if language == 'en' else 
                              ('Онлайн магазины и маркетплейсы' if language == 'ru' else 
                               'Online-Shops und Marktplätze')
            },
            {
                'text': 'Corporate websites' if language == 'en' else ('Корпоративные сайты' if language == 'ru' else 'Unternehmenswebsites'),
                'value': 'corporate',
                'description': 'Business and company websites' if language == 'en' else 
                              ('Бизнес и корпоративные веб-сайты' if language == 'ru' else 
                               'Geschäfts- und Unternehmenswebsites')
            },
            {
                'text': 'Web applications' if language == 'en' else ('Веб-приложения' if language == 'ru' else 'Webanwendungen'),
                'value': 'webapp',
                'description': 'Interactive web-based software' if language == 'en' else 
                              ('Интерактивное веб-программное обеспечение' if language == 'ru' else 
                               'Interaktive webbasierte Software')
            },
            {
                'text': 'Back' if language == 'en' else ('Назад' if language == 'ru' or language == 'uk' else 'Zurück'),
                'value': 'back',
                'description': 'Return to specialist selection' if language == 'en' else 
                              ('Вернуться к выбору специалиста' if language == 'ru' else 
                               ('Повернутися до вибору спеціаліста' if language == 'uk' else
                                'Zurück zur Spezialistenauswahl'))
            }
        ]
        
        return {
            'agent': 'portfolio',
            'answer': greeting,
            'interactive': {
                'text': greeting,
                'buttons': buttons,
                'requires_input': True,
                'meta': {'agent': 'portfolio'}
            }
        }
    
    # Handle specific portfolio categories
    if message.lower() in ['ecommerce', 'corporate', 'webapp']:
        # Show specific portfolio examples based on selection
        portfolio_type = message.lower()
        
        # Add the user's selection to the messages
        messages.append({"role": "user", "content": message})
        
        # Add context about the selected category
        category_prompts = {
            'ecommerce': {
                'en': "The user selected e-commerce projects. Describe our e-commerce portfolio with examples of online stores, marketplaces, and shopping platforms we've created.",
                'ru': "Пользователь выбрал проекты интернет-магазинов. Опишите наше портфолио e-commerce с примерами онлайн-магазинов, маркетплейсов и торговых платформ, которые мы создали.",
                'de': "Der Benutzer hat E-Commerce-Projekte ausgewählt. Beschreiben Sie unser E-Commerce-Portfolio mit Beispielen für Online-Shops, Marktplätze und Handelsplattformen, die wir entwickelt haben.",
                'uk': "Користувач вибрав проекти інтернет-магазинів. Опишіть наше портфоліо e-commerce з прикладами онлайн-магазинів, маркетплейсів та торгових платформ, які ми створили."
            },
            'corporate': {
                'en': "The user selected corporate website projects. Describe our corporate website portfolio with examples of business sites, company presentations, and corporate platforms we've created.",
                'ru': "Пользователь выбрал корпоративные веб-сайты. Опишите наше портфолио корпоративных сайтов с примерами бизнес-сайтов, корпоративных презентаций и платформ, которые мы создали.",
                'de': "Der Benutzer hat Unternehmenswebsite-Projekte ausgewählt. Beschreiben Sie unser Portfolio an Unternehmenswebsites mit Beispielen für Geschäftswebsites, Unternehmenspräsentationen und Unternehmensplattformen, die wir erstellt haben.",
                'uk': "Користувач вибрав корпоративні веб-сайти. Опишіть наше портфоліо корпоративних сайтів з прикладами бізнес-сайтів, корпоративних презентацій і платформ, які ми створили."
            },
            'webapp': {
                'en': "The user selected web application projects. Describe our web application portfolio with examples of interactive platforms, SaaS products, and custom web software we've developed.",
                'ru': "Пользователь выбрал проекты веб-приложений. Опишите наше портфолио веб-приложений с примерами интерактивных платформ, SaaS-продуктов и заказного веб-ПО, которые мы разработали.",
                'de': "Der Benutzer hat Webanwendungsprojekte ausgewählt. Beschreiben Sie unser Portfolio an Webanwendungen mit Beispielen für interaktive Plattformen, SaaS-Produkte und maßgeschneiderte Websoftware, die wir entwickelt haben.",
                'uk': "Користувач вибрав проекти веб-додатків. Опишіть наше портфоліо веб-додатків з прикладами інтерактивних платформ, SaaS-продуктів та замовного веб-ПЗ, які ми розробили."
            }
        }
        
        # Add appropriate context prompt based on portfolio type
        context_prompt = category_prompts.get(portfolio_type, {}).get(language)
        if context_prompt:
            messages.append({"role": "system", "content": context_prompt})
        
        try:
            # Get AI-generated response about the portfolio category
            response_text = get_chat_response(messages, language)
        except Exception as e:
            current_app.logger.error(f"Error getting AI response for portfolio category: {str(e)}")
            # Fallback to hardcoded responses if API call fails
            portfolio_responses = {
                'ecommerce': {
                    'en': "Here are our e-commerce projects examples...",
                    'ru': "Вот примеры наших проектов интернет-магазинов...",
                    'de': "Hier sind unsere E-Commerce-Projektbeispiele...",
                    'uk': "Ось приклади наших проектів інтернет-магазинів..."
                },
                'corporate': {
                    'en': "Here are our corporate website examples...",
                    'ru': "Вот примеры наших корпоративных сайтов...",
                    'de': "Hier sind unsere Beispiele für Unternehmenswebsites...",
                    'uk': "Ось приклади наших корпоративних сайтів..."
                },
                'webapp': {
                    'en': "Here are our web application projects...",
                    'ru': "Вот наши проекты веб-приложений...",
                    'de': "Hier sind unsere Webapplikationsprojekte...",
                    'uk': "Ось наші проекти веб-додатків..."
                }
            }
            response_text = portfolio_responses[portfolio_type].get(language, portfolio_responses[portfolio_type]['en'])
        
        # Only include a back button
        buttons = [{
            'text': 'Back to portfolio' if language == 'en' else ('Назад к портфолио' if language == 'ru' else 'Zurück zum Portfolio'),
            'value': 'portfolio_back',
            'description': 'View other portfolio categories' if language == 'en' else 
                          ('Посмотреть другие категории портфолио' if language == 'ru' else 
                           'Andere Portfolio-Kategorien anzeigen')
        }]
        
        return {
            'agent': 'portfolio',
            'answer': response_text,
            'interactive': {
                'text': response_text,
                'buttons': buttons,
                'requires_input': True,
                'meta': {'agent': 'portfolio', 'category': portfolio_type}
            }
        }
    
    # If user wants to go back to portfolio main view
    if message.lower() == 'portfolio_back':
        # Clear the selected category
        metadata.pop('category', None)
        # Recursively call without message to get the initial portfolio view
        return handle_portfolio(None, metadata)
    
    # Default case: respond to a general portfolio inquiry
    # Add the user message to the conversation
    messages.append({"role": "user", "content": message})
    
    try:
        # Get AI response for the portfolio inquiry
        response_text = get_chat_response(messages, language)
    except Exception as e:
        current_app.logger.error(f"Error getting AI response for portfolio inquiry: {str(e)}")
        # Fallback to hardcoded responses if API call fails
        response_text = "I can show you our portfolio of projects. What type are you interested in seeing?"
        if language == 'ru':
            response_text = "Я могу показать вам наше портфолио проектов. Какой тип вас интересует?"
        elif language == 'de':
            response_text = "Ich kann Ihnen unser Projektportfolio zeigen. Welchen Typ möchten Sie sehen?"
        elif language == 'uk':
            response_text = "Я можу показати вам наше портфоліо проектів. Який тип вас цікавить?"
    
    # Include portfolio category buttons again
    buttons = [
        {
            'text': 'E-commerce' if language == 'en' else ('Интернет-магазины' if language == 'ru' else 'E-Commerce'),
            'value': 'ecommerce',
            'description': 'Online stores and marketplaces' if language == 'en' else 
                          ('Онлайн магазины и маркетплейсы' if language == 'ru' else 
                           'Online-Shops und Marktplätze')
        },
        {
            'text': 'Corporate websites' if language == 'en' else ('Корпоративные сайты' if language == 'ru' else 'Unternehmenswebsites'),
            'value': 'corporate',
            'description': 'Business and company websites' if language == 'en' else 
                          ('Бизнес и корпоративные веб-сайты' if language == 'ru' else 
                           'Geschäfts- und Unternehmenswebsites')
        },
        {
            'text': 'Web applications' if language == 'en' else ('Веб-приложения' if language == 'ru' else 'Webanwendungen'),
            'value': 'webapp',
            'description': 'Interactive web-based software' if language == 'en' else 
                          ('Интерактивное веб-программное обеспечение' if language == 'ru' else 
                           'Interaktive webbasierte Software')
        },
        {
            'text': 'Back' if language == 'en' else ('Назад' if language == 'ru' or language == 'uk' else 'Zurück'),
            'value': 'back',
            'description': 'Return to specialist selection' if language == 'en' else 
                          ('Вернуться к выбору специалиста' if language == 'ru' else 
                           ('Повернутися до вибору спеціаліста' if language == 'uk' else
                            'Zurück zur Spezialistenauswahl'))
        }
    ]
    
    return {
        'agent': 'portfolio',
        'answer': response_text,
        'interactive': {
            'text': response_text,
            'buttons': buttons,
            'requires_input': True,
            'meta': {'agent': 'portfolio'}
        }
    }

def handle_tech_spec_creation(message, metadata):
    """Handle the technical specification creation process"""
    language = metadata.get('language', 'en')
    
    # Get or initialize the tech spec template
    template = TechSpecTemplate(language)
    
    # Check if this is the first interaction with the tech spec creator
    if not metadata.get('tech_spec_started'):
        # Mark that we've started the tech spec creation process
        metadata['tech_spec_started'] = True
        metadata['tech_spec_section'] = 0
        metadata['tech_spec_answers'] = []
        
        # Initial greeting
        greeting = "Let's create a technical specification for your project. I'll ask you a series of questions."
        if language == 'ru':
            greeting = "Давайте создадим техническое задание для вашего проекта. Я задам вам ряд вопросов."
        elif language == 'de':
            greeting = "Lassen Sie uns eine technische Spezifikation für Ihr Projekt erstellen. Ich werde Ihnen eine Reihe von Fragen stellen."
        
        # Start with the first question
        current_section = template.sections[0]
        first_question = current_section['title']
        
        # Combine greeting and first question
        full_response = f"{greeting}\n\n{first_question}"
        
        return {
            'agent': 'requirements',
            'answer': full_response,
            'interactive': {
                'text': full_response,
                'buttons': [],
                'requires_input': True,
                'meta': {'agent': 'requirements'}
            }
        }
    
    # Process the answer to the current question
    current_section_index = metadata.get('tech_spec_section', 0)
    answers = metadata.get('tech_spec_answers', [])
    
    # Store the user's answer for the current section
    if current_section_index < len(template.sections):
        answers.append(message)
        metadata['tech_spec_answers'] = answers
    
    # Advance to the next section
    current_section_index += 1
    metadata['tech_spec_section'] = current_section_index
    
    # Check if we've completed all sections
    if current_section_index >= len(template.sections):
        # Tech spec complete
        thank_message = "Thank you! Your technical specification has been created and sent to our team."
        if language == 'ru':
            thank_message = "Спасибо! Ваше техническое задание создано и отправлено нашей команде."
        elif language == 'de':
            thank_message = "Vielen Dank! Ihre technische Spezifikation wurde erstellt und an unser Team gesendet."
        
        # Prepare tech spec data for notification
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
        
        # Гибридный подход: пытаемся отправить напрямую, в случае неудачи используем очередь
        from app.utils.telegram_queue import send_telegram_message_with_retry
        
        try:
            # Сначала попробуем отправить напрямую
            success = send_tech_spec_notification(tech_spec_data, contact_info)
            if success:
                current_app.logger.info(f"Technical specification notification SENT directly for {user_email}")
            else:
                # Если не удалось отправить напрямую, помещаем в очередь
                message_content = send_tech_spec_notification(tech_spec_data, contact_info, return_message_only=True)
                from app.utils.telegram_queue import queue_telegram_message
                queue_telegram_message(message_content)
                current_app.logger.info(f"Technical specification notification QUEUED for {user_email} (direct send failed)")
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
        
    # Continue with the next question
    current_section = template.sections[current_section_index]
    next_question = current_section['title']
    
    return {
        'agent': 'requirements',
        'answer': next_question,
        'interactive': {
            'text': next_question,
            'buttons': [],
            'requires_input': True,
            'meta': {'agent': 'requirements'}
        }
    }

def handle_quiz(message, metadata):
    """Handle the website cost calculation quiz"""
    language = metadata.get('language', 'en')
    
    # Check if this is the first interaction with the quiz
    if not metadata.get('quiz_started'):
        # Mark that we've started the quiz
        metadata['quiz_started'] = True
        metadata['quiz_step'] = 0
        metadata['quiz_answers'] = []
        
        # Define the quiz structure here or load from a configuration
        quiz_config = [
            {
                'question': {
                    'en': "What type of website do you need?",
                    'ru': "Какой тип сайта вам нужен?",
                    'de': "Welche Art von Website benötigen Sie?"
                },
                'choices': [
                    {
                        'text': {'en': "Landing page", 'ru': "Лендинг", 'de': "Landingpage"},
                        'value': "landing",
                        'cost': 500
                    },
                    {
                        'text': {'en': "Corporate website", 'ru': "Корпоративный сайт", 'de': "Unternehmenswebsite"},
                        'value': "corporate",
                        'cost': 1200
                    },
                    {
                        'text': {'en': "E-commerce", 'ru': "Интернет-магазин", 'de': "E-Commerce"},
                        'value': "ecommerce",
                        'cost': 2000
                    },
                    {
                        'text': {'en': "Web application", 'ru': "Веб-приложение", 'de': "Webanwendung"},
                        'value': "webapp",
                        'cost': 3000
                    }
                ]
            },
            {
                'question': {
                    'en': "Do you need a custom design?",
                    'ru': "Нужен ли вам индивидуальный дизайн?",
                    'de': "Benötigen Sie ein individuelles Design?"
                },
                'choices': [
                    {
                        'text': {'en': "Template-based", 'ru': "На основе шаблона", 'de': "Basierend auf einer Vorlage"},
                        'value': "template",
                        'cost': 0
                    },
                    {
                        'text': {'en': "Custom design", 'ru': "Индивидуальный дизайн", 'de': "Individuelles Design"},
                        'value': "custom",
                        'cost': 800
                    },
                    {
                        'text': {'en': "Premium custom design", 'ru': "Премиум индивидуальный дизайн", 'de': "Premium individuelles Design"},
                        'value': "premium",
                        'cost': 1500
                    }
                ]
            },
            {
                'question': {
                    'en': "Do you need additional features?",
                    'ru': "Нужны ли дополнительные функции?",
                    'de': "Benötigen Sie zusätzliche Funktionen?"
                },
                'choices': [
                    {
                        'text': {'en': "Basic functionality", 'ru': "Базовая функциональность", 'de': "Grundfunktionalität"},
                        'value': "basic",
                        'cost': 0
                    },
                    {
                        'text': {'en': "CMS integration", 'ru': "Интеграция CMS", 'de': "CMS-Integration"},
                        'value': "cms",
                        'cost': 500
                    },
                    {
                        'text': {'en': "Advanced features", 'ru': "Расширенные функции", 'de': "Erweiterte Funktionen"},
                        'value': "advanced",
                        'cost': 1200
                    },
                    {
                        'text': {'en': "Custom functionality", 'ru': "Нестандартная функциональность", 'de': "Benutzerdefinierte Funktionalität"},
                        'value': "custom_func",
                        'cost': 2000
                    }
                ]
            }
        ]
        
        # Store the quiz configuration in metadata
        metadata['quiz_config'] = quiz_config
        
        # Show the first quiz question
        first_step = quiz_config[0]
        question = first_step['question'].get(language, first_step['question']['en'])
        
        # Create buttons from the choices
        buttons = []
        for choice in first_step['choices']:
            buttons.append({
                'text': choice['text'].get(language, choice['text']['en']),
                'value': choice['value'],
                'description': ''
            })
        
        return {
            'agent': 'quiz',
            'answer': question,
            'interactive': {
                'text': question,
                'buttons': buttons,
                'requires_input': True,
                'meta': {'agent': 'quiz'}
            }
        }
    
    # Process the answer to the current question
    current_step = metadata.get('quiz_step', 0)
    quiz_config = metadata.get('quiz_config', [])
    answers = metadata.get('quiz_answers', [])
    
    # Find the choice that was selected and store its value and cost
    selected_choice = None
    current_question = quiz_config[current_step]
    
    for choice in current_question['choices']:
        if choice['value'] == message:
            selected_choice = choice
            break
    
    # If no valid choice was selected, provide an error message
    if not selected_choice:
        error_msg = "Please select one of the available options."
        if language == 'ru':
            error_msg = "Пожалуйста, выберите один из доступных вариантов."
        elif language == 'de':
            error_msg = "Bitte wählen Sie eine der verfügbaren Optionen."
        
        # Recreate buttons for the current question
        buttons = []
        for choice in current_question['choices']:
            buttons.append({
                'text': choice['text'].get(language, choice['text']['en']),
                'value': choice['value'],
                'description': ''
            })
        
        return {
            'agent': 'quiz',
            'answer': error_msg,
            'interactive': {
                'text': error_msg,
                'buttons': buttons,
                'requires_input': True,
                'meta': {'agent': 'quiz'}
            }
        }
    
    # Store the answer
    answers.append({
        'question': current_question['question'].get(language, current_question['question']['en']),
        'answer': selected_choice['text'].get(language, selected_choice['text']['en']),
        'value': selected_choice['value'],
        'cost': selected_choice['cost']
    })
    metadata['quiz_answers'] = answers
    
    # Move to the next question
    current_step += 1
    metadata['quiz_step'] = current_step
    
    # Check if we've completed all questions
    if current_step >= len(quiz_config):
        # Calculate the total cost
        total_cost = sum(answer['cost'] for answer in answers)
        
        # Format the result message
        result_msg = f"Based on your answers, the estimated cost of your website is ${total_cost}."
        if language == 'ru':
            result_msg = f"На основе ваших ответов, ориентировочная стоимость вашего сайта составляет ${total_cost}."
        elif language == 'de':
            result_msg = f"Basierend auf Ihren Antworten beträgt die geschätzte Kosten Ihrer Website ${total_cost}."
        
        # Add summary of selections
        result_msg += "\n\n"
        if language == 'en':
            result_msg += "Summary of your choices:"
        elif language == 'ru':
            result_msg += "Сводка ваших выборов:"
        elif language == 'de':
            result_msg += "Zusammenfassung Ihrer Auswahl:"
        
        for answer in answers:
            result_msg += f"\n- {answer['question']}: {answer['answer']}"
        
        # Add a call to action
        if language == 'en':
            result_msg += "\n\nWould you like to discuss your project with our team?"
        elif language == 'ru':
            result_msg += "\n\nХотите обсудить ваш проект с нашей командой?"
        elif language == 'de':
            result_msg += "\n\nMöchten Sie Ihr Projekt mit unserem Team besprechen?"
        
        # Provide contact buttons
        buttons = [
            {
                'text': 'Contact us' if language == 'en' else ('Связаться с нами' if language == 'ru' else 'Kontaktieren Sie uns'),
                'value': 'contact',
                'description': 'Get in touch with our team' if language == 'en' else 
                              ('Связаться с нашей командой' if language == 'ru' else 
                               'Nehmen Sie Kontakt mit unserem Team auf')
            },
            {
                'text': 'Restart quiz' if language == 'en' else ('Перезапустить тест' if language == 'ru' else 'Quiz neu starten'),
                'value': 'restart_quiz',
                'description': 'Start the cost calculator again' if language == 'en' else 
                              ('Начать калькулятор стоимости заново' if language == 'ru' else 
                               'Starten Sie den Kostenrechner erneut')
            }
        ]
        
        # Clear quiz state but keep the answers for reference
        metadata.pop('quiz_started', None)
        metadata.pop('quiz_step', None)
        
        return {
            'agent': 'quiz',
            'answer': result_msg,
            'interactive': {
                'text': result_msg,
                'buttons': buttons,
                'requires_input': True,
                'meta': {'agent': 'quiz', 'completed': True, 'total_cost': total_cost}
            }
        }
    
    # Show the next question
    next_step = quiz_config[current_step]
    question = next_step['question'].get(language, next_step['question']['en'])
    
    # Create buttons from the choices
    buttons = []
    for choice in next_step['choices']:
        buttons.append({
            'text': choice['text'].get(language, choice['text']['en']),
            'value': choice['value'],
            'description': ''
        })
    
    return {
        'agent': 'quiz',
        'answer': question,
        'interactive': {
            'text': question,
            'buttons': buttons,
            'requires_input': True,
            'meta': {'agent': 'quiz'}
        }
    }

def send_tech_spec_notification(tech_spec_data, contact_info, return_message_only=False):
    """Send a notification about a new technical specification submission"""
    # Format the message
    message = "🔔 New Technical Specification Submission\n\n"
    
    # Add contact information
    message += "👤 Contact Information:\n"
    message += f"Name: {contact_info.get('name', 'N/A')}\n"
    message += f"Email: {contact_info.get('email', 'N/A')}\n"
    message += f"Phone: {contact_info.get('phone', 'N/A')}\n\n"
    
    # Add technical specification answers
    message += "📋 Technical Specification:\n"
    for item in tech_spec_data['answers']:
        message += f"\n❓ {item['question']}\n"
        message += f"➡️ {item['answer']}\n"
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message += f"\n📅 Submitted on: {timestamp}"
    
    # If we only need the message content, return it
    if return_message_only:
        return message
    
    # Otherwise, try to send the message
    try:
        from app.services.telegram_service import send_telegram_message
        return send_telegram_message(message)
    except Exception as e:
        logger.error(f"Failed to send tech spec notification: {e}")
        return False
