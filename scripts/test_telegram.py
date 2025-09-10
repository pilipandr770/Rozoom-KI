#!/usr/bin/env python3
"""
Manual utility to test the Telegram notification system.
"""

import os
import sys
import logging
from datetime import datetime

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

def test_telegram_connection():
    """
    Test the Telegram connection by sending a test message
    """
    try:
        # Import the Telegram service
        from app.services.telegram_service import send_telegram_message
        
        # Create a test message
        message = f"""
<b>🔧 Telegram Connection Test</b>

This is a test message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<i>If you see this message, the Telegram notification system is working correctly.</i>
"""
        
        # Send the message
        result = send_telegram_message(message)
        
        if result:
            logger.info("✅ Test message sent successfully")
            return True
        else:
            logger.error("❌ Failed to send test message")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing Telegram connection: {e}")
        return False

def test_telegram_queue():
    """
    Test the Telegram queue system by queueing a test message
    """
    try:
        # Import the queue function
        from app.utils.telegram_queue import queue_telegram_message
        
        # Create a test message
        message = f"""
<b>📋 Telegram Queue Test</b>

This is a queued test message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<i>If you see this message, the Telegram queue system is working correctly.</i>
"""
        
        # Queue the message
        result = queue_telegram_message(message)
        
        if result:
            logger.info("✅ Test message queued successfully")
            return True
        else:
            logger.error("❌ Failed to queue test message")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing Telegram queue: {e}")
        return False
        
def check_telegram_config():
    """
    Check if Telegram is properly configured
    """
    # Check environment variables
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set")
        print("Please set the TELEGRAM_BOT_TOKEN environment variable")
        return False
        
    if not chat_id:
        logger.error("❌ TELEGRAM_CHAT_ID not set")
        print("Please set the TELEGRAM_CHAT_ID environment variable")
        return False
        
    logger.info("✅ Telegram configuration found")
    return True

def main():
    """
    Run the Telegram tests
    """
    print("=" * 60)
    print("Telegram Notification System Test")
    print("=" * 60)
    
    # First check configuration
    if not check_telegram_config():
        return 1
        
    # Test direct connection
    print("\nTesting direct Telegram connection...")
    direct_result = test_telegram_connection()
    
    # Test queue system
    print("\nTesting Telegram queue system...")
    queue_result = test_telegram_queue()
    
    # Show results
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"Direct connection: {'✅ PASS' if direct_result else '❌ FAIL'}")
    print(f"Queue system: {'✅ PASS' if queue_result else '❌ FAIL'}")
    print("=" * 60)
    
    # Process the queue
    if queue_result:
        print("\nProcessing the queue to send the test message...")
        from app.utils.telegram_queue import telegram_queue
        telegram_queue.process_queue()
    
    return 0 if direct_result and queue_result else 1

if __name__ == "__main__":
    # Create a minimal Flask application context to ensure environment is loaded
    from app import create_app
    app = create_app()
    
    with app.app_context():
        sys.exit(main())
