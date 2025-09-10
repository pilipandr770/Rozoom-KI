# Fix Tech Spec Telegram Notifications

<#
.SYNOPSIS
    Applies a fix for tech spec Telegram notifications in Rozoom-KI application.

.DESCRIPTION
    This script makes the following changes:
    1. Creates a backup of the controller.py file
    2. Modifies the file to send tech spec notifications directly instead of queueing them
    3. Tests the Telegram notification system after the changes

.NOTES
    Author: GitHub Copilot
    Date: September 10, 2025
#>

# Get the script's directory
$scriptDir = $PSScriptRoot
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

# Get the project root directory (should be the parent of the script directory)
$projectRoot = Split-Path -Parent $scriptDir

# Define the path to the controller.py file
$controllerPath = Join-Path -Path $projectRoot -ChildPath "app\agents\controller.py"

# Check if the file exists
if (-not (Test-Path -Path $controllerPath)) {
    Write-Error "Error: Could not find controller.py at $controllerPath"
    exit 1
}

# 1. Create a backup of the file
$backupPath = "$controllerPath.bak"
Write-Host "Creating backup at $backupPath" -ForegroundColor Cyan
Copy-Item -Path $controllerPath -Destination $backupPath -Force

# 2. Apply the patch
Write-Host "Applying fix to $controllerPath..." -ForegroundColor Cyan
$content = Get-Content $controllerPath -Raw

$oldString = @"
                # Generate the message but queue it instead of sending directly
                message_content = send_tech_spec_notification(tech_spec_data, contact_info, return_message_only=True)
                queue_telegram_message(message_content)
                current_app.logger.info(f"Technical specification notification queued for {user_email}")
"@

$newString = @"
                # Send notification directly instead of queuing
                send_tech_spec_notification(tech_spec_data, contact_info)
                current_app.logger.info(f"Technical specification notification SENT for {user_email}")
"@

$content = $content -replace [regex]::Escape($oldString), [System.Text.RegularExpressions.Regex]::Escape($newString).Replace("\r\n", "`r`n").Replace("\\", "\")
Set-Content -Path $controllerPath -Value $content -Encoding UTF8

Write-Host "Fix applied successfully!" -ForegroundColor Green

# 3. Offer to run the test script
Write-Host "`nWould you like to test the Telegram notification system now? (Y/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    $testScript = Join-Path -Path $projectRoot -ChildPath "scripts\test_telegram.py"
    
    # Check if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set
    if (-not $env:TELEGRAM_BOT_TOKEN -or -not $env:TELEGRAM_CHAT_ID) {
        Write-Host "`nTELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables are not set." -ForegroundColor Red
        Write-Host "Would you like to set them now? (Y/N)" -ForegroundColor Yellow
        $setVars = Read-Host
        
        if ($setVars -eq "Y" -or $setVars -eq "y") {
            $env:TELEGRAM_BOT_TOKEN = Read-Host "Enter your Telegram Bot Token"
            $env:TELEGRAM_CHAT_ID = Read-Host "Enter your Telegram Chat ID"
        }
    }
    
    # Run the test script
    Write-Host "`nRunning Telegram test script..." -ForegroundColor Cyan
    python $testScript
}

Write-Host "`nDone. Documentation of this fix is available in docs\TELEGRAM_NOTIFICATION_FIX.md" -ForegroundColor Green
