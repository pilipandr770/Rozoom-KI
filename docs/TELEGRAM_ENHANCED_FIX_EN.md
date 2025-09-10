# Telegram Notification System Enhancement Guide

## Problem Overview

After analysis of logs and code, we identified the following issues with Telegram notifications:

1. **DNS Resolution Problems** - On Render.com server, the application fails to resolve `api.telegram.org` domain name (error: `[Errno -2] Name or service not known`).

2. **No Queue Processing** - After our previous change from queue-based to direct sending, messages are not delivered when network issues occur.

## Implemented Solutions

We've implemented a comprehensive solution with multiple layers of protection:

### 1. Hybrid Sending Approach

Modified code in `controller.py` to first try direct sending, and if that fails, place the message in a queue:

```python
try:
    # First try to send directly
    success = send_tech_spec_notification(tech_spec_data, contact_info)
    if success:
        current_app.logger.info(f"Technical specification notification SENT directly for {user_email}")
    else:
        # If direct sending fails, place in queue
        message_content = send_tech_spec_notification(tech_spec_data, contact_info, return_message_only=True)
        from app.utils.telegram_queue import queue_telegram_message
        queue_telegram_message(message_content)
        current_app.logger.info(f"Technical specification notification QUEUED for {user_email} (direct send failed)")
```

### 2. IP-based Connection

Added a new module `telegram_ip_service.py` that uses direct IP addresses instead of domain name when DNS resolution fails:

```python
# Known IP addresses for api.telegram.org
TELEGRAM_IPS = [
    '149.154.167.220',
    '149.154.167.222',
    '149.154.165.120',
    '91.108.4.5',
    '91.108.56.100'
]
```

### 3. Cron Job for Queue Processing

Added a cron job to `render.yaml` that periodically processes the message queue:

```yaml
# Cron job for processing Telegram message queue
- type: cron
  name: telegram-queue-processor
  runtime: python
  schedule: "*/5 * * * *"  # Run every 5 minutes
  buildCommand: pip install -r requirements.txt
  startCommand: python scripts/process_telegram_queue.py
```

### 4. Enhanced Error Handling

Updated the `send_telegram_message` function to use different message sending strategies and better handle network errors:

```python
# If domain-based approach fails, try IP-based
if dns_failed:
    logger.info("Trying IP-based fallback for Telegram API...")
    try:
        from app.services.telegram_ip_service import send_via_ip_addresses
        return send_via_ip_addresses(message, max_retries=2)
    except Exception as e:
        logger.error(f"IP-based fallback also failed: {str(e)}")
        return False
```

## How It Works

1. When a technical specification is submitted, the system first tries to send a notification directly through the regular domain.
2. If regular connection fails (DNS errors), the system tries to use direct IP addresses.
3. If that also fails, the message is saved to a queue for later delivery.
4. Every 5 minutes, a cron job processes the queue and attempts to send saved messages.

## Testing

We created a `test_telegram_direct.py` script that can be used to test different message sending methods.

## Required Implementation Steps

1. Review and commit changes to the codebase
2. Deploy changes to Render.com server
3. Create necessary directories on the server:
   ```
   mkdir -p /opt/render/project/src/data/telegram_queue
   mkdir -p /opt/render/project/src/logs
   ```
4. Restart the service and ensure the cron job is set up correctly
