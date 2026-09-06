#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ClaudeSrc = Join-Path $ScriptDir 'CLAUDE.md'

$BeginTag  = '<!-- BEGIN spec-forge (managed by install-rules) -->'
$EndTag    = '<!-- END spec-forge -->'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

if (-not (Test-Path -LiteralPath $ClaudeSrc -PathType Leaf)) {
    Write-Error "source not found at $ClaudeSrc"
    exit 1
}

function Install-ManagedSection {
    param(
        [string]$Target
    )

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Target) | Out-Null

    $existing = ''
    if (Test-Path -LiteralPath $Target -PathType Leaf) {
        $existing = [System.IO.File]::ReadAllText($Target)
    }

    $srcContent = [System.IO.File]::ReadAllText($ClaudeSrc)

    $pattern = '(?s)' + [regex]::Escape($BeginTag) + '.*?' + [regex]::Escape($EndTag)
    $newContent = [regex]::Replace($existing, $pattern, '')
    $newContent = $newContent -replace '[\r\n]+$', ''
    $newContent += "`r`n`r`n$BeginTag`r`n"
    $newContent += $srcContent -replace '[\r\n]+$', ''
    $newContent += "`r`n$EndTag`r`n"

    [System.IO.File]::WriteAllText($Target, $newContent, $Utf8NoBom)
}

Install-ManagedSection -Target (Join-Path $env:USERPROFILE '.claude\CLAUDE.md')
Write-Host "  [ok] CLAUDE.md -> $env:USERPROFILE\.claude\CLAUDE.md"

Install-ManagedSection -Target (Join-Path $env:USERPROFILE '.config\opencode\AGENTS.md')
Write-Host "  [ok] CLAUDE.md -> $env:USERPROFILE\.config\opencode\AGENTS.md"
