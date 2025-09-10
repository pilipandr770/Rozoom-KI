# Исправление ошибок отступов в контроллере

## Обнаруженная проблема

При развертывании приложения на сервере Render.com возникла критическая ошибка, блокирующая инициализацию базы данных и запуск приложения:

```
IndentationError: expected an indented block after 'except' statement on line 423
```

## Суть проблемы

В файле `controller.py` были обнаружены две синтаксические ошибки, связанные с отступами:

1. После блока `except` не было правильных отступов для вложенного кода
2. Весь блок кода имел неправильные отступы относительно родительского блока

## Выполненные исправления

1. Восстановлен правильный уровень отступов для кода после блока `except`
2. Удален лишний блок `try` без соответствующего `except`/`finally`
3. Унифицированы все отступы в коде, относящемся к обработке технических заданий
4. Исправлена общая структура вложенности в коде

### До исправления:

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
except Exception as e:
current_app.logger.error(f"Failed to send Telegram notification: {str(e)}")  # Ошибка отступов здесь
```

### После исправления:

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
except Exception as e:
    current_app.logger.error(f"Failed to send Telegram notification: {str(e)}")  # Исправленный отступ
```

## Влияние на систему

Эти ошибки блокировали запуск приложения и инициализацию базы данных. После исправления приложение должно успешно запускаться и функционировать.

## Рекомендации

1. Внедрить автоматическое форматирование кода с помощью инструментов типа `black` или `autopep8`
2. Добавить проверку синтаксиса в процесс CI/CD перед деплоем на сервер
3. Использовать линтеры кода в процессе разработки для выявления таких ошибок на ранних этапах
4. Обеспечить более тщательное тестирование перед деплоем на production-сервер
