# Database-Independent Telegram Queue System

This document describes the database-independent Telegram notification queue system implemented for Rozoom-KI.

## Overview

The system is designed to reliably send Telegram notifications even when the database connection is unstable or unavailable. It uses a file-based queue system that persists messages to disk, ensuring they can be sent later if immediate delivery fails.

## Key Components

1. **File-Based Queue**: All messages are stored in JSON files in the `data/telegram_queue/` directory
2. **Resilient Sending**: Multiple retry mechanisms with exponential backoff
3. **Isolated API Calls**: Direct HTTP requests to Telegram API without database dependency
4. **Queue Processing**: Scheduled tasks to process queued messages

## How It Works

1. When a notification needs to be sent:
   - First attempts to send immediately
   - If that fails, queues the message in the file system
   - If both fail, attempts an emergency direct file save

2. Queue Processing:
   - Messages are loaded from disk files
   - Sent with retry logic
   - Removed from disk after successful sending

3. Periodic Processing:
   - A scheduled task runs `scripts/process_telegram_queue.py` to attempt delivery of queued messages
   - Manual processing can be triggered with `python process_telegram_queue.py`

## Error Handling

The system handles various error types:
- Network connectivity issues
- DNS resolution problems
- Database connection failures
- Telegram API errors

## Configuration

Telegram notifications require two environment variables:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Testing

To test the notification system:
```
python scripts/test_telegram.py
```

This will:
1. Test direct message sending
2. Test the queue system
3. Process the queue to send test messages

## Troubleshooting

If notifications are not being sent:
1. Check if the queue directory contains JSON files
2. Run the manual processor: `python process_telegram_queue.py`
3. Check application logs for errors
4. Verify your Telegram credentials with the test script
