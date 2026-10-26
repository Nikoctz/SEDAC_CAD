# Exporta el PDF de revision del informe y comprueba el resultado.
$ErrorActionPreference = 'Stop'
$base = 'C:\Users\nicol\OneDrive\Documentos\SEDAC_Paquete_Calculo_20261025\01_Informe'
$docx = Join-Path $base 'Informe_SEDAC_Memoria_y_Ensayos_v0.1.docx'
$pdf = Join-Path $base 'Informe_SEDAC_Memoria_y_Ensayos_v0.1.pdf'
if (Test-Path -LiteralPath $pdf) { Remove-Item -LiteralPath $pdf -Force }
$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$wd.DisplayAlerts = 0
$wd.Options.UpdateLinksAtOpen = $false
$doc = $wd.Documents.Open($docx, $false, $true)
Write-Output ('Documento abierto. Parrafos: ' + $doc.Paragraphs.Count + '; tablas: ' + $doc.Tables.Count)
$doc.ExportAsFixedFormat($pdf, 17)   # 17 = wdExportFormatPDF
Write-Output ('PDF exportado: ' + (Test-Path -LiteralPath $pdf))
$doc.Close(0)
$wd.Quit()
if (Test-Path -LiteralPath $pdf) { Write-Output ('Tamano PDF: ' + (Get-Item $pdf).Length + ' bytes') }
