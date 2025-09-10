#!/usr/bin/env python3
"""
Process the Telegram message queue and retry sending messages.
This script is designed to be run as a cron job or scheduled task.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(project_root, 'logs', 'telegram_queue.log'), mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
Path(os.path.join(project_root, 'logs')).mkdir(exist_ok=True)

def main():
    """
    Process the Telegram message queue
    """
    try:
        logger.info("Starting Telegram queue processor")
        
        # Import the queue processor from our application
        from app.utils.telegram_queue import telegram_queue
        
        # Process the queue
        telegram_queue.process_queue()
        
        logger.info("Telegram queue processing completed")
    except Exception as e:
        logger.error(f"Error processing Telegram queue: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
