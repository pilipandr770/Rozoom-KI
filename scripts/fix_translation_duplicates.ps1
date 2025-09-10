# Fix German Translation Duplicates
<#
.SYNOPSIS
    This script fixes duplicate message definitions in the German translation file for Rozoom-KI.
    
.DESCRIPTION
    The script performs the following tasks:
    1. Creates a backup of the current German translation file
    2. Identifies and removes duplicate message entries
    3. Saves a clean version of the file
    4. Compiles the translations using pybabel
    
.NOTES
    Author: GitHub Copilot
    Date: September 10, 2025
#>

# Force Unicode output
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🔍 Starting German translation file cleanup..." -ForegroundColor Cyan

# Get the script directory
$scriptDir = $PSScriptRoot
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

# Navigate to the translations directory
$projectRoot = Split-Path -Parent $scriptDir
$translationsDir = Join-Path -Path $projectRoot -ChildPath "app\translations"
$dePoPath = Join-Path -Path $translationsDir -ChildPath "de\LC_MESSAGES\messages.po"

# Check if the file exists
if (-not (Test-Path -Path $dePoPath)) {
    Write-Error "Error: Could not find German translation file at $dePoPath"
    exit 1
}

# Create a backup of the file
$backupPath = "$dePoPath.bak"
Copy-Item -Path $dePoPath -Destination $backupPath -Force
Write-Host "✅ Created backup at $backupPath" -ForegroundColor Green

# Read the file content
$content = Get-Content -Path $dePoPath -Raw -Encoding UTF8

# Create a hashtable to track unique messages
$uniqueMessages = @{}
$duplicateCount = 0
$totalCount = 0

# Split the file into lines
$lines = $content -split "`n"

# Create a new content array
$newContent = @()
$currentMsgid = ""
$currentEntry = @()
$inHeader = $true

# Process the file line by line
foreach ($line in $lines) {
    # Check if we're still in the header
    if ($inHeader) {
        $newContent += $line
        if ($line -match '^msgid ".+') {
            $inHeader = $false
            
            # Start processing this first non-header entry
            $currentMsgid = $line
            $currentEntry = @($line)
        }
        continue
    }
    
    # Start of a new message entry
    if ($line -match '^msgid ".+') {
        # If we have a previous entry, process it
        if ($currentEntry.Count -gt 0) {
            $totalCount++
            
            # If this message ID is already seen, skip it (it's a duplicate)
            if ($uniqueMessages.ContainsKey($currentMsgid)) {
                $duplicateCount++
            }
            else {
                # Otherwise add it to our tracking and output
                $uniqueMessages[$currentMsgid] = $true
                $newContent += $currentEntry
                $newContent += "" # Empty line between entries
            }
        }
        
        # Start a new entry
        $currentMsgid = $line
        $currentEntry = @($line)
    }
    else {
        # Continue with the current entry
        $currentEntry += $line
    }
}

# Process the last entry
if ($currentEntry.Count -gt 0) {
    $totalCount++
    if (-not $uniqueMessages.ContainsKey($currentMsgid)) {
        $uniqueMessages[$currentMsgid] = $true
        $newContent += $currentEntry
    }
    else {
        $duplicateCount++
    }
}

# Write the new content back to the file
$newContent -join "`n" | Out-File -FilePath $dePoPath -Encoding utf8

# Summary
Write-Host "✅ Removed $duplicateCount duplicate entries" -ForegroundColor Green
Write-Host "✅ Original entries: $totalCount" -ForegroundColor Green
Write-Host "✅ Cleaned entries: $($uniqueMessages.Count)" -ForegroundColor Green

# Check if pybabel is available
$hasPybabel = $null
try {
    $hasPybabel = Get-Command "pybabel" -ErrorAction SilentlyContinue
}
catch {
    $hasPybabel = $null
}

# Compile translations if pybabel is available
if ($hasPybabel) {
    Write-Host "`n🔄 Compiling translations..." -ForegroundColor Cyan
    $currentLocation = Get-Location
    Set-Location -Path $translationsDir
    
    try {
        pybabel compile -d .
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Translations successfully compiled" -ForegroundColor Green
        }
        else {
            Write-Host "❌ Failed to compile translations (Exit code: $LASTEXITCODE)" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ Error compiling translations: $_" -ForegroundColor Red
    }
    finally {
        Set-Location -Path $currentLocation
    }
}
else {
    Write-Host "`nℹ️ pybabel not found. To compile translations manually, run:" -ForegroundColor Yellow
    Write-Host "cd $translationsDir && pybabel compile -d ." -ForegroundColor Yellow
}

Write-Host "`n✨ Translation cleanup complete! ✨" -ForegroundColor Cyan
