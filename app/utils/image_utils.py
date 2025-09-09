import os
import uuid
import requests
import glob
from pathlib import Path
from typing import Optional, Tuple
from flask import current_app
import logging

# Импортируем конфигурацию для хранения файлов
from app.utils.storage_config import StorageConfig

logger = logging.getLogger(__name__)

def download_and_save_image(image_url: str, entity_id: int = None, 
                           entity_type: str = 'blog', subdirectory: str = 'blog',
                           delete_old: bool = True) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Downloads an image from a URL, saves it to the static/img directory, and optionally deletes old images
    
    Args:
        image_url (str): The URL of the image to download
        entity_id (int): Optional ID of the entity (post, content) the image belongs to
        entity_type (str): Type of entity (blog, content)
        subdirectory (str): Subdirectory within static/img to save the image (default: 'blog')
        delete_old (bool): Whether to delete old images for this entity
        
    Returns:
        Tuple[bool, Optional[str], Optional[str]]: 
            - Success status
            - Local path to saved image or None if failed
            - Error message if failed, None if successful
    """
    if not image_url:
        return False, None, "No image URL provided"
    
    try:
        # Получаем базовый путь для хранения изображений из конфигурации
        base_storage_path = StorageConfig.get_image_storage_path()
        
        # Ensure the subdirectory exists within the storage path
        img_dir = Path(base_storage_path) / subdirectory
        os.makedirs(img_dir, exist_ok=True)
        
        # If entity_id is provided and delete_old is True, delete old images for this entity
        if entity_id is not None and delete_old:
            # Pattern for this entity's images, e.g., blog_5_*.png
            old_pattern = f"{entity_type}_{entity_id}_*.png"
            old_files = glob.glob(str(img_dir / old_pattern))
            
            # Delete old files
            for old_file in old_files:
                try:
                    os.remove(old_file)
                    logger.info(f"Deleted old image: {old_file}")
                except Exception as e:
                    logger.warning(f"Failed to delete old image {old_file}: {str(e)}")
        
        # Generate a unique filename with entity info if available
        if entity_id is not None:
            filename = f"{entity_type}_{entity_id}_{uuid.uuid4().hex[:8]}.png"
        else:
            filename = f"{uuid.uuid4().hex}.png"
        
        # Full path where the image will be saved
        file_path = img_dir / filename
        
        # Download the image with timeout
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Save the image to file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        # Return the relative path to be used in templates/database
        relative_path = f'/static/img/{subdirectory}/{filename}'
        
        logger.info(f"Image successfully downloaded and saved to {relative_path}")
        return True, relative_path, None
        
    except requests.RequestException as e:
        error_msg = f"Failed to download image: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg
    except Exception as e:
        error_msg = f"Error saving image: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg
