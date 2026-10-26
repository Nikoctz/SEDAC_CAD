# Abre el informe en Word, comprueba su estructura y exporta el PDF de revisión.
$ErrorActionPreference = 'Stop'
$base = 'C:\Users\nicol\OneDrive\Documentos\SEDAC_Paquete_Calculo_20261025\01_Informe'
$docx = Join-Path $base 'Informe_SEDAC_Memoria_y_Ensayos_v0.1.docx'
$pdf = Join-Path $base 'Informe_SEDAC_Memoria_y_Ensayos_v0.1.pdf'
$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$wd.DisplayAlerts = 0
$doc = $wd.Documents.Open($docx, $false, $true)   # solo lectura para la comprobacion
Write-Output ('Titulo      : ' + $doc.BuiltInDocumentProperties('Title').Value)
Write-Output ('Parrafos    : ' + $doc.Paragraphs.Count)
Write-Output ('Tablas      : ' + $doc.Tables.Count)
Write-Output ('Paginas     : ' + $doc.ComputeStatistics(2))
Write-Output ('Palabras    : ' + $doc.ComputeStatistics(0))
$doc.Close(0)

# Exportacion del PDF de revision
$doc = $wd.Documents.Open($docx)
$doc.SaveAs2($pdf, 17)      # 17 = wdFormatPDF
$doc.Close(0)
$wd.Quit()
Write-Output ('PDF generado: ' + (Test-Path -LiteralPath $pdf))
if (Test-Path -LiteralPath $pdf) { Write-Output ('Tamano PDF : ' + (Get-Item $pdf).Length + ' bytes') }
