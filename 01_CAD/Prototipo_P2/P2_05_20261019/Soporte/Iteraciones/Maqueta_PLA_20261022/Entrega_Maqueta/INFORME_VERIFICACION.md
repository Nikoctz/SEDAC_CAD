# INFORME_VERIFICACION — Maqueta PLA 1:12 (SEDAC_Maqueta_PLA_20261022)

Fecha: 2026-10-22 · Unidades: mm · Entorno: Autodesk Inventor 2027.1 vía MCP `inventor` (execute_python, namespace persistente) + scripts locales (parser STL/3MF propio).

Trazabilidad: cada afirmación está etiquetada **[hecho]** (archivo o lectura verificable), **[cálculo]** (reproducible con fórmula/script), **[supuesto]** (adoptado sin medir), **[hipótesis]** (por comprobar). Lo que no se puede comprobar aquí queda como *pendiente de comprobación en laminador*.

## 1. Fuentes de datos [hecho]

| Fuente | SHA-256 |
|---|---|
| `01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json` | `40F2491D01BDEF73170A46FC3FABC2E019DDE088515FF91DFFC7C2E835293771` |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py` | `BA9AD146AC19AFC85CB68F90936A77677256206C20C4D20D5DE1E496DCF1829B` |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/CONSTRUIR_P2_05.ps1` | `0EC9EF3C67633F5ED05DE8C5DF4783855BD933377A00661D65AD3E1037803459` |

Estos hashes coinciden con los registrados en `FICHA_ALCANCE.md` §B (re-hash de esta sesión, 2026-10-22) [hecho]. Las cotas reales provienen del JSON; el trazado cinta/cuna del `ribbon_path` del generador (L27-34).

## 2. Construcción — etapas y verificación por deltas esperados

Método: cada extrusión se precedió de una **expectativa de volumen** calculada sobre un modelo de cobertura del material ya existente (helpers verificados en vivo por supresión lectura en etapas previas), con muestreo d = 0,025 mm en ribbons y d = 0,05 mm en taladros. Tras cada operación: bodies, bbox y |medido − esperado|.

| Etapa | Esperado [cálculo] | Medido [hecho] | Dif. | Tolerancia | OK |
|---|---:|---:|---:|---|---|
| Strap L (banda x −13,75..−9,583) | 265,3092 | 265,2154 | −0,0938 | ±2,5 | ✓ |
| Strap R (banda x 9,583..13,75) | 265,3092 | 265,2154 | −0,0938 | ±2,5 | ✓ |
| Cuna L (banda x −12,667..−4,334) | 148,8593 | 148,8112 | −0,0481 | ±2,5 | ✓ |
| Cuna R (banda x 4,333..12,666) | 148,8531 | 148,8297 | −0,0234 | ±2,5 | ✓ |
| 4 taladros, corte +13,8 | 23,3135 | 24,3246 | +1,0111 | ±1,5 | ✓ |
| 4 taladros, corte −13,8 | 23,3135 | 24,3246 | +1,0111 | ±1,5 | ✓ |

Notas de etapas:
- El perfil de los 4 taladros fue verificado por discriminante de volumen: una sola extrusión cortó −24,3246 (los 4 aros); si hubiera tomado un solo círculo habría sido ≈ −5,83 [hecho].
- El exceso constante de +1,01 en los taladros es simétrico L/R y compatible con muestreos que caen sobre fronteras exactas (z = 1,529 web/alas de canal, borde inferior de la cinta) [cálculo-estimación]. No se declara otra certeza.
- Estado intermedio A–E (peana, panel, placas, mejillas, canales) se verificó en vivo durante la sesión por cadena de supresiones (V peana 1326,2645; lumbar +106,602; yugos +21,771 c/u; canales +135,047 c/u; mejillas 112,632 total) → V base 1859,1354, bodies = 1 [hecho].

## 3. Consolidado final [hecho]

- Volumen: **2638,5578 mm³** = 1859,1354 + 265,2154×2 + 148,8112 + 148,8297 − 24,3246×2 (identidad exacta) [hecho/cálculo].
- Cuerpos: 1 · Extrusiones: 21 · Sketches: 20 · Planos de trabajo: 14. Centro de masas (0 ; 13,8977 ; 6,1579).
- Bbox (COM ×10 cm→mm): (−13,75 ; 0 ; 0) → (13,75 ; 42 ; 16,0792); envolvente 27,5 × 42 × 16,08 [hecho]. Cabe en 40×40×70 [cálculo].
- Los cuatro nombres de extrusión 2..6 no existen (descartados en el ajuste A–E; sin efecto en geometría final) [hecho].

## 4. STL (inventor export, opciones por defecto) [hecho]

- Binario, 2164 triángulos, 108 284 bytes.
- **Escala mm confirmada**: bbox del archivo = (−13,75 ; 0 ; 0 ; 13,75 ; 42 ; 16,0792): idéntico al modelo en mm; al dividir por 25,4 no coincide [hecho].
- **Hermética**: cada arista dirigida tiene par opuesto con multiplicidad 1 (manifold + orientación consistente) [cálculo sobre archivo → hecho].
- **Componentes conexos**: 1 [hecho].
- **Volumen con signo positivo**: 2640,3154 mm³ (diferencia +0,067 % frente a Inventor = facetado de arcos y taladros) [cálculo].

## 5. STEP

- ISO-10303-21; 1 `MANIFOLD_SOLID_BREP`; 352 `ADVANCED_FACE`; 2330 `CARTESIAN_POINT`; 540 575 bytes [hecho].

## 6. 3MF (montado manualmente)

- Inventor 2027.1 (instalación actual) **no lista translator 3MF** (68 complementos revisados: sí hay USDz, glTF, OBJ, STL) [hecho]. Se generó empaquetado OPC propio: `[Content_Types].xml`, `_rels/.rels`, `3D/3dmodel.model` con `unit="millimeter"` [cálculo → hecho].
- Verificación reabriendo el zip: CRC íntegro, 1024 vértices / 2164 triángulos (igual al STL), bbox idéntica en mm [hecho].

## 7. Capturas [hecho]

`ActiveView.SaveAsBitmap` del documento abierto: 4 PNG 1000×700 tras ocultar los 14 planos de trabajo. Se inspeccionó visualmente CAPB y CAPA (sólido esperado: panel + cinta en arco + cunas + canales + pernos visibles). Dos capturas intermedias con planos visibles se conservan en `Soporte/Capturas_intermedias/` (no se borra nada de la iteración).

## 8. Hashes de outputs [hecho]

| Archivo | Tamaño | SHA-256 |
|---|---:|---|
| `SEDAC_Maqueta_PLA_20261022.ipt` | 609 792 | `9DB9A3700E5CCF7A33395E9D79597623FCC8E9F1AFE6C4DD9167ED36BDD95DE2` |
| `SEDAC_Maqueta_PLA_20261022.stl` | 108 284 | `4FF8B66AA309C56D1C288A9952FC9C655A986B109015EEB09D608D22049A09BC` |
| `SEDAC_Maqueta_PLA_20261022.step` | 540 575 | `D7146A066A2286E001EAC391514A4D7F6AE2DC2FBBD6CF6B3A0036882D0BA3D6` |
| `SEDAC_Maqueta_PLA_20261022.3mf` | 18 771 | `6BC0E929AA4378204A9AD87CD0597CDB55ED803C7088EB342F4B25939D47D2F8` |
| `CAPA_iso_frontal.png` | 272 558 | `32D26B09C00079D7A0AC981B43F2AB0333463D6038E813CD5647347680471DE5` |
| `CAPB_iso_trasera.png` | 289 528 | `899C50C1C08840B05E102013492908A9598CF0AF99A9DC6E84CBD578B6039C24` |
| `CAPC_panel.png` | 252 221 | `AFE404B6B8E47F81A846D4D244C5894D67A27AF7D7FE6B5D22DC540376FF0AB1` |
| `CAPD_trasera.png` | 270 228 | `8AD6EC95A53C22BC17AEE3B955A753C322DE5B3F2518C67E0D00BE0F708F1C01` |
| `LEEME.md` / `DIMENSIONES_Y_ALCANCE.json` / `INFORME_VERIFICACION.md` | — | hash bajo demanda (los tres son texto plano) |

## 9. Lo que NO está verificado (declarado)

- **Laminado real, soportes, g-code, tiempo de impresión, consumo**: pendiente de comprobación en laminador. No se ha laminado ni impreso [hecho por ausencia].
- Boca de canal (C abierta a +z) y zonas de arco de cinta/cuna sobre vacíos: **hipótesis** de requerir soportes locales.
- Boquilla 0,4 mm, perfil de laminador, color: **supuestos** pendientes del centro de impresión.
- La maqueta no valida el diseño P2.05: n=2,2, 70/30, 3 g/1 g, e=107,5 mm, precarga 2000 N siguen en **hipótesis**; P2.05 no queda cerrado.

## 10. Nota de proceso (modelo/plataforma)

- Skill solicitada en el arranque "cad-especificacion-pieza": **no existe** en `.agents/skills/` (10 disponibles); se trabajó con las convenciones del proyecto y la FICHA como especificación.
- `git status` al inicio de la sesión mostró **cambios sin commit hechos por otro agente/escritor** (generar_p2_05.py, calcular_p2_05.py, CONSTRUIR_P2_05.ps1, LEEME_P2_05.md, DECISIONES.md, ESTADO_ACTUAL.md, CHANGELOG_SEDAC.md, 2× INFORME_DISENO_P2_04.md + no rastreadas: Correccion_Dependencias_20261022_192327/, Pruebas/, Auditoria_Coherencia_20261022_185635/, cierre_p2_05.ps1). Se respetó la regla de escritor único: ese trabajo **no se tocó, no se descartó y no se commiteó**; esta entrega solo escribió dentro de `Soporte/Iteraciones/Maqueta_PLA_20261022/`. Sin `git commit`/`git push`/`git reset`/borrados.
- No se ejecutó `CONSTRUIR_P2_05.ps1` completo; la geometría real se leyó del generador Python (hash-verificado).
