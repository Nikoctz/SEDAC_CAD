param([string]$Salida='')
$ErrorActionPreference='Stop'
$base=$PSScriptRoot
if (-not $Salida) {$Salida=Join-Path $base ('Inventor_'+(Get-Date -Format 'yyyyMMdd_HHmmss'))}
New-Item -ItemType Directory -Path $Salida -Force | Out-Null
$python='C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python (Join-Path $base 'generar_p2_02.py') $Salida
if ($LASTEXITCODE -ne 0) {throw 'Error al calcular o generar geometria'}
$data=Get-Content -Raw -LiteralPath (Join-Path $Salida 'MODELO_P2_02.json') | ConvertFrom-Json
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
$app=New-Object -ComObject Inventor.Application
$app.Visible=$true
$tg=$app.TransientGeometry
function Pt([double]$x,[double]$y) {return $tg.CreatePoint2d($x/10,$y/10)}
function Get-SP($sk,$x,$y) {
 $key=('{0:F8},{1:F8}' -f [double]$x,[double]$y)
 if (-not $script:SedacPoints.ContainsKey($key)) {$script:SedacPoints[$key]=$sk.SketchPoints.Add((Pt $x $y),$false)}
 return $script:SedacPoints[$key]
}
function Add-Line($sk,$a,$b) {
 if (([Math]::Abs($a[0]-$b[0])+[Math]::Abs($a[1]-$b[1])) -gt 0.0000001) {
  $null=$sk.SketchLines.AddByTwoPoints((Get-SP $sk $a[0] $a[1]),(Get-SP $sk $b[0] $b[1]))
 }
}
function Add-Loop($sk,$s) {
 $script:SedacPoints=@{}
 if ($s.kind -eq 'circle') {$null=$sk.SketchCircles.AddByCenterRadius((Pt $s.x $s.y),([double]$s.r/10));return}
 if ($s.kind -eq 'poly') {
  for ($j=0;$j -lt $s.pts.Count;$j++) {Add-Line $sk $s.pts[$j] $s.pts[(($j+1)%$s.pts.Count)]}
  return
 }
 $x=[double]$s.x;$y=[double]$s.y;$w=[double]$s.w;$h=[double]$s.h;$r=[double]$s.r
 if ($r -lt 0.0000001) {$null=$sk.SketchLines.AddAsTwoPointRectangle((Pt $x $y),(Pt ($x+$w) ($y+$h)));return}
 $p=@(@(($x+$r),$y),@(($x+$w-$r),$y),@(($x+$w),($y+$r)),@(($x+$w),($y+$h-$r)),@(($x+$w-$r),($y+$h)),@(($x+$r),($y+$h)),@($x,($y+$h-$r)),@($x,($y+$r)))
 $c=@(@(($x+$w-$r),($y+$r)),@(($x+$w-$r),($y+$h-$r)),@(($x+$r),($y+$h-$r)),@(($x+$r),($y+$r)))
 for ($j=0;$j -lt 4;$j++) {
  Add-Line $sk $p[(2*$j)] $p[(2*$j+1)]
  $aa=$p[(2*$j+1)];$bb=$p[((2*$j+2)%8)];$cc=$c[$j]
  $null=$sk.SketchArcs.AddByCenterStartEndPoint((Pt $cc[0] $cc[1]),(Get-SP $sk $aa[0] $aa[1]),(Get-SP $sk $bb[0] $bb[1]),$true)
 }
}
function Add-Operation($doc,$o,$index) {
 $cd=$doc.ComponentDefinition;$s=[double]$o.start/10
 switch ($o.axis) {
 'x' {$org=$tg.CreatePoint($s,0,0);$u=$tg.CreateUnitVector(0,1,0);$v=$tg.CreateUnitVector(0,0,1)}
 'y' {$org=$tg.CreatePoint(0,$s,0);$u=$tg.CreateUnitVector(0,0,1);$v=$tg.CreateUnitVector(1,0,0)}
 'z' {$org=$tg.CreatePoint(0,0,$s);$u=$tg.CreateUnitVector(1,0,0);$v=$tg.CreateUnitVector(0,1,0)}
 }
 $plane=$cd.WorkPlanes.AddFixed($org,$u,$v)
 $plane.Visible=$false
 $sk=$cd.Sketches.Add($plane);$sk.Name='B_'+$index+'_'+$o.label
 foreach ($loop in $o.loops) {Add-Loop $sk $loop}
 $operation=[Inventor.PartFeatureOperationEnum]::kJoinOperation
 if ($o.cut) {$operation=[Inventor.PartFeatureOperationEnum]::kCutOperation}
 $profile=$sk.Profiles.AddForSolid()
 $ed=$cd.Features.ExtrudeFeatures.CreateExtrudeDefinition($profile,$operation)
 $ed.SetDistanceExtent(([double]$o.depth/10),[Inventor.PartFeatureExtentDirectionEnum]::kPositiveExtentDirection)
 $feature=$cd.Features.ExtrudeFeatures.Add($ed);$feature.Name='F_'+$index+'_'+$o.label;$sk.Visible=$false
}
$masses=@();$rounding=@();$stage='inicio'
try {
 foreach ($p in $data.parts) {
  $stage=$p.name;Write-Output ('Pieza: '+$stage)
  $doc=$app.Documents.Add(12290,$app.FileManager.GetTemplateFile(12290),$false)
  $doc.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
  $i=0
  foreach ($o in $p.ops) {$i++;$stage=$p.name+' operacion '+$i;Add-Operation $doc $o $i}
  if ($p.name.StartsWith('Anclaje_hombro') -or $p.name -eq 'Yugo_cinturon') {
   $tx=$app.TransactionManager.StartTransaction($doc,'Redondear contacto con cintas')
   try {
    $edg=$app.TransientObjects.CreateEdgeCollection()
    foreach ($edge in $doc.ComponentDefinition.SurfaceBodies.Item(1).Edges) {$edg.Add($edge)}
    $ff=$doc.ComponentDefinition.Features.FilletFeatures.AddSimple($edg,'0.6 mm')
    $ff.Name='Radio_cantos_0p6'
    if (-not $doc.Update2($false)) {throw 'Redondeo no actualizado'}
    $tx.End();$rounding+=[pscustomobject]@{pieza=$p.name;radio_mm=0.6;aplicado=$true}
   } catch {$tx.Abort();$rounding+=[pscustomobject]@{pieza=$p.name;radio_mm=0.6;aplicado=$false;error=$_.ToString()}}
  }
  if (-not $doc.Update2($false)) {throw ('No actualiza '+$p.name)}
  if ($doc.ComponentDefinition.SurfaceBodies.Count -ne 1) {throw ('No es cuerpo unico '+$p.name)}
  if (-not $doc.ComponentDefinition.SurfaceBodies.Item(1).IsSolid) {throw ('No solido '+$p.name)}
  $props=$doc.PropertySets.Item('Inventor User Defined Properties')
  $null=$props.Add('P2.02 PREDISENO; cargas y medidas provisionales','SEDAC_Estado')
  $null=$props.Add($p.material,'SEDAC_Material_Candidato')
  $null=$props.Add('Editar PARAMETROS_P2_02.json y regenerar. Montaje Grounded.','SEDAC_Edicion')
  $vol=$doc.ComponentDefinition.MassProperties.Volume*1000
  $rho=0.0000027
  if ($p.material -eq '5052') {$rho=0.00000268}
  if ($p.material -eq 'hdpe') {$rho=0.000000953}
  if ($p.material -eq 'pad') {$rho=0.00000006}
  if ($p.material -eq 'herrajes') {$rho=0.000008}
  $mass=$vol*$rho
  $null=$props.Add($mass,'SEDAC_Masa_Estimada_kg')
  $count=@($data.instances | Where-Object {$_.part -eq $p.name}).Count
  $masses+= [pscustomobject]@{pieza=$p.name;material=$p.material;volumen_mm3=$vol;masa_candidata_kg=$mass;cantidad=$count;referencia=$p.reference}
  try {
   $asset=$doc.Assets.Add([Inventor.AssetTypeEnum]::kAssetTypeAppearance,'Generic','SEDAC_Color','SEDAC_Color')
   $asset.Item('generic_diffuse').Value=$app.TransientObjects.CreateColor([int]$p.color[0],[int]$p.color[1],[int]$p.color[2])
   $doc.ActiveAppearance=$asset
  } catch {}
  $doc.SaveAs((Join-Path $Salida ($p.name+'.ipt')),$false);$doc.Close($true)
 }
 $stage='Ensamblar'
 $assy=$app.Documents.Add(12291,$app.FileManager.GetTemplateFile(12291),$true)
 $assy.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
 foreach ($ins in $data.instances) {
  $mx=$tg.CreateMatrix()
  if ($ins.axis -eq 'x') {
   $mx.Cell(1,1)=0;$mx.Cell(2,1)=1;$mx.Cell(3,1)=0
   $mx.Cell(1,2)=0;$mx.Cell(2,2)=0;$mx.Cell(3,2)=1
   $mx.Cell(1,3)=1;$mx.Cell(2,3)=0;$mx.Cell(3,3)=0
  }
  if ($ins.axis -eq 'y') {
   $mx.Cell(1,1)=0;$mx.Cell(2,1)=0;$mx.Cell(3,1)=1
   $mx.Cell(1,2)=1;$mx.Cell(2,2)=0;$mx.Cell(3,2)=0
   $mx.Cell(1,3)=0;$mx.Cell(2,3)=1;$mx.Cell(3,3)=0
  }
  $mx.Cell(1,4)=[double]$ins.position[0]/10;$mx.Cell(2,4)=[double]$ins.position[1]/10;$mx.Cell(3,4)=[double]$ins.position[2]/10
  $occ=$assy.ComponentDefinition.Occurrences.Add((Join-Path $Salida ($ins.part+'.ipt')),$mx)
  $occ.Name=$ins.name;$occ.Grounded=$true
 }
 if (-not $assy.Update2($false)) {throw 'No actualiza ensamblaje'}
 $assy.SaveAs((Join-Path $Salida 'SEDAC_P2_02.iam'),$false)
 $stage='Comprobar interferencias'
 $checkSet=$app.TransientObjects.CreateObjectCollection()
 foreach ($occ in $assy.ComponentDefinition.Occurrences) {$checkSet.Add($occ)}
 $interferences=$assy.ComponentDefinition.AnalyzeInterference($checkSet)
 $issues=@()
 foreach($hit in $interferences) {
  $issues+=[pscustomobject]@{pieza_1=$hit.OccurrenceOne.Name;pieza_2=$hit.OccurrenceTwo.Name;volumen_mm3=($hit.Volume*1000)}
 }
 ConvertTo-Json -InputObject @($issues) -Depth 5 | Set-Content -LiteralPath (Join-Path $Salida 'INTERFERENCIAS.json') -Encoding utf8
 ConvertTo-Json -InputObject @($rounding) -Depth 5 | Set-Content -LiteralPath (Join-Path $Salida 'REDONDEOS.json') -Encoding utf8
 Write-Output ('Interferencias registradas: '+$issues.Count)
 if (@($issues | Where-Object {$_.volumen_mm3 -gt 0.001}).Count -gt 0) {throw 'Hay interferencias: revisar INTERFERENCIAS.json antes de aceptar esta revision'}
 $masses | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Salida 'MASAS_CAD.json') -Encoding utf8
 $assy.Activate()
 function Capture($name,$ex,$ey,$ez) {
  $cam=$app.ActiveView.Camera;$cam.Eye=$tg.CreatePoint($ex,$ey,$ez);$cam.Target=$tg.CreatePoint(0,25,5);$cam.UpVector=$tg.CreateUnitVector(0,1,0);$cam.Perspective=$false;$cam.Fit();$cam.Apply()
  $app.ActiveView.SaveAsBitmap((Join-Path $Salida $name),1600,1600)
 }
 Capture 'VISTA_FRENTE.png' 60 60 85
 Capture 'VISTA_ESPALDA.png' -60 60 -85
 foreach ($occ in $assy.ComponentDefinition.Occurrences) {
  if ($occ.Name.StartsWith('REF_')) {$occ.Visible=$false}
 }
 Capture 'VISTA_ESTRUCTURA.png' 60 60 85
 foreach ($occ in $assy.ComponentDefinition.Occurrences) {$occ.Visible=$true}
 Capture 'VISTA_FRENTE.png' 60 60 85
 $assy.Save()
 $stage='Exportar STEP'
 $translator=$app.ApplicationAddIns.ItemById('{90AF7F40-0C01-11D5-8E83-0010B541CD80}')
 $context=$app.TransientObjects.CreateTranslationContext();$context.Type=[Inventor.IOMechanismEnum]::kFileBrowseIOMechanism
 $options=$app.TransientObjects.CreateNameValueMap()
 $null=$translator.HasSaveCopyAsOptions($assy,$context,$options)
 $options.Value('ApplicationProtocolType')=3
 $medium=$app.TransientObjects.CreateDataMedium();$medium.FileName=Join-Path $Salida 'SEDAC_P2_02_REVISION.step'
 $translator.SaveCopyAs($assy,$context,$options,$medium)
 Set-Content -LiteralPath (Join-Path $Salida 'ESTADO_OK.txt') -Value ('Actualizacion correcta de '+$data.parts.Count+' piezas solidas y '+$data.instances.Count+' ocurrencias. STEP y vistas exportados. No es validacion mecanica.') -Encoding utf8
 Set-Content -LiteralPath (Join-Path $base 'ULTIMA_EJECUCION.txt') -Value $Salida -Encoding utf8
 Write-Output ('TERMINADO: '+$Salida)
} catch {
 Set-Content -LiteralPath (Join-Path $Salida 'ERROR.txt') -Value ($stage+[Environment]::NewLine+$_.ToString()) -Encoding utf8
 throw
}

