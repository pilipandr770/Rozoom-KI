#!/usr/bin/env python3
"""
Manually send a test message to Telegram to diagnose connection issues.
This script uses direct IP address instead of domain resolution for environments
where DNS lookups fail for api.telegram.org.
"""

import os
import sys
import logging
import requests
import socket
import time
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
Path(os.path.join(project_root, 'logs')).mkdir(exist_ok=True)

def send_direct_telegram_message(message, max_retries=3):
    """
    Send message directly to Telegram API using IP address instead of hostname
    to avoid DNS resolution issues.
    
    Args:
        message (str): Message to send
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Отключаем предупреждения для отключенной проверки SSL-сертификатов
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Get Telegram API credentials
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logger.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables")
        return False
    
    # Known IP addresses for api.telegram.org
    # These can change, so it's best to check current ones if this doesn't work
    telegram_ips = [
        '149.154.167.220',
        '149.154.167.222',
        '149.154.165.120',
        '91.108.4.5',
        '91.108.56.100'
    ]
    
    for attempt in range(max_retries):
        # Try with each IP
        for ip in telegram_ips:
            try:
                logger.info(f"Attempting to connect to Telegram API using IP {ip} (attempt {attempt+1}/{max_retries})")
                url = f"https://{ip}/bot{bot_token}/sendMessage"
                headers = {'Host': 'api.telegram.org'}
                payload = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(
                    url, 
                    headers=headers,
                    data=payload, 
                    timeout=(5, 15),
                    verify=False  # Отключаем SSL верификацию для IP-соединений
                )
                
                if response.status_code == 200:
                    logger.info(f"Message sent successfully using IP {ip}")
                    return True
                else:
                    logger.error(f"Failed to send message using IP {ip}: {response.status_code}, {response.text}")
            except Exception as e:
                logger.error(f"Error sending to IP {ip}: {str(e)}")
        
        # Wait before next retry
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            logger.info(f"Waiting {wait_time} seconds before next retry...")
            time.sleep(wait_time)
    
    return False

def send_test_message():
    """
    Send a test message to verify Telegram API connectivity
    """
    message = f"""
<b>🧪 Telegram Connectivity Test</b>

This is a test message sent at {time.strftime('%Y-%m-%d %H:%M:%S')} using direct IP connection to Telegram API.

<i>If you see this message, the direct connection is working correctly.</i>
"""
    
    # Try first with normal domain-based approach
    try:
        logger.info("Testing standard domain-based connection...")
        from app.services.telegram_service import send_telegram_message
        if send_telegram_message(message):
            logger.info("✅ Standard domain-based connection successful")
            return True
    except Exception as e:
        logger.error(f"Standard connection failed: {str(e)}")
    
    # If that fails, try with direct IP approach
    logger.info("Testing direct IP-based connection...")
    if send_direct_telegram_message(message):
        logger.info("✅ Direct IP-based connection successful")
        return True
    else:
        logger.error("❌ All connection attempts failed")
        return False

def main():
    """
    Main function to test Telegram connectivity
    """
    try:
        print("=" * 50)
        print("Telegram Connectivity Test")
        print("=" * 50)
        
        if send_test_message():
            print("\n✅ Test message sent successfully!")
            return 0
        else:
            print("\n❌ Failed to send test message.")
            return 1
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
