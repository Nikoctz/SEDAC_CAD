# SEDAC P2.02 — Prediseño mecánico y registro de decisiones
15 de octubre de 2026 · Modelo maestro en mm, escala 1:1

## Resultado y alcance

Esta revisión transforma la maqueta P2.01 en un prediseño mecánico parametrizado por regeneración. Integra perfiles cerrados, cartelas, refuerzos bajo la cuna, arriostramiento en X, uniones pasantes con casquillos, anclajes de hombro indexados, yugo de cinturón y protecciones de contacto.

**No constituye una garantía de que el equipo no falle, una capacidad de carga certificada ni un prototipo listo para llevar sobre una persona.** Las comprobaciones son modelos analíticos simplificados con hipótesis explícitas. No se hizo FEA, ensayo de fatiga, ensayo de caída ni validación del arnés. La bomba real sigue pendiente.

Se mantuvo el modelo maestro a tamaño real. La miniaturización no simplifica los cálculos ni permite escalar resistencia: una futura impresión pequeña debe ser una exportación separada con espesores adaptados.

## Qué se cambió y por qué

| Cambio | Problema que aborda | Límite pendiente |
|---|---|---|
| Dos tubos cerrados 6061-T6 de 50 × 25 × 2,5 mm | Flexión biaxial y torsión; profundidad contenida | Confirmar disponibilidad, certificado, radios y tolerancias del perfil real |
| Dos cartelas laterales, 5052-H32 de 4 mm, con dos M8 por lado | Transmitir momento de la cuna al marco | Revisar contacto, palanca, radios de plegado y concentraciones con FEA/ensayo |
| Dos tubos transversales bajo la cuna | Evitar que toda la carga dependa de una lámina en voladizo | Contacto real de bolsa y cargas concentradas |
| Piso de 2,5 mm, drenajes y salida circular abierta | Rigidez local, limpieza y espacio para la manguera | Medir posición y radio de curvatura de la manguera |
| Diagonales cruzadas en planos separados | Evitar deformación del rectángulo del marco | Se acredita solo la diagonal que trabaja a tracción, no la comprimida |
| Casquillos metálicos dentro de tubos | Reducir riesgo de aplastar paredes durante el apriete | Longitud real, asentamiento, tolerancias y precarga |
| Posiciones de hombro mediante agujeros discretos | Evitar depender solo de fricción en una ranura | Confirmar altura de torso y arnés real |
| Ranuras de cinta redondeadas y cantos con radio 0,6 mm cuando consta en REDONDEOS.json | Reducir cortes y abrasión | Inspección de acabado y prueba con cinta real |
| Yugo de cinturón independiente | Dar una interfaz explícita para llevar carga a la cadera | Cinturón, costuras, ajuste y liberación no están diseñados/validados |
| Interfaz dorsal en dos módulos con fijación independiente | Ventilación y evitar introducir plástico en uniones principales | Presión de contacto, confort y fijación de acolchado |
| Protector de bolsa sobre la cuna, con cavidades para tuercas | Separar la bolsa de los herrajes | Material térmico definitivo y desgaste |

El modelo tiene más piezas y una ruta de carga más definida que P2.01. **No se afirma que sea más ligero que aquella maqueta incompleta.** El aumento de rigidez y las uniones reales tienen un costo de masa. El peso se registra para poder reducirlo después de probar, sin quitar material a ciegas.

## Base de datos y supuestos

La referencia Scotty publicada indica 19 L, dimensiones de bolsa vacía de 25 × 16,5 pulgadas (635 × 419,1 mm) y conexión de manguera inferior central. Esas dimensiones de bolsa vacía no se sustituyen por dimensiones del volumen lleno. El mismo catálogo indica aproximadamente 18,2 kg lleno, dato que no se adopta para dimensionar porque resulta incoherente con 19 L de agua más equipo.

Se adopta por decisión de prediseño:
- Masa total de referencia: 25 kg de carga/equipo soportado. No es una medición ni una carga autorizada de uso.
- Caso combinado: 3 g verticales totales, incluida gravedad, y 1 g horizontal resultante, con dirección horizontal desfavorable.
- Fv = 735,75 N y Fh = 245,25 N.
- Reparto desigual entre rieles: 70/30.
- Brazo de la carga respecto del eje del riel: 100 mm.
- Altura equivalente de fuerza horizontal respecto de la sujeción: 400 mm.
- Amplificación local provisional K = 2 para tensión del riel. No proviene de una FEA de sus agujeros.
- Objetivo interno de margen frente a fluencia: 2,2 en la selección de riel. No es una exigencia normativa ni un factor global de seguridad.
- Flecha orientativa máxima: 5 mm en el modelo de viga.

Materiales de cálculo:
- 6061-T6 extruido sin soldar: límite de referencia 240 MPa, E = 69 GPa y densidad 2700 kg/m³. Confirmar certificado del producto.
- 5052-H32: se usa 130 MPa de forma conservadora. Atlas distingue mínimos según especificación; no se supone que todos los productos etiquetados 5052 sean equivalentes.
- Tornillería A2-70: límite de referencia 450 MPa para la sección resistente de rosca.
- Materiales y geometrías de contacto son candidatos de banco. La temperatura y el fuego no están incluidos en estos números.

## Selección de riel

Se evaluaron 12 alternativas; todas constan en COMPARACION_RIELES.csv.

Se exige cumplir margen 2,2 y flecha de 5 mm. Después se prioriza una profundidad máxima de 25 mm y menos de 1 kg para el par de rieles, eligiendo la menor masa entre las alternativas que satisfacen esas condiciones. Los límites son decisiones revisables, no una prueba de óptimo global.

La selección final 50 × 25 × 2,5 mm da aproximadamente:
- 0,902 kg para dos rieles sin descontar taladros, de 500 mm cada uno.
- Margen analítico 2,25 frente a fluencia.
- Flecha estimada 3,44 mm.
- 10 mm menos de profundidad que la alternativa 35 × 35 × 2,5 mm, por unos 68 g adicionales.

Esa comparación se refiere a perfiles con las mismas hipótesis. No demuestra una mejora ergonómica respecto de P0/P2.01. La distancia de la bomba al cuerpo depende además de bolsa llena, acolchado, fijaciones y arnés.

## Método de cálculo reproducible

El archivo CALCULOS_PRELIMINARES.json guarda entradas y resultados. El generador calcula área y segundos momentos de los perfiles con esquinas redondeadas por integración de un contorno discretizado fino. En Inventor se modelan arcos circulares reales.

Para cada riel, con s = 0,7:
- N = s Fv.
- Momento por excentricidad = s Fv e.
- Flexión horizontal combinada desfavorable: s Fh L √(1/Zx² + 1/Zz²).
- Tensión normal extrema = s Fv/A + s Fv e/Zx + la contribución horizontal anterior.
- Se añade una estimación de cortante medio y torsión de tubo cerrado por Bredt.
- Tensión equivalente = K √(σ² + 3τ²).
- Margen = límite de fluencia / tensión equivalente.

Se estima flecha con viga elástica en voladizo y superposición de carga horizontal y momento de carga. La condición de empotramiento es una idealización: el arnés real es flexible.

Se calculan también Euler con longitud efectiva 2L y pandeo elástico local de pared apoyada. Sus resultados no sustituyen análisis de pandeo de la sección perforada, imperfecciones, torsión o uniones. Si la tensión elástica calculada supera el límite del material, la fluencia gobierna primero.

En las cartelas:
- Momento externo combinado M = s(Fv e + Fh h).
- Dos M8 separados 45 mm.
- Reacción crítica aproximada = 1,2 √[(V/2)² + (M/45)²].
- Se verifica cortante del tornillo, aplastamiento de una sola pared del tubo y de la cartela, y arrancamiento hacia el borde.
- Se calcula una sección idealizada de la raíz con factor local 2. La abertura de aligeramiento y el ala requieren revisión local adicional.

En la cuna:
- Se combinan presión media duplicada y un parche adicional supuesto de 100 N sobre 50 mm.
- Los tubos inferiores se aproximan como vigas entre cartelas.
- El escenario supone contacto flexible repartido. Un apoyo rígido pequeño de la bomba puede invalidarlo.

Los puentes de ranura de hombro y cinturón se estiman como pequeñas vigas bajo una fuerza fuera del plano. No equivalen a un ensayo de cinta, costura o hebilla. Los M6 se revisan a cortante externo; queda pendiente tensión por palanca y precarga.

**Los márgenes de estas comprobaciones no se multiplican, promedian ni interpretan como un factor global del conjunto.**

## Modos de fallo que siguen abiertos

1. **Fatiga:** falta un espectro de pasos, vibración y golpes, curvas S-N del material y detalle real de agujeros. No se declara vida útil. Reducir cantos y evitar soldadura en 6061-T6 elimina algunas fuentes de incertidumbre, pero no valida fatiga.
2. **Uniones:** par, precarga, aflojamiento, aplastamiento bajo cabeza/arandela, apertura por palanca, fricción y desgaste requieren herraje real y pruebas. Los casquillos deben apoyar antes del apriete sin deformar paredes.
3. **Corrosión:** aislar o proteger adecuadamente contactos aluminio/inox y revisar drenaje. No añadir una lámina blanda que pueda fluir a una unión principal sin reevaluar precarga.
4. **Bolsa flexible:** medir deformación llena, posiciones de costura, manguera y puntos duros. Ensayar retención y desplazamiento sin personas.
5. **Arnés y cinturón:** no están validados. La geometría del yugo no demuestra transferencia efectiva a la cadera.
6. **Temperatura:** HDPE y acolchados son referencias de prototipo; no se han calificado para incendio forestal.
7. **Fabricación:** cuna y cartelas se representan mediante volúmenes nominales unidos. Faltan radio interior real, alivios, factor K, desarrollos y tolerancias. No cortar/plegar directamente desde este STEP.

## Qué medir y cómo decidir la siguiente revisión

Registrar bomba llena/vacía, masas, zonas de apoyo, posición de manguera/tapa, ancho y espesor de cintas, herrajes y ajuste del cinturón. Después editar PARAMETROS_P2_02.json y regenerar. Los límites del generador evitan cambios fuera del intervalo geométrico estudiado; no son límites de uso.

Con el laboratorio, revisar primero interfaces y materiales; después realizar ensayos instrumentados de banco para identificar deslizamiento, deformación residual, holguras y daño de bolsa. Las fuerzas anteriores son casos de cálculo, **no una instrucción de colgar 75 kg ni de hacer un ensayo sobre una persona**.

## Fuentes consultadas el 15/10/2026

- [Scotty, catálogo oficial, Alpha Backpack](https://scottyfire.com/wp-content/uploads/2017/04/2017ScottyFireCatalogue_LR.pdf): capacidad y ubicación de conexión, dimensiones de bolsa vacía.
- [Hydro, ficha de aleación 6061](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf): propiedades de extrusión y pérdida de resistencia local por soldadura.
- [Atlas, ficha 5052](https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf) y [nota 14](https://www.atlassteels.com.au/documents/TN14-5052%20and%205251%20rev%20June%202013.pdf): propiedades y diferencias de especificación.
- [Bossard, tornillería inoxidable](https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf): referencia de clase A2-70.
- [NASA RP-1228, Fastener Design Manual](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf): marco de revisión de grupos de tornillos, cargas combinadas, fatiga y bloqueo. Se utiliza como referencia técnica; SEDAC no se declara conforme a una norma aeroespacial.
- [Notion 03.8](https://app.notion.com/p/3f1f5e4bdb9081949942c96998f88385): antecedentes del concepto P2.



## Resultado geométrico y masa de esta generación

- 54 diseños de pieza sólidos y 70 ocurrencias en Inventor 2027.1.
- Actualización nativa correcta; 0 interferencias volumétricas en el ensamblaje nominal.
- Anclajes de hombro y yugo con redondeos de 0,6 mm.
- STEP de revisión exportado.
- Perfil seleccionado: 50 × 25 × 2,5 mm. Margen analítico aproximado 2.25 bajo las hipótesis del informe.
- Masa de metales sin herrajes: 2.494 kg.
- Masa de todo lo representado: 3.206 kg. Incluye geometría simplificada de herrajes y contacto; no incluye arnés completo, cintas ni hebillas.
- La masa no cumple aún el objetivo conceptual anterior de aproximadamente 1,5–2 kg añadidos. Debe revisarse tras medir y ensayar.
- No se realizó FEA ni se validó fatiga, fabricación, comodidad o seguridad de uso.

Las dos interferencias encontradas en la iteración anterior se resolvieron con agujeros en la pared posterior de la cuna y el aumento de agarre de los dos M6 inferiores. No se acredita esa fijación adicional para aumentar los márgenes calculados de las cartelas.
