"""
Скрипт для очистки существующего контента блога от иконок Font Awesome
"""

import sys
import os
import logging
from datetime import datetime

# Добавляем родительскую директорию в путь, чтобы импортировать app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import BlogPost
from app.utils.text import clean_icons_from_content

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def clean_all_blog_posts():
    """
    Очищает все посты блога от иконок Font Awesome
    """
    app = create_app()
    with app.app_context():
        try:
            # Получаем все посты блога
            posts = BlogPost.query.all()
            logger.info(f"Found {len(posts)} blog posts to clean")
            
            cleaned_count = 0
            for post in posts:
                original_content = post.content
                cleaned_content = clean_icons_from_content(original_content)
                
                if original_content != cleaned_content:
                    post.content = cleaned_content
                    cleaned_count += 1
                    logger.info(f"Cleaned post ID {post.id}: {post.title}")
            
            if cleaned_count > 0:
                db.session.commit()
                logger.info(f"Successfully cleaned {cleaned_count} blog posts")
            else:
                logger.info("No blog posts needed cleaning")
                
        except Exception as e:
            logger.error(f"Error cleaning blog posts: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    clean_all_blog_posts()
