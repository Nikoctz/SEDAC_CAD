# Script de verificación de los puentes HTTP
param(
    [int]$InventorPort = 8766,
    [int]$RevitPort = 8767
)

function Test-Endpoint {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 10
        return @{ success = $true; body = $response.Content }
    }
    catch {
        return @{ success = $false; error = $_.Exception.Message }
    }
}

Write-Host "--- Inventor Bridge (port $InventorPort) ---"
$r = Test-Endpoint "http://localhost:$InventorPort/health"
if ($r.success) {
    Write-Host "OK: $($r.body)"
} else {
    Write-Host "FAIL: $($r.error)"
}

Write-Host ""
Write-Host "--- Revit Bridge (port $RevitPort) ---"
$r = Test-Endpoint "http://localhost:$RevitPort/health"
if ($r.success) {
    Write-Host "OK: $($r.body)"
} else {
    Write-Host "FAIL: $($r.error)"
}
