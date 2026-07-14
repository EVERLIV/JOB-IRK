# Set Vercel environment variables for job-irk and job-irk-recruiter

param(
    [Parameter(Mandatory = $true)]
    [string]$ApiBaseUrl,
    [string]$SiteUrl = "https://job-irk.vercel.app",
    [string]$RecruiterUrl = "https://job-irk-recruiter.vercel.app",
    [string]$Scope = "kg-aerospace"
)

$ErrorActionPreference = "Stop"

function Set-VercelEnv {
    param([string]$Project, [string]$Name, [string]$Value, [string]$Env = "production")
    # Trim so Windows CRLF never gets stored inside the secret value
    $clean = $Value.Trim()
    Write-Host "  $Project : $Name = $clean"
    $clean | vercel env add $Name $Env --scope $Scope --force 2>&1 | Out-Null
}

Write-Host "Setting env for job-irk (site)..."
Set-VercelEnv -Project "job-irk" -Name "PUBLIC_API_BASE_URL" -Value $ApiBaseUrl
Set-VercelEnv -Project "job-irk" -Name "PUBLIC_SITE_URL" -Value $SiteUrl
Set-VercelEnv -Project "job-irk" -Name "PUBLIC_RECRUITER_URL" -Value $RecruiterUrl

Write-Host "Setting env for job-irk-recruiter..."
Set-VercelEnv -Project "job-irk-recruiter" -Name "PUBLIC_API_BASE_URL" -Value $ApiBaseUrl
Set-VercelEnv -Project "job-irk-recruiter" -Name "PUBLIC_SITE_URL" -Value $RecruiterUrl
Set-VercelEnv -Project "job-irk-recruiter" -Name "PUBLIC_JOBSEEKER_URL" -Value $SiteUrl

Write-Host ""
Write-Host "Redeploying..."
Push-Location (Join-Path (Join-Path $PSScriptRoot "..") "site") | Resolve-Path
vercel deploy --prod --scope $Scope --yes 2>&1
Pop-Location

Push-Location (Join-Path (Join-Path $PSScriptRoot "..") "recruiter") | Resolve-Path
vercel deploy --prod --scope $Scope --yes 2>&1
Pop-Location

Write-Host "Done. Test registration at $SiteUrl/register"
