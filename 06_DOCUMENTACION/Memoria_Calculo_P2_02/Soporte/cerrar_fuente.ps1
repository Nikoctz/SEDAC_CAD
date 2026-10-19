$ErrorActionPreference='Stop'
$mc=[Runtime.InteropServices.Marshal]::GetActiveObject('Mathcad.Application')
$list=@($mc.Worksheets)
foreach($ws in $list) {
 if ($ws.FullName -eq 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02\Soporte\fuente_memoria.xmcd') {$ws.Close(2);Write-Output 'Fuente temporal cerrada'}
}

