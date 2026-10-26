#!/usr/bin/env pwsh
# verificar_mathcad.ps1 â€” abre la memoria generada en la instalacion Mathcad 15 de este equipo,
# la recalcula, coteja cada variable contra el control numerico, guarda el archivo final editable
# y exporta una copia HTML para revision.
#
# NO modifica el repositorio SEDAC_CAD: solo trabaja dentro de la carpeta del paquete documental.
$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$fuente = Join-Path $base 'Memoria_SEDAC_P204_MC01_FUENTE.xmcd'
$final = Join-Path $base 'Memoria_SEDAC_P204_MC01_EDITABLE.xmcd'
$html = Join-Path $base 'Memoria_SEDAC_P204_MC01.html'

try { $mc = [Runtime.InteropServices.Marshal]::GetActiveObject('Mathcad.Application') }
catch { $mc = New-Object -ComObject Mathcad.Application }
$mc.Visible = $true
Write-Output ('Mathcad ' + $mc.Version)

$ws = $mc.Worksheets.Open($fuente)
$ws.Recalculate()

$esperado = Import-Csv -LiteralPath (Join-Path $base 'VALORES_ESPERADOS_SI.csv')
$resultados = @(); $errores = @(); $noNumericos = @()
foreach ($p in $esperado) {
    $nombre = $p.variable
    $control = [double]$p.valor_SI
    try {
        $valor = $ws.GetValue($nombre)
        $real = [double]$valor.Real
        $unidad = [string]$valor.UnitString
        $rel = [Math]::Abs($real - $control) / [Math]::Max(1e-30, [Math]::Abs($control))
        $resultados += [pscustomobject]@{
            variable   = $nombre
            mathcad_SI = $real
            control_SI = $control
            unidad     = $unidad
            error_rel  = $rel
            coincide   = ($rel -lt 1e-9)
        }
    }
    catch {
        $noNumericos += [pscustomobject]@{ variable = $nombre; control = $control; error = $_.Exception.Message }
    }
}
$malas = @($resultados | Where-Object { -not $_.coincide })
Write-Output ('Variables numericas verificadas: ' + $resultados.Count + '; fuera de tolerancia: ' + $malas.Count)
if ($malas.Count -gt 0) { $malas | Format-Table -AutoSize | Out-String | Write-Output }
Write-Output ('Variables no numericas (booleanas): ' + $noNumericos.Count)

ConvertTo-Json -InputObject @($resultados) -Depth 5 |
    Set-Content -LiteralPath (Join-Path $base 'VERIFICACION_MATHCAD.json') -Encoding utf8
ConvertTo-Json -InputObject @($noNumericos) -Depth 5 |
    Set-Content -LiteralPath (Join-Path $base 'NO_NUMERICOS.json') -Encoding utf8

$ok = $ws.SaveAs($final, 20)
Write-Output ('SaveAs XMCD: ' + $ok)
$okHtml = $ws.SaveAs($html, 3)
Write-Output ('SaveAs HTML: ' + $okHtml)
Write-Output ('n_min = ' + $ws.GetValue('n_min').Real)
Write-Output ('Mmax = ' + $ws.GetValue('Mmax').Real)
$ws.Close($false)

Write-Output ('Resumen: ' + (Test-Path -LiteralPath $final) + ' / ' + (Test-Path -LiteralPath $html))
if ($malas.Count -gt 0) { throw 'Hay variables fuera de tolerancia' }


