$ErrorActionPreference='Stop'
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
$sedacApp=New-Object -ComObject Inventor.Application
$sedacApp.Visible=$true
$sedacRoot='C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_01_20261015'
$sedacData=Get-Content -Raw -LiteralPath (Join-Path $sedacRoot 'GEOMETRIA_P2.json') | ConvertFrom-Json
$sedacOut=Join-Path $sedacRoot ('Inventor_'+(Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $sedacOut | Out-Null
function New-SedacPart {
 $doc=$sedacApp.Documents.Add(12290,$sedacApp.FileManager.GetTemplateFile(12290),$false)
 $doc.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
 return $doc
}
function Add-SedacBox($doc,$box,$label,$cut) {
 $cd=$doc.ComponentDefinition
 $plane=$cd.WorkPlanes.Item(3)
 if ([Math]::Abs([double]$box[2]) -gt 0.00000001) {
  $plane=$cd.WorkPlanes.AddByPlaneAndOffset($plane,([double]$box[2]/10))
  $plane.Visible=$false
 }
 $sk=$cd.Sketches.Add($plane)
 $sk.Name='B_'+$label
 $tg=$sedacApp.TransientGeometry
 $p1=$tg.CreatePoint2d(([double]$box[0]/10),([double]$box[1]/10))
 $p2=$tg.CreatePoint2d((([double]$box[0]+[double]$box[3])/10),(([double]$box[1]+[double]$box[4])/10))
 $null=$sk.SketchLines.AddAsTwoPointRectangle($p1,$p2)
 $op=[Inventor.PartFeatureOperationEnum]::kJoinOperation
 if ($cut) {$op=[Inventor.PartFeatureOperationEnum]::kCutOperation}
 $profile=$sk.Profiles.AddForSolid()
 $ed=$cd.Features.ExtrudeFeatures.CreateExtrudeDefinition($profile,$op)
 $ed.SetDistanceExtent(([double]$box[5]/10),[Inventor.PartFeatureExtentDirectionEnum]::kPositiveExtentDirection)
 $feat=$cd.Features.ExtrudeFeatures.Add($ed)
 $feat.Name=$label
 $sk.Visible=$false
}
function Save-SedacPart($doc,$path,$color) {
 if (-not $doc.Update2($false)) {throw ('Fallo Update: '+$path)}
 if ($doc.ComponentDefinition.SurfaceBodies.Count -ne 1) {throw ('No tiene un cuerpo: '+$path)}
 if (-not $doc.ComponentDefinition.SurfaceBodies.Item(1).IsSolid) {throw ('No solido: '+$path)}
 $null=$doc.PropertySets.Item('Inventor User Defined Properties').Add('P2.01 - COTAS PROVISIONALES','SEDAC_Estado')
 try {
  $asset=$doc.Assets.Add([Inventor.AssetTypeEnum]::kAssetTypeAppearance,'Generic','SEDAC_Color','SEDAC_Color')
  $asset.Item('generic_diffuse').Value=$sedacApp.TransientObjects.CreateColor([int]$color[0],[int]$color[1],[int]$color[2])
  $doc.ActiveAppearance=$asset
 } catch {Write-Output ('Color opcional: '+$_.Exception.Message)}
 $doc.SaveAs($path,$false)
}
$sedacPaths=@()
try {
 foreach ($spec in $sedacData.parts) {
  Write-Output ('Creando '+$spec.name)
  $doc=New-SedacPart
  $n=0
  foreach ($box in $spec.boxes) {$n++;Add-SedacBox $doc $box ('Vol_'+$n) $false}
  $n=0
  foreach ($box in $spec.cuts) {$n++;Add-SedacBox $doc $box ('Abertura_'+$n) $true}
  $path=Join-Path $sedacOut ($spec.name+'.ipt')
  Save-SedacPart $doc $path $spec.color
  $sedacPaths+=$path
  $doc.Close($true)
 }
 $assy=$sedacApp.Documents.Add(12291,$sedacApp.FileManager.GetTemplateFile(12291),$true)
 $assy.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
 foreach ($path in $sedacPaths) {
  $occ=$assy.ComponentDefinition.Occurrences.Add($path,$sedacApp.TransientGeometry.CreateMatrix())
  $occ.Name=[IO.Path]::GetFileNameWithoutExtension($path)
  $occ.Grounded=$true
 }
 if (-not $assy.Update2($false)) {throw 'Fallo Update ensamblaje'}
 $assy.SaveAs((Join-Path $sedacOut 'SEDAC_P2_01.iam'),$false)
 Write-Output 'Ensamblaje guardado. Creando maqueta.'
 $doc=New-SedacPart
 foreach ($idx in @(2,0,1,3,4,5,6,7)) {
  $spec=$sedacData.mini_parts[$idx];$n=0
  foreach ($box in $spec.boxes) {$n++;Add-SedacBox $doc $box ('M_'+$spec.name+'_'+$n) $false}
  $n=0
  foreach ($box in $spec.cuts) {$n++;Add-SedacBox $doc $box ('Corte_'+$spec.name+'_'+$n) $true}
 }
 Save-SedacPart $doc (Join-Path $sedacOut 'SEDAC_P2_Maqueta_1a12_ADAPTADA.ipt') @(163,184,200)
 $bounds=$doc.ComponentDefinition.SurfaceBodies.Item(1).RangeBox
 $sedacDims=@((($bounds.MaxPoint.X-$bounds.MinPoint.X)*10),(($bounds.MaxPoint.Y-$bounds.MinPoint.Y)*10),(($bounds.MaxPoint.Z-$bounds.MinPoint.Z)*10))
 $doc.Close($true)
 $assy.Activate()
 $cam=$sedacApp.ActiveView.Camera
 $cam.ViewOrientationType=[Inventor.ViewOrientationTypeEnum]::kIsoTopRightViewOrientation
 $cam.Fit()
 $cam.Apply()
 $sedacApp.ActiveView.SaveAsBitmap((Join-Path $sedacOut 'CAPTURA_INVENTOR_P2.png'),1600,1200)
 Set-Content -LiteralPath (Join-Path $sedacOut 'ESTADO_OK.txt') -Value ('P2.01 generado en Inventor 2027.1 mediante API. 12 piezas fijadas + maqueta de un cuerpo. Dimensiones maqueta mm: '+($sedacDims -join ', ')+' . Sin validacion mecanica. Regla iLogic entregada; ejecucion iLogic no comprobada.') -Encoding utf8
 Set-Content -LiteralPath (Join-Path $sedacRoot 'ULTIMA_EJECUCION.txt') -Value $sedacOut -Encoding utf8
 Write-Output $sedacOut
} catch {
 Set-Content -LiteralPath (Join-Path $sedacOut 'ERROR.txt') -Value $_.ToString()
 throw
}

