from app.services.telegram_service import send_telegram_message
import logging
import time
import os

logger = logging.getLogger(__name__)

class TelegramQueue:
    """
    A queue for managing telegram messages and retrying failed attempts
    """
    def __init__(self, max_retries=5, retry_interval=60):
        """
        Initialize the queue
        
        Args:
            max_retries (int): Maximum number of retries per message
            retry_interval (int): Time in seconds between retries
        """
        self.queue = []  # List of (message, attempts) tuples
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.last_attempt = 0
    
    def add_message(self, message):
        """
        Add a message to the queue
        
        Args:
            message (str): The message to be sent
        """
        self.queue.append((message, 0))
        logger.info(f"Added message to telegram queue. Queue size: {len(self.queue)}")
        
        # Try to process the queue right away
        self.process_queue()
    
    def process_queue(self):
        """
        Process the message queue and attempt to send messages
        """
        # Check if enough time has passed since last attempt
        current_time = time.time()
        if current_time - self.last_attempt < self.retry_interval and self.last_attempt > 0:
            return
            
        self.last_attempt = current_time
        
        # No messages to process
        if not self.queue:
            return
            
        # Check if Telegram configuration is available
        if not os.environ.get('TELEGRAM_BOT_TOKEN') or not os.environ.get('TELEGRAM_CHAT_ID'):
            logger.warning("Cannot process Telegram queue: missing environment variables")
            return
        
        # Process the queue
        remaining_messages = []
        for message, attempts in self.queue:
            if attempts >= self.max_retries:
                logger.error(f"Failed to send Telegram message after {attempts} attempts. Dropping message.")
                continue
                
            success = send_telegram_message(message)
            if success:
                logger.info("Successfully sent queued Telegram message")
            else:
                logger.warning(f"Failed to send queued message (attempt {attempts+1}/{self.max_retries}). Will retry later.")
                remaining_messages.append((message, attempts + 1))
        
        # Update the queue
        self.queue = remaining_messages
        
        if self.queue:
            logger.info(f"Telegram queue has {len(self.queue)} remaining messages")

# Global queue instance
telegram_queue = TelegramQueue()

def queue_telegram_message(message):
    """
    Queue a message to be sent to Telegram with automatic retries
    
    Args:
        message (str): The message to send
    
    Returns:
        bool: True if the message was successfully queued
    """
    try:
        telegram_queue.add_message(message)
        return True
    except Exception as e:
        logger.error(f"Error queuing Telegram message: {e}")
        return False

def send_telegram_message_with_retry(message):
    """
    Attempt to send a message immediately, with fallback to queue if it fails
    
    Args:
        message (str): The message to send
    
    Returns:
        bool: True if the message was sent or queued successfully
    """
    try:
        success = send_telegram_message(message)
        if success:
            return True
        else:
            # If immediate send fails, add to queue for later retry
            return queue_telegram_message(message)
    except Exception as e:
        logger.error(f"Error in send_telegram_message_with_retry: {e}")
        # Try to queue the message
        return queue_telegram_message(message)
