# Run database migrations and image migration
Write-Host "Running database migrations..." -ForegroundColor Cyan
python -m flask db upgrade
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to run database migrations. Exiting..." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`nRunning image migration script..." -ForegroundColor Cyan
python migrate_images.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Image migration failed. See error messages above." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`nAll migrations completed successfully!" -ForegroundColor Green
