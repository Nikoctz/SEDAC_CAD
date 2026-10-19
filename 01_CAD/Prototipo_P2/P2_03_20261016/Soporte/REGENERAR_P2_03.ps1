param([string]$Salida='', [string]$Desde='')
$ErrorActionPreference='Stop'
$base=Split-Path $PSScriptRoot -Parent
if (-not $Salida) {$Salida=Join-Path $base 'Entrega\Inventor_Optimizado'}
New-Item -ItemType Directory -Path $Salida -Force | Out-Null
$python='C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python (Join-Path $base 'Soporte\generar_p2_03.py') $Salida
if ($LASTEXITCODE -ne 0) {throw 'Error al calcular o generar geometria'}
$data=Get-Content -Raw -LiteralPath (Join-Path $Salida 'MODELO_API.json') | ConvertFrom-Json
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class SedacCom {
 [DllImport("oleaut32.dll", PreserveSig=false)] static extern void GetActiveObject(ref Guid clsid, IntPtr reserved, [MarshalAs(UnmanagedType.IUnknown)] out object obj);
 public static object Active(string id) {Guid g=Type.GetTypeFromProgID(id).GUID; object o;GetActiveObject(ref g,IntPtr.Zero,out o);return o;}
 public static object Proxy(object obj, object input) {var occ=(Inventor.ComponentOccurrence)obj;object result;occ.CreateGeometryProxy(input,out result);return result;}
 public static int[] Freedom(object obj){var o=(Inventor.ComponentOccurrence)obj;int t,r;Inventor.ObjectsEnumerator et,er;Inventor.Point p;o.GetDegreesOfFreedom(out t,out et,out r,out er,out p);return new int[]{t,r};}
}
'@ -ReferencedAssemblies 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
try{$app=[SedacCom]::Active('Inventor.Application')}catch{$app=New-Object -ComObject Inventor.Application}

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
$masses=@();$rounding=@();$threads=@();$assemblyChecks=@();$stage='inicio'

$priorParts=@{};$priorMass=@{};$priorThreads=@();$priorRounding=@()
if($Desde){
 if(Test-Path -LiteralPath (Join-Path $Desde 'REDONDEOS.json')){$priorRounding=Get-Content -Raw -LiteralPath (Join-Path $Desde 'REDONDEOS.json') | ConvertFrom-Json}
 $pd=Get-Content -Raw -LiteralPath (Join-Path $Desde 'MODELO_API.json') | ConvertFrom-Json
 foreach($pp in $pd.parts){$priorParts[$pp.name]=$pp}
 $pm=Get-Content -Raw -LiteralPath (Join-Path $Desde 'MASAS_CAD.json') | ConvertFrom-Json
 foreach($mm in $pm){$priorMass[$mm.pieza]=$mm}
 $priorThreads=Get-Content -Raw -LiteralPath (Join-Path $Desde 'ROSCAS_NATIVAS.json') | ConvertFrom-Json
}
try {
 foreach ($p in $data.parts) {
  if($priorParts.ContainsKey($p.name) -and $priorMass.ContainsKey($p.name)){
   $oldjson=ConvertTo-Json -InputObject $priorParts[$p.name] -Depth 100 -Compress
   $newjson=ConvertTo-Json -InputObject $p -Depth 100 -Compress
   if($oldjson -eq $newjson){
    Copy-Item -LiteralPath (Join-Path $Desde ($p.name+'.ipt')) -Destination (Join-Path $Salida ($p.name+'.ipt'))
    $m=$priorMass[$p.name];$m.cantidad=@($data.instances | Where-Object {$_.part -eq $p.name}).Count
    $masses+=$m
    $threads+=@($priorThreads | Where-Object {$_.pieza -eq $p.name})
    $rounding+=@($priorRounding | Where-Object {$_.pieza -eq $p.name})
    Write-Output ('Reutilizada sin cambios: '+$p.name)
    continue
   }
  }

  $stage=$p.name;Write-Output ('Pieza: '+$stage)
  $doc=$app.Documents.Add(12290,$app.FileManager.GetTemplateFile(12290),$false)
  $doc.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
  $i=0
  foreach ($o in $p.ops) {$i++;$stage=$p.name+' operacion '+$i;Add-Operation $doc $o $i}
  if ($p.name.StartsWith('Anclaje_hombro') -or $p.name.StartsWith('Anclaje_cinturon')) {
   $tx=$app.TransactionManager.StartTransaction($doc,'Redondear contacto con cintas')
   try {
    $edg=$app.TransientObjects.CreateEdgeCollection()
    foreach ($edge in $doc.ComponentDefinition.SurfaceBodies.Item(1).Edges) {$edg.Add($edge)}
    $ff=$doc.ComponentDefinition.Features.FilletFeatures.AddSimple($edg,'0.4 mm')
    $ff.Name='Radio_cantos_0p4'
    if (-not $doc.Update2($false)) {throw 'Redondeo no actualizado'}
    $tx.End();$rounding+=[pscustomobject]@{pieza=$p.name;radio_mm=0.4;aplicado=$true}
   } catch {$tx.Abort();$rounding+=[pscustomobject]@{pieza=$p.name;radio_mm=0.4;aplicado=$false;error=$_.ToString()}}
  }

  if ($p.thread) {
   $th=$p.thread;$tf=$doc.ComponentDefinition.Features.ThreadFeatures
   $class='6g';if($th.internal){$class='6H'}
   $des='M'+$th.d+'x'+([double]$th.pitch).ToString('0.##',[Globalization.CultureInfo]::InvariantCulture)
   $info=$tf.CreateStandardThreadInfo([bool]$th.internal,$true,'ISO Metric profile',$des,$class)
   $face=$null
   foreach($f in $doc.ComponentDefinition.SurfaceBodies.Item(1).Faces){
    if($f.SurfaceType -eq [Inventor.SurfaceTypeEnum]::kCylinderSurface -and [Math]::Abs($f.Geometry.Radius*10-[double]$th.d/2) -lt 0.00001){$face=$f;break}
   }
   if(-not $face){throw ('Cara cilindrica no encontrada '+$p.name)}
   $edge=$null
   foreach($ee in $face.Edges){if($ee.GeometryType -eq [Inventor.CurveTypeEnum]::kCircleCurve){$edge=$ee;break}}
   if(-not $edge){throw 'Arista circular de rosca no encontrada'}
   
   if($th.internal){$feat=$tf.Add($face,$edge,$info,$false,$true)}
   else{
    $endEdge=$null
    foreach($ee in $face.Edges){if($ee.GeometryType -eq [Inventor.CurveTypeEnum]::kCircleCurve){
     if(-not $endEdge -or $ee.Geometry.Center.Z -gt $endEdge.Geometry.Center.Z){$endEdge=$ee}
    }}
    $feat=$tf.Add($face,$endEdge,$info,$false,$false,([double]$th.length/10),0)
   }
   $feat.Name='Rosca_'+$des+'_'+$class
   $threads+=[pscustomobject]@{pieza=$p.name;rosca=$des;clase=$class;nativa=$true;helice_geometrica=$false}
  }
  if (-not $doc.Update2($false)) {throw ('No actualiza '+$p.name)}
  if ($doc.ComponentDefinition.SurfaceBodies.Count -ne 1) {throw ('No es cuerpo unico '+$p.name)}
  if (-not $doc.ComponentDefinition.SurfaceBodies.Item(1).IsSolid) {throw ('No solido '+$p.name)}
  $props=$doc.PropertySets.Item('Inventor User Defined Properties')
  $null=$props.Add('P2.03 PREDISENO; cargas y medidas provisionales','SEDAC_Estado')
  $null=$props.Add($p.material,'SEDAC_Material_Candidato')
  $null=$props.Add('Editar PARAMETROS_P2_03.json y regenerar. Montaje con restricciones a referencias de posicion; no simulacion de contactos.','SEDAC_Edicion')
  $vol=$doc.ComponentDefinition.MassProperties.Volume*1000
  $rho=0.0000027
  if ($p.material -eq '5052') {$rho=0.00000268}
  if ($p.material -eq 'hdpe') {$rho=0.000000953}
  if ($p.material -eq 'pad') {$rho=0.00000006}
  if ($p.material -eq 'herrajes') {$rho=0.000008}

  $mat=$doc.Materials.Add(('SEDAC_'+$p.material),($rho*1000000))
  $doc.ComponentDefinition.Material=$mat
  $doc.Update2($false) | Out-Null
  $mass=$vol*$rho
  Write-Output ('Material '+$p.name+' dens='+$doc.ComponentDefinition.Material.Density+' vol='+$vol+' masa='+$doc.ComponentDefinition.MassProperties.Mass+' calculada='+$mass)
  if([Math]::Abs($doc.ComponentDefinition.MassProperties.Mass-$mass) -gt 0.00001){throw ('Masa nativa no coincide '+$p.name)}

  $null=$props.Add($mass,'SEDAC_Masa_Estimada_kg')
  if($p.description){$null=$props.Add($p.description,'SEDAC_Compra')}
  $count=@($data.instances | Where-Object {$_.part -eq $p.name}).Count
  $masses+= [pscustomobject]@{pieza=$p.name;material=$p.material;volumen_mm3=$vol;masa_candidata_kg=$mass;cantidad=$count;referencia=$p.reference}
  try {
   $asset=$doc.Assets.Add([Inventor.AssetTypeEnum]::kAssetTypeAppearance,'Generic','SEDAC_Color','SEDAC_Color')
   $asset.Item('generic_diffuse').Value=$app.TransientObjects.CreateColor([int]$p.color[0],[int]$p.color[1],[int]$p.color[2])
   $doc.ActiveAppearance=$asset
  } catch {}
  $doc.SaveAs((Join-Path $Salida ($p.name+'.ipt')),$false);$doc.Close($true)
 }

 $masses | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Salida 'MASAS_CAD.json') -Encoding utf8
 ConvertTo-Json -InputObject @($threads) -Depth 5 | Set-Content -LiteralPath (Join-Path $Salida 'ROSCAS_NATIVAS.json') -Encoding utf8
 $stage='Ensamblar'

 $assy=$app.Documents.Add(12291,$app.FileManager.GetTemplateFile(12291),$true)
 $assy.UnitsOfMeasure.LengthUnits=[Inventor.UnitsTypeEnum]::kMillimeterLengthUnits
 foreach ($ins in $data.instances) {
  $mx=$tg.CreateMatrix()
  if ($ins.axis -in @('x','nx')) {
   $mx.Cell(1,1)=0;$mx.Cell(2,1)=1;$mx.Cell(3,1)=0
   $mx.Cell(1,2)=0;$mx.Cell(2,2)=0;$mx.Cell(3,2)=1
   $mx.Cell(1,3)=1;$mx.Cell(2,3)=0;$mx.Cell(3,3)=0
  }
  if ($ins.axis -eq 'y') {
   $mx.Cell(1,1)=0;$mx.Cell(2,1)=0;$mx.Cell(3,1)=1
   $mx.Cell(1,2)=1;$mx.Cell(2,2)=0;$mx.Cell(3,2)=0
   $mx.Cell(1,3)=0;$mx.Cell(2,3)=1;$mx.Cell(3,3)=0
  }
  if($ins.axis -eq 'nz'){$mx.Cell(1,1)=-1;$mx.Cell(3,3)=-1}
  if($ins.axis -eq 'nx'){for($ri=1;$ri -le 3;$ri++){$mx.Cell($ri,1)=-$mx.Cell($ri,1);$mx.Cell($ri,3)=-$mx.Cell($ri,3)}}
  $mx.Cell(1,4)=[double]$ins.position[0]/10;$mx.Cell(2,4)=[double]$ins.position[1]/10;$mx.Cell(3,4)=[double]$ins.position[2]/10
  $occ=$assy.ComponentDefinition.Occurrences.Add((Join-Path $Salida ($ins.part+'.ipt')),$mx)

  $occ.Name=$ins.name
  if($ins.name -eq 'Riel_I'){$occ.Grounded=$true;continue}
  $occ.Grounded=$false
  $cons=@()
  for($pi=1;$pi -le 3;$pi++){
   $pr=[SedacCom]::Proxy($occ,$occ.Definition.WorkPlanes.Item($pi))
   $normal=$pr.Plane.Normal;$origin=$pr.Plane.RootPoint
   $ap=$null;$dot=0
   for($ai=1;$ai -le 3;$ai++){
    $candidate=$assy.ComponentDefinition.WorkPlanes.Item($ai)
    $pd=$normal.DotProduct($candidate.Plane.Normal)
    if([Math]::Abs($pd) -gt .999){$ap=$candidate;$dot=$pd;break}
   }
   if(-not $ap){throw 'Plano paralelo no encontrado'}
   $n=$ap.Plane.Normal
   $offset=$mx.Cell(1,4)*$n.X+$mx.Cell(2,4)*$n.Y+$mx.Cell(3,4)*$n.Z
   if($dot -gt 0){$co=$assy.ComponentDefinition.Constraints.AddFlushConstraint($ap,$pr,$offset)}
   else{$co=$assy.ComponentDefinition.Constraints.AddMateConstraint($ap,$pr,$offset)}
   $co.Name='Pos_'+$ins.name+'_'+$pi
   $cons+=@{c=$co;n=$n;offset=$offset}
  }
  $null=$assy.Update2($false)
  for($ci=0;$ci -lt $cons.Count;$ci++){
   $v=$cons[$ci];$now=$occ.Transformation
   $dif=($now.Cell(1,4)-$mx.Cell(1,4))*$v.n.X+($now.Cell(2,4)-$mx.Cell(2,4))*$v.n.Y+($now.Cell(3,4)-$mx.Cell(3,4))*$v.n.Z
   if([Math]::Abs($dif) -gt 0.000001){$v.c.Offset.Value=-$v.offset;$null=$assy.Update2($false)}
  }
  $err=0.0
  for($ri=1;$ri -le 3;$ri++){for($cc=1;$cc -le 4;$cc++){$err=[Math]::Max($err,[Math]::Abs($occ.Transformation.Cell($ri,$cc)-$mx.Cell($ri,$cc)))}}
  $freedom=[SedacCom]::Freedom($occ)
  if($freedom[0] -ne 0 -or $freedom[1] -ne 0){throw ('Grados de libertad pendientes '+$ins.name)}
  $assemblyChecks+=[pscustomobject]@{ocurrencia=$ins.name;error_transformacion=$err;restricciones=3;estado='posicion_verificada';traslaciones=$freedom[0];rotaciones=$freedom[1]}
  if($err -gt .000001){Write-Output ('Deseado '+$mx.Cell(1,4)+','+$mx.Cell(2,4)+','+$mx.Cell(3,4)+' Actual '+$occ.Transformation.Cell(1,4)+','+$occ.Transformation.Cell(2,4)+','+$occ.Transformation.Cell(3,4));throw ('Posicion alterada por restricciones '+$ins.name+' error '+$err)}

 }
 if (-not $assy.Update2($false)) {throw 'No actualiza ensamblaje'}
 $assy.SaveAs((Join-Path $Salida 'SEDAC_P2_03.iam'),$false)
 ConvertTo-Json -InputObject @($assemblyChecks) -Depth 6 | Set-Content -LiteralPath (Join-Path $Salida 'RESTRICCIONES.json') -Encoding utf8
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
 $assy.ObjectVisibility.AllWorkFeatures=$false
 function Capture($name,$ex,$ey,$ez) {
  $cam=$app.ActiveView.Camera;$cam.Eye=$tg.CreatePoint($ex,$ey,$ez);$cam.Target=$tg.CreatePoint(0,25,5);$cam.UpVector=$tg.CreateUnitVector(0,1,0);$cam.Perspective=$false;$cam.Fit();$cam.Apply()
  $app.ActiveView.SaveAsBitmap((Join-Path $Salida $name),1600,1600)
 }
 Capture 'VISTA_FRENTE.png' 60 60 85
 Capture 'VISTA_ESPALDA.png' -60 60 -85
 foreach ($occ in $assy.ComponentDefinition.Occurrences) {
  if ($occ.Name.StartsWith('Protector_') -or $occ.Name.StartsWith('REF_')) {$occ.Visible=$false}
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
 $medium=$app.TransientObjects.CreateDataMedium();$medium.FileName=Join-Path $Salida 'SEDAC_P2_03_REVISION.step'
 $translator.SaveCopyAs($assy,$context,$options,$medium)
 Set-Content -LiteralPath (Join-Path $Salida 'ESTADO_OK.txt') -Value ('Actualizacion correcta de '+$data.parts.Count+' piezas solidas y '+$data.instances.Count+' ocurrencias. STEP y vistas exportados. No es validacion mecanica.') -Encoding utf8
 Set-Content -LiteralPath (Join-Path $base 'ULTIMA_EJECUCION.txt') -Value $Salida -Encoding utf8
 Write-Output ('TERMINADO: '+$Salida)
} catch {
 Set-Content -LiteralPath (Join-Path $Salida 'ERROR.txt') -Value ($stage+[Environment]::NewLine+$_.ToString()) -Encoding utf8
 throw
}



