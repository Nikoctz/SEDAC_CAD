# Reinicio agresivo del puente de Revit
$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

# Detener todos los procesos de Revit Bridge
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*revit*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Verificar que el puerto 8767 está libre
$port8767 = netstat -ano | findstr ":8767" | findstr "LISTEN"
if ($port8767) {
    Write-Host "Puerto 8767 aún ocupado, esperando..."
    Start-Sleep -Seconds 5
}

# Iniciar nuevo puente
$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

Write-Host "Iniciando Revit Bridge..."
$proc = Start-Process $RevitVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" -WorkingDirectory $RevitBridgeDir -WindowStyle Hidden -PassThru
Write-Host "PID: $($proc.Id)"

# Esperar y verificar varias veces
for ($i = 1; $i -le 5; $i++) {
    Start-Sleep -Seconds 5
    try {
        $r = Invoke-WebRequest "http://localhost:8767/health" -TimeoutSec 5 -UseBasicParsing
        $health = $r.Content | ConvertFrom-Json
        if ($health.status -eq "ok" -and $health.bridge_connected -eq $true) {
            Write-Host "✓ Revit Bridge OK (intento $i)" -ForegroundColor Green
            Write-Host "  Tools: $($health.tools_count)" -ForegroundColor Green
            exit 0
        }
    } catch {
        Write-Host "  Intento $i: no responde" -ForegroundColor Yellow
    }
}

Write-Host "✗ Revit Bridge no se pudo estabilizar" -ForegroundColor Red
