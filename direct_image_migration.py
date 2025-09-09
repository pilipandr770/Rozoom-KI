#!/usr/bin/env python
"""
Script to add original_image_url column to tables and migrate images
"""
import os
import sys
import logging
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
import requests
import uuid
from pathlib import Path
import time

# Add the app directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_save_image(image_url, app):
    """
    Downloads an image from a URL and saves it to the static/img directory
    
    Args:
        image_url: The URL of the image to download
        app: Flask application context
        
    Returns:
        Tuple: (success, local_path, error_message)
    """
    if not image_url:
        return False, None, "No image URL provided"
    
    try:
        # Generate a unique filename with UUID to avoid collisions
        filename = f"{uuid.uuid4().hex}.png"
        
        # Ensure the subdirectory exists within static/img
        img_dir = Path(app.static_folder) / 'img' / 'blog'
        os.makedirs(img_dir, exist_ok=True)
        
        # Full path where the image will be saved
        file_path = img_dir / filename
        
        # Download the image with timeout
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Save the image to file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        # Return the relative path to be used in templates/database
        relative_path = f'/static/img/blog/{filename}'
        
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

def add_column_if_not_exists(table_name, column_name, column_type):
    """Add a column to a table if it doesn't already exist"""
    connection = None
    try:
        # Use a fresh connection with autocommit
        engine = db.engine.execution_options(isolation_level="AUTOCOMMIT")
        connection = engine.connect()
        
        # Check if column exists
        try:
            connection.execute(sa.text(f"SELECT {column_name} FROM {table_name} LIMIT 0"))
            logger.info(f"Column '{column_name}' already exists in table '{table_name}'")
            return True
        except Exception:
            # Column doesn't exist, add it
            connection.execute(sa.text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
            logger.info(f"Added '{column_name}' column to '{table_name}' table")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return False
    finally:
        if connection:
            connection.close()

def migrate_generated_content_images(app):
    """Migrate images from generated_content table"""
    connection = None
    try:
        # Use a fresh connection with autocommit
        engine = db.engine.execution_options(isolation_level="AUTOCOMMIT")
        connection = engine.connect()
        
        # Get all records with image URLs
        result = connection.execute(sa.text(
            "SELECT id, image_url FROM generated_content WHERE image_url IS NOT NULL AND image_url LIKE 'https://%'"
        ))
        
        rows = result.fetchall()
        logger.info(f"Found {len(rows)} GeneratedContent records with OpenAI image URLs")
        
        success_count = 0
        for row in rows:
            content_id = row[0]
            image_url = row[1]
            
            # Download and save the image
            success, local_path, error = download_and_save_image(image_url, app)
            
            if success:
                # Update the database record
                connection.execute(sa.text(
                    "UPDATE generated_content SET original_image_url = :orig_url, image_url = :local_path WHERE id = :id"
                ), {"orig_url": image_url, "local_path": local_path, "id": content_id})
                
                success_count += 1
                logger.info(f"Updated image for content ID {content_id}")
            else:
                logger.error(f"Failed to update image for content ID {content_id}: {error}")
        
        logger.info(f"Successfully migrated {success_count} out of {len(rows)} GeneratedContent images")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database error during GeneratedContent migration: {str(e)}")
        return False
    finally:
        if connection:
            connection.close()

def migrate_blog_post_images(app):
    """Migrate images from blog_posts table"""
    connection = None
    try:
        # Use a fresh connection with autocommit
        engine = db.engine.execution_options(isolation_level="AUTOCOMMIT")
        connection = engine.connect()
        
        # Get all records with image URLs
        result = connection.execute(sa.text(
            "SELECT id, image_url FROM blog_posts WHERE image_url IS NOT NULL AND image_url LIKE 'https://%'"
        ))
        
        rows = result.fetchall()
        logger.info(f"Found {len(rows)} BlogPost records with OpenAI image URLs")
        
        success_count = 0
        for row in rows:
            post_id = row[0]
            image_url = row[1]
            
            # Download and save the image
            success, local_path, error = download_and_save_image(image_url, app)
            
            if success:
                # Update the database record
                connection.execute(sa.text(
                    "UPDATE blog_posts SET original_image_url = :orig_url, image_url = :local_path WHERE id = :id"
                ), {"orig_url": image_url, "local_path": local_path, "id": post_id})
                
                success_count += 1
                logger.info(f"Updated image for post ID {post_id}")
            else:
                logger.error(f"Failed to update image for post ID {post_id}: {error}")
        
        logger.info(f"Successfully migrated {success_count} out of {len(rows)} BlogPost images")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database error during BlogPost migration: {str(e)}")
        return False
    finally:
        if connection:
            connection.close()

def main():
    """Main function to run the migration"""
    try:
        print("Starting database schema update and image migration...")
        
        app = create_app()
        with app.app_context():
            # Add columns if they don't exist
            if not add_column_if_not_exists('generated_content', 'original_image_url', 'VARCHAR(500)'):
                return 1
                
            if not add_column_if_not_exists('blog_posts', 'original_image_url', 'VARCHAR(500)'):
                return 1
            
            # Allow some time for database changes to propagate
            time.sleep(1)
            
            # Migrate images
            gc_success = migrate_generated_content_images(app)
            bp_success = migrate_blog_post_images(app)
            
            if gc_success and bp_success:
                print("Image migration completed successfully!")
                return 0
            else:
                print("Migration did not complete successfully. Please check the logs.")
                return 1
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
