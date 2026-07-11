# Run Django unit tests on Windows (UTF-8 + reuse test DB)
param(
    [string[]]$Target = @('api')
)

$ErrorActionPreference = 'Stop'
$backendRoot = Split-Path $PSScriptRoot -Parent
Set-Location $backendRoot

$env:PYTHONIOENCODING = 'utf-8'

$python = Join-Path $backendRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Error "Create venv first: python -m venv .venv && .venv\Scripts\pip install -r requirements.txt -r dev-requirements.txt"
}

& $python manage.py test @Target --keepdb --verbosity=1
