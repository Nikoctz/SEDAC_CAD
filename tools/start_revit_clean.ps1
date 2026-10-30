$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*revit*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

Start-Process $RevitVenvPython -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" -WorkingDirectory $RevitBridgeDir -WindowStyle Hidden
Start-Sleep -Seconds 12

try {
    $r = Invoke-WebRequest "http://localhost:8767/health" -TimeoutSec 5 -UseBasicParsing
    $h = $r.Content | ConvertFrom-Json
    Write-Host "Revit Bridge: OK - bridge_connected=$($h.bridge_connected) tools=$($h.tools_count)"
} catch {
    Write-Host "Revit Bridge: FAIL - $_"
}
