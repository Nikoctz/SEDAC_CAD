$ErrorActionPreference='Stop'
$base='C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02'
$mc=New-Object -ComObject Mathcad.Application
$mc.Visible=$true
$ws=$mc.Worksheets.Open((Join-Path $base 'Soporte\fuente_memoria_MC01f.xmcd'))
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
foreach($region in $ws.Regions) {
 try {
  $mi=$region.MathInterface
  if ($mi -and $mi.HasError) {$errors+=[pscustomobject]@{region=$region.Tag;error=$mi.ErrorMsg}}
 } catch {}
}
ConvertTo-Json -InputObject @($results) -Depth 5 | Set-Content -LiteralPath (Join-Path $base 'Soporte\VERIFICACION_MATHCAD.json') -Encoding utf8
ConvertTo-Json -InputObject @($errors) -Depth 5 | Set-Content -LiteralPath (Join-Path $base 'Soporte\ERRORES_MATHCAD.json') -Encoding utf8
Write-Output ('Variables calculadas: '+$results.Count+'; errores: '+$errors.Count)
if ($errors.Count -gt 0) {$errors | ConvertTo-Json -Depth 5;throw 'Hay errores en Mathcad'}
if (@($results | Where-Object {-not $_.coincide}).Count -gt 0) {throw 'Diferencias con control numerico'}
$ws.SaveAs((Join-Path $base 'Memoria_SEDAC_P2_02_MC01_EDITABLE.xmcd'),20)
$ws.SaveAs((Join-Path $base 'Soporte\memoria_final.html'),3)
Write-Output ('Mathcad '+$mc.Version+' guardado. nR='+$ws.GetValue('nR').Real+' nFloor='+$ws.GetValue('nFloor').Real)

