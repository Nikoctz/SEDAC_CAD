# LEEME — SEDAC Optimización real 2026-10-23 (Alternativa C)

## Qué es esta carpeta

Iteración de optimización sobre el **producto real** a escala 1:1 (mm), derivada de P2.04 —entrega
vigente— y del soporte P2.05 —abierta—. Propone **un solo cambio**: el canal de refuerzo pasa de
32 × 24 × 3 mm a **32 × 28 × 2,5 mm** (pared mínima de estudio 2,3 mm).

**Entrada modificada: una sola.** En `PARAMETROS_P2_05.json` cambian únicamente `profundidad_refuerzo`
(24 → 28), `pared_refuerzo` (3 → 2,5) y `pared_minima` (2,8 → 2,3). No cambian materiales, número de
piezas (54), ocurrencias (83), uniones, textiles ni cargas.

**Consecuencia geométrica: varias piezas.** El generador deriva de `D` la altura de las mejillas
(`rect(18,Z_CAPA,100,D-Z_CAPA)` en el lumbar y `rect(376,-2,98,D+2)` en los yugos) y de `t` la longitud
de los casquillos (`B-2t`). Por eso 16 piezas cambian de masa aunque solo se edite una entrada. La masa
nativa lo mide pieza a pieza en `Build/MASAS_CAD.json`; no se supone.

> Una entrada, varias piezas: no es una contradicción. Es la diferencia entre **parámetro editado** y
> **dependencia propagada**, y es exactamente lo que `TABLA_MASAS.md` mide en el CAD.

**No cierra P2.05. No sustituye la entrega P2.04. No está liberada para fabricación ni para uso con
personas.** Es un **borrador declarado**: el cierre R2 queda pendiente por el redondeo del lumbar (D-12).

## Cómo abrirla

1. Abrir `Build/SEDAC_OPT_20261023.iam` en **Inventor 2027**. Las 54 piezas están en la misma carpeta; no
   hay que re-vincular nada (comprobado: 54 referencias, 0 ausentes).
2. Cada pieza es nativa: bocetos y extrusión editables, más roscas cosméticas M5. Los parámetros de
   posición y espesor de cada operación están como parámetros de usuario (`Oxx_Posicion`, `Oxx_Espesor`).
3. **Para un cambio coherente del conjunto**: editar `PARAMETROS_P2_05.json` y regenerar con
   `Soporte/CONSTRUIR_OPT.ps1` en una **carpeta de salida nueva**. Nunca regenerar sobre esta.
4. Revisión externa sin Inventor: `Build/SEDAC_OPT_20261023_REVISION.step`.
5. Vistas: `Build/VISTA_FRENTE/VISTA_ESPALDA/VISTA_LATERAL/VISTA_ISOMETRICA/VISTA_ESTRUCTURA.png`.

> El STEP es un derivado para revisión. **No** demuestra que el ensamblaje nativo sea correcto: eso lo
> acredita el IAM con sus IPT, según `RESULTADO_NATIVO.md`.

## Qué contiene

| Archivo | Para qué |
|---|---|
| `INFORME_OPT.md` | fuentes, decisiones, trade study, verificación y pendientes |
| `TABLA_MASAS.md` | antes/después por grupo y por pieza, con materiales y cantidades |
| `RESULTADO_NATIVO.md` | qué se midió sobre el CAD y con qué alcance |
| `PARAMETROS_P2_05.json` | parámetros de la alternativa (única fuente de la geometría variable) |
| `PARAMETROS_BASE.json` | parámetros heredados, para comparar |
| `Soporte/alternativas.py` | ejecuta el cálculo real sobre 5 secciones y genera la comparación |
| `Soporte/generar_tabla.py` | genera `TABLA_MASAS.md` desde el BOM y las masas nativas |
| `Soporte/verificar_y_vistas.ps1` | verificación nativa y captura de vistas |
| `Soporte/refs_y_actualizacion.ps1` | referencias, ausencias y `Update2` del IAM |
| `Soporte/reevaluar_cierre.ps1` | reevalúa R1/R2/R3 con el nombre real de los archivos |
| `Analisis/` | resultados del cálculo por variante y la comparación |
| `Build/` | CAD nativo, STEP, vistas, masas, interferencias, redondeos |
| `Cierre/` | `CIERRE.json` y sus tres resultados |
| `MANIFIESTO.json` | ruta, tamaño y SHA-256 de todos los archivos |

## Resultado en una línea

**−9,55 g** de masa rígida (1,442328 → 1,432778 kg, 0,66 %), medidos en Inventor, a cambio de bajar el
margen de 2,247 a **2,227** y de que el modo gobernante pase a **pandeo local de alas**. Por eso el
informe **no recomienda adoptarla** todavía: el ahorro es real pero pequeño frente al coste mecánico.

## Qué falta

Mediciones reales (bomba, centro de masa, apoyos, cintas, usuarios) · clasificación de contacto A/B/C
(D-12) · FEA local de pandeo y de placa lumbar · fatiga, dinámica, temperatura, desgaste · liberación de
emergencia y guantes · EPP, manguera y ergonomía · tolerancias de pasador y proceso de fabricación ·
H02/H04/H05 · simplificación de piezas y uniones, que esta iteración **no** consiguió.

## Integridad

- Originales intactos. Sin commit, sin push, sin borrados, sin cambios en Notion.
- `MANIFIESTO.json` incluye SHA-256 de cada archivo para verificar que no se alteró nada después.
- Las salidas de esta carpeta **no** escriben en `Entrega/`, en `Calculos/` históricos ni en las corridas
  anteriores: el generador y el cálculo de la copia reciben su ruta de salida por argumento.
