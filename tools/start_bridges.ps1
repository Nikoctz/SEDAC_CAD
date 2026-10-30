# Script para iniciar ambos puentes HTTP de MCP en segundo plano
# Inventor Bridge en puerto 8766
# Revit Bridge en puerto 8767

$ErrorActionPreference = "Stop"

Write-Host "Iniciando puentes HTTP de MCP..." -ForegroundColor Cyan
Write-Host ""

# Configurar entorno
$env:TEMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$env:TMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:INVENTOR_MCP_CALL_TIMEOUT = "50"
$env:INVENTOR_MCP_STARTUP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\startup-disabled.py"

# Rutas a los venvs
$InventorVenvPython = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe"
$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"

# Verificar que los executables existen
if (-not (Test-Path $InventorVenvPython)) {
    Write-Error "Python de Inventor no encontrado: $InventorVenvPython"
    exit 1
}

if (-not (Test-Path $RevitVenvPython)) {
    Write-Error "Python de Revit no encontrado: $RevitVenvPython"
    exit 1
}

# Directorios de los puentes
$InventorBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\inventor-http-bridge"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

# Iniciar Inventor Bridge
Write-Host "Iniciando Inventor Bridge en puerto 8766..." -ForegroundColor Yellow
$InventorProc = Start-Process -FilePath $InventorVenvPython `
    -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8766" `
    -WorkingDirectory $InventorBridgeDir `
    -PassThru `
    -NoNewWindow

# Esperar un momento para que el puente arranque
Start-Sleep -Seconds 3

# Verificar que el puente de Inventor responde
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8766/health" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Inventor Bridge arrancado correctamente" -ForegroundColor Green
    } else {
        Write-Host "⚠ Inventor Bridge responded with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ No se pudo verificar Inventor Bridge: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Configurar entorno para Revit Bridge
$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

# Iniciar Revit Bridge
Write-Host ""
Write-Host "Iniciando Revit Bridge en puerto 8767..." -ForegroundColor Yellow
$RevitProc = Start-Process -FilePath $RevitVenvPython `
    -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" `
    -WorkingDirectory $RevitBridgeDir `
    -PassThru `
    -NoNewWindow

# Esperar un momento para que el puente arranque
Start-Sleep -Seconds 3

# Verificar que el puente de Revit responde
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8767/health" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Revit Bridge arrancado correctamente" -ForegroundColor Green
    } else {
        Write-Host "⚠ Revit Bridge responded with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ No se pudo verificar Revit Bridge: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Puentes iniciados. PIDs:" -ForegroundColor Cyan
Write-Host "  Inventor: $($InventorProc.Id)"
Write-Host "  Revit: $($RevitProc.Id)"
Write-Host ""
Write-Host "Para detener los puentes, ejecutar:" -ForegroundColor Gray
Write-Host "  Stop-Process -Id $($InventorProc.Id), $($RevitProc.Id) -Force"
