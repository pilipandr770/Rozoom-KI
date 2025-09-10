"""
IP-based implementation of the Telegram API service.
This module provides functions to connect to Telegram API using direct IP addresses
when DNS resolution fails.
"""

import requests
import logging
import time
import os

logger = logging.getLogger(__name__)

# Known IP addresses for api.telegram.org
# These can change, so it's best to check current ones if this doesn't work
TELEGRAM_IPS = [
    '149.154.167.220',
    '149.154.167.222',
    '149.154.165.120',
    '91.108.4.5',
    '91.108.56.100'
]

def get_telegram_config():
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

def send_via_ip_addresses(message, max_retries=3):
    """
    Send message to Telegram API using direct IP addresses instead of domain name.
    This is a workaround for environments with DNS resolution issues.
    
    Args:
        message (str): Message to send
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        bool: True if successful, False otherwise
    """
    bot_token, chat_id, is_valid = get_telegram_config()
    
    if not is_valid:
        logger.error("Invalid Telegram configuration - missing bot token or chat ID")
        return False
    
    for attempt in range(max_retries):
        # Try with each IP
        for ip in TELEGRAM_IPS:
            try:
                logger.info(f"Attempting to connect to Telegram API using IP {ip} (attempt {attempt+1}/{max_retries})")
                url = f"https://{ip}/bot{bot_token}/sendMessage"
                headers = {'Host': 'api.telegram.org'}
                payload = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                # Отключаем проверку сертификата для прямых IP-подключений
                # так как IP-адрес не будет соответствовать имени сертификата
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
