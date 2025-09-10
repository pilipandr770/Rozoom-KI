from app.services.telegram_service import send_telegram_message
import logging
import time
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# Define path for file-based queue storage
QUEUE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'telegram_queue')
Path(QUEUE_DIR).mkdir(parents=True, exist_ok=True)

class TelegramQueue:
    """
    A queue for managing telegram messages and retrying failed attempts
    with file-based persistence for reliability
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
        
        # Load any messages from the file-based queue
        self._load_from_disk()
    
    def _load_from_disk(self):
        """
        Load any queued messages from disk
        """
        try:
            if not os.path.exists(QUEUE_DIR):
                return
                
            files = [f for f in os.listdir(QUEUE_DIR) if f.endswith('.json')]
            for file in files:
                try:
                    with open(os.path.join(QUEUE_DIR, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'message' in data:
                            self.queue.append((data['message'], data.get('attempts', 0)))
                except Exception as e:
                    logger.error(f"Error loading message from {file}: {e}")
                    
            if self.queue:
                logger.info(f"Loaded {len(self.queue)} messages from disk")
        except Exception as e:
            logger.error(f"Error loading queued messages from disk: {e}")
    
    def _save_to_disk(self, message, attempts):
        """
        Save a message to disk for persistence
        
        Args:
            message (str): The message to save
            attempts (int): Number of attempts made so far
        """
        try:
            filename = f"telegram_msg_{int(time.time())}_{hash(message) % 10000}.json"
            filepath = os.path.join(QUEUE_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'message': message,
                    'attempts': attempts,
                    'timestamp': time.time()
                }, f)
                
            logger.info(f"Saved message to disk: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save message to disk: {e}")
            return False
    
    def _remove_from_disk(self, message):
        """
        Remove a message from disk after successful sending
        
        Args:
            message (str): The message to remove
        """
        try:
            message_hash = hash(message) % 10000
            files = [f for f in os.listdir(QUEUE_DIR) if f.endswith('.json')]
            
            for file in files:
                filepath = os.path.join(QUEUE_DIR, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('message') == message:
                            os.remove(filepath)
                            logger.info(f"Removed message from disk: {filepath}")
                            break
                except Exception as e:
                    logger.error(f"Error checking message file {file}: {e}")
        except Exception as e:
            logger.error(f"Failed to remove message from disk: {e}")
            
    def add_message(self, message):
        """
        Add a message to the queue
        
        Args:
            message (str): The message to be sent
        """
        self.queue.append((message, 0))
        # Save to disk for persistence
        self._save_to_disk(message, 0)
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
                # Remove failed message from disk to avoid buildup
                self._remove_from_disk(message)
                continue
            
            try:
                # Exponential backoff - wait longer between retries
                if attempts > 0:
                    backoff_time = min(2 ** (attempts - 1), 300)  # Cap at 5 minutes
                    logger.info(f"Using backoff delay of {backoff_time}s for retry {attempts}")
                
                # Try to send the message
                success = send_telegram_message(message)
                if success:
                    logger.info("Successfully sent queued Telegram message")
                    # Remove from disk storage
                    self._remove_from_disk(message)
                else:
                    logger.warning(f"Failed to send queued message (attempt {attempts+1}/{self.max_retries}). Will retry later.")
                    # Update the attempt count on disk
                    self._remove_from_disk(message)  # Remove old entry
                    self._save_to_disk(message, attempts + 1)  # Create new entry with updated attempts
                    remaining_messages.append((message, attempts + 1))
            except Exception as e:
                # Handle any unexpected errors during sending
                logger.error(f"Error processing queue message: {str(e)}")
                # Keep message in queue for retry
                self._remove_from_disk(message)  # Remove old entry
                self._save_to_disk(message, attempts + 1)  # Create new entry with updated attempts
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
        # Try to send directly first
        from app.services.telegram_service import send_telegram_message
        
        try:
            # Attempt immediate send
            if send_telegram_message(message):
                logger.info("Message sent immediately, no need to queue")
                return True
        except Exception as e:
            # If direct send fails due to network/DB issues, continue to queue
            logger.warning(f"Direct send failed, will queue message: {e}")
        
        # If immediate send failed or raised an exception, queue the message
        telegram_queue.add_message(message)
        return True
    except Exception as e:
        logger.error(f"Error in queue_telegram_message: {e}")
        
        # Last-ditch effort: try to save to disk directly
        try:
            filename = f"telegram_msg_emergency_{int(time.time())}_{hash(message) % 10000}.json"
            filepath = os.path.join(QUEUE_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'message': message,
                    'attempts': 0,
                    'timestamp': time.time(),
                    'emergency': True
                }, f)
                
            logger.info(f"Emergency save of message to disk: {filepath}")
            return True
        except Exception as emergency_e:
            logger.error(f"Emergency save also failed: {emergency_e}")
            return False

def send_telegram_message_with_retry(message, max_immediate_retries=2):
    """
    Attempt to send a message immediately with retries, with fallback to queue if it fails
    
    Args:
        message (str): The message to send
        max_immediate_retries (int): Maximum number of immediate retries before queueing
    
    Returns:
        bool: True if the message was sent or queued successfully
    """
    # Try sending with a few immediate retries first
    for attempt in range(max_immediate_retries):
        try:
            if send_telegram_message(message):
                return True
            else:
                logger.warning(f"Immediate send attempt {attempt+1}/{max_immediate_retries} failed")
                # Small delay before next retry
                time.sleep(1)
        except Exception as e:
            logger.error(f"Error in immediate send attempt {attempt+1}: {e}")
            # Continue to next attempt
    
    # If all immediate attempts fail, queue the message for later processing
    logger.info(f"All {max_immediate_retries} immediate attempts failed, queueing message")
    return queue_telegram_message(message)
