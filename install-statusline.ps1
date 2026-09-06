#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

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
