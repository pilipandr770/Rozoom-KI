"""
Модуль для логирования в приложении
"""
import logging
import os
from datetime import datetime

# Создаем логгер
logger = logging.getLogger('rozoom_ki')

# Устанавливаем уровень логирования
logger.setLevel(logging.INFO)

# Создаем форматтер для сообщений лога
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Создаем обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Создаем обработчик для файла, если указана директория логов
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file = os.path.join(logs_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Функция для получения логгера с определенным именем
def get_logger(name: str = 'rozoom_ki') -> logging.Logger:
    """
    Получить логгер с указанным именем

    Args:
        name: Имя логгера

    Returns:
        logging.Logger: Экземпляр логгера
    """
    return logging.getLogger(name)
