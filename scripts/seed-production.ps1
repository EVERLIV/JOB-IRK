# Seed Neon / production database with Truddy regional catalog + demo jobs.
# Geography: Irkutsk oblast + Buryatia / Zabaykalye / Krasnoyarsk neighbor cities.
# Skills: ordinary work skills (sales, drivers, trade, construction) — not IT stack.
#
# Usage:
#   $env:DATABASE_URL = "postgresql://...@...neon.tech/neondb?sslmode=require"
#   powershell -File scripts/seed-production.ps1

param(
    [string]$DatabaseUrl = $env:DATABASE_URL,
    [string]$SecretKey = $(if ($env:SECRET_KEY) { $env:SECRET_KEY } else { "seed-only-temp-key" }),
    [switch]$SkipUsers
)

$ErrorActionPreference = "Stop"
$backendRoot = (Join-Path (Join-Path $PSScriptRoot "..") "backend") | Resolve-Path
$python = Join-Path $backendRoot ".venv\Scripts\python.exe"

if (-not $DatabaseUrl) {
    Write-Error "Set DATABASE_URL (Neon connection string) or pass -DatabaseUrl"
}

if (-not (Test-Path $python)) {
    Write-Error "Python venv not found at $python"
}

$env:PYTHONIOENCODING = "utf-8"
$env:DJANGO_SETTINGS_MODULE = "jobsp.settings_staging"
$env:DATABASE_URL = $DatabaseUrl
$env:SECRET_KEY = $SecretKey

Push-Location $backendRoot
try {
    Write-Host "==> migrate"
    & $python manage.py migrate --noinput

    Write-Host "==> reload_truddy_catalog"
    if ($SkipUsers) {
        & $python manage.py reload_truddy_catalog --skip-users
    } else {
        & $python manage.py reload_truddy_catalog
        # Keep demo passwords stable after recreate
        & $python -c @"
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jobsp.settings_staging')
django.setup()
from peeldb.models import User
for email in ['admin@jobirk.local','hr@baikaltech.local','recruiter@baikaltech.local','consult@sibirhire.local','seeker@example.local']:
    u = User.objects.filter(email=email).first()
    if u:
        u.set_password('123456')
        u.save()
        print('password ok', email)
"@
    }

    Write-Host ""
    Write-Host "Demo logins: */123456 (admin@jobirk.local, hr@baikaltech.local, recruiter@..., seeker@example.local)"
}
finally {
    Pop-Location
}
