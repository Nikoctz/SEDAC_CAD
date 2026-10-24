# SEDAC — maqueta aligerada R4

**Revisión propuesta para enviar: R4_Aligerada_09mm.** Fecha: 23/10/2026.
El usuario confirmó que el alcance es corregir la maqueta pequeña para el envío al centro. El producto original P2.04 permanece intacto.

## Qué cambió respecto de R3

| Elemento de la maqueta | R3 | R4 |
|---|---:|---:|
| Panel dorsal, espesor | 1,2 mm | 0,9 mm |
| Envolvente de canal | 4 x 3 mm | 3,2 x 2,4 mm |
| Pared nominal de canal | 1,2 mm | 0,9 mm |
| Ventana central, ancho | 9 mm | 13 mm |
| Espesor nominal de cunas | 1,6 mm | 1,6 mm |
| Superficie de las cunas | Continua | Ventanas centrales, bordes y uniones conservados |

Se entalló el contorno lateral del panel, se añadieron dos ranuras centrales superiores y se conservaron los recorridos curvos, posición y anchura exterior de las cunas. Las ventanas de las cunas dejan dos tiras laterales de 2,8 mm y mantienen la zona posterior de unión. Algunas ranuras laterales del panel quedan respaldadas por los canales/yugos integrados; no se presentan como pasos funcionales para cintas.

## Cantidad de material

- Volumen de sólido nativo R3: **2962.56 mm³**.
- Volumen de sólido nativo R4: **1918.45 mm³**.
- Volumen retirado: **1044.11 mm³**; reducción geométrica **35.24 %**.

Estos valores comparan dos maquetas integradas. No son una reducción de masa del sistema real ni un resultado de consumo de filamento: faltan laminado, relleno, adhesión y soportes. El cálculo reproducible está en COMPARACION_R3_R4.json y en Soporte/FINALIZAR_MALLAS.py.

## Archivos y apertura

- **SEDAC_P204_MAQUETA_ALIGERADA_09mm.ipt**: pieza nativa de Inventor, con bocetos y extrusiones editables. Posiciones/espesores de extrusiones con parámetros; los contornos pueden editarse en los bocetos o regenerarse desde el JSON. No se declara restricción completa de todos los bocetos.
- **SEDAC_P204_MAQUETA_ALIGERADA_09mm.step**: intercambio de geometría sólida.
- **SEDAC_P204_MAQUETA_ALIGERADA_09mm.stl** y **SEDAC_P204_MAQUETA_ALIGERADA_09mm.3mf**: la misma pieza preparada en mm y con altura Z de aproximadamente 48 mm. Elegir uno para el laminador, al 100 %.
- VISTA_MAQUETA.png y VISTA_POSTERIOR.png: imágenes obtenidas de Inventor. ORIENTACION_IMPRESION.png: diagrama desde la malla exportada.
- En IPT/STEP se conserva altura Y; en STL/3MF la altura es Z. Dimensiones de impresión: **32.0 x 18.2 x 48.0 mm**.

## Impresión pendiente

**Pendiente de comprobación en laminador con la máquina del centro.** Revisar paredes de 0,9 mm, relieves pequeños, soportes debajo de las cunas, puentes del panel y retirada de soportes. Confirmar que adhesión y soportes caben en **40 x 40 x 70 mm**. Un brim hipotético de 3 mm da unos 38 x 24,2 mm en planta, sin incluir soportes adicionales.

Se adoptó un mínimo nominal de 0,9 mm como referencia aproximada de dos cordones de 0,45 mm; la guía de [Prusa](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135), consultada el 23/10/2026, aclara que depende de los ajustes. No es un perfil confirmado para el centro ni una garantía de impresión. No se incluye G-code.

## Qué se comprobó

- Actualización nativa en Inventor 2027.1 y un cuerpo sólido. Todos los vaciados redujeron volumen; registro en VOLUMEN_POR_OPERACION.json.
- STL final reabierto en mm: un componente cerrado, aristas y vértices manifold, sin caras duplicadas o degeneradas, volumen positivo y dimensiones contrastadas con el sólido nativo.
- Conversión de unidades del STL bruto en cm a mm, rotación con altura Z y traslado al origen positivo. No enviar NATIVO_ORIENTACION_INVENTOR.stl de Soporte.
- 3MF de modelo, unidad millimeter, un objeto, ZIP y XML reabiertos con la misma malla.
- Fuentes P2.04: IAM y manifiesto con SHA-256 conservados. R3 preservada.
- No se realizó detección independiente de autointersecciones ni ensayo físico de impresión/flexión. La comprobación geométrica no acredita resistencia física.

## Materiales y alcance

Toda esta maqueta integrada se propone en PLA. La espaldera del producto P2.04 está descrita como HDPE de 1 mm y sus cunas son textiles; esta representación no reproduce su flexibilidad. Retirar material de la maqueta no cambia los márgenes analíticos del producto ni autoriza usarla para soportar una bomba o sobre personas.

La generación se realizó mediante API COM nativa de Inventor. Habilidades aplicadas: especificación CAD, inventor-modeling y dfm-review. No se ejecutó el generador P2.05, ni se modificaron Mathcad, PDF o Notion.
