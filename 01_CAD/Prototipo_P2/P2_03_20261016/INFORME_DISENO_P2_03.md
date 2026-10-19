# Informe de diseño y comprobación P2.03

Fecha: 16/10/2026. Revisión de P2.02 conservada por separado.

## 1. Resultado y criterio de comparación

La masa rígida estimada baja de **3,153 a 2,333 kg**, una reducción de **26,0 %**. Se descuenta del modelo anterior su espuma de referencia (0,053201 kg) para comparar con el mismo alcance.

La nueva masa representada en Inventor es **2,362658 kg**: incluye **0,029530 kg** de espuma de referencia. Para el sistema completo se suma a la masa rígida una reserva de 0,50 kg que ya incluye todo el acolchado, más 0,08 kg de accesorios. Resultado: **2,913 kg**, sin bomba ni líquido. Con las mismas reservas, el equivalente anterior sería 3,733 kg.

El objetivo de 2 kg no se alcanzó. Este trabajo no acredita un mínimo global de masa. Reducir más requiere datos reales que permitan revisar dimensiones, brazos, cargas e interfaces.

## 2. Desglose de masa

| Grupo | Masa estimada (kg) |
|---|---:|
| Dos rieles | 0,683 |
| Casquillos, pasadores, apoyos y calces | 0,092 |
| Dos cartelas | 0,216 |
| Piso y tres refuerzos de cuna | 0,470 |
| Travesaños y diagonales | 0,152 |
| Anclajes de hombro y cinturón | 0,219 |
| Acolchado de referencia (dentro de reserva textil) | 0,030 |
| Protector HDPE | 0,096 |
| Tornillos, tuercas y arandelas | 0,405 |

Densidades usadas: 6061 y anclajes 2700 kg/m³; 5052 2680; inoxidable 8000; HDPE 953; espuma 60. Las masas nativas se contrastaron contra volumen por densidad. No sustituyen pesaje ni certificado. La rosca cosmética no resta el volumen de una hélice y la tuerca no reproduce su deformación de bloqueo.

## 3. Decisiones de aligeramiento

- **Riel:** pared de 2,5 a 1,5 mm; profundidad de 25 a 40 mm. Se aumenta e a 107,5 y L a 423 para incorporar el desplazamiento de la carga. La masa de los dos rieles taladrados es 0,683 kg.
- **Anclajes:** alma de 2 mm con retornos hasta 18. Se calcula flexión asimétrica de los puentes L, raíz C y pandeo local, con pared mínima 1,8. No se sustituyen por placas planas de 2 mm.
- **Interfaz posterior:** se retiran paneles rígidos y fijaciones secundarias; el arnés y su soporte textil quedan por definir. La espuma es una referencia, no una interfaz validada por sí sola.
- **Protector:** HDPE hueco, cara superior de 2 mm y espacio inferior de 12 mm. El paquete de apriete primario es metálico.
- **Cuna:** se conserva el piso de 2,5 mm y se añade un tercer apoyo. Así se reduce la luz a 45 mm y el voladizo delantero a 20 mm. El apoyo cambia la escotadura de manguera: se debe medir.
- **Material que se conserva:** diagonales en X, altura de refuerzos, ala de cartela de 5 mm y apoyos contra aplastamiento. Adelgazarlos uniformemente no conserva los márgenes.

## 4. Escenario y resultados

Se mantienen **25 kg de masa total transportada**, 3 g verticales totales y 1 g horizontal, con 70 % en el lado más cargado. Incluye estructura, mochila, bomba y líquido. Quedan aproximadamente 22,09 kg del presupuesto para bomba/líquido y elementos no incluidos. Esto no es una carga de uso autorizada.

| Comprobación | Resultado |
|---|---:|
| Riel nominal, fluencia | 2,447 |
| Riel, pared de 1,4 mm | 2,305 |
| Flecha equivalente del riel | 2,038 mm |
| Piso con presión y parche local | 2,830 |
| Refuerzo de cuna | 2,427 |
| Puente de hombro / cinturón | 2,889 / 2,941 |
| Tornillo M6 de marco/X | 2,254 |
| Apoyo interior M5 a compresión | 2,586 |

Las 33 comprobaciones seleccionadas alcanzan n>=2,2 bajo sus hipótesis; la flecha es menor que 5 mm y los cierres residuales son positivos. **El mínimo de esos modelos no certifica el conjunto.** Las hipótesis de contacto, concentraciones, carga y montaje no provienen de ensayos ni FEA. La comparación antigua que citaba n≈2,25 se refería al riel; ahora el valor cercano corresponde al perno del marco.

La memoria MC01 anterior ya había detectado un problema de piso con carga localizada. P2.03 aborda esa observación con apoyo adicional, sin aumentar el espesor del piso. No se usa el margen de piso original de P2.02 como evidencia de aceptación.

## 5. Tornillería y retención

| Unión | Cantidad | Tornillo A2-80 | Paquete sin arandelas/tuerca | Saliente |
|---|---:|---|---:|---:|
| Cartela | 4 | M6x65 | 53 mm | 2,8 mm |
| Marco y X | 4 | M6x60 | 44 / 46 mm | 6,8 / 4,8 mm |
| Hombro y cintura | 8 | M6x55 | 42 mm | 3,8 mm |
| Cuna | 6 | M5x40 | 27,5 mm | 5,5 mm |

Total: 22 tornillos, 44 arandelas y 22 tuercas; todos se representan como piezas separadas. M6: arandelas 6,4/12/1,6, tuerca AF10 y altura 6. M5: 5,3/10/1, tuerca AF8 y altura 5. Rosca parcial nominal b=2d+12; verificar la longitud efectiva del producto comprado. La clase geométrica 6g/6H no es la clase resistente A2-80.

Se orientan las cabezas de hombro y cartela derecha para cubrir el plano crítico con vástago liso. Los pasadores de cartela tienen exterior 10/interior 6,6 y longitud 53; se insertan en taladros 10,2. Los M6 restantes tienen casquillos interiores; los M5 llevan apoyos con contorno igual al interior redondeado de sus refuerzos.

Las tuercas son autofrenantes metálicas derivadas DIN 980; se requiere confirmar un producto de clase 80 y carga de prueba compatible. No se ha modelado la deformación del autofreno ni demostrado que nunca se afloje. Las arandelas distribuyen presión; no son el mecanismo de bloqueo.

Se incluyen tracción por precarga y palanca, cortante y flexión local de perno, compresión de apoyos, presión de asiento, punzonamiento nominal y reserva contra apertura. Precargas de estudio: 1500/1400/1800/1000 N, dispersión 25 %. El ejemplo T=K F0 d con K=0,20 **no es una instrucción de apriete**: falta par prevalente, fricción y calibración.

## 6. Lo comprobado en los archivos

- Inventor: 51 documentos IPT, todos de un sólido; 131 ocurrencias en el IAM.
- Un riel fijado; otras 130 ocurrencias con 3 restricciones a planos de referencia. 390 restricciones de posición, 0 grados de libertad residuales en esas ocurrencias y transformaciones conservadas.
- 0 interferencias volumétricas nominales detectadas en Inventor. No es una comprobación de tolerancias, herramientas ni montaje físico.
- 6 definiciones distintas con rosca nativa, utilizadas en 44 ocurrencias de tornillo/tuerca. Rosca cosmética, sin hélice sólida.
- 4 anclajes con operación nativa de redondeo de 0,4 mm. Acabado y radio de contacto de cintas deben confirmarse en fabricación.
- Mathcad: 247 variables recalculadas, error relativo máximo frente al cálculo independiente menor que 6e-15; 0 errores en XML y 0 solapamientos de regiones tras revisión.
- PDF Beamer: 55 diapositivas compiladas, sin desbordamientos; revisión visual de todas las páginas. La hoja Mathcad tiene 45 páginas lógicas.

Los registros de geometría están en Entrega/Inventor_Optimizado; los de cálculo y presentación en la carpeta Soporte de la memoria. No se ha realizado FEA ni ensayo físico.

## 7. Condiciones para la siguiente versión

Medir bomba llena/vacía, contacto inferior, manguera, tapa, costuras, centro de masa y arnés. Confirmar disponibilidad de perfil 50x40x1,5 con radios y pared mínima compatibles. Cerrar longitudes de pasadores y apoyos: un exceso impide apretar el paquete y una falta permite deformarlo.

Definir planos con tolerancias, proceso y radios de cuna, acceso de llaves, orden para insertar apoyos, protección de cantos, prevención de corrosión y acabado. No sustituir anclajes mecanizados 6061 por chapa doblada 5052 sin recalcular.

Después: FEA de detalles, ensayos de banco, fatiga con espectro real, impacto, vibración, temperatura, textiles y evaluación del contacto con el usuario. La hoja no asigna vida a fatiga ni carga certificada.

## 8. Fuentes

- [Hydro, Alloy 6061](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf).
- [Atlas Steels, 5052](https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf).
- [Bossard, inoxidable ISO 3506](https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf).
- [NASA RP-1228, Fastener Design Manual](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf).
- [MIT OCW, Structural Mechanics](https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/).
- [Autodesk, ThreadFeatures](https://help.autodesk.com/cloudhelp/2024/ENU/Inventor-API/files/ThreadFeatures.htm).

El PDF amplía las referencias de tornillería, arandelas, fractura y representación. Las fuentes respaldan conceptos y propiedades; no aprueban este diseño particular.
