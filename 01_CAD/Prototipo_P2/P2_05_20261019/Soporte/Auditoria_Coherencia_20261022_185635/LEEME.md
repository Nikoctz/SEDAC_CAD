# Uso de la auditoría de coherencia P2.05

**hecho:** fuentes en lectura. Solo se ejecuta el generador descriptivo; no se ejecutan calcular_p2_05.py, el constructor ni Inventor. No modifica parámetros, ecuaciones, CAD ni decisiones. Unidades geométricas mm; propiedades/cargas conservan las unidades indicadas en sus tablas.

## Reproducir A–D en Windows PowerShell 5.1

Desde cualquier terminal PowerShell:

```powershell
& 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635\ejecutar_auditoria.ps1'
```

**hecho:** el archivo exige versión 5.1, captura versión y ruta del proceso real, guarda stdout y retorno, y elige una carpeta nueva. La terminal de la herramienta inició 7.6.5 incluso al solicitar powershell.exe; por eso las dos exploraciones iniciales registran 7.6.5. No se presentan como ejecuciones de 5.1. La ejecución final se invoca como proceso hijo por ruta absoluta y guarda `REGISTRO_ENTORNO_POWERSHELL.json`.

**hecho:** `auditar_coherencia.py` usa la biblioteca estándar de Python disponible. Hace lectura AST y traza de lecturas con los mismos valores en memoria. Omite las escrituras del tramo instrumentado y compara su resultado con una ejecución del generador original en una carpeta nueva. No perturba parámetros. `informe_coherencia.py` produce el informe desde esos resultados. La auditoría de claves es específica de los alias y estructura actuales de estos generadores; cambios futuros de arquitectura requieren revisar el auditor.

**hecho:** cada repetición conserva sus resultados y reescribe únicamente el informe propio `AUDITORIA.md` con la ejecución más reciente. No actualiza el LEEME del proyecto ni el changelog automáticamente. No borra corridas.

## Archivos guardados

- `AUDITORIA.md`: informe único con A–D, hallazgos, líneas de fuente y propuestas priorizadas.
- `Ejecucion_*/RESULTADOS.json`: datos completos; huellas de fuentes leídas, cobertura, referencias, literales, relaciones geométricas y hallazgos.
- `CAMPOS_PARAMETROS.csv`: todos los nodos JSON, estado estático, lectura en control actual y notas. La copia íntegra de parámetros en el manifiesto no cuenta como uso geométrico.
- `LITERALES.csv`: inventario por contexto. La coincidencia numérica solo identifica candidatos; las duplicaciones semánticas revisadas se explican en B/H01–H13. No interpretar todos los números como hipótesis físicas.
- `COMPARACION_GEOMETRICA.csv`: valores del cálculo frente a dos descripciones del modelo; incluye mínimos, nominales e hipótesis sin vínculo único.
- `COTAS_MODELO.csv`: inventario de operaciones/radios; no equivale a una lista de fallos o verificaciones individuales. C enumera los detalles relevantes sin comprobación individual.
- `COMPARACION_GENERACION.json`: comparación recursiva, filas BOM y bytes de los dos archivos originales emitidos.
- `REGISTRO_GENERACION.json`: comando original como argumentos, stdout/stderr, retorno y entorno invocador.
- `REGISTRO_ENTORNO_POWERSHELL.json` y `SALIDA_AUDITORIA.txt`: proceso 5.1 real y salida de la ejecución final.
- `Control_generacion_JSON/`: dos descripciones regeneradas. **No son CAD nativo ni entrega aceptada.** Se retienen como evidencia.
- `INTEGRIDAD_ANTES.json` y `VERIFICACION_INTEGRIDAD.json`: cotejo SHA-256 de archivos previos y metadatos de `all.png`; no se abre este último.
- `REGISTRO_DOCUMENTACION.json`: bytes anteriores y dos inserciones exactas autorizadas para demostrar que el contenido previo permanece. `registrar_documentacion.py` es el registro de la operación única ya realizada; rechaza repetirla.

## Cotejar integridad después de la auditoría

```powershell
$python = 'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python -B 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635\verificar_integridad.py'
```

**hecho:** coteja todos los archivos previos rastreados/no ignorados. Solo permite las dos inserciones documentales exactas registradas; rechaza archivos nuevos fuera de la carpeta de auditoría, borrados y otras modificaciones. Verifica por separado los 818 CAD, los 65 archivos históricos y las dos carpetas ajenas de OpenCode. No ejecuta ensayos ni crea evidencia nativa.

**pendiente:** las severidades y correcciones del informe son propuestas. P2.05 sigue abierto y P2.04 conserva su condición de entrega vigente. No se hace commit ni se cambia D-12/D-16.
