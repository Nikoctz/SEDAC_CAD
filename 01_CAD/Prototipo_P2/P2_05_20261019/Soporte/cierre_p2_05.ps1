# Cierre documental y analítico, 2026-10-22. Este módulo no llama a Inventor.
function Read-SedacJson([string]$Ruta) {
 $texto=Get-Content -Raw -LiteralPath $Ruta -Encoding UTF8
 if ((Get-Command ConvertFrom-Json).Parameters.ContainsKey('AsHashtable')) {
  return ,($texto | ConvertFrom-Json -AsHashtable -NoEnumerate)
 }
 # Windows PowerShell 5.1: conservar las claves distintas z/Z del cálculo.
 Add-Type -AssemblyName System.Web.Extensions
 $lector=New-Object System.Web.Script.Serialization.JavaScriptSerializer
 $lector.MaxJsonLength=[int]::MaxValue
 return ,($lector.DeserializeObject($texto))
}
function Read-SedacEvidencia([string]$Ruta,$Errores) {
 try {return ,(Read-SedacJson $Ruta)} catch {$Errores.Add('Evidencia ausente o ilegible: '+$Ruta+'; '+$_.Exception.Message);return $null}
}
function Test-SedacNumero($Valor) {
 if ($null -eq $Valor -or $Valor -is [bool] -or $Valor -is [string]) {return $false}
 if (-not ($Valor -is [int] -or $Valor -is [long] -or $Valor -is [double] -or $Valor -is [decimal] -or $Valor -is [single])) {return $false}
 return (-not [double]::IsNaN([double]$Valor) -and -not [double]::IsInfinity([double]$Valor))
}
function Test-SedacIgualNumero($A,$B) {
 if (-not (Test-SedacNumero $A) -or -not (Test-SedacNumero $B)) {return $false}
 # Tolerancia de serialización aritmética; no es una tolerancia de fabricación.
 return ([Math]::Abs([double]$A-[double]$B) -le 1e-9*[Math]::Max(1,[Math]::Max([Math]::Abs([double]$A),[Math]::Abs([double]$B))))
}
function Test-SedacLista($Dato) {return ($Dato -is [System.Array] -or $Dato -is [System.Collections.IList])}
function Get-SedacErroresRedondeo($Pieza,$Registro) {
 $errores=New-Object 'System.Collections.Generic.List[string]'
 if ($null -eq $Registro -or $Registro.pieza -cne $Pieza.name) {$errores.Add('Pieza ausente o distinta de la solicitada')}
 if (-not (Test-SedacNumero $Registro.radio_mm) -or $Registro.radio_mm -ne $Pieza.edge_radius) {$errores.Add('Radio ausente o distinto del solicitado')}
 $conteos=(Test-SedacNumero $Registro.aristas_totales) -and (Test-SedacNumero $Registro.aristas_redondeadas)
 if ($conteos) {
  $t=[double]$Registro.aristas_totales;$r=[double]$Registro.aristas_redondeadas
  $conteos=$t -gt 0 -and $t -eq [Math]::Floor($t) -and $r -ge 0 -and $r -eq [Math]::Floor($r) -and $r -le $t
 }
 if (-not $conteos) {$errores.Add('Conteos de aristas ausentes o inválidos')}
 if ($Registro.aplicado -isnot [bool]) {$errores.Add('El campo aplicado debe ser booleano')}
 if ($Registro.estado -notin @('total','parcial','no_aplicado')) {$errores.Add('Estado sin evidencia válida: '+$Registro.estado)}
 if ($conteos -and $Registro.aplicado -is [bool]) {
  if ($Registro.estado -eq 'total' -and (-not $Registro.aplicado -or $r -ne $t)) {$errores.Add('Estado total incompatible con aplicado o conteos')}
  if ($Registro.estado -eq 'parcial' -and ($Registro.aplicado -or $r -le 0 -or $r -ge $t)) {$errores.Add('Estado parcial incompatible con aplicado o conteos')}
  if ($Registro.estado -eq 'no_aplicado' -and ($Registro.aplicado -or $r -ne 0)) {$errores.Add('Estado no_aplicado incompatible con aplicado o conteos')}
 }
 return $errores.ToArray()
}
function Get-SedacRegistroReutilizado($Pieza,$Registros) {
 $coinciden=@($Registros | Where-Object {$null -ne $_ -and $_.pieza -ceq $Pieza.name})
 $errores=@();if ($coinciden.Count -eq 1) {$errores=@(Get-SedacErroresRedondeo $Pieza $coinciden[0])}
 if ($coinciden.Count -eq 1 -and $errores.Count -eq 0) {return $coinciden[0]}
 $estado='registro_invalido';if ($coinciden.Count -eq 0) {$estado='sin_registro'}
 return [pscustomobject]@{pieza=$Pieza.name;radio_mm=$Pieza.edge_radius;aristas_totales=$null;aristas_redondeadas=$null;estado=$estado;aplicado=$false;registros_encontrados=$coinciden.Count;error=('Ausencia de evidencia válida al reutilizar. Se exige exactamente un registro; encontrados: '+$coinciden.Count+'. '+($errores -join '; '))}
}
function Get-SedacCribado([string]$Ruta,$Modelo) {
 $errores=New-Object 'System.Collections.Generic.List[string]'
 $r=Read-SedacEvidencia $Ruta $errores
 if ($null -ne $r -and $r.version -cne $Modelo.version) {$errores.Add('La versión del cálculo no coincide con la del modelo')}
 $umbral=$Modelo.parameters.cargas.margen_objetivo
 $limite=$Modelo.parameters.cargas.flecha_limite_mm
 if (-not (Test-SedacNumero $umbral) -or $umbral -le 0) {$errores.Add('Falta el margen objetivo del modelo')}
 if ($null -eq $r -or $r.cumple_cribado -isnot [bool] -or -not $r.cumple_cribado) {$errores.Add('cumple_cribado falta, no es booleano o es false')}
 if (-not (Test-SedacNumero $r.minimo_margen) -or $r.minimo_margen -lt $umbral) {$errores.Add('Margen mínimo insuficiente o ausente: '+$r.minimo_margen+'; umbral del modelo: '+$umbral)}
 $verificaciones=@($r.verificaciones | Where-Object {$null -ne $_})
 if ($verificaciones.Count -eq 0) {$errores.Add('No hay verificaciones analíticas documentadas')}
 foreach ($v in $verificaciones) {
  if ($v.cumple -isnot [bool] -or -not $v.cumple -or -not (Test-SedacNumero $v.margen) -or $v.margen -lt $umbral -or -not (Test-SedacIgualNumero $v.umbral $umbral)) {$errores.Add('Verificación incumplida o inválida: '+$v.nombre+'; margen='+$v.margen+'; umbral='+$v.umbral)}
 }
 if ($verificaciones.Count -gt 0) {
  $margenes=@($verificaciones | Where-Object {Test-SedacNumero $_.margen} | ForEach-Object {[double]$_.margen})
  if ($margenes.Count -eq $verificaciones.Count -and -not (Test-SedacIgualNumero $r.minimo_margen (($margenes | Measure-Object -Minimum).Minimum))) {$errores.Add('minimo_margen no coincide con las verificaciones')}
 }
 if (-not (Test-SedacNumero $r.cierre_residual_junta_N) -or $r.cierre_residual_junta_N -le 0) {$errores.Add('Cierre residual de junta no positivo o ausente: '+$r.cierre_residual_junta_N)}
 if (-not (Test-SedacNumero $limite) -or -not (Test-SedacNumero $r.flecha_envolvente_mm) -or $r.flecha_envolvente_mm -lt 0 -or $r.flecha_envolvente_mm -gt $limite) {$errores.Add('Flecha ausente, inválida o superior al límite del modelo: '+$r.flecha_envolvente_mm+'; límite='+$limite)}
 if ([string]::IsNullOrWhiteSpace([string]$r.alcance)) {$errores.Add('Falta el alcance del cálculo')}
 return [pscustomobject]@{resultado='R3';nombre='Cribado analítico cumplido';etiqueta='cálculo';cumple=($errores.Count -eq 0);evidencia=$Ruta;minimo_margen=$r.minimo_margen;umbral=$umbral;alcance=$r.alcance;motivos=@($errores.ToArray())}
}
function Get-SedacArchivoGenerado([string]$Ruta) {
 $existe=Test-Path -LiteralPath $Ruta -PathType Leaf
 $bytes=$null;if ($existe) {$bytes=(Get-Item -LiteralPath $Ruta).Length}
 return [pscustomobject]@{ruta=$Ruta;existe=$existe;bytes=$bytes}
}
function Test-SedacExportacion($Cierre,[switch]$AceptarPendientes) {
 # Aceptar pendientes solo permite exportar el borrador; nunca cambia la aceptación.
 return ($Cierre.R3.cumple -and ($Cierre.R2.cumple -or $AceptarPendientes))
}
function Get-SedacCierre([string]$Carpeta,[string]$RutaCalculo) {
 $e1=New-Object 'System.Collections.Generic.List[string]';$e2=New-Object 'System.Collections.Generic.List[string]'
 $modelo=Read-SedacEvidencia (Join-Path $Carpeta 'MODELO_API.json') $e1
 $piezas=@($modelo.parts | Where-Object {$null -ne $_})
 if ($piezas.Count -eq 0) {$e1.Add('El modelo no contiene piezas');$e2.Add('No se pueden determinar las piezas y evidencias esperadas')}
 $nombres=@($piezas | ForEach-Object {$_.name})
 if (@($nombres | Sort-Object -Unique).Count -ne $nombres.Count) {$e2.Add('Hay nombres de pieza duplicados en el modelo')}
 $version=([string]$modelo.version).Replace('.','_')
 $archivos=@($piezas | ForEach-Object {$_.name+'.ipt'})+@(('SEDAC_'+$version+'.iam'),('SEDAC_'+$version+'_REVISION.step'),'VISTA_FRENTE.png','VISTA_ESPALDA.png','VISTA_ESTRUCTURA.png')
 $generados=@(foreach ($archivo in $archivos) {
  $dato=Get-SedacArchivoGenerado (Join-Path $Carpeta $archivo)
  if (-not $dato.existe -or -not (Test-SedacNumero $dato.bytes) -or $dato.bytes -le 0) {$e1.Add('Archivo generado ausente o vacío: '+$archivo)}
  $dato
 })
 $red=Read-SedacEvidencia (Join-Path $Carpeta 'REDONDEOS.json') $e2
 if (-not (Test-SedacLista $red)) {$e2.Add('REDONDEOS.json debe contener una lista, no null ni otro objeto')}
 $pedidas=@($piezas | Where-Object {$_.edge_radius})
 $pendientes=0
 foreach ($p in $pedidas) {
  $reg=@($red | Where-Object {$null -ne $_ -and $_.pieza -ceq $p.name})
  if ($reg.Count -ne 1) {$e2.Add('Redondeo '+$p.name+': se exige exactamente un registro; encontrados '+$reg.Count);$pendientes++;continue}
  $fallos=@(Get-SedacErroresRedondeo $p $reg[0])
  foreach ($fallo in $fallos) {$e2.Add('Redondeo '+$p.name+': '+$fallo)}
  if ($fallos.Count -gt 0 -or $reg[0].aplicado -ne $true) {$pendientes++;$e2.Add('Redondeo pendiente o sin evidencia: '+$p.name+'; estado='+$reg[0].estado)}
 }
 foreach ($reg in @($red | Where-Object {$null -ne $_})) {
  if (@($pedidas | Where-Object {$_.name -ceq $reg.pieza}).Count -ne 1) {$e2.Add('Registro de redondeo sin pieza solicitada inequívoca: '+$reg.pieza)}
 }
 $inter=Read-SedacEvidencia (Join-Path $Carpeta 'INTERFERENCIAS.json') $e2
 if (-not (Test-SedacLista $inter)) {$e2.Add('INTERFERENCIAS.json debe contener una lista; null no acredita ausencia de interferencias')}
 foreach ($v in @($inter | Where-Object {$null -ne $_})) {
  if (-not (Test-SedacNumero $v.volumen_mm3) -or $v.volumen_mm3 -lt 0 -or $v.volumen_mm3 -gt 0.001) {$e2.Add('Interferencia inválida o superior a 0,001 mm³: '+$v.pieza_1+' / '+$v.pieza_2+'; volumen='+$v.volumen_mm3)}
 }
 $restr=Read-SedacEvidencia (Join-Path $Carpeta 'RESTRICCIONES.json') $e2
 if (-not (Test-SedacLista $restr)) {$e2.Add('RESTRICCIONES.json debe contener una lista')}
 $esperadas=@($modelo.instances | Where-Object {$null -ne $_ -and $_.name -cne 'Interfaz_lumbar_aligerada'})
 if ($esperadas.Count -eq 0) {$e2.Add('No hay ocurrencias posicionadas verificables en el modelo')}
 foreach ($ins in $esperadas) {
  $reg=@($restr | Where-Object {$null -ne $_ -and $_.ocurrencia -ceq $ins.name})
  if ($reg.Count -ne 1) {$e2.Add('Restricción ausente o duplicada: '+$ins.name);continue}
  $v=$reg[0]
  if (-not (Test-SedacNumero $v.traslaciones) -or -not (Test-SedacNumero $v.rotaciones) -or $v.traslaciones -ne 0 -or $v.rotaciones -ne 0 -or -not (Test-SedacNumero $v.error_transformacion) -or $v.error_transformacion -lt 0 -or $v.error_transformacion -gt 1e-6) {$e2.Add('Grados de libertad o transformación pendientes: '+$ins.name)}
 }
 foreach ($v in @($restr | Where-Object {$null -ne $_})) {if (@($esperadas | Where-Object {$_.name -ceq $v.ocurrencia}).Count -ne 1) {$e2.Add('Registro de restricción inesperado: '+$v.ocurrencia)}}
 $masas=Read-SedacEvidencia (Join-Path $Carpeta 'MASAS_CAD.json') $e2
 if (-not (Test-SedacLista $masas)) {$e2.Add('MASAS_CAD.json debe contener una lista')}
 $resumen=Read-SedacEvidencia (Join-Path $Carpeta 'RESUMEN_ENTREGA.json') $e2
 if ($null -ne $resumen -and $resumen.version -cne $modelo.version) {$e2.Add('La versión del resumen no coincide con la del modelo')}
 $rigida=0.0;$visual=0.0;$grupos=@{}
 foreach ($p in $piezas) {
  $reg=@($masas | Where-Object {$null -ne $_ -and $_.pieza -ceq $p.name})
  if ($reg.Count -ne 1) {$e2.Add('Masa ausente o duplicada: '+$p.name);continue}
  $v=$reg[0];$cantidad=@($modelo.instances | Where-Object {$_.part -ceq $p.name}).Count
  if (-not (Test-SedacNumero $v.masa_candidata_kg) -or $v.masa_candidata_kg -lt 0 -or -not (Test-SedacNumero $v.cantidad) -or $v.cantidad -ne $cantidad -or $v.referencia -isnot [bool] -or [string]::IsNullOrWhiteSpace([string]$v.grupo)) {$e2.Add('Registro de masa inválido: '+$p.name);continue}
  $peso=[double]$v.masa_candidata_kg*[double]$v.cantidad
  if ($v.referencia) {$visual+=$peso} else {$rigida+=$peso;$g=[string]$v.grupo;if (-not $grupos.ContainsKey($g)) {$grupos[$g]=0.0};$grupos[$g]+=$peso}
 }
 foreach ($v in @($masas | Where-Object {$null -ne $_})) {if (@($piezas | Where-Object {$_.name -ceq $v.pieza}).Count -ne 1) {$e2.Add('Registro de masa inesperado: '+$v.pieza)}}
 $textil=$modelo.parameters.reservas_masa.masa_presupuesto_textil_kg;$reserva=$modelo.parameters.reservas_masa.masa_reserva_kg
 if (-not (Test-SedacNumero $textil) -or -not (Test-SedacNumero $reserva)) {$e2.Add('Reservas de masa ausentes o inválidas en el modelo')}
 $comparar=@{masa_rigida_y_protectores_kg=$rigida;masa_referencias_visuales_kg=$visual;masa_arnes_textiles_kg=$textil;reserva_adicional_kg=$reserva;presupuesto_sistema_kg=($rigida+[double]$textil+[double]$reserva);redondeos_pendientes=$pendientes;interferencias=@($inter | Where-Object {$null -ne $_}).Count}
 foreach ($clave in $comparar.Keys) {if (-not (Test-SedacIgualNumero $resumen.$clave $comparar[$clave])) {$e2.Add('Resumen de masa/coherencia discrepante: '+$clave+'; registrado='+$resumen.$clave+'; derivado='+$comparar[$clave])}}
 foreach ($g in $grupos.Keys) {if (-not (Test-SedacIgualNumero $resumen.grupos.$g $grupos[$g])) {$e2.Add('Subtotal de grupo discrepante: '+$g)}}
 foreach ($g in $resumen.grupos.Keys) {if (-not $grupos.ContainsKey($g)) {$e2.Add('Grupo del resumen sin masas que lo respalden: '+$g)}}
 $r1=[pscustomobject]@{resultado='R1';nombre='Generación terminada';etiqueta='hecho';cumple=($e1.Count -eq 0);archivos=$generados;alcance='Presencia y tamaño de archivos generados; no reinspección del CAD nativo.';motivos=@($e1.ToArray())}
 $r2=[pscustomobject]@{resultado='R2';nombre='Coherencia comprobada';etiqueta='hecho';cumple=($e2.Count -eq 0);redondeos_solicitados=$pedidas.Count;redondeos_pendientes=$pendientes;limite_interferencia_mm3=0.001;limite_error_transformacion=1e-6;tolerancia_aritmetica_relativa=1e-9;masa_rigida_derivada_kg=$rigida;evidencia=@('MODELO_API.json','REDONDEOS.json','INTERFERENCIAS.json','RESTRICCIONES.json','MASAS_CAD.json','RESUMEN_ENTREGA.json');motivos=@($e2.ToArray())}
 $r3=Get-SedacCribado $RutaCalculo $modelo
 return [pscustomobject]@{version=$modelo.version;aceptado=($r1.cumple -and $r2.cumple -and $r3.cumple);R1=$r1;R2=$r2;R3=$r3;alcance='Ninguno de los tres acredita el comportamiento físico del producto (textil, contacto, abrasión, ergonomía, fatiga, seguridad).';clasificacion_funcional='pendiente; D-12. Radio de 0,5 mm: propuesta sin ensayo de desgaste.'}
}
function Write-SedacCierre($Cierre,[string]$Carpeta,[switch]$SoloResultados,[switch]$CasoSintetico) {
 $aviso='';if ($CasoSintetico) {$aviso="casos sintéticos de prueba; no son evidencia de entrega`n"}
 $naturaleza='registro_de_ejecucion';if ($CasoSintetico) {$naturaleza='caso_sintetico'}
 $Cierre | Add-Member -NotePropertyName naturaleza -NotePropertyValue $naturaleza -Force
 $nombresEstado=@{R1='GENERACION';R2='COHERENCIA';R3='CRIBADO'}
 foreach ($nombre in @('R1','R2','R3')) {
  $ruta=Join-Path $Carpeta ($nombre+'_'+$nombresEstado[$nombre]+'.json')
  [pscustomobject]@{naturaleza=$naturaleza;resultado=$Cierre.$nombre;alcance=$Cierre.alcance} | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $ruta -Encoding UTF8
 }
 $Cierre | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $Carpeta 'CIERRE.json') -Encoding UTF8
 if ($SoloResultados) {return}
 $lineas=@($aviso+'hecho: cierre documental y analítico de '+$Cierre.version)
 foreach ($nombre in @('R1','R2','R3')) {$r=$Cierre.$nombre;$lineas+=($r.etiqueta+': '+$nombre+' · '+$r.nombre+'; cumple='+$r.cumple);$lineas+=@($r.motivos | ForEach-Object {'  - '+$_})}
 $lineas+=@('Evidencia: R1_GENERACION.json, R2_COHERENCIA.json, R3_CRIBADO.json y CIERRE.json.','Cribado condicionado; no validación de uso.',$Cierre.alcance,'pendiente: clasificación funcional A/B/C (D-12); radio de 0,5 mm propuesto sin ensayo de desgaste.')
 if ($Cierre.aceptado) {
  if ((Test-Path -LiteralPath (Join-Path $Carpeta 'ERROR.txt')) -or (Test-Path -LiteralPath (Join-Path $Carpeta 'ESTADO_BORRADOR.txt'))) {throw 'No se acepta una carpeta que ya registra error o borrador; usar una salida nueva.'}
  $lineas | Set-Content -LiteralPath (Join-Path $Carpeta 'ESTADO_OK.txt') -Encoding UTF8
 } else {
  @($aviso+'no es una entrega aceptada')+$lineas | Set-Content -LiteralPath (Join-Path $Carpeta 'ESTADO_BORRADOR.txt') -Encoding UTF8
  $lineas | Set-Content -LiteralPath (Join-Path $Carpeta 'ERROR.txt') -Encoding UTF8
  if (-not $Cierre.R3.cumple) {@($aviso+'cálculo: incumplimiento del cribado condicionado')+@($Cierre.R3.motivos) | Set-Content -LiteralPath (Join-Path $Carpeta 'INCUMPLIMIENTO_CRIBADO.txt') -Encoding UTF8}
 }
}
