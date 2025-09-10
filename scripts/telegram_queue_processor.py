import os
import asyncio
from app.utils.telegram_queue import TelegramQueue
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("telegram_queue_processor")

async def process_queue_periodically(queue, interval_seconds=60):
    """
    Process the Telegram message queue at regular intervals
    
    Args:
        queue (TelegramQueue): The queue to process
        interval_seconds (int): How often to process the queue
    """
    while True:
        try:
            logger.info("Processing Telegram message queue...")
            queue.process_queue()
            logger.info(f"Queue processing complete. {len(queue.queue)} messages remaining.")
        except Exception as e:
            logger.error(f"Error processing Telegram queue: {e}")
        
        # Wait for next interval
        await asyncio.sleep(interval_seconds)

async def main():
    """Main entry point for the queue processor"""
    # Check if we have Telegram config
    if not os.environ.get('TELEGRAM_BOT_TOKEN') or not os.environ.get('TELEGRAM_CHAT_ID'):
        logger.error("Missing Telegram environment variables. Cannot process queue.")
        return
    
    # Create queue (will be empty initially)
    queue = TelegramQueue()
    
    # Add a test message if TEST_MESSAGE env var is set
    test_message = os.environ.get('TEST_MESSAGE')
    if test_message:
        logger.info("Adding test message to queue")
        queue.add_message(test_message)
    
    # Start processing the queue
    logger.info("Starting Telegram queue processor...")
    await process_queue_periodically(queue)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Queue processor stopped by user")
    except Exception as e:
        logger.error(f"Queue processor failed: {e}")
