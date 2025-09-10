# Решение проблем с отправкой уведомлений в Telegram

## Выявленные проблемы

При анализе логов и кода были выявлены следующие проблемы с уведомлениями Telegram:

1. **Проблемы с DNS-резолвингом** - На сервере Render.com приложение не может разрешить доменное имя `api.telegram.org` (ошибка `[Errno -2] Name or service not known`).

2. **Отсутствие обработки очереди** - После нашего предыдущего изменения, когда мы переключились с использования очереди на прямую отправку, сообщения не доставляются в случае сетевых проблем.

## Реализованные решения

Мы реализовали комплексное решение, которое включает несколько уровней защиты:

### 1. Гибридный подход отправки

Модифицировали код в `controller.py`, чтобы он сначала пытался отправить уведомление напрямую, а в случае неудачи - помещал его в очередь:

```python
try:
    # Сначала попробуем отправить напрямую
    success = send_tech_spec_notification(tech_spec_data, contact_info)
    if success:
        current_app.logger.info(f"Technical specification notification SENT directly for {user_email}")
    else:
        # Если не удалось отправить напрямую, помещаем в очередь
        message_content = send_tech_spec_notification(tech_spec_data, contact_info, return_message_only=True)
        from app.utils.telegram_queue import queue_telegram_message
        queue_telegram_message(message_content)
        current_app.logger.info(f"Technical specification notification QUEUED for {user_email} (direct send failed)")
```

### 2. Подключение через IP-адреса

Добавили новый модуль `telegram_ip_service.py`, который использует прямые IP-адреса вместо доменного имени в случае проблем с DNS-резолвингом:

```python
# Известные IP-адреса для api.telegram.org
TELEGRAM_IPS = [
    '149.154.167.220',
    '149.154.167.222',
    '149.154.165.120',
    '91.108.4.5',
    '91.108.56.100'
]
```

### 3. Cron-задача для обработки очереди

Добавили cron-задачу в `render.yaml`, которая будет периодически обрабатывать очередь сообщений:

```yaml
# Cron job для обработки очереди Telegram сообщений
- type: cron
  name: telegram-queue-processor
  runtime: python
  schedule: "*/5 * * * *"  # Запуск каждые 5 минут
  buildCommand: pip install -r requirements.txt
  startCommand: python scripts/process_telegram_queue.py
```

### 4. Улучшенная обработка ошибок

Обновили функцию `send_telegram_message`, чтобы она использовала разные стратегии отправки сообщений и лучше обрабатывала сетевые ошибки:

```python
# Если domain-based подход не сработал, пробуем IP-based
if dns_failed:
    logger.info("Trying IP-based fallback for Telegram API...")
    try:
        from app.services.telegram_ip_service import send_via_ip_addresses
        return send_via_ip_addresses(message, max_retries=2)
    except Exception as e:
        logger.error(f"IP-based fallback also failed: {str(e)}")
        return False
```

## Как это работает

1. При отправке технического задания система сначала пытается отправить уведомление напрямую через обычный домен.
2. Если обычное подключение не работает (DNS-ошибки), система пытается использовать прямые IP-адреса.
3. Если и это не удается, сообщение сохраняется в очередь для последующей отправки.
4. Каждые 5 минут cron-задача обрабатывает очередь и пытается отправить сохраненные сообщения.

## Тестирование

Мы создали скрипт `test_telegram_direct.py`, который можно использовать для тестирования разных методов отправки сообщений.

## Необходимые шаги для внедрения

1. Проверить и зафиксировать изменения в кодовой базе
2. Задеплоить изменения на сервер Render.com
3. Создать необходимые директории на сервере:
   ```
   mkdir -p /opt/render/project/src/data/telegram_queue
   mkdir -p /opt/render/project/src/logs
   ```
4. Перезапустить сервис и убедиться, что cron-задача настроена корректно
