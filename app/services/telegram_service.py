import os
import requests
import logging
import socket
import time
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def get_telegram_config() -> tuple:
    """
    Get Telegram configuration from environment variables.
    
    Returns:
        tuple: (bot_token, chat_id, is_valid)
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logger.error("Telegram bot token or chat ID not found in environment variables")
        return None, None, False
    
    return bot_token, chat_id, True

def create_resilient_session() -> requests.Session:
    """
    Create a requests session with retry mechanism for better network resilience.
    
    Returns:
        requests.Session: Session with retry configuration
    """
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # Total number of retries
        status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
        allowed_methods=["GET", "POST"],  # Methods to retry
        backoff_factor=1  # Backoff factor for exponential backoff
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def send_telegram_message(message: str, max_retries: int = 3) -> bool:
    """
    Send a message to Telegram using the bot token and chat ID from environment variables.
    Includes retry mechanism and better error handling.
    
    Args:
        message (str): The message to send
        max_retries (int): Maximum number of retries
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    bot_token, chat_id, is_valid = get_telegram_config()
    
    if not is_valid:
        return False
    
    # Set DNS cache timeout to 0 to force new DNS resolution
    socket.setdefaulttimeout(15)  # 15 seconds timeout
    
    session = create_resilient_session()
    
    for attempt in range(max_retries):
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'  # Support HTML formatting
            }
            
            response = session.post(url, data=payload, timeout=(5, 15))  # Connect timeout, Read timeout
            
            if response.status_code == 200:
                logger.info(f"Message sent to Telegram successfully")
                return True
            else:
                logger.error(f"Failed to send message to Telegram. Status code: {response.status_code}, Response: {response.text}")
                
                if attempt < max_retries - 1:
                    # Wait before retrying (exponential backoff)
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds... (attempt {attempt+1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                return False
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error sending message to Telegram: {str(e)}")
            if "getaddrinfo failed" in str(e) and attempt < max_retries - 1:
                # DNS resolution issue, retry after a delay
                wait_time = 2 ** attempt
                logger.info(f"DNS resolution issue, retrying in {wait_time} seconds... (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
            elif attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Connection error, retrying in {wait_time} seconds... (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                return False
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds... (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                return False
    
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
