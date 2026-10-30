$RevitExe = "C:\Program Files\Autodesk\Revit 2027\Revit.exe"
if (-not (Get-Process -Name Revit -ErrorAction SilentlyContinue)) {
    Write-Host "Iniciando Revit..."
    Start-Process $RevitExe -PassThru
    Write-Host "Revit iniciado"
} else {
    Write-Host "Revit ya está corriendo"
}
