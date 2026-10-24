param([string]$Proyecto)
$ErrorActionPreference='Stop'
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
$app=New-Object -ComObject Inventor.Application
$app.SilentOperation=$true
$app.Visible=$true
if(Test-Path -LiteralPath (Join-Path $Proyecto 'Entrega\SEDAC_P204_MAQUETA_CUNAS_REFORZADAS.ipt')){throw 'La revision ya existe; usar carpeta nueva'}
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
 if ($s.kind -eq 'channel') {
  $cx=[double]$s.cx;$b=[double]$s.B;$d=[double]$s.D;$t=[double]$s.t;$r=[double]$s.r
  $lo=$cx-$b/2;$hi=$cx+$b/2
  $pp=@(@(0,$lo),@($d,$lo),@($d,($lo+$t)),@(($t+$r),($lo+$t)),@($t,($lo+$t+$r)),@($t,($hi-$t-$r)),@(($t+$r),($hi-$t)),@($d,($hi-$t)),@($d,$hi),@(0,$hi))
  for($j=0;$j -lt $pp.Count;$j++) {
   $a=$pp[$j];$bpt=$pp[(($j+1)%$pp.Count)]
   if($j -eq 3 -or $j -eq 5) {
    $cy=$lo+$t+$r;if($j -eq 5){$cy=$hi-$t-$r}
    $null=$sk.SketchArcs.AddByCenterStartEndPoint((Pt ($t+$r) $cy),(Get-SP $sk $a[0] $a[1]),(Get-SP $sk $bpt[0] $bpt[1]),$false)
   } else {Add-Line $sk $a $bpt}
  }
  return
 }
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
 $basePlane=$cd.WorkPlanes.AddFixed($tg.CreatePoint(0,0,0),$u,$v);$basePlane.Visible=$false
 $up=$cd.Parameters.UserParameters
 $pn='O'+$index.ToString('00')+'_Posicion'
 $dn='O'+$index.ToString('00')+'_Espesor'
 if($o.depth_name){$dn=[string]$o.depth_name}
 $null=$up.AddByExpression($pn,(([double]$o.start).ToString('0.########',[Globalization.CultureInfo]::InvariantCulture)+' mm'),[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits)
 $null=$up.AddByExpression($dn,(([double]$o.depth).ToString('0.########',[Globalization.CultureInfo]::InvariantCulture)+' mm'),[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits)
 $plane=$cd.WorkPlanes.AddByPlaneAndOffset($basePlane,$pn)
 $plane.Visible=$false

 $sk=$cd.Sketches.Add($plane);$sk.Name='B_'+$index+'_'+$o.label
 foreach ($loop in $o.loops) {Add-Loop $sk $loop}
 $operation=[Inventor.PartFeatureOperationEnum]::kJoinOperation
 if ($o.cut) {$operation=[Inventor.PartFeatureOperationEnum]::kCutOperation}
 $profile=$sk.Profiles.AddForSolid()
 $ed=$cd.Features.ExtrudeFeatures.CreateExtrudeDefinition($profile,$operation)
 $ed.SetDistanceExtent($dn,[Inventor.PartFeatureExtentDirectionEnum]::kPositiveExtentDirection)
 $feature=$cd.Features.ExtrudeFeatures.Add($ed);$feature.Name='F_'+$index+'_'+$o.label;$sk.Visible=$false
}

$ops=Get-Content -LiteralPath (Join-Path $Proyecto 'Soporte\GEOMETRIA_MAQUETA.json') -Raw | ConvertFrom-Json
$doc=$app.Documents.Add(12290,$app.FileManager.GetTemplateFile(12290),$true)
$doc.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
Write-Output ('Inventor conectado='+$app.SoftwareVersion.DisplayVersion)
$i=0;foreach($o in $ops){$i++;Write-Output ('Operacion '+$i+' '+$o.label);Add-Operation $doc $o $i}
if(-not $doc.Update2($false)){throw 'No actualiza'}
if($doc.ComponentDefinition.SurfaceBodies.Count -ne 1 -or -not $doc.ComponentDefinition.SurfaceBodies.Item(1).IsSolid){throw 'No es un solido conectado'}
$props=$doc.PropertySets.Item('Inventor User Defined Properties')
$null=$props.Add('Maqueta geometrica PLA adaptada de P2.04. No representa piezas funcionales ni nuevo material de producto.','SEDAC_Alcance')
$out=Join-Path $Proyecto 'Entrega'
$name='SEDAC_P204_MAQUETA_CUNAS_REFORZADAS'
$doc.SaveAs((Join-Path $out ($name+'.ipt')),$false)
$b=$doc.ComponentDefinition.RangeBox
$dim=[pscustomobject]@{X_mm=10*($b.MaxPoint.X-$b.MinPoint.X);Y_mm=10*($b.MaxPoint.Y-$b.MinPoint.Y);Z_mm=10*($b.MaxPoint.Z-$b.MinPoint.Z);cuerpos=$doc.ComponentDefinition.SurfaceBodies.Count;volumen_mm3=$doc.ComponentDefinition.MassProperties.Volume*1000;version_inventor=$app.SoftwareVersion.DisplayVersion}
$dim | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $out 'COMPROBACION_NATIVA.json') -Encoding utf8
foreach($id in @('{533E9A98-FC3B-11D4-8E7E-0010B541CD80}','{90AF7F40-0C01-11D5-8E83-0010B541CD80}')){
 $tr=$app.ApplicationAddIns.ItemById($id);$context=$app.TransientObjects.CreateTranslationContext();$context.Type=[Inventor.IOMechanismEnum]::kFileBrowseIOMechanism
 $options=$app.TransientObjects.CreateNameValueMap();$null=$tr.HasSaveCopyAsOptions($doc,$context,$options)
 $medium=$app.TransientObjects.CreateDataMedium()
 if($id -eq '{533E9A98-FC3B-11D4-8E7E-0010B541CD80}'){
  $options.Value('ExportUnits')=4;$options.Value('Resolution')=1;$options.Value('OutputFileType')=0
  $medium.FileName=Join-Path $Proyecto 'Soporte\NATIVO_ORIENTACION_INVENTOR.stl'
 }else{$medium.FileName=Join-Path $out ($name+'.step');$options.Value('ApplicationProtocolType')=3}
 $tr.SaveCopyAs($doc,$context,$options,$medium)
}
$doc.ObjectVisibility.AllWorkFeatures=$false
$app.ActiveView.DisplayMode=[Inventor.DisplayModeEnum]::kShadedWithEdgesRendering
$cam=$app.ActiveView.Camera;$cam.Eye=$tg.CreatePoint(7,6,10);$cam.Target=$tg.CreatePoint(0,2.4,.6);$cam.UpVector=$tg.CreateUnitVector(0,1,0);$cam.Perspective=$false;$cam.SetExtents(7,7);$cam.Apply()
$app.ActiveView.SaveAsBitmap((Join-Path $out 'VISTA_MAQUETA.png'),1400,1400)
$doc.Save()
$app.SilentOperation=$false
Write-Output ('FINAL '+$doc.FullFileName)

