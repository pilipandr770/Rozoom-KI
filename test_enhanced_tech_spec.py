import os
import logging
import requests
from app.services.telegram_service import send_tech_spec_notification
from app.agents.tech_spec import TechSpecTemplate

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
    """Test sending a tech spec notification through Telegram with all answers to questions"""
    # Create template to get questions
    template = TechSpecTemplate()
    
    # Create more detailed test data with answers to each question
    tech_spec_data = {
        'answers': []
    }
    
    # Project Overview section
    tech_spec_data['answers'].append({
        'question': 'Project Overview',
        'answer': 'Create an online shop for handmade products\nTo help artisans sell their products online\nCraft enthusiasts and gift shoppers'
    })
    
    # Functional Requirements section
    tech_spec_data['answers'].append({
        'question': 'Functional Requirements',
        'answer': 'Product listings with categories, shopping cart, payment processing\nUser accounts, order tracking, product reviews\nBrowse products → Add to cart → Checkout → Payment'
    })
    
    # Technical Requirements section
    tech_spec_data['answers'].append({
        'question': 'Technical Requirements',
        'answer': 'Prefer Python/Django or Node.js/React\nIntegration with Stripe for payments and existing inventory system\nPrefer cloud hosting with automatic scaling'
    })
    
    # Timeline & Budget section
    tech_spec_data['answers'].append({
        'question': 'Timeline & Budget',
        'answer': '3-4 months for development and testing\nBudget between 10,000-15,000 EUR\nNeed to launch before the holiday shopping season'
    })
    
    # Contact Information section
    tech_spec_data['answers'].append({
        'question': 'Contact Information',
        'answer': 'Anna Schmidt\nanna.schmidt@example.com\n+49123456789'
    })

    contact_info = {
        'name': 'Anna Schmidt',
        'email': 'anna.schmidt@example.com',
        'phone': '+49123456789'
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
            logger.info(f'Enhanced tech spec notification sent: {result}')
            return result
        except Exception as e:
            logger.error(f'Error sending notification: {str(e)}')
            return False
    else:
        logger.error("Network connection to Telegram API failed, notification not sent")
        return False

if __name__ == "__main__":
    test_tech_spec_notification()
