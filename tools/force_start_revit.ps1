# Fuerza reinicio del puente de Revit

# 1. Detener cualquier proceso en el puerto 8767
$pid8767 = netstat -ano | findstr ":8767" | findstr "LISTEN" | ForEach-Object { $_.Split()[-1] }
if ($pid8767) {
    Write-Host "Deteniendo proceso en puerto 8767 (PID: $pid8767)"
    Stop-Process -Id $pid8767 -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# 2. Iniciar nuevo puente
$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

Write-Host "Iniciando Revit Bridge..."
$proc = Start-Process $RevitVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" -WorkingDirectory $RevitBridgeDir -WindowStyle Hidden -PassThru
Write-Host "PID: $($proc.Id)"

Start-Sleep -Seconds 10

# 3. Verificar
try {
    $r = Invoke-WebRequest "http://localhost:8767/health" -TimeoutSec 5 -UseBasicParsing
    Write-Host "OK: " + $r.Content
} catch {
    Write-Host "FAIL: " + $_.Exception.Message
}
