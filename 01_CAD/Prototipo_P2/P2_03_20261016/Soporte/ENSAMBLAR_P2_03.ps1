$ErrorActionPreference='Stop'
$base='C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_03_20261016'
$Salida=Join-Path $base 'Entrega\Inventor_Optimizado'
$data=Get-Content -Raw -LiteralPath (Join-Path $Salida 'MODELO_API.json') | ConvertFrom-Json
$masses=Get-Content -Raw -LiteralPath (Join-Path $Salida 'MASAS_CAD.json') | ConvertFrom-Json
$threads=Get-Content -Raw -LiteralPath (Join-Path $Salida 'ROSCAS_NATIVAS.json') | ConvertFrom-Json
$rounding=@();$assemblyChecks=@()
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

try {
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



