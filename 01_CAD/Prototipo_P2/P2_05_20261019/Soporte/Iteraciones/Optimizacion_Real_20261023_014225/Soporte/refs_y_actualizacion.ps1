param([string]$Carpeta)
$ErrorActionPreference='Stop'
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
Add-Type -TypeDefinition @'
using System;using System.Runtime.InteropServices;
public static class OptCom2 {
 [DllImport("oleaut32.dll", PreserveSig=false)] static extern void GetActiveObject(ref Guid clsid, IntPtr reserved, [MarshalAs(UnmanagedType.IUnknown)] out object obj);
 public static object Active(string id) {Guid g=Type.GetTypeFromProgID(id).GUID; object o;GetActiveObject(ref g,IntPtr.Zero,out o);return o;}
}
'@ -ReferencedAssemblies 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
try{$app=[OptCom2]::Active('Inventor.Application')}catch{$app=New-Object -ComObject Inventor.Application}
$app.SilentOperation=$true
$doc=$app.Documents.Open((Join-Path $Carpeta 'SEDAC_OPT_20261023.iam'),$false)
$refs=@();foreach($o in $doc.ComponentDefinition.Occurrences){$refs+=$o.Definition.Document.FullFileName};$refs=@($refs | Sort-Object -Unique)
$actualiza=$doc.Update2($false)
$faltan=@();foreach($r in $refs){if(-not (Test-Path -LiteralPath $r)){$faltan+=$r}}
$ipts=@(Get-ChildItem -LiteralPath $Carpeta -Filter *.ipt)
$res=[pscustomobject]@{archivo='SEDAC_OPT_20261023.iam';documentos_referenciados=$refs.Count;referencias_ausentes=$faltan.Count;actualizacion_correcta=[bool]$actualiza;ipt_en_carpeta=$ipts.Count;nombres=$refs;nota='Lectura del IAM nativo: recuento de documentos referenciados, comprobacion de existencia en disco y Update2 del ensamblaje. El documento no se guarda.'}
$res | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Carpeta 'REFERENCIAS_Y_ACTUALIZACION.json') -Encoding utf8
$doc.Close($true)
Write-Output ('referencias='+$refs.Count+' ausentes='+$faltan.Count+' update='+$actualiza+' ipt='+$ipts.Count)
