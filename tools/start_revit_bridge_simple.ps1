# Inicia el puente de Revit de forma simple
$ErrorActionPreference = "Stop"

$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

Write-Host "Iniciando puente de Revit..." -ForegroundColor Yellow
try {
    $proc = Start-Process -FilePath $RevitVenvPython `
        -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" `
        -WorkingDirectory $RevitBridgeDir `
        -PassThru `
        -NoNewWindow `
        -WindowStyle Hidden
    
    Write-Host "Proceso iniciado con PID: $($proc.Id)" -ForegroundColor Green
    
    # Esperar y verificar
    Start-Sleep -Seconds 5
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8767/health" -TimeoutSec 5 -UseBasicParsing
        Write-Host "✓ Revit Bridge respondiendo: $($response.Content)" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Revit Bridge no responde aún: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "  Es posible que Revit no esté abierto o el puente interno (8765) no esté disponible" -ForegroundColor Gray
    }
} catch {
    Write-Host "Error al iniciar: $($_.Exception.Message)" -ForegroundColor Red
}
