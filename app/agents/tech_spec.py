from typing import Dict, List, Optional
from flask import current_app

# Определение структуры технического задания
class TechSpecTemplate:
    def __init__(self, language: str = 'en'):
        self.language = language
        self.sections = self._get_sections_by_language()
        
    def _get_sections_by_language(self) -> List[Dict]:
        """Возвращает секции для технического задания в зависимости от языка"""
        sections_by_language = {
            'en': [
                {
                    'title': 'Project Overview',
                    'questions': [
                        'What is the main purpose of your project?',
                        'What problem are you trying to solve?',
                        'Who is your target audience?'
                    ]
                },
                {
                    'title': 'Functional Requirements',
                    'questions': [
                        'What are the key features you need?',
                        'What specific functionality is critical for your project?',
                        'Are there any particular user flows you have in mind?'
                    ]
                },
                {
                    'title': 'Technical Requirements',
                    'questions': [
                        'Do you have any technology preferences (languages, frameworks, etc.)?',
                        'Do you need integration with any existing systems?',
                        'What are your hosting/deployment preferences?'
                    ]
                },
                {
                    'title': 'Timeline & Budget',
                    'questions': [
                        'What is your expected timeline for this project?',
                        'Do you have a specific budget range in mind?',
                        'Are there any critical deadlines we should be aware of?'
                    ]
                },
                {
                    'title': 'Contact Information',
                    'questions': [
                        'What is your name?',
                        'What is your email address?',
                        'What is your phone number? (optional)'
                    ]
                }
            ],
            'de': [
                {
                    'title': 'Projektübersicht',
                    'questions': [
                        'Was ist der Hauptzweck Ihres Projekts?',
                        'Welches Problem versuchen Sie zu lösen?',
                        'Wer ist Ihre Zielgruppe?'
                    ]
                },
                {
                    'title': 'Funktionale Anforderungen',
                    'questions': [
                        'Welche Schlüsselfunktionen benötigen Sie?',
                        'Welche spezifische Funktionalität ist für Ihr Projekt entscheidend?',
                        'Haben Sie bestimmte Benutzerabläufe im Sinn?'
                    ]
                },
                {
                    'title': 'Technische Anforderungen',
                    'questions': [
                        'Haben Sie Technologiepräferenzen (Sprachen, Frameworks usw.)?',
                        'Benötigen Sie Integration mit bestehenden Systemen?',
                        'Was sind Ihre Hosting-/Bereitstellungspräferenzen?'
                    ]
                },
                {
                    'title': 'Zeitplan & Budget',
                    'questions': [
                        'Was ist Ihr erwarteter Zeitrahmen für dieses Projekt?',
                        'Haben Sie einen bestimmten Budgetrahmen im Sinn?',
                        'Gibt es kritische Fristen, die wir beachten sollten?'
                    ]
                },
                {
                    'title': 'Kontaktinformationen',
                    'questions': [
                        'Wie heißen Sie?',
                        'Wie lautet Ihre E-Mail-Adresse?',
                        'Wie ist Ihre Telefonnummer? (optional)'
                    ]
                }
            ]
        }
        return sections_by_language.get(self.language, sections_by_language['en'])

def get_tech_spec_prompt(metadata: Dict) -> str:
    """Создает промпт для сбора требований для технического задания"""
    language = metadata.get('language', 'en')
    current_section = metadata.get('tech_spec_section', 0)
    template = TechSpecTemplate(language)
    
    if current_section >= len(template.sections):
        # Если мы прошли все секции, то это итоговое резюме
        if language == 'de':
            return ("Danke für alle Ihre Antworten! Ich habe jetzt genügend Informationen, um ein vorläufiges "
                   "technisches Lastenheft zu erstellen. Möchten Sie eine Zusammenfassung Ihrer Anforderungen sehen, "
                   "oder gibt es noch etwas, das Sie hinzufügen möchten?")
        else:
            return ("Thank you for all your answers! I now have enough information to create a preliminary "
                   "technical specification. Would you like to see a summary of your requirements, "
                   "or is there anything else you'd like to add?")
    
    # Получаем текущую секцию
    section = template.sections[current_section]
    questions = section['questions']
    
    # Создаем промпт в зависимости от языка
    if language == 'de':
        prompt = (f"Ich bin der Anforderungsanalyst bei Rozoom-KI. Ich helfe Ihnen, ein technisches Lastenheft "
                 f"zu erstellen. Lassen Sie uns mit dem Abschnitt '{section['title']}' beginnen.\n\n")
                 
        for i, question in enumerate(questions):
            prompt += f"• {question}\n"
            
        prompt += ("\nBitte beantworten Sie eine Frage nach der anderen. Wenn Sie fertig sind, werde ich zum nächsten "
                  "Abschnitt übergehen. Ihre Antworten helfen uns, ein maßgeschneidertes Angebot für Ihr Projekt zu erstellen.")
    else:
        prompt = (f"I am the Requirements Analyst at Rozoom-KI. I'm here to help you create a technical specification. "
                 f"Let's start with the '{section['title']}' section.\n\n")
                 
        for i, question in enumerate(questions):
            prompt += f"• {question}\n"
            
        prompt += ("\nPlease answer one question at a time. When you're done, I'll move on to the next section. "
                  "Your answers will help us create a tailored proposal for your project.")
    
    return prompt
