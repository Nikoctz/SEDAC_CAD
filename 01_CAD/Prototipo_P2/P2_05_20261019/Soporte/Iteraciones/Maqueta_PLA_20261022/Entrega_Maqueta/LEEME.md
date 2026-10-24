# LEEME — Maqueta PLA 1:12 del encapsulado SEDAC (P2.05)

Fecha: 2026-10-22 · Unidades: **milímetros** · Escala maestra: **1:12** (adaptada, no uniforme)
Entrega: `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Maqueta_PLA_20261022/Entrega_Maqueta/`

## Qué es y qué NO es

- **Es**: maqueta visual, de una sola pieza, para impresión FDM en PLA del prototipo P2.05 (encapsulado SEDAC), impresa "de pie" con peana plana en z=0. Los espesores y taladros están adaptados para imprimibilidad; el mapeo de layout es 1:12.
- **NO es**: una reducción uniforme, ni una pieza funcional, ni una validación del producto. No declara resistencia, seguridad, comodidad ni cumplimiento normativo. El diseño P2.05 sigue en **estado prediseño** y **P2.05 no queda cerrado** por esta maqueta. Margen n=2,2, reparto 70/30, 3 g vertical / 1 g horizontal, e=107,5 mm y precarga 2000 N siguen siendo **hipótesis** sin validar.

## UNIDADES

Milímetros. El STL exportado por Inventor es numéricamente mm (verificado: su bbox coincide con la del modelo en mm, y no coincide al dividir por 25,4). El 3MF declara `unit="millimeter"` internamente.

## PARÁMETROS GEOMÉTRICOS (medidos en el modelo final)

- **Envolvente (bbox real del STL) [hecho]**: X 27,5 · Y (altura de impresión) 42,0 · Z 16,0792 → caja impresa 27,5 × 42,0 × 16,08; **cabe en la envolvente 40×40×70** [cálculo].
- **Volumen** [hecho]: 2638,5578 mm³ (Inventor, cuerpo único). Volumen con signo de la malla STL: 2640,3154 mm³ (+0,067 % por facetado de arcos y taladros) [cálculo sobre archivo].
- **Peana**: placa base 2,0 mm de espesor, todo el ancho (x ±13,75), apoyada en z=0.
- **Panel**: espesor 0,8 (real 1 → 0,083 escalado), frente en x ±11,25, de y 1,8 a 41,5.
- **Placas lumbar/yugo** (anclaje): espesor 1,2 (real 3 → 0,25), z 0,171..1,371.
- **Mejillas (8)**: espesor 1,2 (real 3), z 0,2..2,729, en cajas x ±(9,05..10,45) y ±(5,58..6,78), y 3,5..11,83 y 33,33..41,5.
- **Canales directamente integrados**: paredes (web) 0,8 (real 3 → 0,25) z 0,729..1,529 a todo el ancho del canal; alas (prongs) 1,2 z 1,529..2,729; profundidad de canal 2,0 mantenida (24 real → 2,00).
- **Cinta (strap)**: ribbon de espesor **1,2** (real 1,5..2,0 → 0,125/0,167, no imprimible), ancho de banda x 4,1667 (real 50 → 4,17, sin alterar), bandas en x −13,75..−9,583 y espejo 9,583..13,75; arco superior z 16,079.
- **Cuna**: ribbon de espesor **1,2** (real 2,0 → 0,167), ancho de banda x 8,333 (real 100 → 8,33, sin alterar), contorno aplanado (pendientes ≤ 1:1), de y 7,66 a 15,21, z hasta 15,83.
- **Tornillos/pins (marcadores de unión)**: 4 taladros Ø1,2 (pasante) r=0,6, z 1,729, y = 4,9167 / 9,9167 / 34,5 / 39,5. No portan carga ni hilo (señal visual de unión).
- **Ranuras**: la luz mínima se llevó a **≥ 1,0** (se ensancharon las que caían por debajo: lumbar y dos de yugo). Grandes ventanas/taladros del panel según diseño real escalado.
- **Radios r=2 reales** (→ 0,17 escala): omitidos; esquinas rectas.
- **Holgura real panel↔placa 0,3 mm**: colapsada (fusión panel-placa).

### Mapeo 1:12 adoptado (LOCKED, [decisión]/[cálculo])

`x_m = x / 12` · `y_m = 2,0 + y_real / 12` (pedestal de peana 2,0 mm) · `z_m = (z + 8,75) / 12` (ribbons, contornos del generador real)
- **Pernos** [cálculo → hecho en modelo]: y_real 35/95/390/450 → y 4,9167 / 9,9167 / 34,5 / 39,5 (con el +2,0 del pedestal); z_real eje 12 → z 1,7292.
- Nota: la fila "Y de pernos" de la FICHA §C (2,92 / 7,92 / 32,50 / 37,50) correspondía al mapeo **sin** el pedestal de 2,0 y quedó **sustituida** por esta regla LOCKED. Corresponde a los pernos reales 35/95/390/450 (la cifra "7.92" de notas antiguas es esa tabla sin pedestal, no un error geométrico de este modelo).

## OPERACIONES (resumen)

Pieza única Inventor 2027.1 (.ipt nativo, sin .iam): peana (extrusión 2,0) + panel (0,8) + 2 placas (1,2) + 8 mejillas (1,2) + 2 canales (paredes 0,8 + alas 1,2, sección en C abierta a +z) + 2 cintas ribbon (1,2, pliegue/gancho del REAL omitidos, cola apoyada en peana) + 2 cunas ribbon (1,2, contorno aplanado) + 4 taladros de pasador Ø1,2. Todo fundido en **un solo sólido** (bodies = 1, verificado). Los huecos y ranuras del panel/placas se generaron como recortes dentro de cada extrusión; los taladros por extrusión pasante ±13,8.

## MATERIAL Y FABRICACIÓN

PLA según lo pedido. Orientación propuesta: **peana plana sobre la cama (z=0)**, altura total de impresión 42 mm, pie 27,5 × 16,08 → dentro de la placa (40×40 mínimo; deja ~2 mm de margen por lado para borde adhesivo). Supuesto de preparación: **boquilla 0,4 mm**, paredes ≥ 0,8 (2 perímetros), placas ≥ 1,2, agujeros ≥ Ø1,2, ranuras ≥ 1,0. Reconfirmar con el centro de impresión el perfil de laminador, altura de capa y estrategia de soportes.

Zonas a vigilar en laminador [hipótesis, **pendiente de comprobación en laminador**]: boca del canal (interrumpencia C abierta a +z), zonas del arco de la cinta y de la cuna que quedan sobre vacíos del panel/placas, cola de la cinta sobre la peana. Puede requerir soportes locales; no se garantiza impresión con cualquier equipo/configuración.

**Sin G-code, sin perfil de laminado, sin soportes precalculados. No se ha laminado ni impreso.** Esto es solo geometría; el laminado real queda como paso del centro de impresión.

## ENTREGABLES (hashes en INFORME_VERIFICACION.md)

1. `SEDAC_Maqueta_PLA_20261022.ipt` — pieza única nativa Inventor 2027.1.
2. `SEDAC_Maqueta_PLA_20261022.stl` — malla binaria 2164 triángulos, mm, hermética, 1 componente, volumen positivo.
3. `SEDAC_Maqueta_PLA_20261022.step` — AP por el traductor Inventor, 1 sólido manifold, 352 caras.
4. `SEDAC_Maqueta_PLA_20261022.3mf` — contenedor OPC con `unit="millimeter"` (montado manualmente a partir del STL porque Inventor 2027.1 no ofrece translator 3MF en esta instalación; verificado reabriendo el zip).
5. `CAPA_iso_frontal.png`, `CAPB_iso_trasera.png`, `CAPC_panel.png`, `CAPD_trasera.png` — capturas del propio Inventor (planos de trabajo ocultos). Dos capturas intermedias con planos visibles quedaron conservadas en `Soporte/Capturas_intermedias/`.
6. `DIMENSIONES_Y_ALCANCE.json` + `INFORME_VERIFICACION.md`.
7. La fuente de trazado (FICHA_ALCANCE.md y scripts usados) vive en la carpeta raíz de la iteración `Maqueta_PLA_20261022/`.

## DATOS FALTANTES (solo bloquean el laminado, no el modelo)

Impresora y boquilla reales, perfil de laminador, altura de capa, color de PLA, confirmación de soportes bajo boca de canal/arco de cinta. Si el centro de impresión usa otra boquilla, revisar los mínimos de la tabla.

## SUPUESTOS (no son datos medidos ni validados)

Escala 1:12 con espesores/taladros magnificados por reglas de imprimibilidad FDM; boquilla 0,4; Ø de taladro de pasador 1,2 (el pasador real Ø10,2 escalado daría 0,85); espesor ribbons 1,2; aplanado de cuna; omisión de radios; colapso de holgura; peana 2,0; posiciones de banda x de cinta reubicadas a todo el ancho de peana (±13,75), que el REF no tiene. Omisiones declaradas: pernos/herrajes M5 reales (solo taladro indicador), espuma y textiles reales, asa, hebillas, correas, marcadores de tachuela Ø2×0,6 (no construidos), ventana menor de mejilla y demás detalle no imprimible a 1:12.
