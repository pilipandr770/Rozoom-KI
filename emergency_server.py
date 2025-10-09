from flask import Flask, request, jsonify, render_template
import os
import uuid
import logging
from logging.handlers import RotatingFileHandler
import datetime

# Define in-memory conversation store
conversations = {}

def create_app():
    app = Flask(__name__, 
               static_folder='app/static',
               template_folder='app/templates')
    
    # Configure logging
    if not os.path.exists('logs'):
        os.mkdir('logs')

    handler = RotatingFileHandler('logs/emergency_server.log', maxBytes=10000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s'
    ))
    handler.setLevel(logging.INFO)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    
    # Home page - serve the chat test page
    @app.route('/')
    def index():
        return render_template('chat_test.html')
    
    # Simple chat API endpoint
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            # Get data from request
            data = request.get_json() or {}
            message = data.get('message', '')
            metadata = data.get('metadata', {})
            
            app.logger.info(f"Chat request received: {message[:50]}...")
            
            # Ensure conversation_id exists
            if not metadata.get('conversation_id'):
                import uuid
                metadata['conversation_id'] = str(uuid.uuid4())
                
            # Get user language
            language = metadata.get('language', 'uk')
            conversation_id = metadata.get('conversation_id')
            
            # Store message in memory
            if conversation_id not in conversations:
                conversations[conversation_id] = []
                
            conversations[conversation_id].append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Check for specific keywords for better responses
            message_lower = message.lower()
            
            # Check for marketing related keywords
            if any(word in message_lower for word in ["маркет", "market", "marketing", "маркетинг"]):
                if language == 'uk':
                    answer = """Для автоматизації маркетингу Andrii Pylypchuk пропонує:
1. Інтеграцію з CRM системами
2. Автоматичні email-розсилки
3. Аналітику ефективності рекламних кампаній
4. Налаштування таргетованої реклами
5. Автоматизацію постів у соціальних мережах

Який аспект маркетингу вас цікавить найбільше?"""
                elif language == 'ru':
                    answer = """Для автоматизации маркетинга Andrii Pylypchuk предлагает:
1. Интеграцию с CRM системами
2. Автоматические email-рассылки
3. Аналитику эффективности рекламных кампаний
4. Настройку таргетированной рекламы
5. Автоматизацию постов в социальных сетях

Какой аспект маркетинга вас интересует больше всего?"""
                elif language == 'en':
                    answer = """For marketing automation, Andrii Pylypchuk offers:
1. Integration with CRM systems
2. Automated email campaigns
3. Ad campaign performance analytics
4. Targeted advertising setup
5. Social media post automation

Which aspect of marketing are you most interested in?"""
                else:
                    answer = """Für Marketing-Automatisierung bietet Andrii Pylypchuk:
1. Integration mit CRM-Systemen
2. Automatisierte E-Mail-Kampagnen
3. Analyse der Werbekampagnenleistung
4. Einrichtung zielgerichteter Werbung
5. Automatisierung von Social-Media-Beiträgen

Welcher Aspekt des Marketings interessiert Sie am meisten?"""
            # Check for tech spec related keywords
            elif any(word in message_lower for word in ["тех", "tech", "specification", "завдання", "задание", "специфікація"]):
                if language == 'uk':
                    answer = """Ви можете заповнити технічне завдання на нашому сайті у розділі "Технічне завдання" або через форму замовлення. 
Це допоможе нам краще зрозуміти ваші потреби та розробити оптимальне рішення для вашого проекту."""
                elif language == 'ru':
                    answer = """Вы можете заполнить техническое задание на нашем сайте в разделе "Техническое задание" или через форму заказа.
Это поможет нам лучше понять ваши потребности и разработать оптимальное решение для вашего проекта."""
                elif language == 'en':
                    answer = """You can fill out a technical specification on our website in the "Technical Specification" section or through the order form.
This will help us better understand your needs and develop the optimal solution for your project."""
                else:
                    answer = """Sie können eine technische Spezifikation auf unserer Website im Bereich "Technische Spezifikation" oder über das Bestellformular ausfüllen.
Dies hilft uns, Ihre Bedürfnisse besser zu verstehen und die optimale Lösung für Ihr Projekt zu entwickeln."""
                    
            # Check for chat system related keywords
            elif any(word in message_lower for word in ["чат", "chat", "відповід", "отвеч", "answer", "ответ"]):
                if language == 'uk':
                    answer = """Наш чат-бот працює в режимі простих відповідей. Я намагаюся надати вам корисну інформацію про послуги Andrii Pylypchuk.
Якщо у вас є конкретні питання про веб-розробку, дизайн, маркетинг або інші послуги, я радий на них відповісти."""
                elif language == 'ru':
                    answer = """Наш чат-бот работает в режиме простых ответов. Я стараюсь предоставить вам полезную информацию об услугах Rozoom-KI.
Если у вас есть конкретные вопросы о веб-разработке, дизайне, маркетинге или других услугах, я рад на них ответить."""
                elif language == 'en':
                    answer = """Our chatbot operates in a simple response mode. I try to provide you with useful information about Rozoom-KI services.
If you have specific questions about web development, design, marketing, or other services, I'm happy to answer them."""
                else:
                    answer = """Unser Chatbot arbeitet im einfachen Antwortmodus. Ich versuche, Ihnen nützliche Informationen über die Dienste von Rozoom-KI zu geben.
Wenn Sie konkrete Fragen zur Webentwicklung, Design, Marketing oder anderen Dienstleistungen haben, beantworte ich diese gerne."""
                    
            # Default response if no keywords match
            else:
                responses = {
                    'uk': """Дякую за ваше звернення до Rozoom-KI. Ми спеціалізуємось на розробці сучасних веб-сайтів, 
маркетингових рішеннях та автоматизації бізнес-процесів. Чим саме ми можемо вам допомогти?""",
                    'ru': """Спасибо за ваше обращение в Rozoom-KI. Мы специализируемся на разработке современных веб-сайтов, 
маркетинговых решениях и автоматизации бизнес-процессов. Чем именно мы можем вам помочь?""",
                    'en': """Thank you for contacting Rozoom-KI. We specialize in developing modern websites, 
marketing solutions, and business process automation. How exactly can we help you?""",
                    'de': """Vielen Dank für Ihre Kontaktaufnahme mit Rozoom-KI. Wir sind spezialisiert auf die Entwicklung moderner Websites, 
Marketinglösungen und die Automatisierung von Geschäftsprozessen. Wie genau können wir Ihnen helfen?"""
                }
                answer = responses.get(language, responses['uk'])
            
            # Store the response in conversation history
            conversations[conversation_id].append({
                'role': 'assistant',
                'content': answer,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Create the response
            response = {
                'answer': answer,
                'agent': 'ChatGPT',
                'conversation_id': metadata.get('conversation_id')
            }
            
            app.logger.info(f"Sending response: {response['answer'][:50]}...")
            return jsonify(response)
            
        except Exception as e:
            app.logger.error(f"Error processing request: {str(e)}")
            import traceback
            app.logger.error(traceback.format_exc())
            
            # Error messages based on language
            error_messages = {
                'uk': f"Вибачте, сталася помилка. Спробуйте ще раз пізніше.",
                'ru': f"Извините, произошла ошибка. Попробуйте еще раз позже.",
                'en': f"Sorry, an error occurred. Please try again later.",
                'de': f"Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."
            }
            
            language = request.json.get('metadata', {}).get('language', 'uk')
            
            return jsonify({
                'error': str(e),
                'answer': error_messages.get(language, error_messages['uk']),
                'agent': 'ErrorHandler'
            }), 200  # Return 200 so error message displays in UI
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
