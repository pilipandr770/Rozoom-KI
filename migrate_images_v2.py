#!/usr/bin/env python
"""
Скрипт для загрузки существующих изображений из временных URL OpenAI
и сохранения их локально
"""
import os
import sys
import logging
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
import time

# Add the app directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_generated_content_images():
    """Migrate images from generated_content table"""
    app = create_app()
    
    with app.app_context():
        try:
            from app.utils.image_utils import download_and_save_image
            
            # Get records with OpenAI image URLs
            query = sa.text("""
                SELECT id, image_url 
                FROM generated_content 
                WHERE image_url IS NOT NULL 
                  AND image_url LIKE 'https://%'
                  AND (original_image_url IS NULL OR original_image_url = '')
            """)
            
            result = db.session.execute(query)
            rows = result.fetchall()
            
            logger.info(f"Found {len(rows)} GeneratedContent records with OpenAI image URLs")
            
            success_count = 0
            for row in rows:
                content_id = row[0]
                image_url = row[1]
                
                logger.info(f"Processing content ID {content_id}")
                
                # Download and save image with entity ID for proper file naming
                success, local_path, error = download_and_save_image(
                    image_url=image_url,
                    entity_id=content_id,
                    entity_type='content',
                    delete_old=True
                )
                
                if success:
                    # Update the record with new local path and original URL
                    update_query = sa.text("""
                        UPDATE generated_content 
                        SET original_image_url = :orig_url, image_url = :local_path 
                        WHERE id = :id
                    """)
                    
                    db.session.execute(update_query, {
                        "orig_url": image_url, 
                        "local_path": local_path, 
                        "id": content_id
                    })
                    db.session.commit()
                    
                    success_count += 1
                    logger.info(f"Successfully updated image for content ID {content_id}")
                else:
                    logger.error(f"Failed to process image for content ID {content_id}: {error}")
            
            logger.info(f"Successfully migrated {success_count} out of {len(rows)} GeneratedContent images")
            return True
        
        except Exception as e:
            logger.error(f"Error during GeneratedContent migration: {str(e)}")
            return False

def migrate_blog_post_images():
    """Migrate images from blog_posts table"""
    app = create_app()
    
    with app.app_context():
        try:
            from app.utils.image_utils import download_and_save_image
            
            # Get records with OpenAI image URLs
            query = sa.text("""
                SELECT id, image_url 
                FROM blog_posts 
                WHERE image_url IS NOT NULL 
                  AND image_url LIKE 'https://%'
                  AND (original_image_url IS NULL OR original_image_url = '')
            """)
            
            result = db.session.execute(query)
            rows = result.fetchall()
            
            logger.info(f"Found {len(rows)} BlogPost records with OpenAI image URLs")
            
            success_count = 0
            for row in rows:
                post_id = row[0]
                image_url = row[1]
                
                logger.info(f"Processing post ID {post_id}")
                
                # Download and save image with entity ID for proper file naming
                success, local_path, error = download_and_save_image(
                    image_url=image_url,
                    entity_id=post_id,
                    entity_type='blog',
                    delete_old=True
                )
                
                if success:
                    # Update the record with new local path and original URL
                    update_query = sa.text("""
                        UPDATE blog_posts 
                        SET original_image_url = :orig_url, image_url = :local_path 
                        WHERE id = :id
                    """)
                    
                    db.session.execute(update_query, {
                        "orig_url": image_url, 
                        "local_path": local_path, 
                        "id": post_id
                    })
                    db.session.commit()
                    
                    success_count += 1
                    logger.info(f"Successfully updated image for post ID {post_id}")
                else:
                    logger.error(f"Failed to process image for post ID {post_id}: {error}")
            
            logger.info(f"Successfully migrated {success_count} out of {len(rows)} BlogPost images")
            return True
        
        except Exception as e:
            logger.error(f"Error during BlogPost migration: {str(e)}")
            return False

if __name__ == '__main__':
    print("Starting image migration...")
    
    gc_success = migrate_generated_content_images()
    bp_success = migrate_blog_post_images()
    
    if gc_success and bp_success:
        print("Image migration completed successfully!")
        sys.exit(0)
    else:
        print("Some errors occurred during migration. Check logs for details.")
        sys.exit(1)
