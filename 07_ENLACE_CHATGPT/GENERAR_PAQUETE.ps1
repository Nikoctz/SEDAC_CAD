<#
    GENERAR_PAQUETE.ps1
    SEDAC_CAD / 07_ENLACE_CHATGPT

    Genera PAQUETE_CHATGPT.md: UN solo archivo autosuficiente para pegar en el
    proyecto ChatGPT de solo chat. Todo el contenido se LEE de los archivos del
    repositorio; nada se escribe a mano. Regenerar cada vez que cambie el estado.

    Uso:
      powershell -ExecutionPolicy Bypass -File .\07_ENLACE_CHATGPT\GENERAR_PAQUETE.ps1

    Salida:
      PAQUETE_CHATGPT.md      (UTF-8 sin BOM, listo para pegar)
      AVISO_PRIVACIDAD.txt    (solo si detecta rutas o marcas de este equipo)
#>
[CmdletBinding()]
param(
    [string]$Repositorio
)

$ErrorActionPreference = 'Stop'
$inv  = [System.Globalization.CultureInfo]::InvariantCulture

# Carpeta de este script. No sirve calcularla en el bloque param: en PowerShell 5.1
# $PSScriptRoot todavia esta vacio ahi dentro.
$aqui = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($aqui)) { $aqui = Split-Path -Parent $MyInvocation.MyCommand.Definition }
if ([string]::IsNullOrWhiteSpace($aqui)) { $aqui = (Get-Location).Path }
$aqui = (Resolve-Path -LiteralPath $aqui).Path

if ([string]::IsNullOrWhiteSpace($Repositorio)) { $Repositorio = Split-Path -Parent $aqui }
$raiz = (Resolve-Path -LiteralPath $Repositorio).Path
$salida = Join-Path $aqui 'PAQUETE_CHATGPT.md'

$lineas = New-Object 'System.Collections.Generic.List[string]'
function L([string]$t = '') { [void]$lineas.Add($t) }

function N($v) {
    if ($null -eq $v) { return 'pendiente' }
    if ($v -is [double] -or $v -is [single] -or $v -is [decimal]) {
        # 'R' da la representacion exacta y reversible: el numero del paquete es el del archivo
        return [string]::Format($inv, '{0:R}', [double]$v)
    }
    return [string]$v   # enteros y textos: tal cual
}

function K($v) {
    if ($null -eq $v) { return 'pendiente' }
    return ((N $v) + ' kg')
}

# Pega un documento literal bajando sus titulos un nivel, para que no se confundan
# con las secciones del paquete.
function Add-Cita([string]$texto) {
    if ([string]::IsNullOrWhiteSpace($texto)) { L 'pendiente'; return }
    foreach ($ln in ($texto -split "`r?`n")) {
        if ($ln -match '^#') { L ('#' + $ln) } else { L $ln }
    }
}

function Texto([string]$relativo) {
    $p = Join-Path $raiz $relativo
    if (-not (Test-Path -LiteralPath $p)) { return $null }
    return (Get-Content -LiteralPath $p -Raw -Encoding UTF8).Trim()
}

function Json([string]$rutaCompleta) {
    if (-not (Test-Path -LiteralPath $rutaCompleta)) { return $null }
    return ((Get-Content -LiteralPath $rutaCompleta -Raw -Encoding UTF8) | ConvertFrom-Json)
}

# ---------------------------------------------------------------- cabecera ----
$ahora = (Get-Date).ToString('yyyy-MM-dd HH:mm')
L '# PAQUETE DE CONTEXTO SEDAC'
L ''
L ('Generado: ' + $ahora + '  |  por: 07_ENLACE_CHATGPT/GENERAR_PAQUETE.ps1')
L 'Uso: pegar este archivo entero (o subirlo como documento del proyecto). No editar a mano.'
L ''
L 'Este documento lo ha escrito el repositorio SEDAC_CAD de este PC. Los numeros salen de'
L 'los archivos del proyecto, no de la memoria de nadie.'
L ''
L '---'
L ''

# ------------------------------------------------- instrucciones para ChatGPT --
L '## 0. Como quiero que trabajes con este documento'
L ''
L '1. Este documento es la version vigente. Si algo que recuerdes de conversaciones'
L '   anteriores contradice lo que aqui dice, manda este documento.'
L '2. Marca CADA afirmacion que hagas como **[hecho]**, **[calculo]**, **[supuesto]** o'
L '   **[hipotesis]**:'
L '   - **[hecho]** solo si lo respalda un archivo o comando citado aqui.'
L '   - **[calculo]** si es reproducible con una formula o un numero que aparezca aqui.'
L '   - **[supuesto]** si es un valor que se adopta sin medir.'
L '   - **[hipotesis]** si es una condicion aun no comprobada.'
L '3. Si falta un dato, escribe **pendiente**. No lo rellenes con un valor plausible.'
L '4. No declares seguridad, comodidad, resistencia ni cumplimiento normativo que no este'
L '   demostrado por un archivo, un ensayo o un calculo trazable.'
L '5. No inventes resultados de ensayos, FEA, propiedades de materiales ni normas.'
L '6. Distingue siempre lo comprobado de lo que falta por comprobar.'
L '7. Fuentes de cada cosa: el estado tecnico (masas, piezas, pendientes, numeros) sale de'
L '   este documento. Los requisitos y plazos del programa tambien los ves tu en mi espacio de'
L '   Notion; la version citada esta en la seccion 5. Si algo se contradice, no decidas: dime'
L '   el conflicto y que dice cada fuente.'
L '8. Si una pagina de Notion no te aparece, dilo. No la supongas ni la resumas de memoria.'
L '9. No reproduzcas datos personales de terceros (nombres, medidas corporales, salud, imagenes).'
L ''
L '---'
L ''

# ------------------------------------------------------------- estado vigente --
$estado = Texto 'ESTADO_ACTUAL.md'
L '## 1. Estado vigente (ESTADO_ACTUAL.md, literal)'
L ''
if ($estado) { Add-Cita $estado } else { L 'pendiente: no se encontro ESTADO_ACTUAL.md' }
L ''
L '---'
L ''

# ---------------------------------------------------------------- decisiones --
$dec = Texto 'DECISIONES.md'
L '## 2. Decisiones ya adoptadas (DECISIONES.md, literal)'
L ''
if ($dec) { Add-Cita $dec } else { L 'pendiente: no se encontro DECISIONES.md' }
L ''
L '---'
L ''

# ----------------------------------------------------------------- changelog --
$chl = Texto 'CHANGELOG_SEDAC.md'
L '## 3. Cambios registrados (CHANGELOG_SEDAC.md, literal)'
L ''
if ($chl) { Add-Cita $chl } else { L 'pendiente: no se encontro CHANGELOG_SEDAC.md' }
L ''
L '---'
L ''

# ------------------------------------------------- numeros de la ultima corrida
L '## 4. Numeros de la ultima construccion CAD (generados desde el repositorio)'
L ''
$iter = $null
$dirP2 = Join-Path $raiz '01_CAD\Prototipo_P2'
if (Test-Path -LiteralPath $dirP2) {
    $iter = Get-ChildItem -LiteralPath $dirP2 -Directory -Filter 'P2_05*' -ErrorAction SilentlyContinue |
        ForEach-Object { Get-ChildItem -LiteralPath (Join-Path $_.FullName 'Soporte\Iteraciones') -Directory -ErrorAction SilentlyContinue } |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'RESUMEN_ENTREGA.json') } |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
}

if ($iter) {
    $res = Json (Join-Path $iter.FullName 'RESUMEN_ENTREGA.json')
    $red = Json (Join-Path $iter.FullName 'REDONDEOS.json')
    $int = Json (Join-Path $iter.FullName 'INTERFERENCIAS.json')

    L ('- Carpeta de la corrida: ' + $iter.Name + '  (' + $iter.LastWriteTime.ToString('yyyy-MM-dd HH:mm') + ')')
    L ('- Version del resumen: ' + $res.version + '   fecha declarada: ' + $res.fecha)
    L ''
    L '| dato | valor |'
    L '|---|---|'
    L ('| masa rigida + protectores | ' + (K $res.masa_rigida_y_protectores_kg) + ' |')
    L ('| masa de referencias visuales (textiles provisionales) | ' + (K $res.masa_referencias_visuales_kg) + ' |')
    L ('| reserva textil | ' + (K $res.masa_arnes_textiles_kg) + ' |')
    L ('| reserva adicional | ' + (K $res.reserva_adicional_kg) + ' |')
    L ('| presupuesto del sistema | ' + (K $res.presupuesto_sistema_kg) + ' |')
    L ('| masa del sistema realmente medida | ' + (K $res.masa_sistema_medida_kg) + ' |')
    L ('| interferencias | ' + $res.interferencias + ' |')
    L ('| redondeos pendientes declarados | ' + $res.redondeos_pendientes + ' |')
    L ''

    if ($res.grupos) {
        L 'Masa por grupo:'
        L ''
        L '| grupo | kg |'
        L '|---|---|'
        foreach ($g in $res.grupos.PSObject.Properties) { L ('| ' + $g.Name + ' | ' + (N $g.Value) + ' |') }
        L ''
    }

    if ($red) {
        L 'Redondeos declarados por pieza (aristas con radio aplicado):'
        L ''
        L '| pieza | radio_mm | estado | redondeadas/total | criterio | pruebas de sondeo |'
        L '|---|---|---|---|---|---|'
        foreach ($r in @($red)) {
            L ('| ' + $r.pieza + ' | ' + (N $r.radio_mm) + ' | ' + $r.estado + ' | ' + $r.aristas_redondeadas + '/' + $r.aristas_totales + ' | ' + $r.criterio + ' | ' + $r.pruebas + ' |')
        }
        L ''
        L 'Nota: estado "parcial" significa que el redondeo pedido NO se aplico completo. En esa'
        L 'situacion el constructor se detiene a proposito y no escribe el sello ESTADO_OK.txt.'
        L ''
    }

    if ($int) {
        L ('Interferencias registradas (fichero INTERFERENCIAS.json): ' + @($int).Count)
        L ''
    }
} else {
    L 'pendiente: no hay ninguna corrida con RESUMEN_ENTREGA.json en'
    L '01_CAD/Prototipo_P2/P2_05_*/Soporte/Iteraciones/.'
    L ''
}
L '---'
L ''

# --------------------------------------------------- requisitos de programas
$req = Texto 'REQUISITOS_SEDAC.md'
L '## 5. Requisitos y plazos de los programas (REQUISITOS_SEDAC.md, literal)'
L ''
if ($req) { Add-Cita $req } else { L 'pendiente: no se encontro REQUISITOS_SEDAC.md' }
L ''
L '---'
L ''

# ------------------------------------------------------------------- preguntas
$preg = $null
$pPreg = Join-Path $aqui 'PREGUNTAS.md'
if (Test-Path -LiteralPath $pPreg) { $preg = (Get-Content -LiteralPath $pPreg -Raw -Encoding UTF8).Trim() }
L '## 6. Mis preguntas'
L ''
if ($preg) {
    Add-Cita $preg
    L ''
    L '(Si arriba solo aparece la plantilla, significa que no he escrito preguntas nuevas:'
    L 'responde entonces a lo que te pida en el mensaje.)'
} else {
    L 'pendiente: no se encontro 07_ENLACE_CHATGPT/PREGUNTAS.md'
}
L ''
L '---'
L ''

# ------------------------------------------------------------ contexto comun --
L '## 7. Contexto historico'
L ''
L '- CONTEXTO_SEDAC.md describe P0 y esta desactualizado respecto a P2.04. No se incluye aqui.'
L '  En caso de conflicto, manda ESTADO_ACTUAL.md (seccion 1).'
L '- Unidades del proyecto: milimetros. Escala maestra 1:1.'
L '- P2.04 es la base vigente; P2.05 no esta cerrado y es borrador de trabajo.'
L ''
L '---'
L ''

# ----------------------------------------------------- formato de la respuesta
L '## 8. Formato en que quiero tu respuesta'
L ''
L '1. Empieza con un resumen de 5 lineas como maximo.'
L '2. Despues, desarrolla con las marcas [hecho] / [calculo] / [supuesto] / [hipotesis]'
L '   en cada afirmacion.'
L '3. Si detectas una contradiccion entre dos partes de este documento, dilo aparte y'
L '   senala cual crees que es el dato bueno y por que.'
L '4. Termina con una seccion titulada exactamente PROPUESTA DE CAMBIO, redactada para'
L '   copiar y pegar en DECISIONES.md o ESTADO_ACTUAL.md, sin adornos.'
L ''

$texto = ($lineas -join "`r`n")

# ------------------------------------------------------------------- escribir -
$utf8 = New-Object System.Text.UTF8Encoding($false)   # UTF-8 sin BOM, limpio para pegar
[System.IO.File]::WriteAllText($salida, $texto, $utf8)

# ------------------------------------------------- revision de privacidad -----
$riesgo = @()
for ($i = 0; $i -lt $lineas.Count; $i++) {
    if ($lineas[$i] -match '[A-Za-z]:\\|\\Users\\|AppData|OneDrive|Nicol') {
        $riesgo += ('  L' + ($i + 1) + ': ' + $lineas[$i].Substring(0, [Math]::Min(110, $lineas[$i].Length)))
    }
}
$aviso = Join-Path $aqui 'AVISO_PRIVACIDAD.txt'
if ($riesgo.Count -gt 0) {
    $cab = 'El paquete contiene ' + $riesgo.Count + ' linea(s) con posibles rutas locales, marcas de este' + "`r`n" +
           'equipo o un nombre personal. Revisar antes de enviarlo.' + "`r`n" + "`r`n"
    Set-Content -LiteralPath $aviso -Value ($cab + ($riesgo -join "`r`n")) -Encoding UTF8
    Write-Warning ('Revisar privacidad: ' + $riesgo.Count + ' linea(s). Ver ' + $aviso)
} elseif (Test-Path -LiteralPath $aviso) {
    Remove-Item -LiteralPath $aviso -Force
}

Write-Host ''
Write-Host ('PAQUETE generado: ' + $salida)
Write-Host ('  lineas: ' + $lineas.Count + '   caracteres: ' + $texto.Length)
if ($riesgo.Count -gt 0) {
    Write-Host '  privacidad: REVISAR (hay rutas locales o nombres)'
} else {
    Write-Host '  privacidad: sin rutas locales ni marcas del equipo'
}
