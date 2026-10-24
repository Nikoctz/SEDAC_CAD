# SEDAC — maqueta de P2.04 para impresión PLA

Entrega: 23/10/2026. Una pieza integrada; dimensiones de impresión: **32 × 18 × 48 mm**.

## Qué archivo enviar al centro

**SEDAC_P204_MAQUETA_SIN_ARNES.3mf** conserva explícitamente la unidad milímetro. Contiene un único modelo, sin configuración de impresora ni G-code.

Alternativa: **SEDAC_P204_MAQUETA_SIN_ARNES.stl**. Importar en **milímetros**, al **100 %**, sin volver a reducir. Debe medir **32 mm en X, 18 mm en Y y 48 mm de alto en Z**. Si aparece otro tamaño, corregir la unidad de importación antes de laminar.

La geometría y la malla están comprobadas; **pendiente de comprobación en laminador**. El centro debe confirmar el perfil de máquina, boquilla, capas, puentes, soportes y adhesión antes de aceptar la impresión. No se entrega G-code.

## Qué representa

Conserva la distribución del P2.04: dos refuerzos dorsales, panel perforado, interfaz lumbar, yugos superiores y apoyo inferior abierto en el centro para representar el paso de la manguera. Separación entre refuerzos: 19 mm; altura: 48 mm.

Se omitieron correas, arnés, acolchados y hebillas. Los tornillos/pasadores pequeños se representan con relieves integrados, sin roscas ni montaje. Todo está unido en un solo sólido.

**La cuna del producto P2.04 es textil. Aquí se representa mediante dos apoyos rígidos, labios y laterales inclinados únicamente para construir una maqueta manejable. Esto no cambia el diseño de ingeniería del producto.** La maqueta no reproduce la flexibilidad del sistema, no es una pieza funcional para sostener la bomba y no valida cargas ni comodidad.

## Escala y adaptaciones

Distribución nominal **1:10**, con detalles aumentados para esta maqueta. No es una reducción uniforme ni sirve para obtener cotas del producto. Un canal real 32 × 24 × 3 mm mediría 3,2 × 2,4 × 0,3 mm a escala; aquí su envolvente es 4 × 3 mm, con paredes de 1,2 mm. Panel de 1,2 mm, suelo de 2 mm y laterales de 1,2 mm. Los marcadores de fijación tienen Ø1,6 mm y sobresalen 0,6 mm; son detalles visuales.

Las dimensiones mínimas se propusieron pensando en una boquilla de 0,4 mm, **supuesto sin confirmar**. El número de perímetros y la conservación de los relieves requieren el perfil real del centro. Se fusionaron pequeñas holguras y se simplificaron las ranuras de los anclajes; las aberturas grandes se conservaron. El panel se extiende hasta los 48 mm para integrar los extremos de los refuerzos.

## Orientación y espacio

El STL y el 3MF ya están orientados con **Z hacia arriba**, ambos pies y el travesaño inferior en **Z=0**. La abertura frontal en U para manguera tiene 10,4 mm de ancho. Mantener esa orientación como propuesta inicial; ver ORIENTACION_IMPRESION.svg.

La pieza cabe en 40 × 40 × 70 mm. Un brim de **3 mm** daría aproximadamente **38 × 24 × 48 mm** de envolvente, sin contar soportes. Es una propuesta, no una configuración de máquina comprobada. Si se añaden soportes u otra adhesión, comprobar la envolvente completa de nuevo. El suelo ofrece apoyo continuo bajo ambas patas y la parte posterior.

Revisar especialmente el puente de aproximadamente 9 mm sobre la ventana central, las ventanas laterales, los pequeños voladizos de los yugos y los relieves. Los laterales inclinados de la cuna se apoyan sobre el suelo; no hay correas suspendidas. La necesidad y el acceso para retirar soportes quedan pendientes de laminado. No se ha estimado tiempo ni consumo con un perfil real.

## Comprobaciones realizadas

- Inventor 2027.1: lectura real del modelo de DeepSeek y creación nativa de esta maqueta; actualización correcta y un cuerpo sólido.
- STL final reabierto: 2064 triángulos, un componente conectado; sin bordes abiertos, aristas o vértices no manifold, caras duplicadas o triángulos degenerados; orientación de caras coherente y volumen positivo.
- Medidas del STL contrastadas con el IPT, incluyendo la conversión de la exportación original en centímetros a la entrega final en milímetros. El volumen difiere aproximadamente 0,0031 % del sólido por facetado y redondeo numérico.
- 3MF construido con la misma malla, unidad millimeter, un objeto; contenedor y XML reabiertos y comprobados. No es una exportación nativa de 3MF de Inventor ni un proyecto de laminador.
- No se ejecutó una detección independiente de autointersecciones de la malla ni una simulación física de impresión.

## Editables y trazabilidad

SEDAC_P204_MAQUETA_SIN_ARNES.ipt: pieza con bocetos y extrusiones editables. STEP: intercambio de geometría sólida. En estos editables se conserva la convención del proyecto de altura en **Y**: caja **32 × 48 × 18 mm**; el STL/3MF se rotó para que la altura sea Z. El volumen y la forma son los mismos.

Los parámetros de operaciones, generador y exportación inicial quedan en Soporte. El STL inicial de Soporte está en centímetros y en orientación de Inventor: **no enviarlo al centro**. Los archivos para impresión son únicamente los de Entrega indicados arriba.

Se usaron las habilidades locales inventor-modeling, dfm-review y la ficha previa de especificación CAD. Las herramientas MCP de Inventor no están expuestas en esta sesión; se utilizó la API COM nativa, comprobada mediante lectura de versión y del IPT existente. No se cambió la configuración de servidores. Se tomó P2.04 como referencia; no se incorporó ni se ejecutó el generador P2.05 pendiente de cierre.

P2.04, P2.05 y la maqueta de DeepSeek quedan conservados. Esta entrega se guarda en una iteración nueva y no cierra el diseño de ingeniería. No se ha enviado ningún correo.
