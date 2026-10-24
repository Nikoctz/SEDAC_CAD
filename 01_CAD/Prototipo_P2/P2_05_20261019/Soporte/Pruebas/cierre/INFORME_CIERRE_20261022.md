# Corrección del cierre P2.05 — informe del 2026-10-22

**hecho:** se completó el encargo de soporte y documentación autorizado. P2.04 sigue siendo la entrega vigente y P2.05 sigue abierta. No se ejecutó Inventor ni el constructor completo, no se generó CAD, no hubo borrados y **no se hizo commit ni push**.

## 1. Qué se leyó

**hecho:** se leyeron los documentos de gobierno en el orden obligatorio (CONTEXTO → ESTADO → DECISIONES → CHANGELOG), el encargo adjunto, los archivos fuente y los registros siguientes. El parámetro JSON se leyó, no se modificó.

- [AGENTS.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/AGENTS.md)
- [CONTEXTO_SEDAC.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/CONTEXTO_SEDAC.md)
- [ESTADO_ACTUAL.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/ESTADO_ACTUAL.md)
- [DECISIONES.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/DECISIONES.md)
- [CHANGELOG_SEDAC.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/CHANGELOG_SEDAC.md)
- [01_CAD/Prototipo_P2/P2_04_20261016/INFORME_DISENO_P2_04.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_04_20261016/INFORME_DISENO_P2_04.md)
- [01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/REDONDEOS.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/REDONDEOS.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Heredado_P2_04/INFORME_DISENO_P2_04.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Heredado_P2_04/INFORME_DISENO_P2_04.md)
- [01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/CONSTRUIR_P2_05.ps1](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/CONSTRUIR_P2_05.ps1)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py)
- [01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/MODELO_API.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/MODELO_API.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/REDONDEOS.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/REDONDEOS.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/INTERFERENCIAS.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/INTERFERENCIAS.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/RESTRICCIONES.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/RESTRICCIONES.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/MASAS_CAD.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/MASAS_CAD.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/RESUMEN_ENTREGA.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/RESUMEN_ENTREGA.json)
- [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/ERROR.txt](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/ERROR.txt)

**hecho:** también se consultaron en modo lectura las masas/vistas originales P2.04 para los tamaños usados por el simulador R1, y el JSON histórico P2.05 de `Calculos/RESULTADOS_PREDISENO.json`. La escritura documental conserva el estilo del proyecto; no se recuperaron muestras personales externas.

## 2. Qué cambió

| Ruta exacta | Cambio (**hecho**) |
|---|---|
| [01_CAD/Prototipo_P2/P2_04_20261016/INFORME_DISENO_P2_04.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_04_20261016/INFORME_DISENO_P2_04.md) | Fe de erratas fechada: redondeo lumbar solicitado/no aplicado; texto original conservado; propuesta sin ensayo; excepción de huella documentada. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Heredado_P2_04/INFORME_DISENO_P2_04.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Heredado_P2_04/INFORME_DISENO_P2_04.md) | Misma corrección en la copia heredada. |
| [01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md) | Aviso vigente y sección 10: tres resultados, situación de cargas, evidencias, comandos y pendientes. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/CONSTRUIR_P2_05.ps1](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/CONSTRUIR_P2_05.ps1) | Integra el módulo común; R3 antes de Inventor; evidencia obligatoria al reutilizar; borrador con excepción; salida nueva obligatoria. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/cierre_p2_05.ps1](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/cierre_p2_05.ps1) | Módulo nuevo sin COM: valida y publica R1/R2/R3 y bloquea evidencias incompletas o incoherentes. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py) | Añade situacion_de_carga y su print; sin cambiar ecuaciones ni resultados anteriores. |
| [ESTADO_ACTUAL.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/ESTADO_ACTUAL.md) | Estado vigente fechado, pruebas de soporte diferenciadas de corrida nativa y pendientes físicos. |
| [CHANGELOG_SEDAC.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/CHANGELOG_SEDAC.md) | Entrada nueva del 22/10 con cambios y verificaciones; historia conservada. |
| [DECISIONES.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/DECISIONES.md) | D-16: argumento, alcance y reversibilidad del cierre de tres resultados. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/verificar_cierre.ps1](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/verificar_cierre.ps1) | Casos A–D y controles adicionales; presencia de archivos simulada solo en memoria; integración estática sin ejecutar el constructor. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/verificar_calculo.py](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/verificar_calculo.py) | Comparación AST en memoria contra HEAD y comprobación del print; omite escrituras originales. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/LEEME.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/LEEME.md) | Naturaleza sintética, comandos, procedencia, resultados y fallo inicial del preparador corregido. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/VERIFICACION_INTEGRIDAD_20261022.json](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/VERIFICACION_INTEGRIDAD_20261022.json) | Comparación de huellas antes/después y excepción documental P2.04. |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/INFORME_CIERRE_20261022.md](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/INFORME_CIERRE_20261022.md) | Este informe, con rutas y alcance de lo comprobado. |

**hecho:** las carpetas nuevas de `Ejecuciones/` contienen solo copias JSON, estados de prueba e informes. No contienen CAD nuevo. Las ejecuciones previas del banco, incluida una fallida por un error del preparador, se conservaron.

## 3. Qué se verificó y cómo

**hecho:** el constructor importa el mismo módulo de decisión probado. El banco no ejecuta el constructor y sustituye solo la función que observa presencia/tamaño de archivos CAD y vistas; sus tamaños proceden de archivos existentes. Los resultados son **casos sintéticos de prueba; no son evidencia de entrega**.

| Comprobación | Método y evidencia | Resultado (**hecho**) |
|---|---|---|
| Lógica de cierre, PowerShell 7 | `& .\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Pruebas\cierre\verificar_cierre.ps1`; [resultado 7.6.5](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/Ejecuciones/Nueva_20261022_182113_260/RESULTADOS_PRUEBAS.json) | 16 casos, 46 aserciones, 0 fallos |
| Lógica de cierre, Windows PowerShell 5.1 | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Pruebas\cierre\verificar_cierre.ps1`; [resultado 5.1.26100.9711](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/Ejecuciones/Nueva_20261022_182110_520/RESULTADOS_PRUEBAS.json) | 16 casos, 46 aserciones, 0 fallos |
| Invariancia del cálculo | `verificar_calculo.py --salida ...`, intérprete con numpy del constructor; [resultado numérico en memoria](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/Ejecuciones/Calculo_20261022_181742_727/VERIFICACION_CALCULO.json) | 15 verificaciones y todos los valores anteriores idénticos; 26 magnitudes trazadas, bloque presente en print y alcance conservado |
| Integridad de fuentes y CAD | SHA-256 antes/después de 3418 archivos rastreados; [resultado de integridad](C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Pruebas/cierre/VERIFICACION_INTEGRIDAD_20261022.json) | Solo ocho archivos rastreados de soporte/documentación cambiaron; cero cambios fuera del encargo |
| CAD e historial | Misma comparación SHA-256 | 818 archivos CAD idénticos; 65 archivos de Nueva_20261019_060807 idénticos |
| Sintaxis e integración | Parser de PowerShell 5.1 y 7 dentro del banco; revisión del módulo importado, precontrol R3, reutilización y excepción del borrador | Aprobado sin ejecutar código de Inventor |

**hecho:** A (parcial 236/472), B (sin registro) y C (cribado falso) no producen `ESTADO_OK`; sí borrador/error y, en C, diagnóstico de la verificación. D produce R1+R2+R3 y un sello exclusivamente **sintético**, con el texto literal sobre ausencia de acreditación física. Un registro JSON `null` no se trata como evidencia de cero interferencias.

**hecho:** el control de R3 lee tipos booleanos, margen objetivo del modelo (actualmente 2,2), mínimo y verificaciones, cierre residual y flecha. La nueva corrida copiaría el JSON de cálculo a su propia salida, evitando asociar el cierre a un resultado raíz mutable posterior. Se conserva `Prediseno analitico condicionado; NO validacion del conjunto`.

**hecho:** el código de `calcular_p2_05.py` solo recibió metadatos de salida. El JSON y CSV históricos de `Calculos/`, los parámetros, el generador y los registros originales no se regeneraron. Las pruebas numéricas ejecutaron el tramo analítico en memoria omitiendo `mkdir` y escrituras. No se corrigió ninguna ecuación ni se introdujo ningún valor físico nuevo.

**hecho:** `git diff --check` se ejecutó para revisar el parche. El espacio final detectado en las dos líneas de informe fue retirado. Resultado final de `git diff --check`: código de salida 0, sin errores de espacios finales.

## 4. Excepción documental del manifiesto P2.04

**hecho:** el manifiesto histórico incluye `INFORME_DISENO_P2_04.md`. La fe de erratas expresamente solicitada cambia su SHA-256; por tanto ese archivo ya no puede anunciarse como idéntico al texto publicado en el ZIP original. Se conservan tanto la afirmación original en el informe, claramente sustituida, como el manifiesto y el ZIP históricos sin reemitirlos. La excepción queda identificada en ambos informes, estado y changelog. Una nueva entrega necesitará un manifiesto nuevo; **no se ha vuelto a cerrar ni empaquetar P2.04**.

## 5. Pendientes, separados de lo comprobado

- **pendiente:** ejecutar en otra autorización una corrida real de Inventor y verificar los artefactos nativos. La lógica pasó pruebas; la integración nativa modificada no se ejecutó.
- **pendiente:** clasificación A/B/C con recorrido/tensión reales de las cintas (D-12). El lumbar 236/472 no se acepta como solución de diseño. Radio 0,5 mm: propuesta sin ensayo de desgaste (**supuesto**).
- **hipótesis sin medir:** masa real, centro de gravedad, reparto 70/30, apoyos efectivos, 3g/1g, excentricidad 107,5 mm y precarga 2000 N. Margen 2,2: criterio de prediseño sin validación del producto.
- **pendiente:** contacto, abrasión, textiles, fatiga, térmica, ergonomía y liberación. Ninguno de los tres resultados acredita el comportamiento físico del producto.
- **pendiente de revisión posterior, no ejecutada ahora:** correspondencia de parámetros, cálculo y CAD; cotas, tolerancias, cobertura de constantes, bocetos y regeneración completa de documentación/paquete. La lista está en LEEME P2.05 §10.4.
- **limitación analítica conservada:** pandeo local limitado por fluencia, idealización de apoyos y aplicación de cargas; no se modificaron sus ecuaciones. No se detectó ni se corrigió una diferencia numérica introducida por este encargo. Los escenarios de carga alternativos discutidos antes requieren una revisión distinta, no sustituir silenciosamente los valores actuales.

## 6. Decisiones de implementación para revisión del responsable

**hecho de implementación:** se eligieron un módulo común nuevo (`cierre_p2_05.ps1`), nombres separados `R1_GENERACION.json`, `R2_COHERENCIA.json`, `R3_CRIBADO.json`, `CIERRE.json`, `ESTADO_BORRADOR.txt`, `AVISO_CIERRE.txt` e `INCUMPLIMIENTO_CRIBADO.txt`. El sello positivo sigue llamándose `ESTADO_OK.txt`, con alcance explícito. D-16 registra el motivo y reversibilidad.

**supuesto administrativo para ratificar:** tolerancia relativa 1e-9, exclusivamente para comparar sumas serializadas de masas. No es criterio físico ni tolerancia de fabricación. Los nombres de estado también quedan a revisión administrativa del responsable; no se añadió ninguna decisión sobre A/B/C, radios, material o geometría. La política implementada conserva el bloqueo de D-12 y no exige usar `AceptarPendientes`.

## 7. all.png y control de cambios

**hecho:** al iniciar se verificó que `all.png` estaba sin rastrear, tenía 0 bytes y no había referencias en el repositorio. Se tomó la excepción explícita del responsable únicamente para ese archivo. No se leyó como insumo, no se abrió, no se modificó, no se borró y no se añadió al índice. Su longitud y modificación registrada (2026-10-19 16:50:22.410773 -03:00) permanecen iguales. Su borrado queda como decisión del responsable. Las referencias creadas ahora en esta documentación describen esa excepción.

**hecho:** el estado final incluye únicamente los ocho archivos rastreados autorizados modificados, el módulo y banco nuevos, y `all.png` como excepción ajena. **No se hizo commit, push, reset, checkout ni clean.**
