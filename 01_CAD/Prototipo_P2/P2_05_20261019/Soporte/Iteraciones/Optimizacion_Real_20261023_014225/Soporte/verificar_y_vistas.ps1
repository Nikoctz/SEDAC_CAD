param([string]$Carpeta)
$ErrorActionPreference='Stop'
if(-not $Carpeta){$Carpeta=Split-Path -Parent $PSScriptRoot}
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class OptCom {
 [DllImport("oleaut32.dll", PreserveSig=false)] static extern void GetActiveObject(ref Guid clsid, IntPtr reserved, [MarshalAs(UnmanagedType.IUnknown)] out object obj);
 public static object Active(string id) {Guid g=Type.GetTypeFromProgID(id).GUID; object o;GetActiveObject(ref g,IntPtr.Zero,out o);return o;}
}
'@ -ReferencedAssemblies 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
$app=$null
try{$app=[OptCom]::Active('Inventor.Application')}catch{$app=New-Object -ComObject Inventor.Application}
$app.Visible=$true;$app.SilentOperation=$true
$iam=Join-Path $Carpeta 'SEDAC_OPT_20261023.iam'
$doc=$app.Documents.Open($iam,$false)
$cd=$doc.ComponentDefinition
$tg=$app.TransientGeometry
$occ=@($cd.Occurrences)
$refs=@($cd.Occurrences.AllReferencedDocuments)
$grounded=@($occ | Where-Object {$_.Grounded}).Count
$m=@()
foreach($o in $occ){ if(-not $o.Name.StartsWith('REF_')){ } }
$masaTotal=$cd.MassProperties.Mass
# Interferencias sobre piezas fisicas (excluye BOM de referencia)
$set=$app.TransientObjects.CreateObjectCollection()
foreach($o in $occ){ if($o.BOMStructure -ne [Inventor.BOMStructureEnum]::kReferenceBOMStructure){$set.Add($o)} }
$hits=@($cd.AnalyzeInterference($set))
$issues=@()
foreach($h in $hits){$issues+=[pscustomobject]@{a=$h.OccurrenceOne.Name;b=$h.OccurrenceTwo.Name;vol_mm3=[math]::Round($h.Volume*1000,6)}}
# Vistas faltantes: lateral e isometrica
$doc.Activate()
$app.ActiveView.DisplayMode=[Inventor.DisplayModeEnum]::kShadedWithEdgesRendering
function Capture($name,$ex,$ey,$ez){
 $cam=$app.ActiveView.Camera
 $cam.Eye=$tg.CreatePoint($ex,$ey,$ez);$cam.Target=$tg.CreatePoint(0,24,-5)
 $cam.UpVector=$tg.CreateUnitVector(0,1,0);$cam.Perspective=$false;$cam.Fit();$cam.Apply()
 $app.ActiveView.SaveAsBitmap((Join-Path $Carpeta $name),1600,1600)
}
Capture 'VISTA_LATERAL.png' 320 24 -5
Capture 'VISTA_ISOMETRICA.png' 150 130 150
$ver=[pscustomobject]@{
 archivo='SEDAC_OPT_20261023.iam'
 fecha=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
 ocurrencias=$occ.Count
 documentos_referenciados=$refs.Count
 componentes_grounded=$grounded
 restricciones=$cd.Constraints.Count
 masa_ensemble_kg=$masaTotal
 interferencias=$issues.Count
 detalle_interferencias=$issues
 vistas_anadidas=@('VISTA_LATERAL.png','VISTA_ISOMETRICA.png')
 nota='Lectura y captura de vistas sobre el IAM de esta carpeta. No se modifica geometria ni se guarda el documento.'
}
$ver | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Carpeta 'VERIFICACION_NATIVA.json') -Encoding utf8
# Lista de referencias para el manifiesto
$refs | ForEach-Object {$_.FullFileName} | Set-Content -LiteralPath (Join-Path $Carpeta 'REFERENCIAS_IPT.txt') -Encoding utf8
$doc.Close($true)
$app.SilentOperation=$false
Write-Output ('verificado: '+$occ.Count+' ocurrencias, '+$refs.Count+' documentos, '+$issues.Count+' interferencias, masa '+[math]::Round($masaTotal,6)+' kg')
