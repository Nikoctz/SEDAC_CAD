$ErrorActionPreference='Stop'
$mc=New-Object -ComObject Mathcad.Application
$mc.Visible=$true
$doc=$mc.Worksheets.Open('C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02\Memoria_SEDAC_P2_02_MC01_EDITABLE.xmcd')
Write-Output 'Memoria final abierta.'

