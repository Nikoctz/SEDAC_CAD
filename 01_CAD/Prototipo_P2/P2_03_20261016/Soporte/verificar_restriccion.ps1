$ErrorActionPreference='Stop'
Add-Type -Path 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll'
Add-Type -ReferencedAssemblies 'C:\Program Files\Autodesk\Inventor 2027\Bin\Autodesk.Inventor.Interop.dll' -TypeDefinition @'
public static class SedacProxy2 {
 public static object Get(object obj, object input) {
  var o=(Inventor.ComponentOccurrence)obj;
  object output;
  o.CreateGeometryProxy(input,out output);
  return output;
 }
}
'@
$a=[Runtime.InteropServices.Marshal]::GetActiveObject('Inventor.Application')
$doc=$a.Documents.Add(12291,$a.FileManager.GetTemplateFile(12291),$false)
$o=$doc.ComponentDefinition.Occurrences.Add('C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_03_20261016\CAD_Final\Casquillo_M6_I_45.ipt',$a.TransientGeometry.CreateMatrix())
$pr=[SedacProxy2]::Get($o,$o.Definition.WorkPlanes.Item(1))
[pscustomobject]@{proxy=($null -ne $pr);type=$pr.Type;normalX=$pr.Plane.Normal.X}
$doc.Close($true)

