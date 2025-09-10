import os
from app.services.telegram_service import send_tech_spec_notification

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
print(f'TELEGRAM_BOT_TOKEN exists: {bool(os.environ.get("TELEGRAM_BOT_TOKEN"))}')
print(f'TELEGRAM_CHAT_ID exists: {bool(os.environ.get("TELEGRAM_CHAT_ID"))}')

# Test sending notification
result = send_tech_spec_notification(tech_spec_data, contact_info)
print(f'Notification sent: {result}')
