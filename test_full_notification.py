#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

from app import create_app
from app.pages import send_tech_spec_email_notification

def test_full_email_notification():
    """Test the complete email notification system"""
    app = create_app()
    with app.app_context():
        print("Testing complete email notification system...")

        # Test data matching the form structure
        tech_spec_data = {
            'answers': [
                {'question': 'Project Type', 'answer': 'Web Application'},
                {'question': 'Project Goal', 'answer': 'Create an e-commerce platform'},
                {'question': 'Target Users', 'answer': 'Small business owners'},
                {'question': 'Timeline', 'answer': '3 months'},
                {'question': 'Budget Range', 'answer': '$10,000 - $25,000'}
            ],
            'language': 'en'
        }
        contact_info = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123'
        }

        try:
            send_tech_spec_email_notification(tech_spec_data, contact_info)
            print("SUCCESS: Email notification sent successfully!")
            print("The notification system is working correctly.")
            print("When clients submit the technical specification form,")
            print("you will receive email notifications with all the details.")
            return True
        except Exception as e:
            print(f"ERROR: Failed to send email notification: {str(e)}")
            print("This might be due to missing email server configuration.")
            print("Please configure MAIL_SERVER, MAIL_USERNAME, and MAIL_PASSWORD")
            print("in your .env file for email notifications to work.")
            return False

if __name__ == "__main__":
    test_full_email_notification()
