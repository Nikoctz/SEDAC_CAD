# Inicia ambos puentes MCP
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

function Test-Port {
    param([int]$Port)
    try {
        $r = Invoke-WebRequest "http://localhost:$Port/health" -TimeoutSec 3 -UseBasicParsing
        return $true
    } catch {
        return $false
    }
}

Write-Host "Deteniendo procesos existentes..."
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*inventor*" -or $_.Path -like "*revit*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "Iniciando Inventor Bridge (8766)..." -ForegroundColor Yellow
Start-Process $InventorVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8766" -WorkingDirectory $InventorBridgeDir -WindowStyle Hidden
Start-Sleep -Seconds 4

if (Test-Port 8766) {
    Write-Host "✓ Inventor Bridge OK" -ForegroundColor Green
} else {
    Write-Host "⚠ Inventor Bridge no responde" -ForegroundColor Yellow
}

Write-Host "Iniciando Revit Bridge (8767)..." -ForegroundColor Yellow
Start-Process $RevitVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" -WorkingDirectory $RevitBridgeDir -WindowStyle Hidden
Start-Sleep -Seconds 8

if (Test-Port 8767) {
    Write-Host "✓ Revit Bridge OK" -ForegroundColor Green
} else {
    Write-Host "⚠ Revit Bridge no responde" -ForegroundColor Yellow
}
