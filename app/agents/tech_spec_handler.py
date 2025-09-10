from typing import Dict, List, Any, Optional

def handle_tech_spec_creation(message: str, metadata: Dict) -> Dict:
    """Handles the technical specification creation flow"""
    user_lang = metadata.get('language', 'en')
    
    # Если это первое сообщение в потоке создания технического задания
    if not metadata.get('tech_spec_started'):
        metadata['tech_spec_started'] = True
        metadata['tech_spec_section'] = 0
        metadata['tech_spec_answers'] = []
        
        # Получаем первый промпт
        prompt_text = get_tech_spec_prompt(metadata)
        
        # Создаем кнопки для возможных действий
        buttons = []
        if user_lang == 'de':
            buttons.append(InteractiveButton(
                label="Zurück zum Hauptmenü",
                key="main_menu",
                icon="arrow-left"
            ))
        else:
            buttons.append(InteractiveButton(
                label="Back to Main Menu",
                key="main_menu",
                icon="arrow-left"
            ))
        
        return {
            'agent': 'requirements',
            'answer': prompt_text,
            'interactive': {
                'text': prompt_text,
                'buttons': [b.__dict__ for b in buttons],
                'requires_input': True,
                'show_restart': False,
                'meta': {'agent': 'requirements', 'action': 'tech_spec_flow'}
            }
        }
    
    # Если пользователь хочет вернуться в главное меню
    if message.lower() in ["back to main menu", "zurück zum hauptmenü", "main menu", "hauptmenü"]:
        metadata.pop('tech_spec_started', None)
        metadata.pop('tech_spec_section', None)
        metadata.pop('tech_spec_answers', None)
        return handle_greeter(metadata)
    
    # Сохраняем ответ пользователя
    if not metadata.get('tech_spec_answers'):
        metadata['tech_spec_answers'] = []
    metadata['tech_spec_answers'].append(message)
    
    # Переходим к следующему разделу
    current_section = metadata.get('tech_spec_section', 0)
    metadata['tech_spec_section'] = current_section + 1
    
    # Проверяем, закончились ли секции
    template = TechSpecTemplate(user_lang)
    if metadata['tech_spec_section'] >= len(template.sections):
        # Если все секции пройдены, создаем итоговое резюме
        return generate_tech_spec_summary(metadata)
    
    # Получаем следующий промпт
    prompt_text = get_tech_spec_prompt(metadata)
    
    # Создаем кнопки
    buttons = []
    if user_lang == 'de':
        buttons.append(InteractiveButton(
            label="Zurück zum Hauptmenü",
            key="main_menu",
            icon="arrow-left"
        ))
    else:
        buttons.append(InteractiveButton(
            label="Back to Main Menu",
            key="main_menu",
            icon="arrow-left"
        ))
    
    return {
        'agent': 'requirements',
        'answer': prompt_text,
        'interactive': {
            'text': prompt_text,
            'buttons': [b.__dict__ for b in buttons],
            'requires_input': True,
            'show_restart': False,
            'meta': {'agent': 'requirements', 'action': 'tech_spec_flow'}
        }
    }

def generate_tech_spec_summary(metadata: Dict) -> Dict:
    """Generate a summary of the gathered technical specification"""
    user_lang = metadata.get('language', 'en')
    answers = metadata.get('tech_spec_answers', [])
    template = TechSpecTemplate(user_lang)
    
    # Создаем текст резюме в зависимости от языка
    if user_lang == 'de':
        summary_text = "📋 **Zusammenfassung Ihrer technischen Anforderungen:**\n\n"
        
        for i, section in enumerate(template.sections):
            if i < len(answers):
                summary_text += f"**{section['title']}**\n{answers[i]}\n\n"
        
        summary_text += ("Vielen Dank für die Bereitstellung dieser Informationen! "
                        "Unser Team wird diese Anforderungen überprüfen und sich in Kürze mit einem Kostenvoranschlag "
                        "und einem Zeitplan an Sie wenden.\n\n"
                        "Gibt es noch etwas, das Sie hinzufügen oder ändern möchten?")
                        
        # Создаем кнопки для дальнейших действий
        buttons = [
            InteractiveButton(
                label="Anfrage senden",
                key="send_request",
                icon="paper-plane"
            ),
            InteractiveButton(
                label="Anforderungen bearbeiten",
                key="edit_requirements",
                icon="edit"
            ),
            InteractiveButton(
                label="Zurück zum Hauptmenü",
                key="main_menu",
                icon="arrow-left"
            )
        ]
    else:
        summary_text = "📋 **Summary of Your Technical Requirements:**\n\n"
        
        for i, section in enumerate(template.sections):
            if i < len(answers):
                summary_text += f"**{section['title']}**\n{answers[i]}\n\n"
        
        summary_text += ("Thank you for providing this information! "
                        "Our team will review these requirements and get back to you shortly with a cost estimate "
                        "and timeline.\n\n"
                        "Is there anything else you would like to add or change?")
                        
        # Создаем кнопки для дальнейших действий
        buttons = [
            InteractiveButton(
                label="Submit Request",
                key="send_request",
                icon="paper-plane"
            ),
            InteractiveButton(
                label="Edit Requirements",
                key="edit_requirements",
                icon="edit"
            ),
            InteractiveButton(
                label="Back to Main Menu",
                key="main_menu",
                icon="arrow-left"
            )
        ]
    
    return {
        'agent': 'requirements',
        'answer': summary_text,
        'interactive': {
            'text': summary_text,
            'buttons': [b.__dict__ for b in buttons],
            'requires_input': True,
            'show_restart': False,
            'meta': {'agent': 'requirements', 'action': 'tech_spec_summary'}
        }
    }
