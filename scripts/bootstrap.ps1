# path: scripts/bootstrap.ps1
# Використання:  .\scripts\bootstrap.ps1
python -m venv .venv
.\.venv\Scripts\pip install --upgrade pip
Write-Host "Venv готовий. Далі: створити Flask-скелет у Task 01 (див. /agent/TASKS.md)."
