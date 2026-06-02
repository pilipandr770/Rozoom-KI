from typing import Dict, List, Optional
from flask import current_app

# РћРїСЂРµРґРµР»РµРЅРёРµ СЃС‚СЂСѓРєС‚СѓСЂС‹ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ
class TechSpecTemplate:
    def __init__(self, language: str = 'en'):
        self.language = language
        self.sections = self._get_sections_by_language()
        
    def _get_sections_by_language(self) -> List[Dict]:
        """Р’РѕР·РІСЂР°С‰Р°РµС‚ СЃРµРєС†РёРё РґР»СЏ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ СЏР·С‹РєР°"""
        sections_by_language = {
            'uk': [
                {
                    'title': 'РћРіР»СЏРґ РїСЂРѕС”РєС‚Сѓ',
                    'questions': [
                        'РЇРєР° РѕСЃРЅРѕРІРЅР° РјРµС‚Р° РІР°С€РѕРіРѕ РїСЂРѕС”РєС‚Сѓ?',
                        'РЇРєСѓ РїСЂРѕР±Р»РµРјСѓ РІРё РЅР°РјР°РіР°С”С‚РµСЃСЊ РІРёСЂС–С€РёС‚Рё?',
                        'РҐС‚Рѕ С” РІР°С€РѕСЋ С†С–Р»СЊРѕРІРѕСЋ Р°СѓРґРёС‚РѕСЂС–С”СЋ?'
                    ]
                },
                {
                    'title': 'Р¤СѓРЅРєС†С–РѕРЅР°Р»СЊРЅС– РІРёРјРѕРіРё',
                    'questions': [
                        'РЇРєС– РѕСЃРЅРѕРІРЅС– С„СѓРЅРєС†С–С— РІР°Рј РїРѕС‚СЂС–Р±РЅС–?',
                        'РЇРєР° РєРѕРЅРєСЂРµС‚РЅР° С„СѓРЅРєС†С–РѕРЅР°Р»СЊРЅС–СЃС‚СЊ С” РєСЂРёС‚РёС‡РЅРѕСЋ РґР»СЏ РІР°С€РѕРіРѕ РїСЂРѕС”РєС‚Сѓ?',
                        'Р§Рё С” Сѓ РІР°СЃ РєРѕРЅРєСЂРµС‚РЅС– СЃС†РµРЅР°СЂС–С— РІР·Р°С”РјРѕРґС–С— Р· РєРѕСЂРёСЃС‚СѓРІР°С‡РµРј?'
                    ]
                },
                {
                    'title': 'РўРµС…РЅС–С‡РЅС– РІРёРјРѕРіРё',
                    'questions': [
                        'Р§Рё С” Сѓ РІР°СЃ С‚РµС…РЅРѕР»РѕРіС–С‡РЅС– РІРїРѕРґРѕР±Р°РЅРЅСЏ (РјРѕРІРё, С„СЂРµР№РјРІРѕСЂРєРё С‚РѕС‰Рѕ)?',
                        'Р§Рё РїРѕС‚СЂС–Р±РЅР° С–РЅС‚РµРіСЂР°С†С–СЏ Р· С–СЃРЅСѓСЋС‡РёРјРё СЃРёСЃС‚РµРјР°РјРё?',
                        'РЇРєС– Сѓ РІР°СЃ РІРїРѕРґРѕР±Р°РЅРЅСЏ С‰РѕРґРѕ С…РѕСЃС‚РёРЅРіСѓ/СЂРѕР·РіРѕСЂС‚Р°РЅРЅСЏ?'
                    ]
                },
                {
                    'title': 'РўРµСЂРјС–РЅРё С‚Р° Р±СЋРґР¶РµС‚',
                    'questions': [
                        'РЇРєРёР№ РѕС‡С–РєСѓРІР°РЅРёР№ С‚РµСЂРјС–РЅ РІРёРєРѕРЅР°РЅРЅСЏ РїСЂРѕС”РєС‚Сѓ?',
                        'Р§Рё С” Сѓ РІР°СЃ РєРѕРЅРєСЂРµС‚РЅРёР№ РґС–Р°РїР°Р·РѕРЅ Р±СЋРґР¶РµС‚Сѓ?',
                        'Р§Рё С” СЏРєС–СЃСЊ РєСЂРёС‚РёС‡РЅС– РґРµРґР»Р°Р№РЅРё, РїСЂРѕ СЏРєС– РјРё РїРѕРІРёРЅРЅС– Р·РЅР°С‚Рё?'
                    ]
                },
                {
                    'title': 'РљРѕРЅС‚Р°РєС‚РЅР° С–РЅС„РѕСЂРјР°С†С–СЏ',
                    'questions': [
                        'РЇРє РІР°СЃ Р·РІР°С‚Рё?',
                        'РЇРєР° РІР°С€Р° РµР»РµРєС‚СЂРѕРЅРЅР° РїРѕС€С‚Р°?',
                        'РЇРєРёР№ РІР°С€ РЅРѕРјРµСЂ С‚РµР»РµС„РѕРЅСѓ? (РЅРµРѕР±РѕРІ\'СЏР·РєРѕРІРѕ)'
                    ]
                }
            ],
            'ru': [
                {
                    'title': 'РћР±Р·РѕСЂ РїСЂРѕРµРєС‚Р°',
                    'questions': [
                        'РљР°РєРѕРІР° РѕСЃРЅРѕРІРЅР°СЏ С†РµР»СЊ РІР°С€РµРіРѕ РїСЂРѕРµРєС‚Р°?',
                        'РљР°РєСѓСЋ РїСЂРѕР±Р»РµРјСѓ РІС‹ РїС‹С‚Р°РµС‚РµСЃСЊ СЂРµС€РёС‚СЊ?',
                        'РљС‚Рѕ СЏРІР»СЏРµС‚СЃСЏ РІР°С€РµР№ С†РµР»РµРІРѕР№ Р°СѓРґРёС‚РѕСЂРёРµР№?'
                    ]
                },
                {
                    'title': 'Р¤СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ',
                    'questions': [
                        'РљР°РєРёРµ РєР»СЋС‡РµРІС‹Рµ С„СѓРЅРєС†РёРё РІР°Рј РЅСѓР¶РЅС‹?',
                        'РљР°РєР°СЏ РєРѕРЅРєСЂРµС‚РЅР°СЏ С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅРѕСЃС‚СЊ РєСЂРёС‚РёС‡РµСЃРєРё РІР°Р¶РЅР° РґР»СЏ РІР°С€РµРіРѕ РїСЂРѕРµРєС‚Р°?',
                        'Р•СЃС‚СЊ Р»Рё Сѓ РІР°СЃ РєРѕРЅРєСЂРµС‚РЅС‹Рµ СЃС†РµРЅР°СЂРёРё РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёСЏ СЃ РїРѕР»СЊР·РѕРІР°С‚РµР»РµРј?'
                    ]
                },
                {
                    'title': 'РўРµС…РЅРёС‡РµСЃРєРёРµ С‚СЂРµР±РѕРІР°РЅРёСЏ',
                    'questions': [
                        'Р•СЃС‚СЊ Р»Рё Сѓ РІР°СЃ С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРёРµ РїСЂРµРґРїРѕС‡С‚РµРЅРёСЏ (СЏР·С‹РєРё, С„СЂРµР№РјРІРѕСЂРєРё Рё С‚.Рґ.)?',
                        'РќСѓР¶РЅР° Р»Рё РёРЅС‚РµРіСЂР°С†РёСЏ СЃ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРјРё СЃРёСЃС‚РµРјР°РјРё?',
                        'РљР°РєРѕРІС‹ РІР°С€Рё РїСЂРµРґРїРѕС‡С‚РµРЅРёСЏ РїРѕ С…РѕСЃС‚РёРЅРіСѓ/СЂР°Р·РІРµСЂС‚С‹РІР°РЅРёСЋ?'
                    ]
                },
                {
                    'title': 'РЎСЂРѕРєРё Рё Р±СЋРґР¶РµС‚',
                    'questions': [
                        'РљР°РєРѕРІ РѕР¶РёРґР°РµРјС‹Р№ СЃСЂРѕРє РІС‹РїРѕР»РЅРµРЅРёСЏ РїСЂРѕРµРєС‚Р°?',
                        'Р•СЃС‚СЊ Р»Рё Сѓ РІР°СЃ РєРѕРЅРєСЂРµС‚РЅС‹Р№ РґРёР°РїР°Р·РѕРЅ Р±СЋРґР¶РµС‚Р°?',
                        'Р•СЃС‚СЊ Р»Рё РєР°РєРёРµ-С‚Рѕ РєСЂРёС‚РёС‡РµСЃРєРёРµ СЃСЂРѕРєРё, Рѕ РєРѕС‚РѕСЂС‹С… РјС‹ РґРѕР»Р¶РЅС‹ Р·РЅР°С‚СЊ?'
                    ]
                },
                {
                    'title': 'РљРѕРЅС‚Р°РєС‚РЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ',
                    'questions': [
                        'РљР°Рє РІР°СЃ Р·РѕРІСѓС‚?',
                        'РљР°РєРѕР№ РІР°С€ Р°РґСЂРµСЃ СЌР»РµРєС‚СЂРѕРЅРЅРѕР№ РїРѕС‡С‚С‹?',
                        'РљР°РєРѕР№ РІР°С€ РЅРѕРјРµСЂ С‚РµР»РµС„РѕРЅР°? (РЅРµРѕР±СЏР·Р°С‚РµР»СЊРЅРѕ)'
                    ]
                }
            ],
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
                    'title': 'ProjektГјbersicht',
                    'questions': [
                        'Was ist der Hauptzweck Ihres Projekts?',
                        'Welches Problem versuchen Sie zu lГ¶sen?',
                        'Wer ist Ihre Zielgruppe?'
                    ]
                },
                {
                    'title': 'Funktionale Anforderungen',
                    'questions': [
                        'Welche SchlГјsselfunktionen benГ¶tigen Sie?',
                        'Welche spezifische FunktionalitГ¤t ist fГјr Ihr Projekt entscheidend?',
                        'Haben Sie bestimmte BenutzerablГ¤ufe im Sinn?'
                    ]
                },
                {
                    'title': 'Technische Anforderungen',
                    'questions': [
                        'Haben Sie TechnologieprГ¤ferenzen (Sprachen, Frameworks usw.)?',
                        'BenГ¶tigen Sie Integration mit bestehenden Systemen?',
                        'Was sind Ihre Hosting-/BereitstellungsprГ¤ferenzen?'
                    ]
                },
                {
                    'title': 'Zeitplan & Budget',
                    'questions': [
                        'Was ist Ihr erwarteter Zeitrahmen fГјr dieses Projekt?',
                        'Haben Sie einen bestimmten Budgetrahmen im Sinn?',
                        'Gibt es kritische Fristen, die wir beachten sollten?'
                    ]
                },
                {
                    'title': 'Kontaktinformationen',
                    'questions': [
                        'Wie heiГџen Sie?',
                        'Wie lautet Ihre E-Mail-Adresse?',
                        'Wie ist Ihre Telefonnummer? (optional)'
                    ]
                }
            ]
        }
        return sections_by_language.get(self.language, sections_by_language['en'])

def get_tech_spec_prompt(metadata: Dict) -> str:
    """РЎРѕР·РґР°РµС‚ РїСЂРѕРјРїС‚ РґР»СЏ СЃР±РѕСЂР° С‚СЂРµР±РѕРІР°РЅРёР№ РґР»СЏ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ"""
    language = metadata.get('language', 'en')
    current_section = metadata.get('tech_spec_section', 0)
    template = TechSpecTemplate(language)
    
    if current_section >= len(template.sections):
        # Р•СЃР»Рё РјС‹ РїСЂРѕС€Р»Рё РІСЃРµ СЃРµРєС†РёРё, С‚Рѕ СЌС‚Рѕ РёС‚РѕРіРѕРІРѕРµ СЂРµР·СЋРјРµ
        if language == 'uk':
            return ("Р”СЏРєСѓСЋ Р·Р° РІСЃС– РІР°С€С– РІС–РґРїРѕРІС–РґС–! РўРµРїРµСЂ СЏ РјР°СЋ РґРѕСЃС‚Р°С‚РЅСЊРѕ С–РЅС„РѕСЂРјР°С†С–С— РґР»СЏ СЃС‚РІРѕСЂРµРЅРЅСЏ РїРѕРїРµСЂРµРґРЅСЊРѕРіРѕ "
                   "С‚РµС…РЅС–С‡РЅРѕРіРѕ Р·Р°РІРґР°РЅРЅСЏ. Р‘Р°Р¶Р°С”С‚Рµ РїРѕР±Р°С‡РёС‚Рё РїС–РґСЃСѓРјРѕРє РІР°С€РёС… РІРёРјРѕРі, "
                   "С‡Рё С” С‰РѕСЃСЊ, С‰Рѕ РІРё С…РѕС‚С–Р»Рё Р± РґРѕРґР°С‚Рё?")
        elif language == 'ru':
            return ("РЎРїР°СЃРёР±Рѕ Р·Р° РІСЃРµ РІР°С€Рё РѕС‚РІРµС‚С‹! РўРµРїРµСЂСЊ Сѓ РјРµРЅСЏ РґРѕСЃС‚Р°С‚РѕС‡РЅРѕ РёРЅС„РѕСЂРјР°С†РёРё РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РїСЂРµРґРІР°СЂРёС‚РµР»СЊРЅРѕРіРѕ "
                   "С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ. РҐРѕС‚РёС‚Рµ СѓРІРёРґРµС‚СЊ СЂРµР·СЋРјРµ РІР°С€РёС… С‚СЂРµР±РѕРІР°РЅРёР№, "
                   "РёР»Рё РµСЃС‚СЊ С‡С‚Рѕ-С‚Рѕ, С‡С‚Рѕ РІС‹ С…РѕС‚РµР»Рё Р±С‹ РґРѕР±Р°РІРёС‚СЊ?")
        elif language == 'de':
            return ("Danke fГјr alle Ihre Antworten! Ich habe jetzt genГјgend Informationen, um ein vorlГ¤ufiges "
                   "technisches Lastenheft zu erstellen. MГ¶chten Sie eine Zusammenfassung Ihrer Anforderungen sehen, "
                   "oder gibt es noch etwas, das Sie hinzufГјgen mГ¶chten?")
        else:
            return ("Thank you for all your answers! I now have enough information to create a preliminary "
                   "technical specification. Would you like to see a summary of your requirements, "
                   "or is there anything else you'd like to add?")
    
    # РџРѕР»СѓС‡Р°РµРј С‚РµРєСѓС‰СѓСЋ СЃРµРєС†РёСЋ
    section = template.sections[current_section]
    questions = section['questions']
    
    # РЎРѕР·РґР°РµРј РїСЂРѕРјРїС‚ РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ СЏР·С‹РєР°
    if language == 'uk':
        prompt = (f"РЇ Р°РЅР°Р»С–С‚РёРє РІРёРјРѕРі Сѓ Andrii-IT. РЇ РґРѕРїРѕРјРѕР¶Сѓ РІР°Рј СЃС‚РІРѕСЂРёС‚Рё С‚РµС…РЅС–С‡РЅРµ Р·Р°РІРґР°РЅРЅСЏ. "
                 f"РџРѕС‡РЅРµРјРѕ Р· СЂРѕР·РґС–Р»Сѓ '{section['title']}'.\n\n")
                 
        for i, question in enumerate(questions):
            prompt += f"вЂў {question}\n"
            
        prompt += ("\nР‘СѓРґСЊ Р»Р°СЃРєР°, РІС–РґРїРѕРІС–РґР°Р№С‚Рµ РЅР° РїРёС‚Р°РЅРЅСЏ РїРѕ РѕРґРЅРѕРјСѓ. РљРѕР»Рё Р·Р°РєС–РЅС‡РёС‚Рµ, СЏ РїРµСЂРµР№РґСѓ РґРѕ РЅР°СЃС‚СѓРїРЅРѕРіРѕ "
                  "СЂРѕР·РґС–Р»Сѓ. Р’Р°С€С– РІС–РґРїРѕРІС–РґС– РґРѕРїРѕРјРѕР¶СѓС‚СЊ РЅР°Рј СЃС‚РІРѕСЂРёС‚Рё С–РЅРґРёРІС–РґСѓР°Р»СЊРЅСѓ РїСЂРѕРїРѕР·РёС†С–СЋ РґР»СЏ РІР°С€РѕРіРѕ РїСЂРѕС”РєС‚Сѓ.")
    elif language == 'ru':
        prompt = (f"РЇ Р°РЅР°Р»РёС‚РёРє С‚СЂРµР±РѕРІР°РЅРёР№ РІ Andrii-IT. РЇ РїРѕРјРѕРіСѓ РІР°Рј СЃРѕР·РґР°С‚СЊ С‚РµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ. "
                 f"РќР°С‡РЅРµРј СЃ СЂР°Р·РґРµР»Р° '{section['title']}'.\n\n")
                 
        for i, question in enumerate(questions):
            prompt += f"вЂў {question}\n"
            
        prompt += ("\nРџРѕР¶Р°Р»СѓР№СЃС‚Р°, РѕС‚РІРµС‡Р°Р№С‚Рµ РЅР° РІРѕРїСЂРѕСЃС‹ РїРѕ РѕРґРЅРѕРјСѓ. РљРѕРіРґР° Р·Р°РєРѕРЅС‡РёС‚Рµ, СЏ РїРµСЂРµР№РґСѓ Рє СЃР»РµРґСѓСЋС‰РµРјСѓ "
                  "СЂР°Р·РґРµР»Сѓ. Р’Р°С€Рё РѕС‚РІРµС‚С‹ РїРѕРјРѕРіСѓС‚ РЅР°Рј СЃРѕР·РґР°С‚СЊ РёРЅРґРёРІРёРґСѓР°Р»СЊРЅРѕРµ РїСЂРµРґР»РѕР¶РµРЅРёРµ РґР»СЏ РІР°С€РµРіРѕ РїСЂРѕРµРєС‚Р°.")
    elif language == 'de':
        prompt = (f"Ich bin der Anforderungsanalyst bei Andrii-IT. Ich helfe Ihnen, ein technisches Lastenheft "
                 f"zu erstellen. Lassen Sie uns mit dem Abschnitt '{section['title']}' beginnen.\n\n")
                 
        for i, question in enumerate(questions):
            prompt += f"вЂў {question}\n"
            
        prompt += ("\nBitte beantworten Sie eine Frage nach der anderen. Wenn Sie fertig sind, werde ich zum nГ¤chsten "
                  "Abschnitt Гјbergehen. Ihre Antworten helfen uns, ein maГџgeschneidertes Angebot fГјr Ihr Projekt zu erstellen.")
    else:
        prompt = (f"I am the Requirements Analyst at Andrii-IT. I'm here to help you create a technical specification. "
                 f"Let's start with the '{section['title']}' section.\n\n")
                 
        for i, question in enumerate(questions):
            prompt += f"вЂў {question}\n"
            
        prompt += ("\nPlease answer one question at a time. When you're done, I'll move on to the next section. "
                  "Your answers will help us create a tailored proposal for your project.")
    
    return prompt

