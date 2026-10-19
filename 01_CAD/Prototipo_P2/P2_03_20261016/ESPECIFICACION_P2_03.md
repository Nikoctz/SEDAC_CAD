# Especificación final SEDAC P2.03 / 16-10-2026

## UNIDADES

Milímetros, newtons, MPa y kilogramos. CAD maestro a escala 1:1; no se reduce la escala para disminuir la masa declarada.

## TIPO DE PIEZA/PLANO

Ensamblaje auxiliar de doble riel para bomba de espalda. Revisión de prediseño aligerada, con uniones comerciales representadas y memoria analítica. No incluye planos de fabricación liberados.

## PARÁMETROS GEOMÉTRICOS

- Altura 500; separación de ejes 200; cuna 300 x 125; piso a Y=135, espesor 2,5.
- Riel 50 x 40 x 1,5; radios exteriores 3 e interiores 1,5. Pared mínima propuesta para recepción: 1,4.
- Tres refuerzos 20 x 10 x 1,5, a 15/60/105 desde el borde posterior.
- Cartelas: alma 3, ala 5, raíz de altura 115. Dos pasadores huecos por lado, OD10/ID6,6/L53, taladro 10,2; M6 interno.
- Anclajes de hombro/cinturón: alma 2, retornos hasta profundidad 18, puentes 24/26; cálculo con pared 1,8 y luz de ranura 52.
- Protector HDPE: cara continua de 2; hueco inferior de 12; apoyos perimetrales e interiores. Separa puntas de M5 de la bolsa.
- Diagonales 20 x 2 en planos distintos; travesaños 232 x 28 x 2.
- Casquillos M6 interiores OD10/ID6,6/L37. Apoyos M5 con perfil interior redondeado 17 x 7, ancho 10 y taladro 5,5.
- Tornillos ISO 4762 M6x55/60/65 y M5x40, rosca parcial; arandelas ISO 7089; tuercas metálicas autofrenantes derivadas DIN 980.
- Roscas M6x1 y M5x0,8, derechas, 6g externas/6H internas. No hay M8 en la entrega final. La clave interna heredada bolt8_y solo conserva el nombre histórico de las posiciones 20/100.

## OPERACIONES

Sólidos nativos por extrusión, vaciados y taladros; redondeos de 0,4 en los cuatro anclajes; roscas cosméticas nativas. Un riel fijado y 3 restricciones de posición por cada otra ocurrencia. CAD de chapa representado como sólido nominal; no hay desarrollo validado de plegado.

## MATERIAL Y FABRICACIÓN

6061-T6 sin soldar para rieles, refuerzos, cartelas, anclajes y apoyos; 5052-H32 para cuna y diagonales. Anclajes y cartelas se plantean mecanizados, no doblados de 6061-T6 con propiedades asumidas intactas. Tornillos A2-80. Tuercas clase 80 requerida; producto autofrenante y carga de prueba pendientes de proveedor. HDPE y espuma son candidatos.

Confirmar perfiles, radios, temple y espesores reales. Definir proceso de cuna, tolerancias, desbarbado, acabado de cantos para cintas, protección contra corrosión y accesibilidad de montaje. No se acredita soldadura.

## ENTREGABLES

51 IPT, 1 IAM con 131 ocurrencias, STEP, tres vistas reales, BOM, masas y registros; parámetros y generadores; Mathcad editable con resultados guardados; fuente LaTeX y PDF Beamer de 55 diapositivas; hoja personal de medición.

## DATOS FALTANTES CRÍTICOS

Bomba llena/vacía, centro de masa, contacto, manguera y arnés real. Productos comerciales, tolerancias y asiento de pasadores. Fatiga, impacto, vibración, temperatura, desgaste, FEA de detalles, textiles y comportamiento biomecánico. Estos datos condicionan la siguiente iteración y su eventual fabricación.

## SUPUESTOS

Masa total de cálculo 25 kg, incluyendo el auxiliar y arnés; 3 g verticales totales, 1 g horizontal, reparto 70/30, n requerido 2,2 y flecha límite 5. Brazo e=107,5 y longitud L=423. Factores locales Kt=2, Kb=1,2 y Kslot=1,5 provisionales. Reserva textil 0,50 kg y otros accesorios 0,08 kg. Datos de prediseño, no mediciones.
