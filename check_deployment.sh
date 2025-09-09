#!/bin/bash
# check_deployment.sh - Скрипт для проверки готовности развертывания

echo "=== ПРОВЕРКА ГОТОВНОСТИ РАЗВЕРТЫВАНИЯ ==="

# Проверяем наличие необходимых файлов
echo "Проверка наличия необходимых файлов..."

files=(
    "render.yaml"
    "render_start.sh"
    "direct_start.sh"
    "run.py"
    "gunicorn_config.py"
    "requirements.txt"
    "init_postgres_schemas.py"
    "init_migrations.py"
    "direct_db_init.py"
    "simple_create_tables.py"
)

missing_files=()
for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
        echo "❌ $file - НЕ НАЙДЕН"
    else
        echo "✅ $file - найден"
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo ""
    echo "❌ ОШИБКА: Следующие файлы отсутствуют:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

# Проверяем права на выполнение скриптов
echo ""
echo "Проверка прав на выполнение скриптов..."
scripts=(
    "render_start.sh"
    "direct_start.sh"
)

for script in "${scripts[@]}"; do
    if [ -x "$script" ]; then
        echo "✅ $script - исполняемый"
    else
        echo "⚠️  $script - не исполняемый, устанавливаем права..."
        chmod +x "$script"
        echo "✅ $script - права установлены"
    fi
done

# Проверяем переменные окружения
echo ""
echo "Проверка переменных окружения..."
required_vars=(
    "DATABASE_URL"
    "SECRET_KEY"
    "OPENAI_API_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -n "${!var}" ]; then
        echo "✅ $var - установлена"
    else
        echo "⚠️  $var - НЕ установлена (должна быть установлена в Render)"
    fi
done

echo ""
echo "=== ПРОВЕРКА ЗАВЕРШЕНА ==="
echo "Все необходимые файлы присутствуют и имеют правильные права."
echo "Переменные окружения будут установлены в Render dashboard."
