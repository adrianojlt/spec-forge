#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillSrc  = Join-Path $ScriptDir 'skills'
$SkillDest = Join-Path $env:USERPROFILE '.claude\skills'

if (-not (Test-Path -LiteralPath $SkillSrc -PathType Container)) {
    Write-Error "skills directory not found at $SkillSrc"
    exit 1
}

Write-Host "Installing skills to: $SkillDest"
New-Item -ItemType Directory -Force -Path $SkillDest | Out-Null

$skills = Get-ChildItem -LiteralPath $SkillSrc -Directory
foreach ($skill in $skills) {
    $dest = Join-Path $SkillDest $skill.Name
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Path (Join-Path $skill.FullName '*') -Destination $dest -Recurse -Force
    Write-Host "  [ok] $($skill.Name)"
}

Write-Host ""
Write-Host "Done. $($skills.Count) skills installed to $SkillDest"
