import os
import logging
import time
import socket
from datetime import datetime
from app.services.telegram_service import send_telegram_message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dns_resolution(hostname="api.telegram.org"):
    """Check if DNS resolution is working for a hostname"""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False

def test_network_stability():
    """Test network stability by checking DNS and sending a test message with retries"""
    
    # Check environment variables
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    logger.info(f'TELEGRAM_BOT_TOKEN exists: {bool(telegram_token)}')
    logger.info(f'TELEGRAM_CHAT_ID exists: {bool(telegram_chat_id)}')
    
    if not telegram_token or not telegram_chat_id:
        logger.error("Missing environment variables for Telegram")
        return False
    
    # Check DNS resolution
    dns_check = check_dns_resolution()
    logger.info(f"DNS resolution for api.telegram.org: {'Success' if dns_check else 'Failed'}")
    
    if not dns_check:
        logger.info("Attempting to refresh DNS cache and retry...")
        # Wait to let system potentially refresh DNS
        time.sleep(2)
        dns_check = check_dns_resolution()
        logger.info(f"Second DNS resolution attempt: {'Success' if dns_check else 'Failed'}")
    
    # Test sending a message with the improved service
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_message = f"<b>🔧 Network Stability Test</b>\n\n" \
                   f"This is a test message to verify network connectivity and DNS resolution.\n" \
                   f"DNS Check: {'✅ Success' if dns_check else '❌ Failed'}\n\n" \
                   f"<i>Test run at: {timestamp}</i>"
    
    result = send_telegram_message(test_message)
    
    if result:
        logger.info("Network test successful, Telegram message sent!")
    else:
        logger.error("Network test failed, could not send Telegram message")
    
    return result

if __name__ == "__main__":
    test_network_stability()
