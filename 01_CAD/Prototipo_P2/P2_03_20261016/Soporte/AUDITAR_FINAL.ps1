$ErrorActionPreference='Stop'
$base='C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_03_20261016\Entrega\Inventor_Optimizado'
$app=[Runtime.InteropServices.Marshal]::GetActiveObject('Inventor.Application')
$assy=$null
foreach($d in $app.Documents){if($d.FullFileName -eq (Join-Path $base 'SEDAC_P2_03.iam')){$assy=$d;break}}
if(-not $assy){throw 'No se encuentra el ensamblaje final abierto'}
$seen=@{};$rows=@()
foreach($o in $assy.ComponentDefinition.Occurrences){
 $d=$o.Definition.Document;$key=[IO.Path]::GetFileNameWithoutExtension($d.FullFileName)
 if($seen.ContainsKey($key)){continue};$seen[$key]=$true
 $cd=$d.ComponentDefinition
 $rows+=[pscustomobject]@{pieza=$key;ruta=$d.FullFileName;solidos=$cd.SurfaceBodies.Count;masa_nativa_kg=$cd.MassProperties.Mass;volumen_mm3=1000*$cd.MassProperties.Volume;roscas_nativas=$cd.Features.ThreadFeatures.Count;redondeos=$cd.Features.FilletFeatures.Count}
}
ConvertTo-Json -InputObject @($rows) -Depth 6 | Set-Content -LiteralPath (Join-Path $base 'AUDITORIA_NATIVA.json') -Encoding utf8
Write-Output ('Masa ensamblaje kg: '+$assy.ComponentDefinition.MassProperties.Mass)
$rows | Where-Object {$_.pieza -like 'Anclaje*'} | Select-Object pieza,redondeos | ConvertTo-Json
