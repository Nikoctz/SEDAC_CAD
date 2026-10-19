# P2.02 — Ficha de especificación CAD

## UNIDADES:
- mm, N, MPa y kg. Maestro a escala 1:1.
- Ejes X ancho, Y altura, Z hacia la bolsa.

## TIPO DE PIEZA/PLANO:
- Prediseño de marco de mochila SEDAC con cuna, uniones, anclajes y referencias de contacto.
- Ensamblaje de Inventor con piezas editables y posiciones fijadas.
- Configuración central y regeneración automática. No es ensamblaje adaptativo ni plano de fabricación.

## PARÁMETROS GEOMÉTRICOS:
- Fuente editable: PARAMETROS_P2_02.json.
- H = 500; separación de rieles = 200; cuna = 300 × 125; piso a Y = 120 y espesor 2,5.
- Sección seleccionada por cálculo y preferencia de proximidad: 50 × 25 × 2,5, con radios de representación exteriores 5 e interiores 2,5.
- Cartelas 4; refuerzos inferiores 20 × 20 × 1,5; anclajes y yugo 5.
- Hombros ajustables por patrón discreto de agujeros, paso 20, tornillos separados 40.
- M6 diámetro de paso 6,6; M8 diámetro de paso 8,6; M5 5,5; M4 4,5: valores de diseño provisionales.
- Tolerancias: pendientes. No extrapolar ajuste de casquillos desde las dimensiones nominales.
- Roscas: no modeladas; herrajes representados por envolventes.
- Cotas de bomba llena: pendientes. No se modeló una bomba ficticia como si fuera medida.

## OPERACIONES:
- Extrusiones y vaciados con perfiles redondeados, taladros, ranuras, refuerzos y montaje.
- Cantos de anclajes y yugo: redondeo 0,6 mm confirmado cuando REDONDEOS.json indica aplicado.
- Verificación de cuerpos sólidos, actualización nativa e interferencias volumétricas.
- Cambio de parámetros -> cálculo -> geometría -> nueva carpeta Inventor -> verificación.
- Si los criterios de riel no se cumplen o hay interferencias significativas, la regeneración debe detenerse y conservar el resultado parcial identificado.

## MATERIAL Y FABRICACIÓN:
- Candidatos: 6061-T6 extruido sin soldar para perfiles y placas pequeñas; 5052-H32 para cartelas, cuna y diagonales.
- Certificación de aleación, temple, espesor y disponibilidad de perfiles: pendiente.
- Acabados: proteger cantos y contacto de cintas, bolsa y cuerpo. Ensayo de desgaste pendiente.
- Uniones principales pasantes y con casquillos metálicos; no se acredita fricción para transmitir carga.
- Par, arandelas, tuercas, longitud comercial y prevención de aflojamiento: por especificar con componentes reales.
- Radios de plegado, factor K, alivios y desarrollos: pendientes. Los pliegues nominales del CAD no son una instrucción de plegado.
- HDPE y pads son candidatos de prototipo, sin calificación térmica.

## ENTREGABLES:
- IPT de cada diseño de pieza, IAM, STEP de revisión, capturas PNG.
- Parámetros, generador y comando de regeneración.
- Cálculos, comparación de perfiles, BOM, masas según volumen, interferencias y registro de redondeos.
- Sin STL nuevo para fabricación funcional. La versión pequeña P2.01 no queda convertida automáticamente en P2.02.

## DATOS FALTANTES CRÍTICOS:
- No bloquean el prediseño geométrico: dimensiones finales, masa y forma de bolsa llena.
- Bloquean fabricar/usar: medidas e interfaces reales, caracterización de carga, definición de arnés/cinturón, revisión de uniones, materiales certificados, proceso y ensayos.
- Fatiga, temperatura, golpe/caída y ergonomía: no resueltos por la malla ni por el margen de fluencia.

## SUPUESTOS:
- 25 kg de masa total de cálculo; 3 g verticales totales y 1 g horizontal resultante; reparto 70/30.
- Brazo de 100 mm y altura equivalente no menor de 400 mm ni de H−100.
- Factores locales son provisionales. No equivalen a concentraciones de tensión verificadas.
- Véase INFORME_DISENO.md y cada resultado de CALCULOS_PRELIMINARES.json.

