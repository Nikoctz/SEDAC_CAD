# P2.01 — Especificación de maqueta · 15/10/2026

## UNIDADES:
- Milímetros. Ejes: X ancho, Y altura, Z hacia la bomba.
- Disposición de miniatura aproximadamente 1:12; espesores aumentados. No es una reducción uniforme.

## TIPO DE PIEZA/PLANO:
- Ensamblaje geométrico de doble riel para estudiar arquitectura P2 en Inventor.
- 12 componentes: 2 rieles, 3 travesaños, cuna, 2 anclajes, interfaz dorsal y 3 pads.
- Una segunda pieza integra la estructura en miniatura. No contiene respaldo, pads, bomba ni arnés.
- No son planos de fabricación ni un sistema funcional.

## PARÁMETROS GEOMÉTRICOS:
| Elemento | Geometría de representación en mm | Origen |
|---|---|---|
| Altura de riel | 420 | Altura del panel provisional P0 |
| Separación entre ejes de rieles | 180 | Referencia de separación de fijaciones P0, propuesta para P2 |
| Sección de riel | canal de 30 de ancho, 15 de profundidad, 1,5 de espesor | Nueva propuesta de maqueta |
| Travesaños | 210 × 30 × 2, a alturas 50, 210 y 360 | Nueva propuesta de maqueta |
| Cuna | piso 280 × 140 × 2, pared posterior hasta altura 60; labios laterales de 15 sobre piso | Envolvente P0; espesor candidato de Notion |
| Abertura frontal de cuna | 60 × 60; esquinas rectas simplificadas | Ancho de referencia P0; profundidad propuesta |
| Anclajes | 70 × 60 × 3; abertura de cinta 52 × 5 y dos ventanas 6,2 × 20 | Rediseño provisional a partir de anclajes P0 |
| Interfaz HDPE | 260 × 390 × 2,5 | Nueva envolvente propuesta; espesor dentro de rango de Notion |
| Pads laterales | 90 × 240 × 10 cada uno | Volumen visual propuesto, no selección ergonómica |
| Pad lumbar | 200 × 50 × 10 | Volumen visual propuesto |
- Parámetros editables: las seis coordenadas/dimensiones de cada operación Block en la regla, en orden X,Y,Z,ancho,alto,profundidad. También se entrega GEOMETRIA_P2.json.
- Los bocetos y extrusiones son editables; no están completamente acotados. No existe asociatividad de montaje: modificar y regenerar una versión.
- Tolerancias: no especificadas.
- Roscas: no modeladas, selección pendiente.
- Radios y ranuras redondeadas: pendientes; las ventanas actuales son rectangulares.
- Miniatura: espesor de representación mínimo 1,2; piso 1,4. Omite ranuras diminutas y aumenta algunos contornos. Envolvente calculada 24,37 × 35 × 11,96.

## OPERACIONES:
- Bocetos rectangulares, extrusiones de unión y cortes; piezas separadas en ensamblaje fijado (Grounded).
- La sección en canal representa la forma plegada. No usa el entorno de chapa: sin radios reales, factor K ni desarrollo.
- La miniatura une los elementos en un cuerpo, con geometría aumentada para representación.
- Uniones reales de travesaños/rieles/cuna y fijación al cinturón: por diseñar. Contactos geométricos no son uniones mecánicas.

## MATERIAL Y FABRICACIÓN:
- Candidato estructural de Notion: AA5052-H32, 1,5–2 mm; anclajes 2–3 mm. No asignado como material mecánico validado en Inventor.
- HDPE candidato 2–3 mm. Pads: grado, dureza y espesor funcional no especificados.
- Colores son apariencia. No usar la masa de material predeterminado de Inventor como estimación de SEDAC.
- Acabados, radios de plegado, herrajes, procesos y tolerancias de fabricación: no especificados.
- Impresión de miniatura: material, orientación, soportes y resolución a acordar con el laboratorio. Verificar límite actual.
- Bomba, cintas, tirantes, cinturón y tornillería no incluidos. La conexión al cinturón requiere desarrollo posterior.

## ENTREGABLES:
- Regla SEDAC_P2_GENERAR.iLogicVb.
- Piezas IPT y ensamblaje IAM si la ejecución nativa finaliza; consultar ESTADO_OK.txt.
- Miniatura STL cerrada de un volumen, vista previa PNG y datos geométricos JSON.
- Registro de verificación geométrica. No certifica impresión, ergonomía ni resistencia.

## DATOS FALTANTES CRÍTICOS:
- Ninguno que impida esta maqueta conceptual con cotas provisionales.
- Para el siguiente modelo ajustado: dimensiones de bomba vacía/llena, volumen real, tapa, manguera, puntos de sujeción, arnés/cinturón y distancia al cuerpo.
- Para fabricación: carga objetivo, uniones y tornillería, radios de plegado, material definitivo y proceso disponible.
- Para evaluación funcional: cálculo/revisión y pruebas de banco.

## SUPUESTOS:
- La petición de construir maquetas permite adoptar envolventes de representación; todas las nuevas cotas de esta ficha son decisiones provisionales de diseño, no medidas de la bomba.
- Se conserva la altura general P0 y el tamaño de su cuna para comparar arquitecturas.
- No se ha demostrado que P2 pese menos ni acerque más la bomba con estas cotas. Debe compararse tras asignar materiales y completar arnés/bomba.
- Referencias: Notion 03.8 https://app.notion.com/p/3f1f5e4bdb9081949942c96998f88385 y 03.5 https://app.notion.com/p/951bc2fbad5048a690a15a153a2fab77.

