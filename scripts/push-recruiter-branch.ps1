# Sync recruiter/ from master into the deploy-only `recruiter` git branch.
# Vercel project job-irk-recruiter deploys from that branch.

$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

$current = git branch --show-current
if ($current -ne 'master') {
    git checkout master
}

git subtree split --prefix=recruiter -b recruiter
git push everliv recruiter --force

if ($current -ne 'master') {
    git checkout $current
}

Write-Host 'Recruiter deploy branch updated on GitHub (everliv/recruiter).'
