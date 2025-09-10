from app.services.telegram_service import send_telegram_message

def send_telegram_message_retry(message):
    """
    Wrapper for send_telegram_message with automatic retries
    """
    MAX_RETRIES = 3
    
    for i in range(MAX_RETRIES):
        try:
            success = send_telegram_message(message)
            if success:
                return True
        except Exception as e:
            if i == MAX_RETRIES - 1:
                print(f"Failed to send Telegram message after {MAX_RETRIES} attempts: {e}")
            continue
            
    return False
