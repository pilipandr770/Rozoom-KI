# Розверніть цей файл на вашому сервері, щоб перевірити підключення до Telegram API
# Допоможе діагностувати та виправити проблеми з відправкою повідомлень

import os
import requests
import socket
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

def check_environment():
    """Check if required environment variables are set"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return False
    
    if not chat_id:
        logger.error("TELEGRAM_CHAT_ID not found in environment variables")
        return False
    
    logger.info("Environment variables for Telegram are set correctly")
    return True

def check_dns_resolution():
    """Test DNS resolution for Telegram API domain"""
    domain = "api.telegram.org"
    try:
        ip_address = socket.gethostbyname(domain)
        logger.info(f"DNS resolution successful: {domain} resolves to {ip_address}")
        return True
    except socket.gaierror as e:
        logger.error(f"DNS resolution failed for {domain}: {e}")
        return False

def check_network_connectivity():
    """Test basic network connectivity to Telegram API"""
    try:
        response = requests.get("https://api.telegram.org", timeout=5)
        logger.info(f"Network connectivity test: Status code {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Network connectivity test failed: {e}")
        return False

def send_test_message():
    """Try to send a test message to Telegram"""
    if not check_environment():
        return False
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        'chat_id': chat_id,
        'text': f"🔄 Server diagnostic test message from Render.com\nTimestamp: {timestamp}",
        'parse_mode': 'HTML'
    }
    
    try:
        logger.info("Attempting to send test message to Telegram...")
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("Test message sent successfully!")
            return True
        else:
            logger.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return False

def run_diagnostics():
    """Run all diagnostic tests"""
    logger.info("==== Starting Telegram API Diagnostics ====")
    
    # Check environment variables
    env_check = check_environment()
    
    # Check DNS resolution
    dns_check = check_dns_resolution()
    
    # Check network connectivity
    network_check = check_network_connectivity()
    
    # Try sending a message if previous checks passed
    message_sent = False
    if env_check and dns_check and network_check:
        message_sent = send_test_message()
    
    # Print summary
    logger.info("\n==== Diagnostic Results ====")
    logger.info(f"Environment variables: {'✅ PASS' if env_check else '❌ FAIL'}")
    logger.info(f"DNS resolution: {'✅ PASS' if dns_check else '❌ FAIL'}")
    logger.info(f"Network connectivity: {'✅ PASS' if network_check else '❌ FAIL'}")
    logger.info(f"Message sending: {'✅ PASS' if message_sent else '❌ FAIL'}")
    
    if env_check and dns_check and network_check and message_sent:
        logger.info("✅ All tests passed! Your Telegram integration should be working correctly.")
    else:
        logger.info("❌ Some tests failed. Review the logs above for details.")

if __name__ == "__main__":
    run_diagnostics()
