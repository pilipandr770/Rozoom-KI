@echo off
echo Running database migrations...
python -m flask db upgrade
if %ERRORLEVEL% NEQ 0 (
    echo Failed to run database migrations. Exiting...
    exit /b %ERRORLEVEL%
)

echo.
echo Running image migration script...
python migrate_images.py
if %ERRORLEVEL% NEQ 0 (
    echo Image migration failed. See error messages above.
    exit /b %ERRORLEVEL%
)

echo.
echo All migrations completed successfully!
