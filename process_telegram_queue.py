# Helper file to manually trigger sending queued Telegram messages
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Create a minimal Flask application context
from app import create_app
app = create_app()

# Use the application context for database and configuration access
with app.app_context():
    # Import and process the queue
    from app.utils.telegram_queue import telegram_queue
    
    print("Processing Telegram message queue...")
    telegram_queue.process_queue()
    print("Queue processing complete.")
