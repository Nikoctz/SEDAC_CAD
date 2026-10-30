# Script de lanzamiento para el puente HTTP de Inventor
# Requiere PowerShell 5.1+ y Python en el PATH o ruta absoluta

param(
    [int]$Port = 8766,
    [string]$Host = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

# Ruta al venv de Inventor
$InventorVenv = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe"

if (-not (Test-Path $InventorVenv)) {
    Write-Error "Python del venv de Inventor no encontrado: $InventorVenv"
    Write-Host "Alternativas:"
    Write-Host "  1. Usar Python del sistema: python server.py"
    Write-Host "  2. Especificar ruta: --python C:\ruta\a\python.exe"
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ServerScript = Join-Path $ScriptDir "server.py"

if (-not (Test-Path $ServerScript)) {
    Write-Error "Servidor no encontrado: $ServerScript"
    exit 1
}

Write-Host "Iniciando puente HTTP de Inventor..." -ForegroundColor Cyan
Write-Host "  Host: $Host"
Write-Host "  Port: $Port"
Write-Host "  Script: $ServerScript"
Write-Host ""

# Variables de entorno adicionales
$Env:TEMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$Env:TMP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"
$Env:PYTHONUTF8 = "1"
$Env:PYTHONDONTWRITEBYTECODE = "1"
$Env:INVENTOR_MCP_CALL_TIMEOUT = "50"
$Env:INVENTOR_MCP_STARTUP = "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\startup-disabled.py"

# Iniciar el servidor
& $InventorVenv $ServerScript --host $Host --port $Port

exit $LASTEXITCODE
