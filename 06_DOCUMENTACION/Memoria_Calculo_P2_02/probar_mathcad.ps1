$ErrorActionPreference='Stop'
$mc=New-Object -ComObject Mathcad.Application
$mc.Visible=$true
Write-Output ('Mathcad: '+$mc.Version)
$w=$mc.Worksheets.Open('C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02\prueba_formato.xmcd')
$w.Recalculate()
Write-Output ('Fv='+$w.GetValue('Fv').Real)
$w.Save()
$w.SaveAs('C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02\prueba_formato.html',3)

