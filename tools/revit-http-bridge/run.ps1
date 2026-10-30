# Script de lanzamiento para el puente HTTP de Revit
# Requiere PowerShell 5.1+ y Python en el PATH o ruta absoluta

param(
    [int]$Port = 8767,
    [string]$Host = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

# Ruta al venv de Revit
$RevitVenv = "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe"

if (-not (Test-Path $RevitVenv)) {
    Write-Error "Python del venv de Revit no encontrado: $RevitVenv"
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

Write-Host "Iniciando puente HTTP de Revit..." -ForegroundColor Cyan
Write-Host "  Host: $Host"
Write-Host "  Port: $Port"
Write-Host "  Bridge: $env:REVIT_MCP_HOST`:$env:REVIT_MCP_PORT"
Write-Host ""

# Variables de entorno para el puente
$Env:REVIT_MCP_HOST = if ($env:REVIT_MCP_HOST) { $env:REVIT_MCP_HOST } else { "127.0.0.1" }
$Env:REVIT_MCP_PORT = if ($env:REVIT_MCP_PORT) { $env:REVIT_MCP_PORT } else { "8765" }
$Env:REVIT_MCP_TIMEOUT = "600"
$Env:REVIT_MCP_ALLOW_WRITES = "0"

# Iniciar el servidor
& $RevitVenv $ServerScript --host $Host --port $Port

exit $LASTEXITCODE
