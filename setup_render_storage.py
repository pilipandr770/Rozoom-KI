import os
import sys
import logging
from pathlib import Path
import shutil
import glob

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def ensure_render_storage():
    """
    Ensure that Render persistent storage is properly set up
    and copy existing images to it if needed.
    """
    render_dir = os.environ.get('RENDER_PERSISTENT_DIR')
    
    if not render_dir:
        logger.warning("RENDER_PERSISTENT_DIR environment variable is not set. Skipping storage migration.")
        return
    
    # Create necessary directories
    render_img_dir = os.path.join(render_dir, 'static', 'img', 'blog')
    os.makedirs(render_img_dir, exist_ok=True)
    logger.info(f"Created Render persistent storage directory: {render_img_dir}")
    
    # Check if we need to migrate images from app/static to persistent storage
    static_img_dir = os.path.join('app', 'static', 'img', 'blog')
    if os.path.exists(static_img_dir):
        # Count images in both locations
        static_images = glob.glob(os.path.join(static_img_dir, '*.png')) + \
                       glob.glob(os.path.join(static_img_dir, '*.jpg'))
        render_images = glob.glob(os.path.join(render_img_dir, '*.png')) + \
                       glob.glob(os.path.join(render_img_dir, '*.jpg'))
        
        logger.info(f"Found {len(static_images)} images in static directory")
        logger.info(f"Found {len(render_images)} images in Render persistent directory")
        
        # Only migrate if we have images in static that aren't in persistent storage
        if len(static_images) > len(render_images):
            logger.info("Starting image migration to persistent storage...")
            
            # Copy each image file
            migrated = 0
            for img_path in static_images:
                img_filename = os.path.basename(img_path)
                dest_path = os.path.join(render_img_dir, img_filename)
                
                # Skip if file already exists in destination
                if os.path.exists(dest_path):
                    continue
                
                try:
                    shutil.copy2(img_path, dest_path)
                    logger.info(f"Copied: {img_filename}")
                    migrated += 1
                except Exception as e:
                    logger.error(f"Error copying {img_filename}: {str(e)}")
            
            logger.info(f"Migration complete: {migrated} images moved to persistent storage")
        else:
            logger.info("No new images to migrate to persistent storage")
    else:
        logger.info(f"No static images directory found at {static_img_dir}")

if __name__ == "__main__":
    logger.info("Starting Render storage initialization...")
    ensure_render_storage()
    logger.info("Storage initialization completed")
