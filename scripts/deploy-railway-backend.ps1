# Deploy Django API to Railway with Neon PostgreSQL
# Prerequisites: npx @railway/cli, railway login, DATABASE_URL in env or passed below

param(
    [string]$DatabaseUrl = $env:DATABASE_URL,
    [string]$SecretKey = $env:SECRET_KEY,
    [string]$SiteUrl = "https://job-irk.vercel.app",
    [string]$RecruiterUrl = "https://job-irk-recruiter.vercel.app"
)

$ErrorActionPreference = "Stop"
$backendRoot = (Join-Path (Join-Path $PSScriptRoot "..") "backend") | Resolve-Path

if (-not $DatabaseUrl) {
    Write-Error "Set DATABASE_URL env var or pass -DatabaseUrl"
}

if (-not $SecretKey) {
    $SecretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 48 | ForEach-Object { [char]$_ })
    Write-Host "Generated SECRET_KEY (save it): $SecretKey"
}

Write-Host "Checking Railway login..."
if ($env:RAILWAY_TOKEN) {
    Write-Host "Using RAILWAY_TOKEN from environment"
} else {
    npx --yes @railway/cli@4.5.4 whoami
}

Push-Location $backendRoot
try {
    if (-not (Test-Path ".railway")) {
        Write-Host "Initializing Railway project..."
        npx @railway/cli@4.5.4 init --name job-irk-api
    }

    Write-Host "Setting environment variables..."
    npx @railway/cli@4.5.4 variables `
        --set "DJANGO_SETTINGS_MODULE=jobsp.settings_staging" `
        --set "DEBUG=false" `
        --set "SECRET_KEY=$SecretKey" `
        --set "DATABASE_URL=$DatabaseUrl" `
        --set "AUTO_VERIFY_EMAIL=true" `
        --set "AUTH_COOKIE_SECURE=true" `
        --set "AUTH_COOKIE_SAMESITE=Lax" `
        --set "SITE_FRONTEND_URL=$SiteUrl" `
        --set "RECRUITER_FRONTEND_URL=$RecruiterUrl" `
        --set "DEFAULT_FROM_EMAIL=Truddy <noreply@truddy.ru>" `
        --set "ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,api-production-e35c.up.railway.app"

    Write-Host "Deploying backend..."
    npx @railway/cli@4.5.4 up --detach

    Write-Host "Fetching service URL..."
    $domain = npx @railway/cli@4.5.4 domain 2>&1 | Select-Object -Last 1
    if ($domain -match '\.railway\.app') {
        $apiUrl = "https://$domain/api/v1"
        npx @railway/cli@4.5.4 variables --set "PEEL_URL=https://$domain/"
        Write-Host ""
        Write-Host "API deployed: https://$domain"
        Write-Host "Set on Vercel: PUBLIC_API_BASE_URL=$apiUrl"
        Write-Host "Run: powershell -File scripts/set-vercel-env.ps1 -ApiBaseUrl $apiUrl"
    }
}
finally {
    Pop-Location
}
