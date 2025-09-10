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

def test_fully_detailed_tech_spec():
    """
    Test sending a tech spec notification with detailed questions and answers.
    This version includes specific answers to each of the 15 questions (3 per section).
    """
    # Get the template to access all 15 questions
    template = TechSpecTemplate()
    
    # Create detailed test data with all 15 question/answer pairs
    tech_spec_data = {
        'answers': [],
        'language': 'en'
    }
    
    # Project Overview section - with individual answers to each question
    project_overview_answers = [
        "An e-commerce platform for handmade artisanal products",
        "Artisans struggle to sell their products online due to technical barriers",
        "Craft enthusiasts, gift shoppers, and people interested in unique handmade items"
    ]
    
    tech_spec_data['answers'].append({
        'question': 'Project Overview',
        'answer': '\n'.join(project_overview_answers)
    })
    
    # Functional Requirements section - with individual answers
    functional_req_answers = [
        "Product listings with categories, shopping cart, secure payment processing, user accounts",
        "Order management, inventory tracking, review system, search functionality with filters",
        "Browse → Product Details → Add to Cart → Checkout → Payment → Order Confirmation"
    ]
    
    tech_spec_data['answers'].append({
        'question': 'Functional Requirements',
        'answer': '\n'.join(functional_req_answers)
    })
    
    # Technical Requirements section - with individual answers
    technical_req_answers = [
        "Prefer Python/Django backend with React frontend, PostgreSQL database",
        "Need integration with Stripe for payments, existing inventory system via API",
        "AWS cloud hosting with auto-scaling capabilities and CDN for global delivery"
    ]
    
    tech_spec_data['answers'].append({
        'question': 'Technical Requirements',
        'answer': '\n'.join(technical_req_answers)
    })
    
    # Timeline & Budget section - with individual answers
    timeline_budget_answers = [
        "4 months development timeline with 1 month for testing and refinement",
        "Budget range of €15,000-20,000 including development and first-year hosting",
        "Must launch before November 15th to capture holiday shopping season"
    ]
    
    tech_spec_data['answers'].append({
        'question': 'Timeline & Budget',
        'answer': '\n'.join(timeline_budget_answers)
    })
    
    # Contact Information section
    contact_info_answers = [
        "Maria Kunsthandwerk",
        "maria@kunsthandwerk-shop.de",
        "+49 176 5551234"
    ]
    
    tech_spec_data['answers'].append({
        'question': 'Contact Information',
        'answer': '\n'.join(contact_info_answers)
    })

    # Prepare contact info dictionary separately
    contact_info = {
        'name': contact_info_answers[0],
        'email': contact_info_answers[1],
        'phone': contact_info_answers[2]
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
            logger.info(f'Fully detailed tech spec notification sent: {result}')
            return result
        except Exception as e:
            logger.error(f'Error sending notification: {str(e)}')
            return False
    else:
        logger.error("Network connection to Telegram API failed, notification not sent")
        return False

if __name__ == "__main__":
    test_fully_detailed_tech_spec()
