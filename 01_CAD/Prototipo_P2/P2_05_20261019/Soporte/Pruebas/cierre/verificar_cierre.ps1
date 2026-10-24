param([string]$Salida='')
$ErrorActionPreference='Stop'
$soporte=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$base=Split-Path -Parent $soporte
. (Join-Path $soporte 'cierre_p2_05.ps1')
if (-not $Salida) {$Salida=Join-Path $PSScriptRoot ('Ejecuciones/Nueva_'+(Get-Date -Format 'yyyyMMdd_HHmmss_fff'))}
$raizPruebas=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'Ejecuciones'))+[IO.Path]::DirectorySeparatorChar
$salidaAbsoluta=[IO.Path]::GetFullPath($Salida)
if (-not $salidaAbsoluta.StartsWith($raizPruebas,[StringComparison]::OrdinalIgnoreCase)) {throw 'La salida de pruebas debe ser nueva y estar dentro de Pruebas/cierre/Ejecuciones.'}
if (Test-Path -LiteralPath $Salida) {throw 'La salida ya existe; cada prueba usa una carpeta nueva.'}
New-Item -ItemType Directory -Path $Salida | Out-Null
$origen=Join-Path $base 'Soporte/Iteraciones/Nueva_20261019_060807'
$p204=Join-Path (Split-Path -Parent $base) 'P2_04_20261016/Entrega/Inventor'
$script:catalogo=@{}
foreach ($f in Get-ChildItem -LiteralPath $p204 -File) {$script:catalogo[$f.Name]=[pscustomobject]@{ruta=$f.FullName;bytes=$f.Length}}
$script:faltaGeneracion=$false
# Sustitución solo en memoria: no se crean archivos CAD ni se llama a Inventor.
# Los tamaños proceden de archivos existentes; su presencia en la salida es simulada.
function Get-SedacArchivoGenerado([string]$Ruta) {
 $nombre=(Split-Path -Leaf $Ruta).Replace('P2_05','P2_04')
 $dato=$script:catalogo[$nombre]
 return [pscustomobject]@{ruta=$Ruta;existe=($null -ne $dato -and -not $script:faltaGeneracion);bytes=$dato.bytes;simulado=$true;origen_solo_lectura=$dato.ruta}
}
function Write-CasoJson($Dato,[string]$Ruta) {ConvertTo-Json -InputObject $Dato -Depth 100 | Set-Content -LiteralPath $Ruta -Encoding UTF8}
function New-Caso([string]$Nombre,[switch]$Conforme) {
 $d=Join-Path $Salida $Nombre;New-Item -ItemType Directory -Path $d | Out-Null
 foreach ($f in @('MODELO_API.json','REDONDEOS.json','INTERFERENCIAS.json','RESTRICCIONES.json','MASAS_CAD.json','RESUMEN_ENTREGA.json')) {Copy-Item -LiteralPath (Join-Path $origen $f) -Destination (Join-Path $d $f)}
 Copy-Item -LiteralPath (Join-Path $base 'Calculos/RESULTADOS_PREDISENO.json') -Destination (Join-Path $d 'RESULTADOS_PREDISENO.json')
 'casos sintéticos de prueba; no son evidencia de entrega' | Set-Content -LiteralPath (Join-Path $d 'CASO_SINTETICO.txt') -Encoding UTF8
 if ($Conforme) {
  $rs=Read-SedacJson (Join-Path $d 'REDONDEOS.json')
  foreach ($r in $rs) {$r.estado='total';$r.aplicado=$true;$r.aristas_redondeadas=$r.aristas_totales;$r.criterio='todas'}
  Write-CasoJson $rs (Join-Path $d 'REDONDEOS.json')
  $res=Read-SedacJson (Join-Path $d 'RESUMEN_ENTREGA.json');$res.redondeos_pendientes=0
  Write-CasoJson $res (Join-Path $d 'RESUMEN_ENTREGA.json')
 }
 return $d
}
function Assert-Cierre([bool]$Condicion,[string]$Mensaje) {if (-not $Condicion) {throw $Mensaje};$script:aserciones++}
function Invoke-Decision([string]$Carpeta) {
 $decision=Get-SedacCierre $Carpeta (Join-Path $Carpeta 'RESULTADOS_PREDISENO.json')
 Write-SedacCierre $decision $Carpeta -CasoSintetico
 return $decision
}
$script:aserciones=0;$script:casos=New-Object 'System.Collections.Generic.List[object]'
function Invoke-Caso([string]$Nombre,[scriptblock]$Prueba) {
 $inicio=$script:aserciones
 try {& $Prueba;$script:casos.Add([pscustomobject]@{caso=$Nombre;cumple=$true;aserciones=($script:aserciones-$inicio);error=$null})}
 catch {$script:casos.Add([pscustomobject]@{caso=$Nombre;cumple=$false;aserciones=($script:aserciones-$inicio);error=$_.Exception.Message})}
}
Invoke-Caso 'A · redondeo parcial 236/472, con y sin AceptarPendientes' {
 $d=New-Caso 'A_parcial';$r=Invoke-Decision $d
 Assert-Cierre (-not $r.aceptado -and -not $r.R2.cumple -and $r.R3.cumple) 'El parcial debe bloquear la aceptación'
 Assert-Cierre (Test-SedacExportacion $r -AceptarPendientes) 'La opción solo permite exportar borrador'
 Assert-Cierre (-not (Test-SedacExportacion $r)) 'Sin opción, debe detenerse antes de exportar'
 Assert-Cierre (-not (Test-Path (Join-Path $d 'ESTADO_OK.txt'))) 'No puede existir ESTADO_OK'
 Assert-Cierre ((Get-Content (Join-Path $d 'ESTADO_BORRADOR.txt') -Raw -Encoding UTF8).Contains('no es una entrega aceptada')) 'Debe declarar el borrador'
 Assert-Cierre (Test-Path (Join-Path $d 'ERROR.txt')) 'Debe registrar error'
}
Invoke-Caso 'B · ausencia de registro al reutilizar' {
 $d=New-Caso 'B_sin_registro' -Conforme;$m=Read-SedacJson (Join-Path $d 'MODELO_API.json')
 $pieza=@($m.parts | Where-Object {$_.name -eq 'Interfaz_lumbar_aligerada'})[0]
 $rs=Read-SedacJson (Join-Path $d 'REDONDEOS.json')
 $rs=@($rs | Where-Object {$_.pieza -ne $pieza.name})
 $falta=Get-SedacRegistroReutilizado $pieza $rs
 Assert-Cierre ($falta.estado -eq 'sin_registro' -and $null -eq $falta.aristas_totales) 'No inventar conteos para la evidencia ausente'
 Write-CasoJson @($rs+$falta) (Join-Path $d 'REDONDEOS.json')
 $r=Invoke-Decision $d
 Assert-Cierre (-not $r.aceptado -and $r.R2.redondeos_pendientes -eq 1) 'La ausencia debe contarse y bloquear'
 Assert-Cierre (($r.R2.motivos -join ';').Contains('sin_registro')) 'Debe explicarse la ausencia de evidencia'
 Assert-Cierre (-not (Test-Path (Join-Path $d 'ESTADO_OK.txt'))) 'No hay sello para registro ausente'
}
Invoke-Caso 'C · cumple_cribado=false y verificación incumplida' {
 $d=New-Caso 'C_cribado_falso' -Conforme;$c=Read-SedacJson (Join-Path $d 'RESULTADOS_PREDISENO.json')
 $c.cumple_cribado=$false;$c.verificaciones[0].cumple=$false;$c.verificaciones[0].margen=$c.verificaciones[0].umbral/2;$c.minimo_margen=$c.verificaciones[0].margen
 Write-CasoJson $c (Join-Path $d 'RESULTADOS_PREDISENO.json');$r=Invoke-Decision $d
 Assert-Cierre ($r.R2.cumple -and -not $r.R3.cumple -and -not $r.aceptado) 'Un cálculo incumplido bloquea aun con R2 conforme'
 Assert-Cierre (-not (Test-SedacExportacion $r -AceptarPendientes)) 'La opción no permite saltarse R3'
 Assert-Cierre (Test-Path (Join-Path $d 'INCUMPLIMIENTO_CRIBADO.txt')) 'Falta el diagnóstico del cribado'
 Assert-Cierre ((Get-Content (Join-Path $d 'INCUMPLIMIENTO_CRIBADO.txt') -Raw -Encoding UTF8).Contains($c.verificaciones[0].nombre)) 'Debe identificar la verificación que falla'
 Assert-Cierre (-not (Test-Path (Join-Path $d 'ESTADO_OK.txt'))) 'No puede aceptar el cálculo falso'
}
Invoke-Caso 'D · todo conforme, con generación simulada' {
 $d=New-Caso 'D_conforme_sintetico' -Conforme;$r=Invoke-Decision $d
 Assert-Cierre ($r.R1.cumple -and $r.R2.cumple -and $r.R3.cumple -and $r.aceptado) 'El caso conforme debe satisfacer R1+R2+R3'
 Assert-Cierre (Test-Path (Join-Path $d 'ESTADO_OK.txt')) 'Falta el sello sintético'
 $txt=Get-Content (Join-Path $d 'ESTADO_OK.txt') -Raw -Encoding UTF8
 Assert-Cierre ($txt.Contains('casos sintéticos de prueba; no son evidencia de entrega')) 'El sello de prueba debe identificarse como sintético'
 Assert-Cierre ($txt.Contains('Ninguno de los tres acredita el comportamiento físico del producto')) 'Falta el alcance físico literal'
 Assert-Cierre (-not (Test-Path (Join-Path $d 'ERROR.txt'))) 'El caso conforme no debe registrar error'
 foreach ($f in @('R1_GENERACION.json','R2_COHERENCIA.json','R3_CRIBADO.json')) {Assert-Cierre (Test-Path (Join-Path $d $f)) ('Falta evidencia separada: '+$f)}
}
foreach ($modo in @('duplicado','conteos','radio','booleano','heredado_sin_campos')) {
 Invoke-Caso ('Registro inválido · '+$modo) {
  $d=New-Caso ('registro_'+$modo) -Conforme;$rs=Read-SedacJson (Join-Path $d 'REDONDEOS.json')
  switch ($modo) {
   'duplicado' {$rs=@($rs)+@($rs[0])}
   'conteos' {$rs[0].aristas_redondeadas=$rs[0].aristas_totales+1}
   'radio' {$rs[0].radio_mm=$rs[0].radio_mm*2}
   'booleano' {$rs[0].aplicado='true'}
   'heredado_sin_campos' {$rs[0].Remove('estado');$rs[0].Remove('aristas_totales');$rs[0].Remove('aristas_redondeadas')}
  }
  Write-CasoJson $rs (Join-Path $d 'REDONDEOS.json');$r=Invoke-Decision $d
  Assert-Cierre (-not $r.R2.cumple -and -not $r.aceptado) ('Debe bloquear el registro '+$modo)
  Assert-Cierre (-not (Test-Path (Join-Path $d 'ESTADO_OK.txt'))) 'No se acepta evidencia inválida'
 }
}
Invoke-Caso 'R3 ausente' {
 $d=New-Caso 'cribado_sin_campo' -Conforme;$c=Read-SedacJson (Join-Path $d 'RESULTADOS_PREDISENO.json');$c.Remove('cumple_cribado')
 Write-CasoJson $c (Join-Path $d 'RESULTADOS_PREDISENO.json');$r=Invoke-Decision $d
 Assert-Cierre (-not $r.R3.cumple -and -not $r.aceptado) 'El campo ausente debe bloquear'
}
Invoke-Caso 'R2 · interferencia por encima del límite existente' {
 $d=New-Caso 'interferencia' -Conforme
 Write-CasoJson @(@{pieza_1='caso_sintetico_A';pieza_2='caso_sintetico_B';volumen_mm3=0.001*2}) (Join-Path $d 'INTERFERENCIAS.json');$r=Invoke-Decision $d
 Assert-Cierre (-not $r.R2.cumple -and -not $r.aceptado) 'El solape superior al límite debe bloquear'
}
Invoke-Caso 'R2 · grados de libertad pendientes' {
 $d=New-Caso 'restriccion' -Conforme;$rs=Read-SedacJson (Join-Path $d 'RESTRICCIONES.json');$rs[0].traslaciones=1
 Write-CasoJson $rs (Join-Path $d 'RESTRICCIONES.json');$r=Invoke-Decision $d
 Assert-Cierre (-not $r.R2.cumple -and -not $r.aceptado) 'Una traslación pendiente debe bloquear'
}
Invoke-Caso 'R2 · registro de interferencias nulo' {
 $d=New-Caso 'interferencias_sin_evidencia' -Conforme
 'null' | Set-Content -LiteralPath (Join-Path $d 'INTERFERENCIAS.json') -Encoding UTF8
 $r=Invoke-Decision $d
 Assert-Cierre (-not $r.R2.cumple -and -not $r.aceptado) 'Un registro nulo no equivale a una lista vacía verificada'
}
Invoke-Caso 'R2 · resumen de masas incoherente' {
 $d=New-Caso 'masa' -Conforme;$res=Read-SedacJson (Join-Path $d 'RESUMEN_ENTREGA.json');$res.presupuesto_sistema_kg=$res.presupuesto_sistema_kg*2
 Write-CasoJson $res (Join-Path $d 'RESUMEN_ENTREGA.json');$r=Invoke-Decision $d
 Assert-Cierre (-not $r.R2.cumple -and -not $r.aceptado) 'La masa discrepante debe bloquear'
}
Invoke-Caso 'R1 · archivo generado ausente' {
 $d=New-Caso 'generacion_incompleta' -Conforme;$script:faltaGeneracion=$true
 try {$r=Invoke-Decision $d} finally {$script:faltaGeneracion=$false}
 Assert-Cierre (-not $r.R1.cumple -and $r.R2.cumple -and $r.R3.cumple -and -not $r.aceptado) 'La generación incompleta debe bloquear por sí sola'
}
Invoke-Caso 'Integración estática del constructor, sin ejecutarlo' {
 $ruta=Join-Path $soporte 'CONSTRUIR_P2_05.ps1';$texto=Get-Content -LiteralPath $ruta -Raw -Encoding UTF8
 $tokens=$null;$errores=$null;$null=[System.Management.Automation.Language.Parser]::ParseFile($ruta,[ref]$tokens,[ref]$errores)
 Assert-Cierre (@($errores).Count -eq 0) 'La sintaxis del constructor debe ser válida'
 Assert-Cierre ($texto.Contains(". (Join-Path `$base 'Soporte/cierre_p2_05.ps1')")) 'El constructor debe importar el mismo módulo que el banco'
 Assert-Cierre ($texto.IndexOf('Get-SedacCribado') -lt $texto.IndexOf('Add-Type')) 'R3 debe comprobarse antes de cargar Inventor'
 Assert-Cierre ($texto.Contains('Get-SedacRegistroReutilizado')) 'La reutilización debe exigir evidencia'
 Assert-Cierre ($texto.Contains('Test-SedacExportacion $sedacCierre -AceptarPendientes:$AceptarPendientes')) 'La opción debe usar la decisión común de borrador'
 Assert-Cierre ($texto.Contains("if (-not `$sedacCierre.aceptado) {throw 'Borrador con pendientes")) 'El borrador debe terminar con excepción'
 Assert-Cierre (-not $texto.Contains("Join-Path `$Salida 'ESTADO_OK.txt'")) 'El constructor no debe escribir un sello al margen del módulo'
}
$fallos=@($script:casos | Where-Object {-not $_.cumple})
$resumen=[pscustomobject]@{naturaleza='casos sintéticos de prueba; no son evidencia de entrega';interprete=$PSVersionTable.PSVersion.ToString();casos=$script:casos.ToArray();total_casos=$script:casos.Count;aserciones=$script:aserciones;fallos=$fallos.Count;inventor_ejecutado=$false;carpeta=$salidaAbsoluta}
Write-CasoJson $resumen (Join-Path $Salida 'RESULTADOS_PRUEBAS.json')
$resumen | Select-Object total_casos,aserciones,fallos,interprete,carpeta | ConvertTo-Json
if ($fallos.Count -gt 0) {throw ('Fallaron casos: '+(($fallos | ForEach-Object {$_.caso+': '+$_.error}) -join '; '))}
