import os
import logging
import requests
from app.services.telegram_service import send_tech_spec_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_network_connection():
    """Test if the network connection to Telegram API is working"""
    try:
        response = requests.get("https://api.telegram.org", timeout=5)
        logger.info(f"Telegram API connection test: Status code {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Failed to connect to Telegram API: {str(e)}")
        return False

def test_tech_spec_notification():
    """Test sending a tech spec notification through Telegram"""
    # Set up test data
    tech_spec_data = {
        'answers': [
            {
                'question': 'Project Type',
                'answer': 'Website Development'
            },
            {
                'question': 'Project Goals',
                'answer': 'Create a responsive company website'
            },
            {
                'question': 'Features',
                'answer': 'Contact form, About page, Services'
            }
        ]
    }

    contact_info = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+1234567890'
    }

    # Check environment variables
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    logger.info(f'TELEGRAM_BOT_TOKEN exists: {bool(telegram_token)}')
    logger.info(f'TELEGRAM_CHAT_ID exists: {bool(telegram_chat_id)}')

    # Test network connection first
    if test_network_connection():
        # Test sending notification
        try:
            result = send_tech_spec_notification(tech_spec_data, contact_info)
            logger.info(f'Notification sent: {result}')
            return result
        except Exception as e:
            logger.error(f'Error sending notification: {str(e)}')
            return False
    else:
        logger.error("Network connection to Telegram API failed, notification not sent")
        return False

if __name__ == "__main__":
    test_tech_spec_notification()
