param([string]$Carpeta)
$ErrorActionPreference='Stop'
if(-not $Carpeta){$Carpeta=Split-Path -Parent $PSScriptRoot}
$build=Join-Path $Carpeta 'Build'
$dest=Join-Path $Carpeta 'Cierre'
if(Test-Path -LiteralPath $dest){throw 'La carpeta Cierre ya existe; no se sobrescribe.'}
New-Item -ItemType Directory -Path $dest | Out-Null
. (Join-Path $PSScriptRoot 'cierre_p2_05.ps1')
$script:SedacPrefijoIAM='SEDAC_OPT_20261023'
$c=Get-SedacCierre $build (Join-Path $build 'RESULTADOS_PREDISENO.json')
Write-SedacCierre $c $dest
Write-Output ('R1='+$c.R1.cumple+' R2='+$c.R2.cumple+' R3='+$c.R3.cumple+' aceptado='+$c.aceptado)
foreach($m in @($c.R1.motivos)){Write-Output ('R1 motivo: '+$m)}
foreach($m in @($c.R2.motivos)){Write-Output ('R2 motivo: '+$m)}
