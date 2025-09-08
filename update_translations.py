import os
import subprocess
from shutil import copy

# Путь к директории с переводами
translations_dir = os.path.join(os.getcwd(), 'app', 'translations')
de_messages_dir = os.path.join(translations_dir, 'de', 'LC_MESSAGES')

# 1. Создаем резервную копию текущего файла переводов
if os.path.exists(os.path.join(de_messages_dir, 'messages.po')):
    copy(
        os.path.join(de_messages_dir, 'messages.po'),
        os.path.join(de_messages_dir, 'messages.po.backup')
    )
    print("✅ Создана резервная копия текущего файла переводов")

# 2. Копируем полный файл переводов в основной
copy(
    os.path.join(de_messages_dir, 'messages.po.complete'),
    os.path.join(de_messages_dir, 'messages.po')
)
print("✅ Полный файл переводов скопирован в основной файл")

# 3. Компилируем файл переводов
try:
    subprocess.run(['pybabel', 'compile', '-d', 'app/translations'], check=True)
    print("✅ Файл переводов успешно скомпилирован")
except Exception as e:
    print(f"❌ Ошибка при компиляции файла переводов: {e}")

# 4. Проверяем наличие скомпилированного файла
if os.path.exists(os.path.join(de_messages_dir, 'messages.mo')):
    print("✅ Скомпилированный файл переводов (.mo) успешно создан")
else:
    print("❌ Скомпилированный файл переводов (.mo) не найден")

print("\nПереводы обновлены и готовы к использованию!")
