# Banco de cierre P2.05 — 2026-10-22

**casos sintéticos de prueba; no son evidencia de entrega**

## Alcance y procedencia

**hecho:** el banco importa `Soporte/cierre_p2_05.ps1`, exactamente el módulo que utiliza `CONSTRUIR_P2_05.ps1`. No ejecuta el constructor, no carga su Interop, no abre Inventor y no crea archivos `.ipt`, `.iam`, `.step`, `.stl` ni `.3mf`.

**hecho:** las copias de entrada proceden de `Soporte/Iteraciones/Nueva_20261019_060807/` y del JSON histórico de `Calculos/`. Solo se modifican las copias dentro de carpetas nuevas de `Ejecuciones/`. No se toca la evidencia original.

**supuesto sintético de prueba:** se sustituye en memoria `Get-SedacArchivoGenerado` para simular la presencia de archivos completos, utilizando tamaños de archivos ya existentes de la entrega P2.04. Esto permite aislar la decisión de cierre sin fabricar archivos CAD ficticios. El origen de cada tamaño y la marca `simulado:true` quedan en R1. El caso D cambia en la copia de redondeos los estados/conteos a total y ajusta el contador del resumen; no representa un redondeo realmente ejecutado ni una masa física posterior a ese acabado.

## Casos y resultado exigido

| Caso | Entrada | Decisión exigida |
|---|---|---|
| A | Lumbar parcial 236/472 real, con generación simulada | R2 falso; borrador y error; ningún `ESTADO_OK`, incluso con `AceptarPendientes` |
| B | Registro lumbar ausente al reutilizar | `sin_registro`, conteos desconocidos `null`, R2 falso y sin aceptación |
| C | `cumple_cribado=false` y verificación incumplida en copia | R3 falso, diagnóstico con nombre y margen; la opción de pendientes tampoco permite exportar |
| D | Registros conformes sintéticos, generación simulada y cribado verdadero | R1+R2+R3, sello **sintético** con alcance literal; no es evidencia de entrega |

**hecho:** también se prueban registros duplicados, conteos imposibles, radio distinto, booleano como texto, registro heredado sin campos, ausencia de `cumple_cribado`, interferencia superior al umbral, grados de libertad pendientes, JSON de interferencias `null`, presupuesto de masa incoherente y generación incompleta. La prueba estática comprueba sintaxis e integración del constructor, sin ejecutarlo.

## Comandos reproducibles desde la raíz del repositorio

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Pruebas\cierre\verificar_cierre.ps1
```

En PowerShell 7:

```powershell
& .\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Pruebas\cierre\verificar_cierre.ps1
```

**hecho:** cada ejecución crea una carpeta nueva con fecha. Una salida existente se rechaza sin borrar ni sobrescribir sus evidencias. Cada caso contiene `CASO_SINTETICO.txt`; los ficheros de estado, R1/R2/R3 y el resumen también indican su naturaleza sintética. Un fallo del banco termina con excepción y código de salida distinto de cero; los casos bloqueados esperados se consideran pruebas aprobadas cuando no obtienen aceptación.

La comparación del cálculo se hace con el intérprete con numpy configurado en el constructor:

```powershell
$python = 'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$banco = '.\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Pruebas\cierre'
$destino = Join-Path $banco ('Ejecuciones/Calculo_'+(Get-Date -Format 'yyyyMMdd_HHmmss_fff'))
New-Item -ItemType Directory -Path $destino | Out-Null
& $python -B (Join-Path $banco 'verificar_calculo.py') --salida (Join-Path $destino 'VERIFICACION_CALCULO.json')
```

**hecho:** este verificador obtiene el script previo desde Git (solo lectura), ejecuta en memoria el tramo que construye `result`, omite `mkdir` y todas las escrituras originales, y compara el diccionario anterior con el actual sin `situacion_de_carga`. También comprueba la salida `print` y el alcance. No regenera `Calculos/`.

## Ejecuciones conservadas

- **hecho:** PowerShell 7.6.5, `Ejecuciones/Nueva_20261022_182113_260/RESULTADOS_PRUEBAS.json`: **16 casos, 46 aserciones, 0 fallos**.
- **hecho:** Windows PowerShell 5.1.26100.9711, `Ejecuciones/Nueva_20261022_182110_520/RESULTADOS_PRUEBAS.json`: **16 casos, 46 aserciones, 0 fallos**.
- **hecho:** `Ejecuciones/Calculo_20261022_181742_727/VERIFICACION_CALCULO.json` contiene la comprobación en memoria. El resultado documenta las 15 verificaciones numéricas idénticas y las 26 magnitudes trazadas.
- **hecho:** la primera ejecución `Nueva_20261022_181620_622` conserva un fallo del propio preparador B: al filtrar directamente la salida no enumerada del lector, no se retiraba el registro. Se corrigió el preparador separando lectura y filtrado; no fue un resultado de Inventor ni un cambio numérico. Las corridas posteriores de 15 casos se conservan como evidencia intermedia; las finales son las de 16 casos indicadas arriba.

**pendiente:** corrida nativa futura, clasificación A/B/C y ensayos del producto. El caso D aprobado no cierra la iteración P2.05.
