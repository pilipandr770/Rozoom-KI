#!/bin/bash
echo "Running database migrations..."
python -m flask db upgrade
if [ $? -ne 0 ]; then
    echo "Failed to run database migrations. Exiting..."
    exit 1
fi

echo ""
echo "Running image migration script..."
python migrate_images.py
if [ $? -ne 0 ]; then
    echo "Image migration failed. See error messages above."
    exit 1
fi

echo ""
echo "All migrations completed successfully!"
