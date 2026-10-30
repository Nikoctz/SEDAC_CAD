# Inicia Revit 2027 si no está corriendo
$RevitExe = "C:\Program Files\Autodesk\Revit 2027\Revit.exe"

if (-not (Get-Process -Name Revit -ErrorAction SilentlyContinue)) {
    Write-Host "Iniciando Revit 2027..."
    try {
        $proc = Start-Process $RevitExe -PassThru -Wait
        Write-Host "Revit iniciado con PID: $($proc.Id)"
    } catch {
        Write-Host "Error al iniciar Revit: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Revit ya está corriendo" -ForegroundColor Green
}
