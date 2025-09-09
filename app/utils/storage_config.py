import os
import logging

logger = logging.getLogger(__name__)

# Настройки для хранения файлов
class StorageConfig:
    # Базовый путь для хранения изображений
    @staticmethod
    def get_image_storage_path():
        # Render.com предоставляет переменную окружения RENDER_PERSISTENT_DIR
        # для хранения файлов между перезагрузками контейнера
        if os.environ.get('RENDER_PERSISTENT_DIR'):
            storage_dir = os.path.join(os.environ.get('RENDER_PERSISTENT_DIR'), 'static', 'img')
            logger.info(f"Используем Render persistent storage: {storage_dir}")
            return storage_dir
        else:
            # Локальное хранение для разработки
            from flask import current_app
            if current_app:
                return os.path.join(current_app.static_folder, 'img')
            else:
                # Резервный вариант, если Flask контекст недоступен
                return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'img')
