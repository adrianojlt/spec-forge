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

function Install-StatusLine {
    $src      = Join-Path $ScriptDir 'statusline-command.ps1'
    $dest     = Join-Path $env:USERPROFILE '.claude\statusline-command.ps1'
    $settings = Join-Path $env:USERPROFILE '.claude\settings.json'

    if (-not (Test-Path -LiteralPath $src -PathType Leaf)) {
        Write-Host "  [skip] statusline: source not found at $src"
        return
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
    Copy-Item -LiteralPath $src -Destination $dest -Force

    $config = $null
    if (Test-Path -LiteralPath $settings -PathType Leaf) {
        $raw = [System.IO.File]::ReadAllText($settings)
        if ($raw.Trim()) {
            $config = $raw | ConvertFrom-Json
        }
    }
    if ($null -eq $config) {
        $config = New-Object PSObject
    }

    $statusLine = [PSCustomObject]@{
        type    = 'command'
        command = "powershell -NoProfile -File `"$dest`""
    }

    if ($config.PSObject.Properties['statusLine']) {
        $config.statusLine = $statusLine
    } else {
        $config | Add-Member -MemberType NoteProperty -Name 'statusLine' -Value $statusLine
    }

    $json = $config | ConvertTo-Json -Depth 100
    [System.IO.File]::WriteAllText($settings, $json, $Utf8NoBom)

    Write-Host "  [ok] statusline -> $dest"
}

Install-StatusLine
