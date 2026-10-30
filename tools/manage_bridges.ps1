# Gestión de puentes MCP - Inicia y verifica ambos puentes
# Uso: .\manage_bridges.ps1 [start|stop|status|restart]

param([string]$Action = "status")

$InventorVenvPython = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe"
$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"
$InventorBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\inventor-http-bridge"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

$env:TEMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$env:TMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:INVENTOR_MCP_CALL_TIMEOUT = "50"
$env:INVENTOR_MCP_STARTUP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\startup-disabled.py"
$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

function Get-BridgeStatus {
    param([int]$Port)
    try {
        $r = Invoke-WebRequest "http://localhost:$Port/health" -TimeoutSec 3 -UseBasicParsing
        return @{ ok = $true; content = $r.Content }
    } catch {
        return @{ ok = $false; error = $_.Exception.Message }
    }
}

function Start-InventorBridge {
    Write-Host "Iniciando Inventor Bridge..."
    Start-Process $InventorVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8766" -WorkingDirectory $InventorBridgeDir -WindowStyle Hidden -PassThru | Out-Null
    Start-Sleep -Seconds 3
    $status = Get-BridgeStatus 8766
    if ($status.ok) { Write-Host "✓ Inventor Bridge OK" -ForegroundColor Green } else { Write-Host "⚠ Inventor Bridge: $($status.error)" -ForegroundColor Yellow }
}

function Start-RevitBridge {
    Write-Host "Iniciando Revit Bridge..."
    Start-Process $RevitVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" -WorkingDirectory $RevitBridgeDir -WindowStyle Hidden -PassThru | Out-Null
    Start-Sleep -Seconds 5
    $status = Get-BridgeStatus 8767
    if ($status.ok) { Write-Host "✓ Revit Bridge OK" -ForegroundColor Green } else { Write-Host "⚠ Revit Bridge: $($status.error)" -ForegroundColor Yellow }
}

function Stop-Bridges {
    Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*inventor*" -or $_.Path -like "*revit*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "Puentes detenidos"
}

function Show-Status {
    $inv = Get-BridgeStatus 8766
    $rev = Get-BridgeStatus 8767
    Write-Host "--- Inventor Bridge (8766) ---"
    if ($inv.ok) { Write-Host "OK: $($inv.content)" -ForegroundColor Green } else { Write-Host "FAIL: $($inv.error)" -ForegroundColor Red }
    Write-Host ""
    Write-Host "--- Revit Bridge (8767) ---"
    if ($rev.ok) { Write-Host "OK: $($rev.content)" -ForegroundColor Green } else { Write-Host "FAIL: $($rev.error)" -ForegroundColor Red }
}

switch ($Action) {
    "start" { Start-InventorBridge; Start-RevitBridge }
    "stop" { Stop-Bridges }
    "restart" { Stop-Bridges; Start-Sleep 2; Start-InventorBridge; Start-RevitBridge }
    "status" { Show-Status }
    default { Write-Host "Uso: manage_bridges.ps1 [start|stop|status|restart]" }
}
