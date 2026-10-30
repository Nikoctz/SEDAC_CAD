# Inicia solo el puente de Revit en segundo plano
$ErrorActionPreference = "Stop"

$RevitVenvPython = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"
$RevitBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge"

$env:REVIT_MCP_HOST = "127.0.0.1"
$env:REVIT_MCP_PORT = "8765"
$env:REVIT_MCP_TIMEOUT = "600"
$env:REVIT_MCP_ALLOW_WRITES = "0"

Start-Process -FilePath $RevitVenvPython `
    -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8767" `
    -WorkingDirectory $RevitBridgeDir `
    -PassThru `
    -NoNewWindow
