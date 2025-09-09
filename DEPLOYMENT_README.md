# Развертывание Rozoom-KI на Render.com

## 🚀 Быстрое развертывание

### 1. Подготовка к развертыванию

Убедитесь, что все файлы присутствуют:
```bash
# В Windows PowerShell:
.\check_deployment.sh
```

### 2. Развертывание через Render

1. **Создайте новый сервис** в Render dashboard
2. **Выберите метод развертывания**: "Connect Git repository"
3. **Подключите ваш GitHub репозиторий**
4. **Настройте переменные окружения** в Render dashboard:

#### Обязательные переменные:
```
DATABASE_URL=postgresql://... (автоматически создается Render)
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
STRIPE_TEST_PRICE_ID=your-stripe-price-id
CALENDAR_API_KEY=your-calendar-api-key
```

#### Опциональные переменные (уже настроены в render.yaml):
```
FLASK_APP=run.py
FLASK_ENV=production
ENVIRONMENT=production
PYTHON_VERSION=3.13
POSTGRES_SCHEMA=rozoom_ki_schema
POSTGRES_SCHEMA_CLIENTS=rozoom_ki_clients
POSTGRES_SCHEMA_SHOP=rozoom_ki_shop
POSTGRES_SCHEMA_PROJECTS=rozoom_ki_projects
OPENAI_MODEL=gpt-5-nano
OPENAI_MODEL_FALLBACK=gpt-4o-mini
USE_CHAT_COMPLETION=true
```

### 3. Настройка базы данных

1. **Создайте PostgreSQL базу данных** в Render
2. **Свяжите её с веб-сервисом** через переменную `DATABASE_URL`
3. **База данных будет автоматически инициализирована** при первом запуске

## 📋 Процесс запуска

Приложение использует **двойную систему запуска** для максимальной надежности:

### Основной путь (render_start.sh):
1. ✅ Инициализация PostgreSQL схем
2. ✅ Исправление проблем с `app/database.py`
3. ✅ Исправление дублирующихся столбцов
4. ✅ Исправление проблем с ревизией миграции
5. ✅ Инициализация миграций с поддержкой CASCADE
6. ✅ Инициализация таблиц базы данных
7. ✅ Запуск Gunicorn сервера

### Fallback путь (direct_start.sh):
Если основной путь не сработает, автоматически запускается альтернативный:
1. ✅ Инициализация PostgreSQL схем
2. ✅ Исправление проблем с базой данных
3. ✅ Прямая инициализация таблиц (без миграций)
4. ✅ Запуск Gunicorn сервера

## 🔧 Диагностика проблем

### Логи развертывания
Мониторьте логи в Render dashboard для диагностики:
- `✅` - успешные операции
- `⚠️` - предупреждения (не критичные)
- `❌` - ошибки (критичные)

### Распространенные проблемы:

#### 1. Ошибка миграций
```
ОШИБКА [flask_migrate] Ошибка: Не удается найти ревизию, идентифицированную как '31dcbe661935'
```
**Решение:** Система автоматически переключается на прямую инициализацию БД.

#### 2. Проблемы с PostgreSQL схемами
```
Ошибка при создании схем
```
**Решение:** Проверьте права доступа к базе данных.

#### 3. Ошибки импорта
```
ModuleNotFoundError
```
**Решение:** Убедитесь, что все зависимости установлены в `requirements.txt`.

## 📊 Мониторинг

### Health Check
Приложение имеет endpoint `/health` для проверки состояния.

### Переменные окружения для мониторинга:
- `ENVIRONMENT=production` - режим работы
- `FLASK_ENV=production` - Flask режим

## 🔄 Обновление приложения

1. **Внесите изменения** в код
2. **Зафиксируйте изменения** в Git
3. **Отправьте в репозиторий**: `git push`
4. **Render автоматически переразвернет** приложение

## 📞 Поддержка

Если возникнут проблемы:
1. Проверьте логи в Render dashboard
2. Убедитесь, что все переменные окружения установлены
3. Проверьте подключение к базе данных
4. Свяжитесь с разработчиком при необходимости

---

**Примечание:** Система развертывания разработана для максимальной надежности с множественными fallback'ами, поэтому большинство проблем решаются автоматически.
