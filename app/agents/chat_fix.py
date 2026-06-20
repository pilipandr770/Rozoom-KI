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
    'uk': """Р’Рё - Р°СЃРёСЃС‚РµРЅС‚ РґР»СЏ РІРµР±-СЃС‚СѓРґС–С— Andrii-IT. Р’С–РґРїРѕРІС–РґР°Р№С‚Рµ РєР»С–С”РЅС‚Р°Рј РІРІС–С‡Р»РёРІРѕ С‚Р° РїСЂРѕС„РµСЃС–Р№РЅРѕ.
РњРѕРІР° СЃРїС–Р»РєСѓРІР°РЅРЅСЏ: СѓРєСЂР°С—РЅСЃСЊРєР°. Р’С–РґРїРѕРІС–РґР°Р№С‚Рµ РєРѕСЂРѕС‚РєРѕ С‚Р° РїРѕ СЃСѓС‚С–.""",
    'ru': """Р’С‹ - Р°СЃСЃРёСЃС‚РµРЅС‚ РґР»СЏ РІРµР±-СЃС‚СѓРґРёРё Andrii-IT. РћС‚РІРµС‡Р°Р№С‚Рµ РєР»РёРµРЅС‚Р°Рј РІРµР¶Р»РёРІРѕ Рё РїСЂРѕС„РµСЃСЃРёРѕРЅР°Р»СЊРЅРѕ.
РЇР·С‹Рє РѕР±С‰РµРЅРёСЏ: СЂСѓСЃСЃРєРёР№. РћС‚РІРµС‡Р°Р№С‚Рµ РєСЂР°С‚РєРѕ Рё РїРѕ СЃСѓС‰РµСЃС‚РІСѓ.""",
    'en': """You are an assistant for the Andrii-IT web studio. Respond to clients politely and professionally.
Communication language: English. Keep your answers short and to the point.""",
    'de': """Sie sind ein Assistent fГјr das Webstudio Andrii-IT. Antworten Sie hГ¶flich und professionell auf Kunden.
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
                'uk': "Р’С–С‚Р°СЋ! РЇ РІС–СЂС‚СѓР°Р»СЊРЅРёР№ Р°СЃРёСЃС‚РµРЅС‚ Andrii-IT. Р§РёРј РјРѕР¶Сѓ РґРѕРїРѕРјРѕРіС‚Рё?",
                'ru': "Р—РґСЂР°РІСЃС‚РІСѓР№С‚Рµ! РЇ РІРёСЂС‚СѓР°Р»СЊРЅС‹Р№ Р°СЃСЃРёСЃС‚РµРЅС‚ Andrii-IT. Р§РµРј РјРѕРіСѓ РїРѕРјРѕС‡СЊ?",
                'en': "Hello! I'm the Andrii-IT virtual assistant. How can I help you?",
                'de': "Hallo! Ich bin der virtuelle Assistent von Andrii-IT. Wie kann ich Ihnen helfen?"
            }
            answer = responses.get(language, responses['uk'])
        else:
            # Check for specific keywords first for better responses
            message_lower = message.lower()
        
            # Check for keyword "РјР°СЂРєРµС‚" (marketing)
            if any(word in message_lower for word in ["РјР°СЂРєРµС‚", "market", "marketing", "РјР°СЂРєРµС‚РёРЅРі"]):
                if language == 'uk':
                    answer = """Р”Р»СЏ Р°РІС‚РѕРјР°С‚РёР·Р°С†С–С— РјР°СЂРєРµС‚РёРЅРіСѓ Andrii-IT РїСЂРѕРїРѕРЅСѓС”:
1. Р†РЅС‚РµРіСЂР°С†С–СЋ Р· CRM СЃРёСЃС‚РµРјР°РјРё
2. РђРІС‚РѕРјР°С‚РёС‡РЅС– email-СЂРѕР·СЃРёР»РєРё
3. РђРЅР°Р»С–С‚РёРєСѓ РµС„РµРєС‚РёРІРЅРѕСЃС‚С– СЂРµРєР»Р°РјРЅРёС… РєР°РјРїР°РЅС–Р№
4. РќР°Р»Р°С€С‚СѓРІР°РЅРЅСЏ С‚Р°СЂРіРµС‚РѕРІР°РЅРѕС— СЂРµРєР»Р°РјРё
5. РђРІС‚РѕРјР°С‚РёР·Р°С†С–СЋ РїРѕСЃС‚С–РІ Сѓ СЃРѕС†С–Р°Р»СЊРЅРёС… РјРµСЂРµР¶Р°С…

РЇРєРёР№ Р°СЃРїРµРєС‚ РјР°СЂРєРµС‚РёРЅРіСѓ РІР°СЃ С†С–РєР°РІРёС‚СЊ РЅР°Р№Р±С–Р»СЊС€Рµ?"""
                elif language == 'ru':
                    answer = """Р”Р»СЏ Р°РІС‚РѕРјР°С‚РёР·Р°С†РёРё РјР°СЂРєРµС‚РёРЅРіР° Andrii-IT РїСЂРµРґР»Р°РіР°РµС‚:
1. РРЅС‚РµРіСЂР°С†РёСЋ СЃ CRM СЃРёСЃС‚РµРјР°РјРё
2. РђРІС‚РѕРјР°С‚РёС‡РµСЃРєРёРµ email-СЂР°СЃСЃС‹Р»РєРё
3. РђРЅР°Р»РёС‚РёРєСѓ СЌС„С„РµРєС‚РёРІРЅРѕСЃС‚Рё СЂРµРєР»Р°РјРЅС‹С… РєР°РјРїР°РЅРёР№
4. РќР°СЃС‚СЂРѕР№РєСѓ С‚Р°СЂРіРµС‚РёСЂРѕРІР°РЅРЅРѕР№ СЂРµРєР»Р°РјС‹
5. РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЋ РїРѕСЃС‚РѕРІ РІ СЃРѕС†РёР°Р»СЊРЅС‹С… СЃРµС‚СЏС…

РљР°РєРѕР№ Р°СЃРїРµРєС‚ РјР°СЂРєРµС‚РёРЅРіР° РІР°СЃ РёРЅС‚РµСЂРµСЃСѓРµС‚ Р±РѕР»СЊС€Рµ РІСЃРµРіРѕ?"""
                elif language == 'en':
                    answer = """For marketing automation, Andrii-IT offers:
1. Integration with CRM systems
2. Automated email campaigns
3. Ad campaign performance analytics
4. Targeted advertising setup
5. Social media post automation

Which aspect of marketing are you most interested in?"""
                elif language == 'de':
                    answer = """FГјr Marketing-Automatisierung bietet Andrii-IT:
1. Integration mit CRM-Systemen
2. Automatisierte E-Mail-Kampagnen
3. Analyse der Werbekampagnenleistung
4. Einrichtung zielgerichteter Werbung
5. Automatisierung von Social-Media-BeitrГ¤gen

Welcher Aspekt des Marketings interessiert Sie am meisten?"""
                    
            # Check for tech spec related keywords
            elif any(word in message_lower for word in ["С‚РµС…", "tech", "specification", "Р·Р°РІРґР°РЅРЅСЏ", "Р·Р°РґР°РЅРёРµ", "СЃРїРµС†РёС„С–РєР°С†С–СЏ"]):
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
                        answer = """Р’Рё РјРѕР¶РµС‚Рµ Р·Р°РїРѕРІРЅРёС‚Рё С‚РµС…РЅС–С‡РЅРµ Р·Р°РІРґР°РЅРЅСЏ РЅР° РЅР°С€РѕРјСѓ СЃР°Р№С‚С– Сѓ СЂРѕР·РґС–Р»С– "РўРµС…РЅС–С‡РЅРµ Р·Р°РІРґР°РЅРЅСЏ" Р°Р±Рѕ С‡РµСЂРµР· С„РѕСЂРјСѓ Р·Р°РјРѕРІР»РµРЅРЅСЏ. 
Р¦Рµ РґРѕРїРѕРјРѕР¶Рµ РЅР°Рј РєСЂР°С‰Рµ Р·СЂРѕР·СѓРјС–С‚Рё РІР°С€С– РїРѕС‚СЂРµР±Рё С‚Р° СЂРѕР·СЂРѕР±РёС‚Рё РѕРїС‚РёРјР°Р»СЊРЅРµ СЂС–С€РµРЅРЅСЏ РґР»СЏ РІР°С€РѕРіРѕ РїСЂРѕС”РєС‚Сѓ.

РЇРєС‰Рѕ С…РѕС‡РµС‚Рµ СЂРѕР·РїРѕС‡Р°С‚Рё Р·Р°РїРѕРІРЅРµРЅРЅСЏ С‚РµС…РЅС–С‡РЅРѕРіРѕ Р·Р°РІРґР°РЅРЅСЏ Р·Р°СЂР°Р·, РїСЂРѕСЃС‚Рѕ СЃРєР°Р¶С–С‚СЊ "РїРѕС‡Р°С‚Рё С‚РµС…Р·Р°РІРґР°РЅРЅСЏ" С– СЏ РїСЂРѕРІРµРґСѓ РІР°СЃ С‡РµСЂРµР· С†РµР№ РїСЂРѕС†РµСЃ."""
                    elif language == 'ru':
                        answer = """Р’С‹ РјРѕР¶РµС‚Рµ Р·Р°РїРѕР»РЅРёС‚СЊ С‚РµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ РЅР° РЅР°С€РµРј СЃР°Р№С‚Рµ РІ СЂР°Р·РґРµР»Рµ "РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ" РёР»Рё С‡РµСЂРµР· С„РѕСЂРјСѓ Р·Р°РєР°Р·Р°.
Р­С‚Рѕ РїРѕРјРѕР¶РµС‚ РЅР°Рј Р»СѓС‡С€Рµ РїРѕРЅСЏС‚СЊ РІР°С€Рё РїРѕС‚СЂРµР±РЅРѕСЃС‚Рё Рё СЂР°Р·СЂР°Р±РѕС‚Р°С‚СЊ РѕРїС‚РёРјР°Р»СЊРЅРѕРµ СЂРµС€РµРЅРёРµ РґР»СЏ РІР°С€РµРіРѕ РїСЂРѕРµРєС‚Р°.

Р•СЃР»Рё С…РѕС‚РёС‚Рµ РЅР°С‡Р°С‚СЊ Р·Р°РїРѕР»РЅРµРЅРёРµ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ СЃРµР№С‡Р°СЃ, РїСЂРѕСЃС‚Рѕ СЃРєР°Р¶РёС‚Рµ "РЅР°С‡Р°С‚СЊ С‚РµС…Р·Р°РґР°РЅРёРµ" Рё СЏ РїСЂРѕРІРµРґСѓ РІР°СЃ С‡РµСЂРµР· СЌС‚РѕС‚ РїСЂРѕС†РµСЃСЃ."""
                    elif language == 'en':
                        answer = """You can fill out a technical specification on our website in the "Technical Specification" section or through the order form.
This will help us better understand your needs and develop the optimal solution for your project.

If you want to start filling out the technical specification now, just say "start tech spec" and I'll guide you through the process."""
                    elif language == 'de':
                        answer = """Sie kГ¶nnen eine technische Spezifikation auf unserer Website im Bereich "Technische Spezifikation" oder Гјber das Bestellformular ausfГјllen.
Dies hilft uns, Ihre BedГјrfnisse besser zu verstehen und die optimale LГ¶sung fГјr Ihr Projekt zu entwickeln.

Wenn Sie jetzt mit dem AusfГјllen der technischen Spezifikation beginnen mГ¶chten, sagen Sie einfach "Technische Spezifikation starten" und ich fГјhre Sie durch den Prozess."""
                    
            # Check for tech spec start keywords
            elif any(phrase in message_lower for phrase in ["РїРѕС‡Р°С‚Рё С‚РµС…Р·Р°РІРґР°РЅРЅСЏ", "РЅР°С‡Р°С‚СЊ С‚РµС…Р·Р°РґР°РЅРёРµ", "start tech spec", "С‚РµС…РЅС–С‡РЅРµ Р·Р°РІРґР°РЅРЅСЏ", "С‚РµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ"]):
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
                        answer = """РќР° РґР°РЅРёР№ РјРѕРјРµРЅС‚ Сѓ РЅР°СЃ РІРёРЅРёРєР»Рё С‚РµС…РЅС–С‡РЅС– С‚СЂСѓРґРЅРѕС‰С– Р· Р·Р°РїСѓСЃРєРѕРј РїСЂРѕС†РµСЃСѓ Р·Р°РїРѕРІРЅРµРЅРЅСЏ С‚РµС…РЅС–С‡РЅРѕРіРѕ Р·Р°РІРґР°РЅРЅСЏ. 
Р‘СѓРґСЊ Р»Р°СЃРєР°, СЃРїСЂРѕР±СѓР№С‚Рµ РїС–Р·РЅС–С€Рµ Р°Р±Рѕ Р·Р°РїРѕРІРЅС–С‚СЊ С„РѕСЂРјСѓ РЅР° РЅР°С€РѕРјСѓ РІРµР±-СЃР°Р№С‚С–."""
                    elif language == 'ru':
                        answer = """Р’ РЅР°СЃС‚РѕСЏС‰РµРµ РІСЂРµРјСЏ Сѓ РЅР°СЃ РІРѕР·РЅРёРєР»Рё С‚РµС…РЅРёС‡РµСЃРєРёРµ С‚СЂСѓРґРЅРѕСЃС‚Рё СЃ Р·Р°РїСѓСЃРєРѕРј РїСЂРѕС†РµСЃСЃР° Р·Р°РїРѕР»РЅРµРЅРёСЏ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ. 
РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РїРѕРїСЂРѕР±СѓР№С‚Рµ РїРѕР·Р¶Рµ РёР»Рё Р·Р°РїРѕР»РЅРёС‚Рµ С„РѕСЂРјСѓ РЅР° РЅР°С€РµРј РІРµР±-СЃР°Р№С‚Рµ."""
                    elif language == 'en':
                        answer = """We are currently experiencing technical difficulties with starting the technical specification process. 
Please try again later or fill out the form on our website."""
                    else:
                        answer = """Wir haben derzeit technische Schwierigkeiten mit dem Start des technischen Spezifikationsprozesses. 
Bitte versuchen Sie es spГ¤ter erneut oder fГјllen Sie das Formular auf unserer Website aus."""
            
            # Check for chat system related keywords
            elif any(word in message_lower for word in ["С‡Р°С‚", "chat", "РІС–РґРїРѕРІС–Рґ", "РѕС‚РІРµС‡", "answer", "РѕС‚РІРµС‚"]):
                if language == 'uk':
                    answer = """РќР°С€ С‡Р°С‚-Р±РѕС‚ РїСЂР°С†СЋС” РІ СЂРµР¶РёРјС– РїСЂРѕСЃС‚РёС… РІС–РґРїРѕРІС–РґРµР№. РЇ РЅР°РјР°РіР°СЋСЃСЏ РЅР°РґР°С‚Рё РІР°Рј РєРѕСЂРёСЃРЅСѓ С–РЅС„РѕСЂРјР°С†С–СЋ РїСЂРѕ РїРѕСЃР»СѓРіРё Andrii-IT.
РЇРєС‰Рѕ Сѓ РІР°СЃ С” РєРѕРЅРєСЂРµС‚РЅС– РїРёС‚Р°РЅРЅСЏ РїСЂРѕ РІРµР±-СЂРѕР·СЂРѕР±РєСѓ, РґРёР·Р°Р№РЅ, РјР°СЂРєРµС‚РёРЅРі Р°Р±Рѕ С–РЅС€С– РїРѕСЃР»СѓРіРё, СЏ СЂР°РґРёР№ РЅР° РЅРёС… РІС–РґРїРѕРІС–СЃС‚Рё."""
                elif language == 'ru':
                    answer = """РќР°С€ С‡Р°С‚-Р±РѕС‚ СЂР°Р±РѕС‚Р°РµС‚ РІ СЂРµР¶РёРјРµ РїСЂРѕСЃС‚С‹С… РѕС‚РІРµС‚РѕРІ. РЇ СЃС‚Р°СЂР°СЋСЃСЊ РїСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РІР°Рј РїРѕР»РµР·РЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёСЋ РѕР± СѓСЃР»СѓРіР°С… Andrii-IT.
Р•СЃР»Рё Сѓ РІР°СЃ РµСЃС‚СЊ РєРѕРЅРєСЂРµС‚РЅС‹Рµ РІРѕРїСЂРѕСЃС‹ Рѕ РІРµР±-СЂР°Р·СЂР°Р±РѕС‚РєРµ, РґРёР·Р°Р№РЅРµ, РјР°СЂРєРµС‚РёРЅРіРµ РёР»Рё РґСЂСѓРіРёС… СѓСЃР»СѓРіР°С…, СЏ СЂР°Рґ РЅР° РЅРёС… РѕС‚РІРµС‚РёС‚СЊ."""
                elif language == 'en':
                    answer = """Our chatbot operates in a simple response mode. I try to provide you with useful information about Andrii-IT services.
If you have specific questions about web development, design, marketing, or other services, I'm happy to answer them."""
                elif language == 'de':
                    answer = """Unser Chatbot arbeitet im einfachen Antwortmodus. Ich versuche, Ihnen nГјtzliche Informationen Гјber die Dienste von Andrii-IT zu geben.
Wenn Sie konkrete Fragen zur Webentwicklung, Design, Marketing oder anderen Dienstleistungen haben, beantworte ich diese gerne."""
                    
            # Check for website development keywords
            elif any(word in message_lower for word in ["РІРµР±", "СЃР°Р№С‚", "web", "website", "СЂРѕР·СЂРѕР±РєР°", "СЂР°Р·СЂР°Р±РѕС‚РєР°", "development"]):
                if language == 'uk':
                    answer = """Andrii-IT РїСЂРѕРїРѕРЅСѓС” РїРѕРІРЅРёР№ С†РёРєР» СЂРѕР·СЂРѕР±РєРё РІРµР±-СЃР°Р№С‚С–РІ:

1. Р РѕР·СЂРѕР±РєР° С–РЅС‚РµСЂРЅРµС‚-РјР°РіР°Р·РёРЅС–РІ
2. РЎС‚РІРѕСЂРµРЅРЅСЏ РєРѕСЂРїРѕСЂР°С‚РёРІРЅРёС… СЃР°Р№С‚С–РІ
3. Р РѕР·СЂРѕР±РєР° Р»РµРЅРґС–РЅРі-СЃС‚РѕСЂС–РЅРѕРє
4. Р†РЅС‚РµРіСЂР°С†С–СЏ Р· CRM С‚Р° РїР»Р°С‚С–Р¶РЅРёРјРё СЃРёСЃС‚РµРјР°РјРё
5. РђРґР°РїС‚РёРІРЅРёР№ РґРёР·Р°Р№РЅ РґР»СЏ РІСЃС–С… РїСЂРёСЃС‚СЂРѕС—РІ
6. SEO-РѕРїС‚РёРјС–Р·Р°С†С–СЏ

РќР°С€Р° РєРѕРјР°РЅРґР° РІРёРєРѕСЂРёСЃС‚РѕРІСѓС” СЃСѓС‡Р°СЃРЅС– С‚РµС…РЅРѕР»РѕРіС–С— РґР»СЏ СЃС‚РІРѕСЂРµРЅРЅСЏ С€РІРёРґРєРёС…, Р±РµР·РїРµС‡РЅРёС… С‚Р° С„СѓРЅРєС†С–РѕРЅР°Р»СЊРЅРёС… РІРµР±-СЂС–С€РµРЅСЊ.
РЇРєРёР№ С‚РёРї СЃР°Р№С‚Сѓ РІР°СЃ С†С–РєР°РІРёС‚СЊ?"""
                elif language == 'ru':
                    answer = """Andrii-IT РїСЂРµРґР»Р°РіР°РµС‚ РїРѕР»РЅС‹Р№ С†РёРєР» СЂР°Р·СЂР°Р±РѕС‚РєРё РІРµР±-СЃР°Р№С‚РѕРІ:

1. Р Р°Р·СЂР°Р±РѕС‚РєР° РёРЅС‚РµСЂРЅРµС‚-РјР°РіР°Р·РёРЅРѕРІ
2. РЎРѕР·РґР°РЅРёРµ РєРѕСЂРїРѕСЂР°С‚РёРІРЅС‹С… СЃР°Р№С‚РѕРІ
3. Р Р°Р·СЂР°Р±РѕС‚РєР° Р»РµРЅРґРёРЅРі-СЃС‚СЂР°РЅРёС†
4. РРЅС‚РµРіСЂР°С†РёСЏ СЃ CRM Рё РїР»Р°С‚РµР¶РЅС‹РјРё СЃРёСЃС‚РµРјР°РјРё
5. РђРґР°РїС‚РёРІРЅС‹Р№ РґРёР·Р°Р№РЅ РґР»СЏ РІСЃРµС… СѓСЃС‚СЂРѕР№СЃС‚РІ
6. SEO-РѕРїС‚РёРјРёР·Р°С†РёСЏ

РќР°С€Р° РєРѕРјР°РЅРґР° РёСЃРїРѕР»СЊР·СѓРµС‚ СЃРѕРІСЂРµРјРµРЅРЅС‹Рµ С‚РµС…РЅРѕР»РѕРіРёРё РґР»СЏ СЃРѕР·РґР°РЅРёСЏ Р±С‹СЃС‚СЂС‹С…, Р±РµР·РѕРїР°СЃРЅС‹С… Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅС‹С… РІРµР±-СЂРµС€РµРЅРёР№.
РљР°РєРѕР№ С‚РёРї СЃР°Р№С‚Р° РІР°СЃ РёРЅС‚РµСЂРµСЃСѓРµС‚?"""
                elif language == 'en':
                    answer = """Andrii-IT offers a full cycle of website development:

1. E-commerce development
2. Corporate website creation
3. Landing page development
4. CRM and payment system integration
5. Responsive design for all devices
6. SEO optimization

Our team uses modern technologies to create fast, secure, and functional web solutions.
What type of website are you interested in?"""
                else:
                    answer = """Andrii-IT bietet einen vollstГ¤ndigen Webentwicklungszyklus:

1. E-Commerce-Entwicklung
2. Erstellung von Unternehmenswebsites
3. Entwicklung von Landingpages
4. CRM- und Zahlungssystemintegration
5. Responsives Design fГјr alle GerГ¤te
6. SEO-Optimierung

Unser Team verwendet moderne Technologien, um schnelle, sichere und funktionale WeblГ¶sungen zu erstellen.
An welchem Websitetyp sind Sie interessiert?"""

            # Check for AI/ML related keywords
            elif any(word in message_lower for word in ["ai", "ml", "artificial", "machine", "С€С‚СѓС‡РЅ", "РёСЃРєСѓСЃСЃС‚РІ", "РјР°С€РёРЅ", "СЂРѕР·СѓРјРЅ"]):
                if language == 'uk':
                    answer = """Andrii-IT РїСЂРѕРїРѕРЅСѓС” С–РЅРЅРѕРІР°С†С–Р№РЅС– СЂС–С€РµРЅРЅСЏ Сѓ СЃС„РµСЂС– С€С‚СѓС‡РЅРѕРіРѕ С–РЅС‚РµР»РµРєС‚Сѓ:

1. Р†РЅС‚РµРіСЂР°С†С–СЏ AI-С‡Р°С‚-Р±РѕС‚С–РІ РґР»СЏ РѕР±СЃР»СѓРіРѕРІСѓРІР°РЅРЅСЏ РєР»С–С”РЅС‚С–РІ
2. РЎРёСЃС‚РµРјРё Р°РЅР°Р»С–Р·Сѓ РґР°РЅРёС… РЅР° РѕСЃРЅРѕРІС– РјР°С€РёРЅРЅРѕРіРѕ РЅР°РІС‡Р°РЅРЅСЏ
3. РђРІС‚РѕРјР°С‚РёР·Р°С†С–СЏ Р±С–Р·РЅРµСЃ-РїСЂРѕС†РµСЃС–РІ Р·Р° РґРѕРїРѕРјРѕРіРѕСЋ AI
4. РџРµСЂСЃРѕРЅР°Р»С–Р·РѕРІР°РЅС– СЂРµРєРѕРјРµРЅРґР°С†С–Р№РЅС– СЃРёСЃС‚РµРјРё
5. РљРѕРјРї'СЋС‚РµСЂРЅРёР№ Р·С–СЂ РґР»СЏ Р°РІС‚РѕРјР°С‚РёР·Р°С†С–С— РїСЂРѕС†РµСЃС–РІ

РЇРєРёР№ РЅР°РїСЂСЏРјРѕРє AI РІР°СЃ С†С–РєР°РІРёС‚СЊ РЅР°Р№Р±С–Р»СЊС€Рµ?"""
                elif language == 'ru':
                    answer = """Andrii-IT РїСЂРµРґР»Р°РіР°РµС‚ РёРЅРЅРѕРІР°С†РёРѕРЅРЅС‹Рµ СЂРµС€РµРЅРёСЏ РІ СЃС„РµСЂРµ РёСЃРєСѓСЃСЃС‚РІРµРЅРЅРѕРіРѕ РёРЅС‚РµР»Р»РµРєС‚Р°:

1. РРЅС‚РµРіСЂР°С†РёСЏ AI-С‡Р°С‚-Р±РѕС‚РѕРІ РґР»СЏ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ РєР»РёРµРЅС‚РѕРІ
2. РЎРёСЃС‚РµРјС‹ Р°РЅР°Р»РёР·Р° РґР°РЅРЅС‹С… РЅР° РѕСЃРЅРѕРІРµ РјР°С€РёРЅРЅРѕРіРѕ РѕР±СѓС‡РµРЅРёСЏ
3. РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ Р±РёР·РЅРµСЃ-РїСЂРѕС†РµСЃСЃРѕРІ СЃ РїРѕРјРѕС‰СЊСЋ AI
4. РџРµСЂСЃРѕРЅР°Р»РёР·РёСЂРѕРІР°РЅРЅС‹Рµ СЂРµРєРѕРјРµРЅРґР°С‚РµР»СЊРЅС‹Рµ СЃРёСЃС‚РµРјС‹
5. РљРѕРјРїСЊСЋС‚РµСЂРЅРѕРµ Р·СЂРµРЅРёРµ РґР»СЏ Р°РІС‚РѕРјР°С‚РёР·Р°С†РёРё РїСЂРѕС†РµСЃСЃРѕРІ

РљР°РєРѕРµ РЅР°РїСЂР°РІР»РµРЅРёРµ AI РІР°СЃ РёРЅС‚РµСЂРµСЃСѓРµС‚ Р±РѕР»СЊС€Рµ РІСЃРµРіРѕ?"""
                elif language == 'en':
                    answer = """Andrii-IT offers innovative solutions in artificial intelligence:

1. Integration of AI chatbots for customer service
2. Machine learning based data analysis systems
3. Business process automation with AI
4. Personalized recommendation systems
5. Computer vision for process automation

Which AI direction interests you the most?"""
                else:
                    answer = """Andrii-IT bietet innovative LГ¶sungen im Bereich der kГјnstlichen Intelligenz:

1. Integration von KI-Chatbots fГјr den Kundenservice
2. Datenanalysesysteme auf Basis von maschinellem Lernen
3. Automatisierung von GeschГ¤ftsprozessen mit KI
4. Personalisierte Empfehlungssysteme
5. Computer Vision fГјr Prozessautomatisierung

Welche KI-Richtung interessiert Sie am meisten?"""
            
            # Default response if no keywords match
            else:
                responses = {
                    'uk': """Р”СЏРєСѓСЋ Р·Р° РІР°С€Рµ Р·РІРµСЂРЅРµРЅРЅСЏ РґРѕ Andrii-IT. РњРё СЃРїРµС†С–Р°Р»С–Р·СѓС”РјРѕСЃСЊ РЅР°:

1. Р РѕР·СЂРѕР±С†С– СЃСѓС‡Р°СЃРЅРёС… РІРµР±-СЃР°Р№С‚С–РІ С‚Р° РІРµР±-РґРѕРґР°С‚РєС–РІ
2. РњР°СЂРєРµС‚РёРЅРіРѕРІРёС… СЂС–С€РµРЅРЅСЏС… С‚Р° Р°РІС‚РѕРјР°С‚РёР·Р°С†С–С— СЂРµРєР»Р°РјРё
3. РђРІС‚РѕРјР°С‚РёР·Р°С†С–С— Р±С–Р·РЅРµСЃ-РїСЂРѕС†РµСЃС–РІ Р·Р° РґРѕРїРѕРјРѕРіРѕСЋ AI
4. Р РѕР·СЂРѕР±С†С– РјРѕР±С–Р»СЊРЅРёС… РґРѕРґР°С‚РєС–РІ
5. РўРµС…РЅС–С‡РЅС–Р№ РїС–РґС‚СЂРёРјС†С– С‚Р° РѕР±СЃР»СѓРіРѕРІСѓРІР°РЅРЅС–

Р§РёРј СЃР°РјРµ РјРё РјРѕР¶РµРјРѕ РІР°Рј РґРѕРїРѕРјРѕРіС‚Рё? РќР°РїРёС€С–С‚СЊ РїСЂРѕ РІР°С€ РїСЂРѕС”РєС‚ Р°Р±Рѕ РїРѕС‚СЂРµР±Сѓ РґРµС‚Р°Р»СЊРЅС–С€Рµ.""",
                    'ru': """РЎРїР°СЃРёР±Рѕ Р·Р° РІР°С€Рµ РѕР±СЂР°С‰РµРЅРёРµ РІ Andrii-IT. РњС‹ СЃРїРµС†РёР°Р»РёР·РёСЂСѓРµРјСЃСЏ РЅР°:

1. Р Р°Р·СЂР°Р±РѕС‚РєРµ СЃРѕРІСЂРµРјРµРЅРЅС‹С… РІРµР±-СЃР°Р№С‚РѕРІ Рё РІРµР±-РїСЂРёР»РѕР¶РµРЅРёР№
2. РњР°СЂРєРµС‚РёРЅРіРѕРІС‹С… СЂРµС€РµРЅРёСЏС… Рё Р°РІС‚РѕРјР°С‚РёР·Р°С†РёРё СЂРµРєР»Р°РјС‹
3. РђРІС‚РѕРјР°С‚РёР·Р°С†РёРё Р±РёР·РЅРµСЃ-РїСЂРѕС†РµСЃСЃРѕРІ СЃ РїРѕРјРѕС‰СЊСЋ AI
4. Р Р°Р·СЂР°Р±РѕС‚РєРµ РјРѕР±РёР»СЊРЅС‹С… РїСЂРёР»РѕР¶РµРЅРёР№
5. РўРµС…РЅРёС‡РµСЃРєРѕР№ РїРѕРґРґРµСЂР¶РєРµ Рё РѕР±СЃР»СѓР¶РёРІР°РЅРёРё

Р§РµРј РёРјРµРЅРЅРѕ РјС‹ РјРѕР¶РµРј РІР°Рј РїРѕРјРѕС‡СЊ? РќР°РїРёС€РёС‚Рµ Рѕ РІР°С€РµРј РїСЂРѕРµРєС‚Рµ РёР»Рё РїРѕС‚СЂРµР±РЅРѕСЃС‚Рё РїРѕРґСЂРѕР±РЅРµРµ.""",
                    'en': """Thank you for contacting Andrii-IT. We specialize in:

1. Development of modern websites and web applications
2. Marketing solutions and advertising automation
3. Business process automation using AI
4. Mobile app development
5. Technical support and maintenance

How exactly can we help you? Please write about your project or need in more detail.""",
                    'de': """Vielen Dank fГјr Ihre Kontaktaufnahme mit Andrii-IT. Wir sind spezialisiert auf:

1. Entwicklung moderner Websites und Webanwendungen
2. MarketinglГ¶sungen und Werbungsautomatisierung
3. Automatisierung von GeschГ¤ftsprozessen mit KI
4. Entwicklung mobiler Anwendungen
5. Technischer Support und Wartung

Wie genau kГ¶nnen wir Ihnen helfen? Bitte schreiben Sie ausfГјhrlicher Гјber Ihr Projekt oder Ihren Bedarf."""
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
            'uk': f"Р’РёР±Р°С‡С‚Рµ, СЃС‚Р°Р»Р°СЃСЏ РїРѕРјРёР»РєР°. РЎРїСЂРѕР±СѓР№С‚Рµ С‰Рµ СЂР°Р· РїС–Р·РЅС–С€Рµ.",
            'ru': f"РР·РІРёРЅРёС‚Рµ, РїСЂРѕРёР·РѕС€Р»Р° РѕС€РёР±РєР°. РџРѕРїСЂРѕР±СѓР№С‚Рµ РµС‰Рµ СЂР°Р· РїРѕР·Р¶Рµ.",
            'en': f"Sorry, an error occurred. Please try again later.",
            'de': f"Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es spГ¤ter erneut."
        }
        
        language = metadata.get('language', 'uk')
        
        return {
            'error': str(e),
            'answer': error_messages.get(language, error_messages['uk']),
            'agent': 'ErrorHandler',
            'conversation_id': metadata.get('conversation_id', str(uuid.uuid4()))
        }

