# OpenAI Image Persistence Update

## Overview

This update addresses the issue of disappearing OpenAI-generated images by implementing a system to download and persistently store images locally.

## Changes Made

1. **New Utility Function (`app/utils/image_utils.py`)**
   - Added `download_and_save_image()` function that downloads images from URLs and saves them to the local filesystem
   - Images are stored in the `app/static/img/blog` directory with unique UUIDs as filenames

2. **Updated OpenAI Service**
   - Modified `generate_image()` to download and save images locally instead of just returning the temporary OpenAI URL
   - Added proper error handling and logging

3. **Database Schema Updates**
   - Added `original_image_url` column to `GeneratedContent` and `BlogPost` models to keep a reference to the original OpenAI URL
   - Updated models to use the local image path instead of temporary OpenAI URL

4. **Content Scheduler Updates**
   - Updated the content scheduler to store both the local path and original URL

5. **Data Migration Script**
   - Created `migrate_images.py` to download existing OpenAI images and update database records

## How to Run the Migration

To migrate existing OpenAI image URLs to local storage, run:

```
python migrate_images.py
```

This will:
1. Find all existing content with OpenAI image URLs
2. Download the images (if they haven't expired)
3. Save them to `app/static/img/blog`
4. Update the database records to point to the local files

## Technical Details

- Images are saved with universally unique identifiers (UUIDs) to prevent filename collisions
- The original OpenAI URLs are preserved in the `original_image_url` column for reference
- The system gracefully handles download failures with proper error messages
- Image paths in the database are stored as relative paths (`/static/img/blog/[filename]`)

## Note About Existing Images

If OpenAI image URLs have already expired (typically after 1 hour), the migration script won't be able to download them. In this case, those content items may need to have new images generated.
