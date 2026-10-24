# FICHA_ALCANCE — Maqueta física PLA del P2.05, escala 1:12

- Iteración: `Soporte/Iteraciones/Maqueta_PLA_20261022/` (única carpeta de trabajo; entregables en `Entrega_Maqueta/`).
- Fecha: 2026-10-22 · Unidades: mm · Escala maestra de la maqueta: **1:12**.
- Regla del proyecto (AGENTS.md §3/§8): sin commits, sin borrados, no se tocan entregas P2.04/P2.05, ni parámetros, ni generadores.
- Esta ficha es el registro del diseño de la maqueta adoptado en esta iteración.

## A. Qué es y qué NO es

- **Es**: maqueta visual para impresión FDM en PLA del prototipo P2.05 (encapsulado SEDAC), pieza única con peana, impresa "de pie".
- **NO es**: validación del producto. No declara resistencia, seguridad, comodidad ni cumplimiento normativo. El diseño base P2.05 sigue en estado **prediseño**: margen n=2,2, reparto 70/30, 3 g vertical/1 g horizontal, excentricidad e=107,5 mm y precarga 2000 N son **hipótesis** no validadas (así lo recoge el propio JSON de parámetros).

## B. Fuente de datos y hashes (hecho)

| Fuente | SHA-256 |
|---|---|
| `Verificacion/PARAMETROS_P2_05.json` (copia de `01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json`) | `40F2491D01BDEF73170A46FC3FABC2E019DDE088515FF91DFFC7C2E835293771` |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py` (generador corregido H03/H13, ya verificado 2026-10-22) | `BA9AD146AC19AFC85CB68F90936A77677256206C20C4D20D5DE1E496DCF1829B` |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/CONSTRUIR_P2_05.ps1` | `0EC9EF3C67633F5ED05DE8C5DF4783855BD933377A00661D65AD3E1037803459` |

La geometría de la maqueta se deriva de esos archivos (hecho = lectura; el mapeo 1:12 es cálculo). Las cotas reales citadas abajo provienen del JSON verificado; los trazados de cinta/cuna provienen del generador verificado.

## C. Escala 1:12 (cálculo, examen del JSON)

| Magnitud (real) | Real | 1:12 |
|---|---:|---:|
| Alto refuerzo | 480 | 40,00 |
| Separación refuerzos | 190 | 15,83 |
| Ancho refuerzo | 32 | 2,67 |
| Profundidad refuerzo | 24 | 2,00 |
| Panel (ancho×alto×espesor) | 270×472×1 | 22,50×39,33×0,083 |
| Ancho cuna | 100 | 8,33 |
| Ancho / espesor cinta | 50 / 1,5 | 4,17 / 0,125 |
| Y de pernos | 35 / 95 / 390 / 450 | 2,92 / 7,92 / 32,50 / 37,50 |
| Taladro de unión / pasador Ø | 10,2 / 10 | 0,85 / 0,83 |
| Espesores panel / cuerpo lumbar / mejilla / anclaje / arandela | 1 / 3 / 3 / 6 / 3 | 0,083 / 0,25 / 0,25 / 0,50 / 0,25 |

Con la regla general "1 mm de pegamento", ninguno de los espesores/circulares escalados es imprimible; de ahí las adaptaciones del punto D.

## D. Adaptaciones de impresión (supuesto de fabricación, documentadas)

Criterio: con boquilla 0,4 mm (supuesto, ver §H): pared mínima ≥ 0,8 = 2 perímetros; placa aislada ≥ 1,2; agujero ≥ Ø1,2; ranura ≥ 1,0; detalle menor → marque ( entail).

1. **Espesor panel 0,8** (real 1 → 0,083; escalado no imprimible).
2. **Espesor placas lumbar/yugo 1,2** (real 3 → 0,25).
3. **Espesor mejillas 1,2** (real 3).
4. **Paredes del canal (web y alas) 0,8** (real 3 → 0,25); **profundidad del canal mantiene 2,00** (24 → 2,00, tal como está).
5. **Cinta y cuna como "ribbons" de 1,2** (real 1,5 y 2,0 → 0,125/0,167); ancho cinta 4,17 y cuna 8,33 sin alterar.
6. **Pies de cinta/cuña apoyados en la peana**: baseline geometric plan.
7. **Agujeros de pasador Ø1,2** (real 10,2 → 0,85): no funcionales, señal visual.
8. **Marcadores de pasador/arandela**: tachuelas Ø2,0×0,6 en las posiciones de pasador M5 (pasador Ø10, casquillo Ø12,5, arandela espesor 3 → solo referencia).
9. **Ranuras alargadas llevadas a ≥ 1,0** de luz (las por debajo se ensanchan; las por encima no se tocan).
10. **Separación real panel↔placa (0,3 mm) colapsada**: en el modelo quedan en contacto por la línea (fusión panel-placa).
11. **Radios de raíz r=2** (→ 0,17 en escala) **omitidos**: esquinas rectas en el modelo.
12. **Cuna (arco de espuma/cinta inferior) aplanada**: el contorno real de la cuna se lleva a pendientes ≤ 1:1 (arc repetition); la profundidad real se adapta por trazado (real ~174 → trazado según generación de la pieza), ancho 8,33 sin alterar.
13. **Peana**: placa base impresa, 2,0 mm de espesor; ops: `y_modelo = pedestal 0..2,0; cuerpo 2,0 + y_real/12`.
14. **Omisiones declaradas**: pernos/hardware M5 (solo marcadores), espuma y textiles reales (REF acolchados, asa, hebillas, correas estabilizadoras), ventana menor de mejilla y demás detalle no imprimible a 1:12.

## E. Diseño adoptado (decisión de esta iteración)

- **Una pieza única integrada** (no ensamblaje de piezas separadas): peana + 2 refuerzos-canal + panel + placas lumbar/yugo + mejillas + anclajes + cinta-cuna simplificadas. Sin .iam.
- **Orientación de impresión**: de pie, con la peana como base plana abajo; eje vertical de impresión = eje real `y` (480 → 40 mm).
- **Apilado (stack) de capas**: en el eje Y real; análisis geométrico de solapado entre capas consecutivas indica **sin puntos flotantes ni puentes**, salvo la **boca del canal** (C abierto a +z, real rgjd) y pocas regiones del ribbon strap sobre la peana/juya — **pendiente de confirmar en el laminador** (hipótesis).
- **Mapeo modelo** (reglas; ejecución en script):
  - `X_modelo = x_real / 12`… detalle de alineación por simetría.
  - `Y_modelo = 2,0 + y_real / 12`, peana ocupa 0..2,0 (peana: x ±13,33; z 0..≈15,42).
  - Envolvente de capas: panel z 0..0,8; placas 0,8..2,0; a partir de ahí escala continua `z = 2,0 + (rz_real + 3,7)/12` → base del canal rz 0 → 2,31, tope rz 24 → 4,31.
  - Ribbons (cinta/cuna): `z_modelo = (rz_real + 8) / 12` con contornos (y,z) reales del generador, aplanados según regla 12; feet a z 0 (aspie) y cruces de capas resueltos con solapamientos vertical en el stack Y.
- **Envolvente impresa estimada (cálculo, aproximada)**: X ≈ 26,7 · profundidad ≈ 16,4 · altura ≈ 42 con peana. Se verificará con el bbox real del STL (pasará a hecho).

## F. Entregables

En `Entrega_Maqueta/`:
1. `SEDAC_Maqueta_PLA_20261022.ipt` — pieza única nativa Inventor 2027.1.
2. `SEDAC_Maqueta_PLA_20261022.stl` — STL en mm (exportado por Inventor; verificado más abajo).
3. `SEDAC_Maqueta_PLA_20261022.step` — intercambio neutral.
4. `SEDAC_Maqueta_PLA_20261022.3mf` — contenedor con la malla; si el AddIn 3MF de Inventor no está disponible se monta zip+XML manual. Sin G-code: lo no comprobable queda "pendiente de comprobación en laminador".
5. Capturas PNG del modelo y de la vista de impresión.
6. `LEEME.md`, `DIMENSIONES_Y_ALCANCE.json`, `INFORME_VERIFICACION.md` (hashes de entrada/salida incluidos).

Verificación del STL (parser propio, hecho-después): bbox vs envolvente (cálculo), malla cerrada (cada arista compartida exactamente 2 veces), componentes conexos = 1, volumen con signo > 0, unidades mm declaradas.

## G. Trazabilidad (categorías)

- **hecho** — datos y hashes de §B; conexión Inventor 2027.1 (verificada con `status`: «Connected, no document open»); tras construir: bbox/estructura STL, componentes, volumen.
- **cálculo** — conversión 1:12 de §C; mapeos y envolvente de §E; volúmenes de malla.
- **supuesto** — adaptaciones de impresión de §D (espesores ≥0,8/1,2, Ø1,2, ranuras ≥1,0, peana 2,0, aplanado de cuna, colapso de holgura, omisión de radios r=2), boquilla 0,4 si el usuario no indica otra, color de material.
- **hipótesis** — que el diseño P2.05 (prediseño) es base apropiada de maqueta de formato físico; que la impresión "de pie" no requiere soportes críticos; que el laminador acepta la boca del canal y las regiones del strap. El laminado real queda **pendiente de comprobación en laminador**.

## H. Datos pendientes del usuario (bloquean solo el laminado, no el modelo)

- Impresora / boquilla (se asume 0,4) / perfil de laminador.
- Color de PLA (solo afecta capturas/LEEME).
- Confirmación explícita (AGENTS.md §6) para crear el `.ipt` nuevo y exportar — se solicitará antes de escribir CAD.

## I. Nota de proceso

- La skill descrita "cad-especificacion-pieza" **no existe** en el catálogo de `.agents/skills/` (10 skills disponibles); se informará en el informe final tal como se acordó.
- No se ha ejecutado `CONSTRUIR_P2_05.ps1` completo: la verificación §5 usó solo el generador Python, antes vs después, invariante y propagación documentadas en `Verificacion/`.
