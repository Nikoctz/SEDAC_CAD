# Inicia solo el puente de Inventor en segundo plano
$ErrorActionPreference = "Stop"

$InventorVenvPython = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe"
$InventorBridgeDir = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\inventor-http-bridge"

$env:TEMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$env:TMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:INVENTOR_MCP_CALL_TIMEOUT = "50"
$env:INVENTOR_MCP_STARTUP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\startup-disabled.py"

Start-Process -FilePath $InventorVenvPython `
    -ArgumentList "server.py", "--host", "127.0.0.1", "--port", "8766" `
    -WorkingDirectory $InventorBridgeDir `
    -PassThru `
    -NoNewWindow
