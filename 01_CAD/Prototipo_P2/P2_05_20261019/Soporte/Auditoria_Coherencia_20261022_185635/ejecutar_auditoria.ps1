param()
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) {
    throw 'Invocar este archivo con C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe (5.1).'
}
$env:PYTHONIOENCODING = 'utf-8'
$sedacPython = 'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$sedacSalida = Join-Path $PSScriptRoot ('Ejecucion_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))
$sedacResultado = & $sedacPython -B (Join-Path $PSScriptRoot 'auditar_coherencia.py') --salida $sedacSalida --powershell $PSVersionTable.PSVersion.ToString() 2>&1
$sedacRetorno = $LASTEXITCODE
if (Test-Path -LiteralPath $sedacSalida) {
    [IO.File]::WriteAllText((Join-Path $sedacSalida 'SALIDA_AUDITORIA.txt'), ($sedacResultado -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
    $sedacRegistro = [ordered]@{
        etiqueta = 'hecho'
        fecha = (Get-Date).ToString('o')
        version = $PSVersionTable.PSVersion.ToString()
        ejecutable = (Get-Process -Id $PID).Path
        invocacion = $MyInvocation.MyCommand.Path
        salida = $sedacSalida
        retorno_python = $sedacRetorno
        alcance = 'Auditoria AST y generador JSON; sin Inventor ni calculador'
    }
    [IO.File]::WriteAllText((Join-Path $sedacSalida 'REGISTRO_ENTORNO_POWERSHELL.json'), ($sedacRegistro | ConvertTo-Json -Depth 6), [Text.UTF8Encoding]::new($false))
}
Write-Output $sedacResultado
Write-Output $sedacSalida
if ($sedacRetorno -ne 0) { throw ('La auditoria termino con codigo ' + $sedacRetorno) }
