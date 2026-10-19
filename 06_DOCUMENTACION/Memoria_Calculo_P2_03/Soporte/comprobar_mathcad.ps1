$ErrorActionPreference='Stop'
$base='C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_03'
try {$mc=[Runtime.InteropServices.Marshal]::GetActiveObject('Mathcad.Application')} catch {$mc=New-Object -ComObject Mathcad.Application}
$mc.Visible=$true
$ws=$mc.Worksheets.Open((Join-Path $base 'Soporte\fuente_MC02d.xmcd'))
$ws.Recalculate()
$expected=Get-Content -Raw -LiteralPath (Join-Path $base 'Soporte\VALORES_ESPERADOS_SI.json') | ConvertFrom-Json
$results=@();$errors=@()
foreach($p in $expected) {
 try {
  $actual=[double]$ws.GetValue($p.Name).Real
  $rel=[Math]::Abs($actual-[double]$p.Value)/[Math]::Max(1e-12,[Math]::Abs([double]$p.Value))
  $results+=[pscustomobject]@{variable=$p.Name;valor_mathcad_SI=$actual;valor_control_SI=$p.Value;error_relativo=$rel;coincide=($rel -lt 1e-8)}
 } catch {$errors+=[pscustomobject]@{variable=$p.Name;error=$_.ToString()}}
}
ConvertTo-Json -InputObject @($results) -Depth 5 | Set-Content -LiteralPath (Join-Path $base 'Soporte\VERIFICACION_MATHCAD.json') -Encoding utf8
ConvertTo-Json -InputObject @($errors) -Depth 5 | Set-Content -LiteralPath (Join-Path $base 'Soporte\ERRORES_MATHCAD.json') -Encoding utf8
Write-Output ('Variables calculadas: '+$results.Count+'; errores: '+$errors.Count)
if ($errors.Count -gt 0) {$errors | ConvertTo-Json -Depth 5;throw 'Hay errores en Mathcad'}
if (@($results | Where-Object {-not $_.coincide}).Count -gt 0) {throw 'Diferencias con control numerico'}
$ok=$ws.SaveAs((Join-Path $base 'Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd'),20)
Write-Output ('SaveAs XMCD: '+$ok)
if(-not (Test-Path -LiteralPath (Join-Path $base 'Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd'))){throw 'No se guardo la memoria final'}
$okHTML=$ws.SaveAs((Join-Path $base 'Soporte\memoria_MC02_final.html'),3)
Write-Output ('SaveAs HTML: '+$okHTML)
Write-Output ('Mathcad '+$mc.Version+' guardado. nRail='+$ws.GetValue('nRail').Real+' nFloor='+$ws.GetValue('nFloor').Real)


