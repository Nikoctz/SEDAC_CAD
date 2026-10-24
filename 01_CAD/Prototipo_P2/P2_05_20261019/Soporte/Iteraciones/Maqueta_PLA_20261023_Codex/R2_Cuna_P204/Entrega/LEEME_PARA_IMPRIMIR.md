# SEDAC — maqueta P2.04 sin arnés, con cuna original

Entrega: 23/10/2026. **Una pieza, aproximadamente 32 × 18 × 48 mm** en orientación de impresión (X × Y × altura Z). Usar esta revisión **R2_Cuna_P204**; el primer borrador de bandeja plana queda como antecedente y no es el archivo propuesto para enviar.

## Para el centro de impresión

Enviar **SEDAC_P204_MAQUETA_CUNA_CURVA.3mf** (unidad milímetro incluida) o **SEDAC_P204_MAQUETA_CUNA_CURVA.stl** (importar en milímetros, al 100 %). No volver a reducir. Confirmar en el laminador unos **48 mm de alto**.

Es una maqueta visual para PLA. **Pendiente de comprobación en laminador**: se necesita el perfil real de la máquina y revisar **soportes bajo las dos cunas curvas elevadas**. No se entrega G-code ni se garantiza impresión sin soportes. No es una pieza funcional para cargar una bomba.

El volumen máximo comunicado es 40 × 40 × 70 mm. La pieza cabe; un brim hipotético de 3 mm daría aproximadamente 38 × 24 mm de envolvente en planta. Los soportes y cualquier otra adhesión también deben quedar dentro de 40 × 40 mm: comprobarlo con el laminado real. Boquilla 0,4 mm es únicamente el supuesto utilizado al proponer los espesores.

## Relación con el modelo que eligió el usuario

Referencia: **SEDAC_P2_04.iam** de P2_04_20261016/Entrega/Inventor. Se preservan el panel dorsal perforado, los dos canales, el lumbar y los yugos. Se omiten el arnés, las correas largas, acolchados, hebillas y fundas. Las fijaciones pequeñas quedan como relieves, sin roscas reales.

Las dos cunas toman **su posición, ancho y recorrido del contorno REF_Cuna_textil_I/D del manifiesto de ese P2.04**, a 1:10. No se desplazan hacia abajo ni se sustituyen por una bandeja plana. Se aumentó su espesor a 1,2 mm y se unieron a los canales engrosados de la maqueta. Se retiraron la bandeja y los laterales triangulares del primer borrador. El registro REFERENCIA_GEOMETRICA_P204.json contiene los recorridos y huellas de las fuentes.

**La cuna del producto original sigue siendo textil. Su representación rígida aquí es exclusivamente una adaptación de maqueta.** La geometría de fabricación y los cálculos del producto no se modifican.

## Escala y edición

Distribución nominal 1:10 con espesores magnificados. No es una reducción uniforme ni permite obtener dimensiones reales del producto. Canales: envolvente 4 × 3 mm y pared 1,2 mm, frente a 3,2 × 2,4 × 0,3 mm que resultarían al reducir uniformemente la sección del producto. Panel nominal 1,2 mm y cuna 1,2 mm. Se integran holguras para formar un único sólido. Algunos pequeños relieves sobresalen 0,6 mm y requieren comprobar que el laminador los conserve.

El IPT contiene bocetos y extrusiones editables; STEP es la alternativa de intercambio. En IPT/STEP se conserva altura Y, con caja aproximada 32 × 48 × 18 mm. En STL/3MF la altura es Z: aproximadamente 32 × 18 × 48 mm. El paquete para el centro contiene los archivos de malla y las instrucciones; los editables quedan en la carpeta Entrega.

## Qué se comprobó

- Creación nativa en Inventor 2027.1; actualización, un sólido y geometría editable.
- STL reabierto: un componente cerrado, aristas y vértices manifold, sin caras duplicadas o degeneradas, orientación de caras coherente y volumen positivo. Dimensiones contrastadas con el IPT.
- La exportación inicial de Inventor estaba en centímetros; el STL final está convertido a milímetros y girado aZ vertical. El archivo inicial de Soporte no debe enviarse.
- 3MF de modelo creado con la misma malla; ZIP/XML reabiertos, unidad millimeter y un objeto. No es un proyecto laminado ni una exportación3MF del traductor de Inventor.
- Detalles numéricos en VERIFICACION_MALLAS.json. No se realizó una detección independiente de autointersecciones ni un ensayo de impresión.

## Cómo se preparó

Habilidades de especificaciónCAD, inventor-modeling y dfm-review. La creación y exportación utilizaron la API COM nativa; no había herramientas MCP de Inventor expuestas en esta sesión. El manifiesto fuente es P2.04; no se ejecutó ni incorporó el generador P2.05 pendiente de cierre.

Las fuentes y la maqueta de DeepSeek se conservan. Esta maqueta no cierraP2.05 ni valida resistencia, flexibilidad o comodidad del sistema auxiliar.
