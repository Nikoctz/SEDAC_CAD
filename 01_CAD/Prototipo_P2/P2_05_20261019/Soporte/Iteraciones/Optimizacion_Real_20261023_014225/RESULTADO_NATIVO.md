# Resultado nativo — qué se comprobó realmente

Registro de lo medido sobre el CAD de esta carpeta. Complementa a `INFORME_OPT.md` §6.
Todo lo de esta página es **hecho** (archivo o comando); nada acredita comportamiento físico.

## 1. Archivos generados

| Archivo | Contenido |
|---|---|
| `Build/SEDAC_OPT_20261023.iam` | ensamblaje nativo, 83 ocurrencias, 54 documentos referenciados |
| `Build/*.ipt` | **54** piezas nativas editables (bocetos + extrusión + roscas cosméticas) |
| `Build/SEDAC_OPT_20261023_REVISION.step` | STEP del conjunto (protocolo de aplicación 3) |
| `Build/VISTA_FRENTE.png` | vista frontal |
| `Build/VISTA_ESPALDA.png` | vista posterior |
| `Build/VISTA_LATERAL.png` | vista lateral (añadida en esta fase) |
| `Build/VISTA_ISOMETRICA.png` | vista isométrica (añadida en esta fase) |
| `Build/VISTA_ESTRUCTURA.png` | conjunto sin textiles ni espaldera |
| `Build/MASAS_CAD.json` | masa nativa por pieza, cantidad, grupo y referencia |
| `Build/INTERFERENCIAS.json` | lista de solapes (vacía = sin solapes) |
| `Build/RESTRICCIONES.json` | 82 ocurrencias posicionadas, grados de libertad y error de transformación |
| `Build/REDONDEOS.json` | registro por pieza: aristas totales/redondeadas, criterio, estado |
| `Build/RESUMEN_ENTREGA.json` | masas derivadas y grupos |
| `Build/VERIFICACION_NATIVA.json` | recuento de ocurrencias, referencias, interferencias y masa del IAM |
| `Build/REFERENCIAS_Y_ACTUALIZACION.json` | 54 referencias, ausencias y `Update2` |
| `Cierre/CIERRE.json` | R1/R2/R3 y motivos |

## 2. Números medidos

| Magnitud | Valor | Cómo se obtuvo |
|---|---:|---|
| Piezas nativas | 54 | archivos `.ipt` en `Build/` |
| Ocurrencias en el IAM | 83 | `ComponentDefinition.Occurrences` |
| Documentos referenciados únicos | 54 | `Definition.Document.FullFileName` por ocurrencia |
| Referencias ausentes en disco | **0** | comprobación de existencia de cada ruta |
| `Update2` del ensamblaje | **True** | actualización forzada al abrir |
| Interferencias (umbral 0,001 mm³) | **0** | `AnalyzeInterference` sobre piezas físicas |
| Masa del ensamblaje | **1,432778 kg** | `MassProperties.Mass` |
| Suma de piezas | 1,432778 kg | `MASAS_CAD.json` × cantidad |
| Masa rígida + protectores | 1,432778 kg | excluye BOM de referencia |
| Referencias visuales | 0,482846 kg | no se suman al presupuesto |

La coincidencia entre la masa del IAM y la suma de piezas es la comprobación de que no hay piezas
duplicadas, omitidas ni con cantidad mal contada.

## 3. Materiales y densidades

El constructor **crea** un material por familia (`SEDAC_6061`, `SEDAC_hdpe`, …) con la densidad del JSON y
comprueba `|masa nativa − volumen × densidad| < 1e-5 kg` en cada pieza; si falla, aborta la corrida. Por
tanto las masas de la tabla no usan el material predeterminado de Inventor.

| Familia | ρ (g/cm³) | E (MPa) | Sy (MPa) |
|---|---:|---:|---:|
| 6061 (T6, mínimos de prediseño) | 2,7 | 69 000 | 240 |
| HDPE (espaldera) | 0,953 | — | sin crédito resistente |
| herrajes (A2-80 / arandela) | 8,0 | 193 000 / 200 000 | 600 / 200 |
| textil / espuma (referencias) | 0,75 / 0,06 | — | sin crédito resistente |

`Sy` y `E` son **mínimos de prediseño**, no certificados de suministro.

## 4. Cierre (D-16)

`Cierre/CIERRE.json`: **R1 cumple · R2 no cumple · R3 cumple · aceptado = false.**

- **R1:** 54 IPT + IAM + STEP + las tres vistas exigidas, presentes y no vacíos.
- **R2:** el lumbar queda con redondeo **parcial** (criterio A/B/C pendiente, D-12). Es el único motivo.
- **R3:** 15/15 verificaciones ≥ 2,2; mínimo **2,227** (pandeo local de alas); flecha 0,666 mm;
  cierre residual de junta > 0.

Por eso el build termina en `ESTADO_BORRADOR.txt` con `ERROR.txt`: **borrador declarado, no entrega
aceptada**. No se forzó la aceptación del redondeo ni se inventó la clasificación de contacto.

## 5. Incidente registrado: falso negativo de R1 por nombres

El `CIERRE.json` original del build marcó R1 = falso con el motivo «archivo ausente: `SEDAC_P2_05.iam`».
No faltaba nada: el módulo de cierre deriva el nombre esperado de `MODELO_API.version` (que sigue siendo
`P2.05`) mientras esta corrida nombra sus archivos `SEDAC_OPT_20261023`. Se corrigió **solo el nombre
esperado**, parametrizándolo en la copia local del módulo (`Soporte/cierre_p2_05.ps1`), y se reevaluó en
`Cierre/`. La comprobación de existencia y tamaño no se relajó. El primer intento se conserva en
`Cierre_intento1_nombre/` y el build original en `Build/CIERRE.json`.

## 6. Límites de esta verificación

- No hay FEA, ensayo ni pesaje. Las masas son de modelo.
- El umbral de interferencias (0,001 mm³) y la tolerancia 1e-6 son los heredados, no tolerancias de fabricación.
- Los 8 pasadores y sus holguras no se verificaron con tolerancias reales (H04 abierta).
- Los textiles son envolventes; no se les atribuye resistencia por área dibujada.
- El STEP se exportó correctamente pero **no se reimportó** para comprobar su contenido: es un derivado,
  no la prueba del nativo. La prueba del nativo es el IAM + sus 54 IPT.
