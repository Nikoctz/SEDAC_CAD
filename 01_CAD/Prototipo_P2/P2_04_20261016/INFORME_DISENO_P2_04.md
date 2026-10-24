# SEDAC P2.04 — diseño y alcance de la entrega

Revisión iniciada el 16/10/2026 y entrega cerrada el 17/10/2026. Inventor 2027.1, escala maestra 1:1. Prediseño con dimensiones propuestas, todavía sin medir la bomba real. Reemplaza a P2.03 como propuesta local actual; no es liberación para fabricar o usar con personas.

## 1. Arquitectura adoptada

Dos canales independientes de aluminio 6061-T6, 32 × 24 × 3 mm y 480 mm de largo, separados 190 mm. La cara abierta mira hacia la bolsa; se cubre mediante funda textil. Desaparecen la bandeja rígida, las cartelas grandes y la X metálica. La cuna textil sostiene la bolsa por debajo, con dos superficies de 100 mm y una abertura central nominal de 104 mm para la manguera.

El recorrido de carga propuesto queda representado en el CAD: bolsa → cuna y cintas longitudinales → ranuras dedicadas en interfaz lumbar/yugos → canales y anclajes del arnés → cinturón/hombros → usuario. Las correas transversales limitan el desplazamiento lateral; su ajuste, protección de costuras y eficacia con agua en movimiento siguen pendientes. La bomba no se sostiene de la tapa, la salida de manguera ni su asa original.

La interfaz lumbar tiene cuerpo de 3 mm, mejillas de 3 mm y refuerzos locales hasta 6 mm en las ranuras de carga. Los yugos superiores tienen placa de 6 mm con ventanas y mejillas de 3 mm. Los refuerzos locales permiten conservar espesor donde entran las fuerzas sin engrosar toda la placa. El panel HDPE perforado de 1 mm distribuye contacto y permite flexión; no se le asigna resistencia estructural.

Se conservaron las almas completas de los canales: una ventana pequeña ahorraba pocos gramos y dependía demasiado de dónde entrara el momento de la carga. Se retiró material principalmente en la interfaz lumbar, los yugos y el panel de contacto, dejando continuidad hacia los anclajes.

La movilidad se busca mediante alas textiles del cinturón, hombreras independientes y ausencia de un travesaño metálico superior. No se ha demostrado comodidad, ventilación ni movilidad de un usuario real. Los canales siguen siendo elementos resistentes, no resortes deliberadamente blandos. La cuna, cintas, acolchados y hebillas son envolventes CAD de referencia: todavía no son patrones de confección ni mecanismos certificados. Los extremos de las cintas indican interfaces; las costuras y retornos completos se definirán con el arnés elegido.

## 2. Uniones desmontables

Ocho uniones con tornillo M5×55 ISO 4762 A2-80, dos arandelas gruesas 5,3 × 16 × 3 mm y tuerca metálica autofrenante por unión. Envolvente de arandela basada en GN 6341-ST-5-16-A-ZB; confirmar suministro y sus propiedades. La tuerca es una envolvente compatible con DIN 980 M5: selección de clase, carga de prueba, par prevalente y reutilización pendientes.

Cada unión añade un pasador hueco extraíble 6061-T6 de Ø10/Ø5,5 y 37,6 mm de largo. Dentro del canal hay un separador independiente Ø12,5/Ø10,2, largo nominal 26 mm. Se coloca el separador por la boca del canal; después se presenta la interfaz, se introduce el pasador por los taladros Ø10,2 y se instala el M5 con sus arandelas y tuerca. Las dos piezas separadas hacen posible el montaje sin abrir las alas del canal.

El pasador recibe el cortante y el M5 mantiene el apriete y la retención. Los extremos del pasador quedan nominalmente retraídos 0,2 mm respecto de las mejillas. El separador evita cerrar las alas durante el apriete. Dos fijaciones separadas 60 mm en cada interfaz limitan el giro relativo. La tuerca autofrenante aporta retención frente al aflojamiento; su eficacia bajo vibración aún debe comprobarse.

Roscas nativas M5×0,8, 6g/6H, de representación cosmética. No se ha modelado la hélice ni la deformación del autofreno. Longitud roscada nominal del tornillo: 22 mm; salida nominal tras la tuerca: 6 mm. Proteger extremos y herrajes frente a roce/enganches mediante la funda.

**Corrección documental — 2026-10-22. Motivo: discrepancia entre el acabado descrito y el registro de la entrega.**

> Texto original del 17/10/2026, conservado como historial y sustituido por esta corrección:
> El CAD incluye radios de 0,35 mm en canales y 0,5 mm en interfaces; esos radios por sí solos no validan desgaste de cintas: hacen falta fundas/protecciones de contacto y ensayos.

**hecho:** `REDONDEOS.json` de la entrega P2.04 registra los canales con radio de 0,35 mm y los yugos con radio de 0,5 mm como aplicados. El redondeo de 0,5 mm de `Interfaz_lumbar_aligerada` fue **solicitado y NO aplicado**: `aplicado: false`, error COM E_FAIL. Su masa registrada, 0,31108983098374 kg, coincide con la geometría sin esa operación adicional según la comparación documentada en `P2_05_20261019/LEEME_P2_05.md` §3. Se corrige el texto; no se ha hecho una nueva inspección ni se ha cambiado el CAD. Evidencia fuente: `P2_04_20261016/Entrega/Inventor/REDONDEOS.json` y `MASAS_CAD.json`.

**hecho de trazabilidad (2026-10-22):** esta fe de erratas cambia los bytes y la huella SHA-256 del informe. El manifiesto `HUELLAS_ENTREGA.json` y el ZIP históricos de P2.04 se conservan sin reemitir: describen el texto original. La excepción documental queda registrada; una nueva entrega necesitará su propio manifiesto. La geometría y los registros originales de entrega no se modificaron.

**supuesto:** el radio de 0,5 mm sigue siendo una **propuesta sin ensayo de desgaste**. El acabado de contacto lumbar sigue pendiente de clasificación funcional A/B/C (D-12), fabricación y ensayos. Ni el radio solicitado ni los radios registrados como aplicados acreditan desgaste o compatibilidad con las cintas.

La precarga de 2000 N es una hipótesis de cálculo, no un par de montaje publicado. No se entrega un par sin conocer lubricación, fricción, material real y par prevalente. Deben definirse ajustes, tolerancias apiladas, recubrimientos y aislamiento entre aluminio y acero. El montaje propuesto requiere confirmar el acceso a herramientas y el espacio real del textil.

## 3. Masa: comparación verificable

| Concepto | P2.03 | P2.04 |
|---|---:|---:|
| Piezas resistentes, herrajes y protectores CAD | 2.333 kg | 1.442 kg |
| Reserva completa de textiles, acolchados y hebillas | 0,500 kg | 0.650 kg |
| Reserva adicional de acabados/accesorios | 0,080 kg | 0.120 kg |
| Presupuesto total del sistema auxiliar | 2.913 kg | 2.212 kg |

Reducción de la parte CAD comparable: **38.2 %**. Reducción del presupuesto completo: **24.1 %**, a pesar de aumentar la reserva para mochila. Con la misma reserva anterior de 0,580 kg, P2.04 sumaría 2.022 kg; no se adopta ese valor como presupuesto de entrega.

Se incluye el protector HDPE en ambas revisiones para comparar lo mismo. En la BOM de P2.03 estaba marcado como referencia, aunque su subtotal publicado de 2,333 kg sí lo incluía.

El objetivo de 2 kg sigue pendiente: el presupuesto actual lo supera en 0.212 kg. El peso real exige pesar materiales, arnés y accesorios. Estas masas excluyen bomba y agua. La reserva de 0,650 kg sustituye los 0.481 kg ilustrativos de componentes REF; no se suman dos veces. Densidades asignadas en Inventor: aluminio 2700 kg/m³, HDPE 953 kg/m³ y herrajes 8000 kg/m³ (aproximación conservadora para la arandela de acero). Los textiles usan densidades visuales aproximadas y no determinan el presupuesto.

| Grupo CAD sin referencias textiles | Masa, kg |
|---|---:|
| estructura | 0.569 |
| uniones | 0.068 |
| anclajes | 0.560 |
| protecciones | 0.081 |
| fijaciones | 0.165 |

## 4. Comprobaciones analíticas de prediseño

Escenario heredado: masa total transportada 25 kg, aceleración vertical total 3g, horizontal 1g, g=9,81 m/s², reparto 70/30 y excentricidad 107,5 mm. La masa de 25 kg debe entenderse incluyendo el sistema auxiliar; la combinación real bomba llena + sistema debe medirse. No se ha reducido la carga por conveniencia.

Por lado más cargado: N=515.025 N y Q=171.675 N. Luz entre apoyos nominales del arnés/cinturón L=380 mm. Momento excéntrico M0=N·e=55.365 N·m. Se envuelven momentos aplicados en cualquiera de los extremos con M(x)=M0·max(1−x/L,x/L)+Q·x·(L−x)/L; el máximo es 55.739 N·m. Esa envolvente presupone apoyos efectivos de hombro y cinturón; no describe un canal en voladizo ni cubre todos los repartos posibles de presión sobre la bolsa.

Canal calculado con pared mínima 2,8 mm y esquina ideal sin acreditar material extra de los radios. Se combina N/A, flexión principal con K=1,25, flexión lateral y torsión de Saint-Venant mediante von Mises. También se examinan Euler, placa sobresaliente k=0,43 y pandeo lateral torsional ideal. La comprobación de taladro usa K=3 como aproximación, no como resultado de FEA.

E del aluminio=69 GPa; límite de fluencia adoptado=240 MPa, condicionado a material y tratamiento certificados. Para el M5 se adopta resistencia convencional de 600 MPa de A2-80. Se estudian dispersión de precarga ±25 %, rigidez relativa de junta 0,2 y factor de palanca 1,5. En el cortante de la unión se incluye la reacción debida al momento; el pasador se revisa conservadoramente tomando una sola interfaz efectiva. Las arandelas requieren espesor mínimo 2,9 mm y Sy mínimo de estudio 200 MPa, a confirmar con el proveedor.

| Comprobación | Margen calculado |
|---|---:|
| Refuerzo combinado, pared minima | 2.25 |
| Pandeo Euler, eje debil | 108.58 |
| Pandeo local de alas | 2.25 |
| Pandeo lateral torsional ideal | 26.61 |
| Taladro en alas, tension local | 2.76 |
| M5 combinacion precarga y servicio | 2.55 |
| Aplastamiento ala por pasador | 6.35 |
| Aplastamiento mejilla por pasador | 6.35 |
| Arrancamiento ala | 5.11 |
| Casquillo compresion | 3.59 |
| Pasador hueco flexion y cortante | 2.97 |
| Arandela gruesa flexion local | 2.28 |
| Arandela presion bajo tuerca | 2.26 |
| Puente anclaje arnes/cinturon biaxial | 2.36 |
| Puente inferior de cuna | 3.70 |

Umbral elegido para este cribado: 2,20. Mínimo obtenido: **2.247**. No es un factor de seguridad validado del producto completo. Flecha envolvente ideal: 0.867 mm; giro torsional ideal: 3.18°. No son mediciones de comodidad. Compresión residual de junta en el modelo: 282.2 N, sensible al asiento y a la dispersión real de apriete.

Carga de rama de cuna: 314.4 N. Carga envolvente de anclaje de arnés/cinturón: 628.7 N. Como requisito inicial, factor 5 sobre estas cargas para el conjunto cinta-costura-hebilla da 1572 N en cuna y 3144 N en arnés/cinturón. Es un objetivo de selección/ensayo, no una resistencia atribuida a la geometría textil representada ni un requisito normativo identificado.

No se ha calculado vida de fatiga, contacto local completo, pandeo distorsional, desgaste, caída, comportamiento térmico ni liberación de emergencia. Tampoco se ha validado el reparto de fuerzas con el usuario corriendo o la deformación de la bolsa. Cambiar la arquitectura obliga a estas comprobaciones nuevas: no se heredan automáticamente las conclusiones de P2.03.

## 5. Comprobación del archivo nativo

54 diseños de piezas sólidas y 83 ocurrencias. Referencias locales resueltas. Una interfaz lumbar fijada y 246 restricciones de posición; el conjunto conserva su colocación al actualizar. Esas restricciones se basan en planos de origen: no simulan contacto, fricción ni articulación del tejido.

Se revisaron actualización, cuerpos sólidos, salud de operaciones y propiedades mecánicas de los metales. Las unidades reales expuestas por la API para E y resistencias son kilopascales; se verificó la conversión desde MPa. Hay parámetros nativos vinculados a posiciones de planos y profundidades de extrusión; el largo del canal usa Altura_refuerzo. El modelo conserva bocetos editables. No todo el ensamblaje está gobernado por una única tabla de parámetros de Inventor: para cambios coherentes entre piezas se modifica el JSON y se regenera.

Cero interferencias volumétricas nominales entre los componentes rígidos seleccionados. Se excluyeron las referencias textiles/espuma/hebillas: tienen contacto y solapes esquemáticos y todavía requieren confección. Este resultado no demuestra tolerancias, montaje físico, acceso de herramientas ni ausencia de roce con la bolsa.

## 6. Siguiente decisión

Medir bolsa llena/vacía, masa y centro de gravedad, costuras, manguera/tapa y arnés. Ajustar las cotas y comprobar el recorrido de las cintas antes de mecanizar. Seleccionar y pesar textiles, acolchados y cierres; confirmar temperatura de servicio. Después completar FEA local, fatiga, prototipo de montaje y ensayos de carga/movimiento. La memoria completa Mathcad y PDF se hará sobre la geometría acordada, según la preferencia de no rehacerla en cada concepto.

## Fuentes y evidencia

- [Hydro, ficha 6061](https://www.hydro.com/Document/Index?id=560718&name=Alloy+6061.pdf): referencia de material extruido y tratamiento; no garantiza el lote que se compre.
- [NASA, Fastener Design Manual](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf): criterios de precarga, uniones y retención; los factores numéricos de este estudio siguen siendo hipótesis.
- [MIT, Structural Mechanics](https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/): modelos de viga y estabilidad empleados como aproximaciones analíticas.
- [Ganter, GN 6341](https://www.ganternorm.com/en/products/3.2-Mounting-Positioning-Leveling-with-Retaining-Cables-Screws-Clamping-and-Supporting-Elements/Washers/GN-6341-Washers-Steel): familia y dimensiones de arandelas de mayor espesor; no se ha confirmado stock local.
- Archivos de evidencia: PARAMETROS_P2_04.json, Calculos/RESULTADOS_PREDISENO.json, BOM_Y_MASAS.csv y registros nativos de Entrega/Inventor.
