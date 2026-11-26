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

function Register-AntigravitySkills {
    $configPath  = Join-Path $env:USERPROFILE '.gemini\config\skills.json'
    $targetEntry = '~/.claude/skills'
    $utf8NoBom   = New-Object System.Text.UTF8Encoding($false)

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $configPath) | Out-Null

    $config = $null
    if (Test-Path -LiteralPath $configPath -PathType Leaf) {
        $raw = [System.IO.File]::ReadAllText($configPath)
        if ($raw.Trim()) {
            $config = $raw | ConvertFrom-Json
        }
    }
    if ($null -eq $config) {
        $config = New-Object PSObject
    }

    $entries = @()
    if ($config.PSObject.Properties['entries'] -and $null -ne $config.entries) {
        $entries = @($config.entries)
    }

    $exists = $false
    foreach ($entry in $entries) {
        if ($entry.PSObject.Properties['path'] -and $entry.path -eq $targetEntry) {
            $exists = $true
            break
        }
    }

    if (-not $exists) {
        $entries += [PSCustomObject]@{ path = $targetEntry }
    }

    if ($config.PSObject.Properties['entries']) {
        $config.entries = [object[]]$entries
    } else {
        $config | Add-Member -MemberType NoteProperty -Name 'entries' -Value ([object[]]$entries)
    }

    $json = $config | ConvertTo-Json -Depth 100
    [System.IO.File]::WriteAllText($configPath, "$json`r`n", $utf8NoBom)
    Write-Host "  [ok] Antigravity skills pointer -> $configPath ($targetEntry)"
}

Write-Host ""
Register-AntigravitySkills
Write-Host ""
Write-Host "Done. $($skills.Count) skills installed to $SkillDest"
