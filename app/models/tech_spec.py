"""
Модуль для работы с шаблонами технических заданий
"""
from app.models.language import get_text_by_key


class TechSpecTemplate:
    """
    Класс для работы с шаблонами технических заданий
    """

    def __init__(self, language='de'):
        """
        Инициализация шаблона технического задания

        Args:
            language: Код языка ('de',  'en')
        """
        self.language = language
        self.sections = self._get_sections()

    def _get_sections(self):
        """
        Получить список секций технического задания

        Returns:
            list: Список секций с вопросами
        """
        sections = [
            {
                'id': 'project_type',
                'title': self._get_text('project_type_question'),
                'description': self._get_text('project_type_description'),
                'required': True
            },
            {
                'id': 'project_goal',
                'title': self._get_text('project_goal_question'),
                'description': self._get_text('project_goal_description'),
                'required': True
            },
            {
                'id': 'target_audience',
                'title': self._get_text('target_audience_question'),
                'description': self._get_text('target_audience_description'),
                'required': True
            },
            {
                'id': 'features',
                'title': self._get_text('features_question'),
                'description': self._get_text('features_description'),
                'required': True
            },
            {
                'id': 'design_preferences',
                'title': self._get_text('design_preferences_question'),
                'description': self._get_text('design_preferences_description'),
                'required': False
            },
            {
                'id': 'references',
                'title': self._get_text('references_question'),
                'description': self._get_text('references_description'),
                'required': False
            },
            {
                'id': 'technical_requirements',
                'title': self._get_text('technical_requirements_question'),
                'description': self._get_text('technical_requirements_description'),
                'required': True
            },
            {
                'id': 'integrations',
                'title': self._get_text('integrations_question'),
                'description': self._get_text('integrations_description'),
                'required': False
            },
            {
                'id': 'content_requirements',
                'title': self._get_text('content_requirements_question'),
                'description': self._get_text('content_requirements_description'),
                'required': False
            },
            {
                'id': 'timeline',
                'title': self._get_text('timeline_question'),
                'description': self._get_text('timeline_description'),
                'required': True
            },
            {
                'id': 'budget',
                'title': self._get_text('budget_question'),
                'description': self._get_text('budget_description'),
                'required': True
            },
            {
                'id': 'post_launch_services',
                'title': self._get_text('post_launch_services_question'),
                'description': self._get_text('post_launch_services_description'),
                'required': False
            },
            {
                'id': 'discovery_source',
                'title': self._get_text('discovery_source_question'),
                'description': self._get_text('discovery_source_description'),
                'required': False
            },
            {
                'id': 'communication_preference',
                'title': self._get_text('communication_preference_question'),
                'description': self._get_text('communication_preference_description'),
                'required': True
            },
            {
                'id': 'contact_info',
                'title': self._get_text('contact_info_question'),
                'description': self._get_text('contact_info_description'),
                'required': True
            }
        ]

        return sections

    def _get_text(self, key):
        """
        Получить текст по ключу для текущего языка

        Args:
            key: Ключ текста

        Returns:
            str: Текст на текущем языке
        """
        # Словарь с текстами на разных языках
        texts = {
            # Вопросы
            'project_type_question': {
                'de': '1. Welche Art von Projekt planen Sie?',
                'ru': '1. Какой тип проекта вы планируете?',
                'en': '1. What type of project are you planning?'
            },
            'project_goal_question': {
                'de': '2. Was ist das Hauptziel Ihres Projekts?',
                'ru': '2. Какова основная цель вашего проекта?',
                'en': '2. What is the main goal of your project?'
            },
            'target_audience_question': {
                'de': '3. Wer ist Ihre Zielgruppe?',
                'ru': '3. Кто является вашей целевой аудиторией?',
                'en': '3. Who is your target audience?'
            },
            'features_question': {
                'de': '4. Welche Funktionen soll Ihr Projekt haben?',
                'ru': '4. Какие функции должно иметь ваше проект?',
                'en': '4. What features should your project have?'
            },
            'design_preferences_question': {
                'de': '5. Haben Sie Design-Vorlieben oder -Anforderungen?',
                'ru': '5. Есть ли у вас предпочтения или требования к дизайну?',
                'en': '5. Do you have design preferences or requirements?'
            },
            'references_question': {
                'de': '6. Haben Sie Referenzen oder Beispiele, die Ihnen gefallen?',
                'ru': '6. Есть ли у вас референсы или примеры, которые вам нравятся?',
                'en': '6. Do you have references or examples you like?'
            },
            'technical_requirements_question': {
                'de': '7. Welche technischen Anforderungen haben Sie?',
                'ru': '7. Какие у вас технические требования?',
                'en': '7. What are your technical requirements?'
            },
            'integrations_question': {
                'de': '8. Welche Integrationen benötigen Sie?',
                'ru': '8. Какие интеграции вам нужны?',
                'en': '8. What integrations do you need?'
            },
            'content_requirements_question': {
                'de': '9. Welche Inhaltsanforderungen haben Sie?',
                'ru': '9. Какие у вас требования к контенту?',
                'en': '9. What are your content requirements?'
            },
            'timeline_question': {
                'de': '10. Welchen Zeitrahmen haben Sie im Blick?',
                'ru': '10. Какой у вас временной рамки?',
                'en': '10. What timeline do you have in mind?'
            },
            'budget_question': {
                'de': '11. Welches Budget steht Ihnen zur Verfügung?',
                'ru': '11. Какой у вас бюджет?',
                'en': '11. What budget do you have available?'
            },
            'post_launch_services_question': {
                'de': '12. Welche Dienstleistungen benötigen Sie nach dem Launch?',
                'ru': '12. Какие услуги вам нужны после запуска?',
                'en': '12. What services do you need after launch?'
            },
            'discovery_source_question': {
                'de': '13. Wie haben Sie von uns erfahren?',
                'ru': '13. Как вы узнали о нас?',
                'en': '13. How did you hear about us?'
            },
            'communication_preference_question': {
                'de': '14. Wie möchten Sie kommunizieren?',
                'ru': '14. Как вы предпочитаете общаться?',
                'en': '14. How would you like to communicate?'
            },
            'contact_info_question': {
                'de': '15. Bitte geben Sie Ihre Kontaktdaten an:',
                'ru': '15. Пожалуйста, укажите ваши контактные данные:',
                'en': '15. Please provide your contact information:'
            },

            # Описания
            'project_type_description': {
                'de': 'z.B. Website, Web-App, Mobile-App, Desktop-Anwendung',
                'ru': 'например: сайт, веб-приложение, мобильное приложение, десктопное приложение',
                'en': 'e.g. website, web app, mobile app, desktop application'
            },
            'project_goal_description': {
                'de': 'Beschreiben Sie das Hauptziel Ihres Projekts',
                'ru': 'Опишите основную цель вашего проекта',
                'en': 'Describe the main goal of your project'
            },
            'target_audience_description': {
                'de': 'Beschreiben Sie Ihre Zielgruppe',
                'ru': 'Опишите вашу целевую аудиторию',
                'en': 'Describe your target audience'
            },
            'features_description': {
                'de': 'Listen Sie die gewünschten Funktionen auf',
                'ru': 'Перечислите желаемые функции',
                'en': 'List the desired features'
            },
            'design_preferences_description': {
                'de': 'Farben, Stil, besondere Anforderungen',
                'ru': 'Цвета, стиль, особые требования',
                'en': 'Colors, style, special requirements'
            },
            'references_description': {
                'de': 'Links zu Websites oder Beispiele',
                'ru': 'Ссылки на сайты или примеры',
                'en': 'Links to websites or examples'
            },
            'technical_requirements_description': {
                'de': 'Technologien, Frameworks, Datenbanken',
                'ru': 'Технологии, фреймворки, базы данных',
                'en': 'Technologies, frameworks, databases'
            },
            'integrations_description': {
                'de': 'API, Zahlungssysteme, externe Dienste',
                'ru': 'API, платежные системы, внешние сервисы',
                'en': 'API, payment systems, external services'
            },
            'content_requirements_description': {
                'de': 'Texte, Bilder, Videos, andere Medien',
                'ru': 'Тексты, изображения, видео, другие медиа',
                'en': 'Texts, images, videos, other media'
            },
            'timeline_description': {
                'de': 'Wann soll das Projekt fertig sein?',
                'ru': 'Когда проект должен быть готов?',
                'en': 'When should the project be completed?'
            },
            'budget_description': {
                'de': 'Ihr verfügbares Budget für das Projekt',
                'ru': 'Ваш доступный бюджет на проект',
                'en': 'Your available budget for the project'
            },
            'post_launch_services_description': {
                'de': 'Support, Wartung, Updates, Schulungen',
                'ru': 'Поддержка, обслуживание, обновления, обучение',
                'en': 'Support, maintenance, updates, training'
            },
            'discovery_source_description': {
                'de': 'Google, Empfehlung, Social Media, etc.',
                'ru': 'Google, рекомендация, социальные сети и т.д.',
                'en': 'Google, recommendation, social media, etc.'
            },
            'communication_preference_description': {
                'de': 'E-Mail, Telefon, Video-Call, Chat',
                'ru': 'Email, телефон, видеозвонок, чат',
                'en': 'Email, phone, video call, chat'
            },
            'contact_info_description': {
                'de': 'Name, E-Mail, Telefonnummer',
                'ru': 'Имя, email, номер телефона',
                'en': 'Name, email, phone number'
            }
        }

        # Получить текст по ключу
        text_dict = texts.get(key, {})
        return text_dict.get(self.language, text_dict.get('de', key))

    def get_section_by_index(self, index):
        """
        Получить секцию по индексу

        Args:
            index: Индекс секции

        Returns:
            dict: Секция или None, если индекс вне диапазона
        """
        if 0 <= index < len(self.sections):
            return self.sections[index]
        return None

    def get_total_sections(self):
        """
        Получить общее количество секций

        Returns:
            int: Количество секций
        """
        return len(self.sections)

    def validate_answer(self, section_index, answer):
        """
        Валидировать ответ на вопрос секции

        Args:
            section_index: Индекс секции
            answer: Ответ пользователя

        Returns:
            bool: True, если ответ валиден
        """
        section = self.get_section_by_index(section_index)
        if not section:
            return False

        # Для обязательных полей проверяем, что ответ не пустой
        if section.get('required', False):
            return bool(answer and answer.strip())

        # Для необязательных полей любой ответ считается валидным
        return True
