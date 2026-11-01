# Ficha de cotas — Mosquetón giratorio P0

Unidades: **milímetros**. Escala 1:1. Tolerancia general indicada; las cotas
marcadas **supuesto** son valores provisionales editables en `SCRIPTS/modelo_p0.py`.

Clasificación: **medida** = tomada con instrumento (no hay ninguna en esta
ficha) · **cálculo** = derivada del modelo o de una fórmula del informe ·
**supuesto** = adoptada sin medir, provisional.

Las cotas "medida" de la bomba y del arnés están **pendientes**: no se midió
nada en esta sesión. Lo que sigue son cotas del modelo CAD.

---

## 1. Cuerpo del gancho (`P0_Cuerpo_Gancho`)

| Cota | Valor | Origen | Comentario |
|---|---|---|---|
| Espesor de placa (Y) | 9,0 | supuesto | holgura de impresión incluida en el hueco, no aquí |
| Luz interior de garganta (X) | 15,0 | supuesto | debe admitir el anillo real de la bolsa: **pendiente** |
| Radio interior de canasta | 7,5 | supuesto | define la superficie de apoyo del anillo |
| Espesor de brazo | 6,0 | supuesto | |
| Refuerzo exterior de espina | +3,1 (total 9,1) | cálculo | añadido para reducir flexión por excentricidad |
| Cara superior de brazo (Z) | 21,0 | supuesto | |
| Casquete de extremo de brazo | R3,0 | cálculo | = espesor de brazo / 2 |
| Bloque de horquilla: X | −14,0 a −3,0 | cálculo | contiene el eje del pivote |
| Bloque de horquilla: Z | 19,5 a 34,5 | cálculo | 1,5 mm de solape con el brazo |
| Ancho de horquilla (Y) | 16,0 | cálculo | 2 tetones de 3,3 + hueco de 9,4 |
| Hueco entre tetones (Y) | 9,4 | cálculo | = 9,0 del cubo + 0,4 de juego axial |
| Fondo del hueco (Z) | 21,4 | cálculo | 1,1 mm bajo el cubo; evita apoyo parásito |
| Eje del pivote (X, Z) | −6,5 ; 28,0 | cálculo | eje de giro, paralelo a Y |
| Agujero del pivote | Ø6,2 | cálculo | hombro ISO 7379 Ø6 h9 → juego radial 0,1 |
| Agujero del cierre | Ø4,2 a Z = 17,5 | cálculo | pasador Ø4 en doble cortante |
| Excentricidad eje de giro ↔ centro de canasta | 6,5 | cálculo | genera flexión en la espina (ver informe) |
| Bbox | 30,10 × 16,00 × 40,50 | cálculo | |
| Volumen / masa (PETG 1,27 g/cm³) | 4537 mm³ / 5,76 g | cálculo | |

## 2. Argolla (`P0_Argolla`)

| Cota | Valor | Origen | Comentario |
|---|---|---|---|
| Cubo | Ø11,0 × 9,0 | supuesto | pared de 2,4 mm alrededor del agujero |
| Agujero del cubo | Ø6,2 | cálculo | mismo hombro del pivote |
| Cuello | 6,0 × 9,0 | cálculo | esbelto para no chocar con la horquilla |
| Anilla exterior | 22,0 × 20,0 × 9,0 | supuesto | |
| Hueco de anilla | 12,0 × 11,0 | supuesto | para gancho metálico del arnés, **no** para cinta de 25 mm |
| Radio de esquinas de anilla | 3,95 | cálculo | deriva de 22/20 y del hueco 12/11 |
| Base de la anilla (Z) | 36,5 | cálculo | 2,0 mm sobre el tope de la horquilla |
| Bbox | 22,00 × 9,00 × 34,00 | cálculo | |
| Volumen / masa | 3413 mm³ / 4,33 g | cálculo | |

## 3. Herrajes comerciales (por unidad)

| Elemento | Designación | Origen | Función |
|---|---|---|---|
| Eje del pivote | ISO 7379 M6×16, A2 (hombro Ø6 h9, rosca M5) | supuesto | eje de giro; trabaja a cortante, no a tracción |
| Tuerca | M5 nylon-insert (nyloc), A2 | supuesto | retención axial del eje |
| Arandela | DIN 125 M5, A2 (1 ud.) | supuesto | apoyo de la tuerca sobre el tetón |
| Cierre | Pasador de horquilla Ø4×30 (DIN 1443) + clip | supuesto | cierre del gancho; trabaja a cortante |
| Suplemento de giro | arandela de PTFE/nylon 0,2 mm (opcional) | hipótesis | para fijar el juego axial; **sin seleccionar** |

Paso útil del pivote: 3,3 (tetón) + 9,4 (hueco) + 3,3 (tetón) = **16,0**, igual
a la longitud del hombro del tornillo M6×16. **hecho** por construcción del
modelo; **pendiente** verificar en la pieza comprada.

## 4. Conjunto

| Cota | Valor | Origen |
|---|---|---|
| Envolvente en montaje | 31,01 × 16,00 × 62,50 | cálculo |
| Masa impresa total (PETG) | 10,10 g | cálculo |
| Juego axial cubo–tetones | 0,40 (0,20 por cara) | cálculo |
| Juego radial cubo–hombro | 0,10 (0,20 diametral) | cálculo |
| Interferencia en posición de montaje | 0,0 mm³ | cálculo (booleano) |
| Distancia mínima en montaje | 0,20 mm | cálculo (BRepExtrema) |

## 5. Interfaz con la bomba y el arnés — **pendiente**

Nada de esta sección está medido. Se describe lo que se ve en las fotografías
aportadas y lo que hay que medir.

| Punto | Observación visual (no medición) | Estado |
|---|---|---|
| Ojales de esquina de la bolsa | ojal remachado, Ø interior aparente ≈10 mm según cinta métrica en la foto | **pendiente de medir** |
| Anillos superiores | cinta negra con dos anillos metálicos junto a la manija/conector | **pendiente de identificar y medir** |
| Anillos de la manija | el manual prohíbe conectar ahí los clips del arnés | **excluidos por manual** |
| Ganchos del arnés | ganchos metálicos de resorte tipo langosta + una anilla en D | **pendiente de medir** (paso de gancho) |
| Ancho de cinta del arnés | cinta de mochila, a ojo 25–30 mm | **pendiente de medir** |
| Estado del arnés | cintas cortadas y deshilachadas en varios puntos | **no usar para ensayos cargados sin reparar** |

Consecuencia de diseño: el hueco de la anilla (12 × 11) se dimensionó para el
**gancho metálico** del arnés, no para cinta de 25 mm. Si el montaje final usa
cinta, hay que subir `SLOT_W` a ~26 y rehacer la pieza (la anilla pasaría a
medir 36 de ancho y habría que reorientar la impresión).

## 6. Qué ajustar cuando llegue la bomba

1. Medir el **anillo real** (diámetro interior, diámetro de material, forma) y
   comprobar que pasa por la garganta de 15 mm y apoya en la canasta de R7,5.
2. Medir el **gancho del arnés** (paso de la abertura) y comprobar el hueco
   12 × 11 de la anilla.
3. Medir el **espesor y ancho de cinta** en los cuatro puntos y decidir si la
   anilla va a cinta o a gancho.
4. Verificar que la pieza no interfiere con la manguera ni con el conector
   rápido al plegar la bolsa.
5. Repetir la verificación de interferencias con la geometría corregida.
