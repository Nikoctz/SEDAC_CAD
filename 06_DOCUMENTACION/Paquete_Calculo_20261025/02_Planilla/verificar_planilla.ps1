# Verifica la planilla en Excel: apertura sin reparacion, formulas calculadas y comportamiento
# con entradas faltantes. Deja el libro guardado por Excel para que conserve los resultados.
$ErrorActionPreference = 'Stop'
$path = 'C:\Users\nicol\OneDrive\Documentos\SEDAC_Paquete_Calculo_20261025\02_Planilla\Planilla_SEDAC_Captura_y_Seu'
$path = 'C:\Users\nicol\OneDrive\Documentos\SEDAC_Paquete_Calculo_20261025\02_Planilla\Planilla_SEDAC_Captura_y_Seguimiento_v0.1.xlsx'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
$wb = $xl.Workbooks.Open($path)
Write-Output ('Hojas: ' + $wb.Worksheets.Count)
foreach ($ws in $wb.Worksheets) { Write-Output ('  - ' + $ws.Name + ' (' + $ws.UsedRange.Rows.Count + ' filas x ' + $ws.UsedRange.Columns.Count + ' cols)') }
$xl.CalculateFullRebuild()

$portada = $wb.Worksheets.Item('00_Portada')
Write-Output '--- indicadores de portada ---'
for ($r = 1; $r -le 30; $r++) {
    $a = $portada.Cells.Item($r, 1).Text
    $b = $portada.Cells.Item($r, 2).Text
    if ($a -and $b) { Write-Output ('  ' + $a + ' = ' + $b) }
}

$var = $wb.Worksheets.Item('02_Variables')
Write-Output '--- control de variables (primeras 6) ---'
for ($r = 3; $r -le 8; $r++) {
    Write-Output ('  ' + $var.Cells.Item($r, 1).Text + ' | estado=' + $var.Cells.Item($r, 8).Text + ' | control=' + $var.Cells.Item($r, 14).Text)
}

$res = $wb.Worksheets.Item('08_Resultados')
Write-Output '--- resultados: diferencia con entradas faltantes ---'
for ($r = 3; $r -le 6; $r++) {
    Write-Output ('  ' + $res.Cells.Item($r, 1).Text + ' | dif=' + $res.Cells.Item($r, 8).Text + ' | estado=' + $res.Cells.Item($r, 12).Text)
}

# Prueba de comportamiento: escribir un valor medido y ver que la formula deja de decir PENDIENTE
$res.Cells.Item(3, 4).Value2 = 1.5
$res.Cells.Item(3, 7).Value2 = 1.4
$xl.CalculateFullRebuild()
Write-Output ('  tras simular D3=1.5 y G3=1.4 -> H3=' + $res.Cells.Item(3, 8).Text + ' ; I3=' + $res.Cells.Item(3, 9).Text + ' ; L3=' + $res.Cells.Item(3, 12).Text)
$res.Cells.Item(3, 4).ClearContents()
$res.Cells.Item(3, 7).ClearContents()
$xl.CalculateFullRebuild()
Write-Output ('  tras borrar la simulacion -> H3=' + $res.Cells.Item(3, 8).Text + ' ; L3=' + $res.Cells.Item(3, 12).Text)

$wb.Save()
$wb.Close($true)
$xl.Quit()
Write-Output ('Guardado por Excel: ' + (Test-Path -LiteralPath $path))
