#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json

$cwd = ''
if ($payload.PSObject.Properties['workspace'] -and $payload.workspace.PSObject.Properties['current_dir']) {
    $cwd = $payload.workspace.current_dir
}

$model = 'Unknown'
if ($payload.PSObject.Properties['model'] -and $payload.model.PSObject.Properties['display_name'] -and $payload.model.display_name) {
    $model = $payload.model.display_name
}

$ctx = 'ctx:-'
if ($payload.PSObject.Properties['context_window'] -and $payload.context_window.PSObject.Properties['used_percentage']) {
    $usedPct = $payload.context_window.used_percentage
    if ($null -ne $usedPct -and $usedPct -ne '') {
        $ctx = 'ctx:{0:F0}%' -f [double]$usedPct
    }
}

$sessionName = ''
if ($payload.PSObject.Properties['session_name'] -and $payload.session_name) {
    $sessionName = $payload.session_name
}

if ($sessionName) {
    Write-Host -NoNewline ("{0} | {1} | {2} | {3}" -f $model, $ctx, $cwd, $sessionName)
} else {
    Write-Host -NoNewline ("{0} | {1} | {2}" -f $model, $ctx, $cwd)
}
