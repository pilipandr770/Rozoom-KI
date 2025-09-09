"""
Утилиты для управления файловой системой
"""
import os
import datetime
from pathlib import Path
import re
import humanize

def get_images_info(static_folder, subdirectory='blog'):
    """
    Получает информацию о всех изображениях в указанной директории
    
    Args:
        static_folder (str): Путь к папке static
        subdirectory (str): Поддиректория внутри img/
        
    Returns:
        dict: Информация об изображениях
    """
    img_dir = Path(static_folder) / 'img' / subdirectory
    
    if not img_dir.exists():
        return {
            'count': 0,
            'files': []
        }
    
    files = []
    
    # Паттерн для извлечения информации о сущности из имени файла
    entity_pattern = re.compile(r'(content|blog)_(\d+)_')
    
    for file_path in img_dir.glob('*.png'):
        # Базовая информация о файле
        stats = file_path.stat()
        size_bytes = stats.st_size
        modified_date = datetime.datetime.fromtimestamp(stats.st_mtime)
        
        # Преобразуем размер в человеко-читаемый формат
        size_human = humanize.naturalsize(size_bytes)
        
        # Получаем относительный путь для шаблона
        relative_path = f'/static/img/{subdirectory}/{file_path.name}'
        
        # Проверяем, есть ли информация о сущности в имени файла
        entity_info = None
        entity_match = entity_pattern.match(file_path.name)
        if entity_match:
            entity_type, entity_id = entity_match.groups()
            entity_info = f"Тип: {entity_type}, ID: {entity_id}"
        
        file_info = {
            'name': file_path.name,
            'path': relative_path,
            'size': size_human,
            'date': modified_date.strftime('%Y-%m-%d %H:%M:%S'),
            'entity_info': entity_info
        }
        
        files.append(file_info)
    
    # Сортировка файлов по дате изменения (сначала новые)
    files.sort(key=lambda x: x['date'], reverse=True)
    
    return {
        'count': len(files),
        'files': files,
        'directory': str(img_dir)
    }
