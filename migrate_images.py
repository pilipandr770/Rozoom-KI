#!/usr/bin/env python
"""
Script to migrate existing OpenAI image URLs to local storage.
This downloads images from temporary OpenAI URLs and saves them locally,
updating the database records to point to the local files.
"""
import os
import sys
from pathlib import Path
import logging
import sqlalchemy as sa

# Add the app directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.content_generation import GeneratedContent
from app.models.blog import BlogPost
from app.utils.image_utils import download_and_save_image

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_column_exists(table_name, column_name):
    """Check if column exists in the database table"""
    try:
        with db.engine.connect() as connection:
            # Try to select the column - if it doesn't exist, this will raise an exception
            connection.execute(sa.text(f"SELECT {column_name} FROM {table_name} LIMIT 0"))
            return True
    except Exception:
        return False

def migrate_generated_content_images():
    """Migrate images from GeneratedContent model"""
    app = create_app()
    
    with app.app_context():
        # Check if original_image_url column exists
        if not check_column_exists('generated_content', 'original_image_url'):
            logger.error("Column 'original_image_url' does not exist in 'generated_content' table. Run migrations first.")
            return False
            
        # Get all generated content records with image URLs
        contents = GeneratedContent.query.filter(
            GeneratedContent.image_url.isnot(None),
            GeneratedContent.image_url.like('https://%')  # Only process OpenAI URLs
        ).all()
        
        logger.info(f"Found {len(contents)} GeneratedContent records with OpenAI image URLs")
        
        for content in contents:
            original_url = content.image_url
            
            # Skip if already processed (has original_image_url)
            if hasattr(content, 'original_image_url') and content.original_image_url:
                logger.info(f"Skipping already processed content ID {content.id}")
                continue
                
            # Download and save the image
            success, local_path, error = download_and_save_image(original_url)
            
            if success:
                # Update the record
                content.original_image_url = original_url  # Save original URL for reference
                content.image_url = local_path  # Update to local path
                logger.info(f"Successfully migrated image for content ID {content.id}")
            else:
                logger.error(f"Failed to migrate image for content ID {content.id}: {error}")
        
        # Save changes to database
        db.session.commit()
        logger.info("Generated content migration completed")

def migrate_blog_post_images():
    """Migrate images from BlogPost model"""
    app = create_app()
    
    with app.app_context():
        # Check if original_image_url column exists
        if not check_column_exists('blog_posts', 'original_image_url'):
            logger.error("Column 'original_image_url' does not exist in 'blog_posts' table. Run migrations first.")
            return False
            
        # Get all blog posts with image URLs
        posts = BlogPost.query.filter(
            BlogPost.image_url.isnot(None),
            BlogPost.image_url.like('https://%')  # Only process OpenAI URLs
        ).all()
        
        logger.info(f"Found {len(posts)} BlogPost records with OpenAI image URLs")
        
        for post in posts:
            original_url = post.image_url
            
            # Skip if already processed (has original_image_url)
            if hasattr(post, 'original_image_url') and post.original_image_url:
                logger.info(f"Skipping already processed post ID {post.id}")
                continue
                
            # Download and save the image
            success, local_path, error = download_and_save_image(original_url)
            
            if success:
                # Update the record
                post.original_image_url = original_url  # Save original URL for reference
                post.image_url = local_path  # Update to local path
                logger.info(f"Successfully migrated image for post ID {post.id}")
            else:
                logger.error(f"Failed to migrate image for post ID {post.id}: {error}")
        
        # Save changes to database
        db.session.commit()
        logger.info("Blog post migration completed")

if __name__ == '__main__':
    print("Starting image migration process...")
    
    try:
        # Check if migrations need to be run first
        app = create_app()
        with app.app_context():
            gc_column_exists = check_column_exists('generated_content', 'original_image_url')
            bp_column_exists = check_column_exists('blog_posts', 'original_image_url')
            
            if not gc_column_exists or not bp_column_exists:
                print("ERROR: Database schema is not up to date.")
                print("Please run the following commands first:")
                print("flask db upgrade")
                sys.exit(1)
        
        # If columns exist, proceed with migration
        success_gc = migrate_generated_content_images()
        success_bp = migrate_blog_post_images()
        
        if success_gc is False or success_bp is False:
            print("Migration did not complete successfully. Please check the logs.")
            sys.exit(1)
        else:
            print("Image migration completed successfully!")
            
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        sys.exit(1)
