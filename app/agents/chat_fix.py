"""
Emergency fix for chat functionality
"""
from flask import current_app
import os
import json
import time
import uuid
from ..models import ChatMessage
from .. import db

# Default system prompts for different languages
SYSTEM_PROMPTS = {
    'uk': """Ви - асистент для веб-студії Rozoom-KI. Відповідайте клієнтам ввічливо та професійно.
Мова спілкування: українська. Відповідайте коротко та по суті.""",
    'ru': """Вы - ассистент для веб-студии Rozoom-KI. Отвечайте клиентам вежливо и профессионально.
Язык общения: русский. Отвечайте кратко и по существу.""",
    'en': """You are an assistant for the Rozoom-KI web studio. Respond to clients politely and professionally.
Communication language: English. Keep your answers short and to the point.""",
    'de': """Sie sind ein Assistent für das Webstudio Rozoom-KI. Antworten Sie höflich und professionell auf Kunden.
Kommunikationssprache: Deutsch. Halten Sie Ihre Antworten kurz und auf den Punkt gebracht."""
}

def simple_chat_response(message, metadata=None):
    """
    Simple chat response function that doesn't depend on external APIs or databases
    """
    if metadata is None:
        metadata = {}
        
    try:
        # Get language from metadata or default to Ukrainian
        language = metadata.get('language', 'uk')
        
        # Generate a conversation_id if not provided
        conversation_id = metadata.get('conversation_id')
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            metadata['conversation_id'] = conversation_id
            
        current_app.logger.info(f"Simple chat: Processing message in {language} language")
        
        # Skip database storage completely to avoid database schema issues
        current_app.logger.info("Skipping database storage for chat messages")
        
        # Create a response based on the message
        if not message or message.strip() == '':
            # Initial greeting if no message is provided
            responses = {
                'uk': "Вітаю! Я віртуальний асистент Rozoom-KI. Чим можу допомогти?",
                'ru': "Здравствуйте! Я виртуальный ассистент Rozoom-KI. Чем могу помочь?",
                'en': "Hello! I'm the Rozoom-KI virtual assistant. How can I help you?",
                'de': "Hallo! Ich bin der virtuelle Assistent von Rozoom-KI. Wie kann ich Ihnen helfen?"
            }
            answer = responses.get(language, responses['uk'])
        else:
            # Check for specific keywords first for better responses
            message_lower = message.lower()
        
            # Check for keyword "маркет" (marketing)
            if any(word in message_lower for word in ["маркет", "market", "marketing", "маркетинг"]):
                if language == 'uk':
                    answer = """Для автоматизації маркетингу Rozoom-KI пропонує:
1. Інтеграцію з CRM системами
2. Автоматичні email-розсилки
3. Аналітику ефективності рекламних кампаній
4. Налаштування таргетованої реклами
5. Автоматизацію постів у соціальних мережах

Який аспект маркетингу вас цікавить найбільше?"""
                elif language == 'ru':
                    answer = """Для автоматизации маркетинга Rozoom-KI предлагает:
1. Интеграцию с CRM системами
2. Автоматические email-рассылки
3. Аналитику эффективности рекламных кампаний
4. Настройку таргетированной рекламы
5. Автоматизацию постов в социальных сетях

Какой аспект маркетинга вас интересует больше всего?"""
                elif language == 'en':
                    answer = """For marketing automation, Rozoom-KI offers:
1. Integration with CRM systems
2. Automated email campaigns
3. Ad campaign performance analytics
4. Targeted advertising setup
5. Social media post automation

Which aspect of marketing are you most interested in?"""
                elif language == 'de':
                    answer = """Für Marketing-Automatisierung bietet Rozoom-KI:
1. Integration mit CRM-Systemen
2. Automatisierte E-Mail-Kampagnen
3. Analyse der Werbekampagnenleistung
4. Einrichtung zielgerichteter Werbung
5. Automatisierung von Social-Media-Beiträgen

Welcher Aspekt des Marketings interessiert Sie am meisten?"""
                    
            # Check for tech spec related keywords
            elif any(word in message_lower for word in ["тех", "tech", "specification", "завдання", "задание", "специфікація"]):
                try:
                    # Try to use the tech_spec module for more interactive responses
                    from .tech_spec import get_tech_spec_prompt
                    tech_spec_section = metadata.get('tech_spec_section', 0)
                    
                    # First time asking about tech spec
                    if tech_spec_section == 0:
                        # Update metadata to start the tech spec process
                        metadata['tech_spec_section'] = 0
                        answer = get_tech_spec_prompt(metadata)
                    else:
                        # User is already in the tech spec process, move to next section
                        metadata['tech_spec_section'] = tech_spec_section + 1
                        answer = get_tech_spec_prompt(metadata)
                        
                except Exception as e:
                    # Fall back to static responses if there's an error
                    current_app.logger.error(f"Error using tech_spec module: {e}")
                    if language == 'uk':
                        answer = """Ви можете заповнити технічне завдання на нашому сайті у розділі "Технічне завдання" або через форму замовлення. 
Це допоможе нам краще зрозуміти ваші потреби та розробити оптимальне рішення для вашого проєкту.

Якщо хочете розпочати заповнення технічного завдання зараз, просто скажіть "почати техзавдання" і я проведу вас через цей процес."""
                    elif language == 'ru':
                        answer = """Вы можете заполнить техническое задание на нашем сайте в разделе "Техническое задание" или через форму заказа.
Это поможет нам лучше понять ваши потребности и разработать оптимальное решение для вашего проекта.

Если хотите начать заполнение технического задания сейчас, просто скажите "начать техзадание" и я проведу вас через этот процесс."""
                    elif language == 'en':
                        answer = """You can fill out a technical specification on our website in the "Technical Specification" section or through the order form.
This will help us better understand your needs and develop the optimal solution for your project.

If you want to start filling out the technical specification now, just say "start tech spec" and I'll guide you through the process."""
                    elif language == 'de':
                        answer = """Sie können eine technische Spezifikation auf unserer Website im Bereich "Technische Spezifikation" oder über das Bestellformular ausfüllen.
Dies hilft uns, Ihre Bedürfnisse besser zu verstehen und die optimale Lösung für Ihr Projekt zu entwickeln.

Wenn Sie jetzt mit dem Ausfüllen der technischen Spezifikation beginnen möchten, sagen Sie einfach "Technische Spezifikation starten" und ich führe Sie durch den Prozess."""
                    
            # Check for tech spec start keywords
            elif any(phrase in message_lower for phrase in ["почати техзавдання", "начать техзадание", "start tech spec", "технічне завдання", "техническое задание"]):
                try:
                    # Use the tech_spec module to start the tech spec process
                    from .tech_spec import get_tech_spec_prompt
                    
                    # Reset tech_spec_section to start from the beginning
                    metadata['tech_spec_section'] = 0
                    answer = get_tech_spec_prompt(metadata)
                        
                except Exception as e:
                    # Fall back to static responses if there's an error
                    current_app.logger.error(f"Error starting tech spec process: {e}")
                    if language == 'uk':
                        answer = """На даний момент у нас виникли технічні труднощі з запуском процесу заповнення технічного завдання. 
Будь ласка, спробуйте пізніше або заповніть форму на нашому веб-сайті."""
                    elif language == 'ru':
                        answer = """В настоящее время у нас возникли технические трудности с запуском процесса заполнения технического задания. 
Пожалуйста, попробуйте позже или заполните форму на нашем веб-сайте."""
                    elif language == 'en':
                        answer = """We are currently experiencing technical difficulties with starting the technical specification process. 
Please try again later or fill out the form on our website."""
                    else:
                        answer = """Wir haben derzeit technische Schwierigkeiten mit dem Start des technischen Spezifikationsprozesses. 
Bitte versuchen Sie es später erneut oder füllen Sie das Formular auf unserer Website aus."""
            
            # Check for chat system related keywords
            elif any(word in message_lower for word in ["чат", "chat", "відповід", "отвеч", "answer", "ответ"]):
                if language == 'uk':
                    answer = """Наш чат-бот працює в режимі простих відповідей. Я намагаюся надати вам корисну інформацію про послуги Rozoom-KI.
Якщо у вас є конкретні питання про веб-розробку, дизайн, маркетинг або інші послуги, я радий на них відповісти."""
                elif language == 'ru':
                    answer = """Наш чат-бот работает в режиме простых ответов. Я стараюсь предоставить вам полезную информацию об услугах Rozoom-KI.
Если у вас есть конкретные вопросы о веб-разработке, дизайне, маркетинге или других услугах, я рад на них ответить."""
                elif language == 'en':
                    answer = """Our chatbot operates in a simple response mode. I try to provide you with useful information about Rozoom-KI services.
If you have specific questions about web development, design, marketing, or other services, I'm happy to answer them."""
                elif language == 'de':
                    answer = """Unser Chatbot arbeitet im einfachen Antwortmodus. Ich versuche, Ihnen nützliche Informationen über die Dienste von Rozoom-KI zu geben.
Wenn Sie konkrete Fragen zur Webentwicklung, Design, Marketing oder anderen Dienstleistungen haben, beantworte ich diese gerne."""
                    
            # Check for website development keywords
            elif any(word in message_lower for word in ["веб", "сайт", "web", "website", "розробка", "разработка", "development"]):
                if language == 'uk':
                    answer = """Rozoom-KI пропонує повний цикл розробки веб-сайтів:

1. Розробка інтернет-магазинів
2. Створення корпоративних сайтів
3. Розробка лендінг-сторінок
4. Інтеграція з CRM та платіжними системами
5. Адаптивний дизайн для всіх пристроїв
6. SEO-оптимізація

Наша команда використовує сучасні технології для створення швидких, безпечних та функціональних веб-рішень.
Який тип сайту вас цікавить?"""
                elif language == 'ru':
                    answer = """Rozoom-KI предлагает полный цикл разработки веб-сайтов:

1. Разработка интернет-магазинов
2. Создание корпоративных сайтов
3. Разработка лендинг-страниц
4. Интеграция с CRM и платежными системами
5. Адаптивный дизайн для всех устройств
6. SEO-оптимизация

Наша команда использует современные технологии для создания быстрых, безопасных и функциональных веб-решений.
Какой тип сайта вас интересует?"""
                elif language == 'en':
                    answer = """Rozoom-KI offers a full cycle of website development:

1. E-commerce development
2. Corporate website creation
3. Landing page development
4. CRM and payment system integration
5. Responsive design for all devices
6. SEO optimization

Our team uses modern technologies to create fast, secure, and functional web solutions.
What type of website are you interested in?"""
                else:
                    answer = """Rozoom-KI bietet einen vollständigen Webentwicklungszyklus:

1. E-Commerce-Entwicklung
2. Erstellung von Unternehmenswebsites
3. Entwicklung von Landingpages
4. CRM- und Zahlungssystemintegration
5. Responsives Design für alle Geräte
6. SEO-Optimierung

Unser Team verwendet moderne Technologien, um schnelle, sichere und funktionale Weblösungen zu erstellen.
An welchem Websitetyp sind Sie interessiert?"""

            # Check for AI/ML related keywords
            elif any(word in message_lower for word in ["ai", "ml", "artificial", "machine", "штучн", "искусств", "машин", "розумн"]):
                if language == 'uk':
                    answer = """Rozoom-KI пропонує інноваційні рішення у сфері штучного інтелекту:

1. Інтеграція AI-чат-ботів для обслуговування клієнтів
2. Системи аналізу даних на основі машинного навчання
3. Автоматизація бізнес-процесів за допомогою AI
4. Персоналізовані рекомендаційні системи
5. Комп'ютерний зір для автоматизації процесів

Який напрямок AI вас цікавить найбільше?"""
                elif language == 'ru':
                    answer = """Rozoom-KI предлагает инновационные решения в сфере искусственного интеллекта:

1. Интеграция AI-чат-ботов для обслуживания клиентов
2. Системы анализа данных на основе машинного обучения
3. Автоматизация бизнес-процессов с помощью AI
4. Персонализированные рекомендательные системы
5. Компьютерное зрение для автоматизации процессов

Какое направление AI вас интересует больше всего?"""
                elif language == 'en':
                    answer = """Rozoom-KI offers innovative solutions in artificial intelligence:

1. Integration of AI chatbots for customer service
2. Machine learning based data analysis systems
3. Business process automation with AI
4. Personalized recommendation systems
5. Computer vision for process automation

Which AI direction interests you the most?"""
                else:
                    answer = """Rozoom-KI bietet innovative Lösungen im Bereich der künstlichen Intelligenz:

1. Integration von KI-Chatbots für den Kundenservice
2. Datenanalysesysteme auf Basis von maschinellem Lernen
3. Automatisierung von Geschäftsprozessen mit KI
4. Personalisierte Empfehlungssysteme
5. Computer Vision für Prozessautomatisierung

Welche KI-Richtung interessiert Sie am meisten?"""
            
            # Default response if no keywords match
            else:
                responses = {
                    'uk': """Дякую за ваше звернення до Rozoom-KI. Ми спеціалізуємось на:

1. Розробці сучасних веб-сайтів та веб-додатків
2. Маркетингових рішеннях та автоматизації реклами
3. Автоматизації бізнес-процесів за допомогою AI
4. Розробці мобільних додатків
5. Технічній підтримці та обслуговуванні

Чим саме ми можемо вам допомогти? Напишіть про ваш проєкт або потребу детальніше.""",
                    'ru': """Спасибо за ваше обращение в Rozoom-KI. Мы специализируемся на:

1. Разработке современных веб-сайтов и веб-приложений
2. Маркетинговых решениях и автоматизации рекламы
3. Автоматизации бизнес-процессов с помощью AI
4. Разработке мобильных приложений
5. Технической поддержке и обслуживании

Чем именно мы можем вам помочь? Напишите о вашем проекте или потребности подробнее.""",
                    'en': """Thank you for contacting Rozoom-KI. We specialize in:

1. Development of modern websites and web applications
2. Marketing solutions and advertising automation
3. Business process automation using AI
4. Mobile app development
5. Technical support and maintenance

How exactly can we help you? Please write about your project or need in more detail.""",
                    'de': """Vielen Dank für Ihre Kontaktaufnahme mit Rozoom-KI. Wir sind spezialisiert auf:

1. Entwicklung moderner Websites und Webanwendungen
2. Marketinglösungen und Werbungsautomatisierung
3. Automatisierung von Geschäftsprozessen mit KI
4. Entwicklung mobiler Anwendungen
5. Technischer Support und Wartung

Wie genau können wir Ihnen helfen? Bitte schreiben Sie ausführlicher über Ihr Projekt oder Ihren Bedarf."""
                }
                answer = responses.get(language, responses['uk'])
        
        # Return the response
        return {
            'agent': 'ChatGPT',
            'answer': answer,
            'conversation_id': conversation_id
        }
            
    except Exception as e:
        import traceback
        current_app.logger.error(f"Error in simple_chat_response: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        # Return error message in the appropriate language
        error_messages = {
            'uk': f"Вибачте, сталася помилка. Спробуйте ще раз пізніше.",
            'ru': f"Извините, произошла ошибка. Попробуйте еще раз позже.",
            'en': f"Sorry, an error occurred. Please try again later.",
            'de': f"Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."
        }
        
        language = metadata.get('language', 'uk')
        
        return {
            'error': str(e),
            'answer': error_messages.get(language, error_messages['uk']),
            'agent': 'ErrorHandler',
            'conversation_id': metadata.get('conversation_id', str(uuid.uuid4()))
        }
