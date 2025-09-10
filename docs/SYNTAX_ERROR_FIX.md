# Критическая ошибка: SyntaxError в controller.py

## Обнаруженная проблема

На сервере Render.com при запуске приложения возникала синтаксическая ошибка:

```
File "/opt/render/project/src/app/agents/controller.py", line 423
    except Exception as e:
SyntaxError: expected 'except' or 'finally' block
```

## Причина ошибки

В файле `controller.py` был неправильно отформатирован блок try-except. Проблема заключалась в некорректном отступе для блока `except`. Это вызывало ошибку синтаксиса при запуске приложения.

### Некорректный код (до исправления)

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
except Exception as e:  # <- Неправильный отступ! Ожидается на том же уровне что и `try`
```

### Исправленный код

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
except Exception as e:  # <- Исправленный отступ
```

## Как было исправлено

Отступ для блока `except` был выровнен с соответствующим блоком `try`. Это исправление синтаксической ошибки позволит приложению успешно запускаться и функционировать.

## Влияние на систему

Эта ошибка блокировала запуск всего приложения, включая инициализацию базы данных и все остальные компоненты. После исправления приложение должно запускаться нормально.

## Рекомендации

1. После внесения изменений в код перед деплоем рекомендуется проверять его на синтаксические ошибки с помощью линтеров
2. Добавить автоматический синтаксический контроль в процесс CI/CD
3. Рассмотреть возможность автоматического форматирования кода с помощью инструментов типа `black` или `autopep8`
