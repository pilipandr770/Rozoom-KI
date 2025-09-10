import os
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def send_telegram_message(message: str) -> bool:
    """
    Send a message to Telegram using the bot token and chat ID from environment variables.
    
    Args:
        message (str): The message to send
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logger.error("Telegram bot token or chat ID not found in environment variables")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'  # Support HTML formatting
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            logger.info(f"Message sent to Telegram successfully")
            return True
        else:
            logger.error(f"Failed to send message to Telegram. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {str(e)}")
        return False

def send_tech_spec_notification(tech_spec_data: Dict[str, Any], contact_info: Optional[Dict[str, str]] = None) -> bool:
    """
    Send a notification about a new technical specification submission.
    
    Args:
        tech_spec_data (Dict[str, Any]): The technical specification data
        contact_info (Optional[Dict[str, str]]): Dictionary containing name, email, and phone
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    # Format the technical specification data into a readable message
    message = "<b>🔔 New Technical Specification Submitted</b>\n\n"
    
    # Add contact information if available
    if contact_info:
        message += "<b>📋 Contact Information:</b>\n"
        if contact_info.get('name'):
            message += f"<b>Name:</b> {contact_info.get('name')}\n"
        if contact_info.get('email'):
            message += f"<b>Email:</b> {contact_info.get('email')}\n"
        if contact_info.get('phone'):
            message += f"<b>Phone:</b> {contact_info.get('phone')}\n"
        message += "\n"
    
    # Add divider for better readability
    message += "<b>═══════════ TECHNICAL SPECIFICATION ═══════════</b>\n\n"
    
    # Add each section of the tech spec with detailed questions and answers
    if 'answers' in tech_spec_data:
        # First, load the TechSpecTemplate to get all questions
        from app.agents.tech_spec import TechSpecTemplate
        template = TechSpecTemplate(language=tech_spec_data.get('language', 'en'))
        
        for i, answer in enumerate(tech_spec_data.get('answers', [])):
            if 'question' in answer and 'answer' in answer:
                section_title = answer.get('question', '')
                message += f"<b>{i+1}. {section_title}</b>\n\n"
                
                # Get the actual questions for this section
                section_questions = []
                if i < len(template.sections):
                    section_questions = template.sections[i]['questions']
                
                # Split the answers by newline
                answer_text = answer.get('answer', '')
                answers_list = answer_text.split('\n')
                
                # If we have all the answers (one per line) and the questions
                if len(answers_list) >= len(section_questions) and section_questions:
                    # Display each question with its corresponding answer
                    for q_idx, question in enumerate(section_questions):
                        if q_idx < len(answers_list):
                            message += f"   <b>❓ {question}</b>\n"
                            answer_line = answers_list[q_idx].strip()
                            if answer_line:  # Only add if we have an answer
                                message += f"   <b>👉</b> {answer_line}\n\n"
                            else:
                                message += f"   <i>No answer provided</i>\n\n"
                else:
                    # Fallback to displaying the entire answer text
                    formatted_answer = answer_text.replace('\n', '\n   ')
                    if formatted_answer.strip():
                        message += f"   {formatted_answer}\n\n"
                    else:
                        message += f"   <i>No details provided</i>\n\n"
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message += f"<b>═════════════════════════════════════════</b>\n"
    message += f"<i>Submitted at: {timestamp}</i>"
    
    return send_telegram_message(message)

def send_contact_form_notification(form_data: Dict[str, str]) -> bool:
    """
    Send a notification about a new contact form submission.
    
    Args:
        form_data (Dict[str, str]): The form data containing name, email, and message
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    name = form_data.get('name', 'Not provided')
    email = form_data.get('email', 'Not provided')
    message_content = form_data.get('message', 'No message')
    
    message = "<b>📩 New Contact Form Submission</b>\n\n"
    message += f"<b>Name:</b> {name}\n"
    message += f"<b>Email:</b> {email}\n"
    message += f"<b>Message:</b>\n{message_content}\n"
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message += f"\n<i>Submitted at: {timestamp}</i>"
    
    return send_telegram_message(message)
