@echo off
echo Running Chat Message schema migrations...

set FLASK_APP=run.py
echo Setting FLASK_APP=%FLASK_APP%

echo Activating virtual environment...
call .venv\Scripts\activate

echo Running migrations script...
python -c "from app import create_app; from app.services.update_chat_schema import run_migrations; app = create_app(); with app.app_context(): success = run_migrations(); exit(0 if success else 1)"

if %ERRORLEVEL% EQU 0 (
    echo Migration completed successfully!
) else (
    echo Migration failed!
    exit /b 1
)

echo Done!
