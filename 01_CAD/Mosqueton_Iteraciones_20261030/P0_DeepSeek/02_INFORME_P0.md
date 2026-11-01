# Informe P0 — Mosquetón giratorio para bomba de espalda

Versión P0, 2026-10-29. Prediseño para prototipos de laboratorio.
**No validado para personas ni para combate de incendios.** No hay FEA ni
ensayo físico en este documento.

---

## 1. Decisión de arquitectura

**Hipótesis de montaje (no comprobada):** dos conexiones superiores, una por
lado, entre el anillo superior de la bolsa y el gancho del arnés; los puntos
inferiores quedan para ajuste y estabilización. **No se supone reparto igual**
entre los cuatro puntos.

**Topología elegida para P0:** gancho tipo mosquetón con **pivote transversal**
sobre **tornillo de hombro comercial ISO 7379 M6×16**, y **cierre por pasador
de horquilla Ø4** en doble cortante.

Esto resuelve el problema que el modelo previo dejó abierto: el eje Ø7 con
cabezales Ø15 no podía pasar por el alojamiento Ø8. En P0 los cabezales
integrales se sustituyen por un herraje que se monta y se desmonta, y la
retención axial queda **separada de la superficie de giro** (el hombro trabaja
dentro del cubo; la tuerca y la arandela apoyan fuera, sobre la cara exterior
del tetón, 3,3 mm más allá).

**Camino de carga (principal):** anillo de la bolsa → canasta → espina → tetones
→ tornillo Ø6 (cortante doble) → cubo de la argolla → anilla → gancho del arnés.
Los brazos y el pasador de cierre **no** están en ese camino: solo retienen.

---

## 2. Cargas

| Caso | Valor | Origen |
|---|---|---|
| Masa supuesta del sistema lleno | 20 kg | supuesto del encargo |
| Peso estático total | 196,2 N | cálculo (20 · 9,81) |
| Reparto ideal entre 2 conexiones | 98,1 N | cálculo, **hipótesis de reparto igual** |
| Carga concentrada en una conexión | 196,2 N | cálculo, caso conservador |
| Factor dinámico adoptado | k = 2,0 | **supuesto de prediseño** |
| Carga de diseño usada en los cálculos | 392,4 N | cálculo |

Sobre el factor k = 2,0: se adopta como **supuesto de prediseño** para
contemplar marcha sobre terreno irregular y manejo de la bomba. **No proviene de
una norma** y no se atribuye a ninguna. Es revisable con mediciones de
aceleración en uso real. No se adopta factor de seguridad: **queda pendiente**,
porque no hay resistencias admisibles trazables para una pieza FDM.

---

## 3. Cálculos reproducibles

Script: `SCRIPTS/calculos_p0.py` (ejecutado; salida en
`EVIDENCIAS/calculos_p0.json`). Fórmulas elementales de resistencia de
materiales. **Límites:** sección constante, material isótropo, sin
concentración de esfuerzo, sin fluencia, sin efecto de capas ni de temperatura.

| Modo | F [N] | σ [MPa] | Comentario |
|---|---|---|---|
| Tornillo Ø6 en cortante doble | 392,4 | 6,50 | acero A2; no es el elemento crítico |
| Presión de contacto cubo (PETG) sobre hombro | 392,4 | 7,03 | área proyectada Ø6,2 × 9 |
| Presión de contacto por tetón (2 tetones) | 196,2 | 9,59 | reparto 50/50 supuesto |
| Sección neta del tetón (arranque) | 196,2 | 12,39 | sin Kt; Kt real > 1 |
| **Flexión de la espina, carga estática** | 196,2 | **10,50** | e = 6,5 mm; sección 9,1 × 9 |
| **Flexión de la espina, caso conservador** | 392,4 | **20,99** | mismo modelo con k = 2 |
| Arco de canasta (media circunferencia) | 196,2 | 9,45 | coeficiente 0,32: aproximado |
| Pasador de cierre Ø4 en cortante doble | 392,4 | 15,61 | solo si la bolsa empuja el cierre |
| Torsión del cuello (excentricidad supuesta 10 mm) | 196,2 | 13,71 | indica centrar la cinta en el eje |

**Lectura:** el modo que controla es la **flexión de la espina por la
excentricidad de 6,5 mm** entre el centro de la canasta y el eje de giro.

Con la resistencia de referencia del PETG impreso (39 MPa en el plano de capa,
16,4 MPa entre capas — Prusament PETG V0, ficha), la relación es:

- carga estática, solicitación **en el plano** de capa: 39 / 10,50 = **3,7**
- carga estática, solicitación **entre capas**: 16,4 / 10,50 = **1,56**
- caso conservador (k = 2), **entre capas**: 16,4 / 20,99 = **0,78 → supera la referencia**

Estas relaciones **no son un factor de seguridad**: son comparaciones contra
valores de ficha de probeta, no contra admisibles de la pieza. Lo que sí se
concluye: **con PETG y la orientación desfavorable, el caso conservador no se
sostiene ni siquiera frente a la ficha.** El ensayo debe hacerse a carga
reducida y con la orientación favorable, y el rediseño debe bajar la
excentricidad o cambiar de material.

---

## 4. Modos de falla a vigilar

| # | Modo | Dónde | Cómo se manifiesta | Se controla con |
|---|---|---|---|---|
| F1 | Flexión excesiva / rotura de la espina | unión canasta–horquilla | deformación permanente, blanqueo, rotura en la capa | tracción hasta falla |
| F2 | Arranque del tetón por la sección del agujero | tetones de la horquilla | apertura de la horquilla, holgura creciente | tracción + inspección |
| F3 | Ovalización del agujero del cubo | cubo de la argolla | juego radial, giro con holgura | ciclado + medición Ø |
| F4 | Fluencia del PETG por presión de contacto | cara del cubo / hombro | marca, asentamiento, aumento de juego axial | carga sostenida |
| F5 | Apertura del cierre | pasador Ø4 | pérdida del clip, pasador desplazado | inspección + tracción con carga lateral |
| F6 | Falla del pasador en cortante | agujeros del brazo | corte del pasador o desgarro del agujero | carga lateral |
| F7 | Aflojamiento de la tuerca del pivote | rosca M5 | juego axial, cubo suelto | ciclado + par de apriete |
| F8 | Desgaste del par PETG–acero | cubo / hombro | aumento de juego, ruido | 500 ciclos |
| F9 | Rotura de la anilla | sección de la anilla | apertura del hueco | tracción hasta falla |
| F10 | Falla de la interfaz bolsa/arnés (fuera de la pieza) | anillos y cintas | desgarro, costura | **no se ensaya con esta pieza** |

---

## 5. Comparación de las dos formas de resolver el giro

| | A. Impresión conjunta (print-in-place) | B. Montaje posterior con retención desmontable (elegida) |
|---|---|---|
| Fabricación | una sola impresión, sin armado | 2 piezas + herrajes |
| Holgura de giro | la que deje la impresora entre capas (≈0,2–0,4); no ajustable | fijada por el hombro Ø6 h9 y el agujero Ø6,2; **ajustable** |
| Retención axial | tiene que ser un resalte impreso; no se puede inspeccionar | tornillo + tuerca nyloc; **verificable y reemplazable** |
| Superficie de giro | PETG sobre PETG, con rebabas de la separación | acero sobre PETG; se puede cambiar el herraje |
| Verificación | no se puede desarmar sin romper | se desarma y se vuelve a montar |
| Riesgo | si la holgura sale mal, se descarta la pieza | si la holgura sale mal, se cambia el herraje o el cubo |
| Modo de falla propio | fusión parcial de la junta; retén impreso frágil | rosca/tuerca que se afloja (F7) |

**Elegida: B.** Razón: la A no permite inspeccionar la retención ni corregir la
holgura, y su retén axial sería justamente la "lámina frágil" que el encargo
pide evitar. El costo de B es un herraje comercial y un armado.

**Alternativa considerada y descartada para P0:** giro de 360° por caña
(barrel) alrededor de la línea de carga. Da el giro que un "giratorio" suele
necesitar, pero exige un retén axial desmontable **accesible desde un extremo**;
como el ojo de la argolla tapa el extremo inferior, habría que desplazar el ojo
lateralmente —lo que introduce un momento por excentricidad— o partir la
argolla. Queda como **iteración P1**, no como parte de P0.

---

## 6. Materiales

Servicio de impresión: procesos y materiales **sin confirmar**. Todo lo que
sigue es comparación de **fichas de fabricante**, no de la pieza.

| Propiedad | PETG (Prusament PETG V0) | PETG (PolyLite) | PA6-CF20 (Fiberon) |
|---|---|---|---|
| Densidad | 1,27 g/cm³ | 1,25 g/cm³ | no publicada en la ficha consultada |
| σ tracción XY / Z | 39 ± 2 / — (adherencia entre capas 16,4 ± 1,3) | 50,8 / 42,8 MPa | 105 / 67,7 MPa |
| Módulo E XY / Z | 1,7 / 1,8 GPa | 2117 / 1899 MPa | 7453 / 4354 MPa |
| Alargamiento | 3,5 % (en fluencia) | 8,4 / 3,3 % | 3,0 / 2,5 % |
| Flexión | 60–64 MPa | 69,6 MPa | 169 MPa |
| Charpy entallado | no aplica | 2,6 kJ/m² | 13,3 kJ/m² (sin entalla) |
| HDT | 68 °C (0,45 MPa) | 78 °C (0,45 MPa) | 215 °C (0,45 MPa) |

Fuentes: prusament.com (TDS PETG V0), wiki.polymaker.com (PolyLite PETG),
polymaker.com / fiberon.polymaker.com (PA6-CF20).

**Elección para P0: PETG FDM**, por disponibilidad, rigidez intermedia y
alargamiento suficiente para no romper frágilmente en el armado. **No se le
atribuyen** a la pieza las propiedades de la probeta: la resistencia real
depende de orientación, paredes, relleno, temperatura y humedad, y no se conoce
el proceso del servicio.

**Candidato para carga:** PA6-CF20 (≈2,7× la resistencia en XY y 3,4× el módulo
del PETG), con dos costos: es más frágil (3 % de alargamiento) y exige boquilla
endurecida, secado y 280–300 °C, lo que **no está confirmado** en el servicio.

---

## 7. Orientación de impresión

| Pieza | Orientación propuesta | Por qué | Limitación |
|---|---|---|---|
| Cuerpo del gancho | eje del pivote (Y del modelo) vertical | agujeros Ø6,2 y Ø4,2 salen redondos; espesor de placa en el plano de capa | la flexión de la espina queda **entre capas** (16,4 MPa de referencia) |
| Argolla | eje del pivote vertical | agujero del cubo redondo | el hueco de la anilla se imprime como puente de 12 mm (leve flecha) |

**hecho (limitación detectada en el análisis):** con la orientación de la tabla,
el tetón superior de la horquilla queda **en voladizo sobre el hueco de 9,4 mm**
y necesita soporte; además su unión al resto es un nervio de 0,5 mm en el
extremo del bloque. Es un defecto de fabricación del P0, no un detalle.

**Corrección propuesta para P1 (no ejecutada):** abrir el hueco de la horquilla
hacia arriba (horquilla en "U" abierta) para que ningún tetón quede en voladizo,
y cerrar el giro con el hombro del tornillo por un solo lado. Alternativa: girar
la horquilla 90° respecto de la placa.

Parámetros de referencia (a acordar con el servicio): boquilla 240–250 °C, cama
80 °C, capa 0,2 mm, 4 perímetros, relleno 60–100 %, ventilador bajo, filamento
seco. No son parámetros verificados en este equipo.

---

## 8. Verificación ejecutada (y la que no)

**hecho — verificado en esta sesión, con los scripts del paquete:**

1. El modelo se construye sin error y cada sólido es válido (`isValid`).
2. STEP reimportado: volúmenes coinciden (gancho 4537,3 mm³; argolla 3412,5 mm³;
   conjunto 2 sólidos, 7949,8 mm³ = suma exacta de ambas piezas).
3. STL: binarios consistentes (1728 y 3880 triángulos); tamaño de archivo
   coherente con la cabecera en los cuatro archivos.
4. **Conjunto en posición de montaje: interferencia 0,0 mm³** (booleano),
   **distancia mínima 0,20 mm** y **0 vértices dentro** del otro sólido.
5. Envolventes: gancho 30,10 × 16,00 × 40,50; argolla 22,00 × 9,00 × 34,00;
   conjunto 31,01 × 16,00 × 62,50.
6. Sobre de impresión: ambas piezas caben en la referencia histórica
   40 × 40 × 70. **Esa referencia no está confirmada para este servicio**: se
   comprobó contra ella, no contra el volumen real, que se desconoce.

**no verificado — no se declara:**

- **No hay `.iam` ni `.ipt`**: no se guardó, no se reabrió y por tanto **no se
  comprobó la persistencia de restricciones** en Inventor. La comprobación de
  "guarda y reabre" del encargo **no se ejecutó**.
- **Barrido de giro: inconcluso.** Tres métodos dan resultados distintos:
  el booleano de intersección devuelve volúmenes con coordenadas imposibles
  (material de la argolla a |Y| > 4,5 donde no existe); la distancia mínima
  devuelve 0,0 desde ±4° pese a una holgura modelada de 2,0 mm; el muestreo de
  vértices no detecta penetración en ±90° pero es demasiado grueso para
  concluir. **No se declara un rango de giro validado.**
- Por geometría, el primer contacto esperado es entre el borde inferior de la
  anilla y la cara superior de la horquilla: con 2,0 mm de luz y un brazo de
  7,5 mm, **θ ≈ arcsen(2,0/7,5) ≈ 15°**. Es un **cálculo**, no una verificación.
- No se comprobó el ajuste físico con la bomba ni con el arnés.

**Consecuencia honesta:** P0 es un **pivote de recorrido limitado (≈±15°)**,
no un giratorio de 360°. Para el primer prototipo alcanza para montar y para
ver la cinemática, pero **no cumple** el objetivo de giro si se exige libertad
completa. La corrección está en §5 (alternativa barrel) y en subir la luz
anilla–horquilla.

---

## 9. Plan de ensayos de banco

**Reglas:** banco con carga inerte, **sin personas en la zona de carga**,
pantalla de contención, carga lenta (≈5 mm/min), registro de carga y
desplazamiento, fotografía del modo de falla. Nada de esto se ha ejecutado.

| Ensayo | Muestra | Carga / criterio | Qué se mide |
|---|---|---|---|
| E1 Tracción estática hasta falla | 2 | rampa hasta rotura | carga máxima, modo (F1/F2/F9), desplazamiento |
| E2 Prueba de prueba (proof) a 98 N | 2 | 98 N sostenidos 60 s | deformación residual, marcas |
| E3 Carga lateral / cross-load | 1 | 50 % de la carga de E1 | apertura del cierre (F5/F6) |
| E4 Ciclado del giro | 1 | 500 ciclos sin carga | juego radial, desgaste (F8), temperatura |
| E5 Ciclado del cierre | 1 | 200 aperturas/cierres | retención del clip, holgura |
| E6 Retención axial inversa | 1 | 20 % del peso, 10 ciclos | desplazamiento del cubo, tuerca (F7) |

**Sobre las 4 unidades previstas: no alcanzan.** Con 2 unidades para montaje y
2 para ensayos, no se cubre E1–E6 ni se puede repetir una muestra. Propuesta:

- 2 unidades para montaje dimensional (una de ellas queda montada en la bomba).
- 2 unidades para E1 (permite ver dispersión entre dos piezas).
- 1 unidad para E3, 1 para E4, 1 para E5, 1 para E6.
- 2 de reserva por rotura en armado o por repetición.

**Total recomendado: 10 unidades** (≈101 g de PETG). Si se quiere afirmar algo
sobre dispersión, harían falta 3 probetas por ensayo, es decir 12–15 unidades.
Con 4 solo se puede hacer una demostración, no un ensayo.

---

## 10. Pendientes

1. **Medir** bomba y arnés: anillos (Ø interior, material, forma), cintas
   (ancho, espesor), masa llena y vacía, centro de masa. Bloquea el ajuste.
2. **Reparar o reemplazar el arnés**: las fotos muestran cintas cortadas y
   deshilachadas; no sirve para ensayos cargados.
3. **Confirmar** procesos, materiales y volumen de impresión del servicio
   (la referencia 40 × 40 × 70 no está confirmada).
4. **Rediseñar la horquilla** (§7) y **decidir el tipo de giro** (§5): pivote
   con más recorrido o caña de 360° con retén accesible.
5. **Reducir la excentricidad** de 6,5 mm (alinear canasta y eje) o cambiar a
   PA6-CF20, y repetir los cálculos.
6. **Reconstruir el modelo nativo en Inventor** y ejecutar la verificación que
   aquí falta: guardar, reabrir, mover el giro y comprobar restricciones e
   interferencias (puntual o continua, declarándolo).
7. **Definir el par de apriete** de la tuerca del pivote y el juego axial
   objetivo, con galga.
8. **Seleccionar** el suplemento de giro (PTFE/nylon) y el pasador con su clip.
9. **Ejecutar E1–E6** y recién entonces discutir resistencia.
10. **No liberar** el conjunto para uso con personas ni para servicio.
