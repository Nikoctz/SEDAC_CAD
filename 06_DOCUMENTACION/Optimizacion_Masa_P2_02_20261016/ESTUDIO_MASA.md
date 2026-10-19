# SEDAC: estudio preliminar de reducción de masa

Fecha: 16/10/2026. Referencia: P2.02, Inventor_20261015_152625.
Alcance: balance, sensibilidad y propuesta de trabajo. No se ha generado ni validado un CAD aligerado.
Los resultados de masa son estimaciones del modelo nominal, no pesajes.

## 1. Definición del objetivo completo

Se propone como objetivo de estudio **2,0 kg para todo el sistema añadido**.
Se trata de una meta propuesta; todavía no es un resultado de diseño.

Debe incluir estructura, fijaciones, protecciones, correas, cinturón, hebillas,
acolchados y ajustes que se agreguen. Si se reutiliza el arnés original sin añadirlo
al sistema, su masa se cuenta una sola vez en la masa completa de la bomba.
Las piezas originales retiradas y reemplazadas se deben identificar para calcular
también el incremento neto real de masa.

Como primer presupuesto se reserva **0,5 kg para el conjunto textil y de ajuste**,
incluido su acolchado, dejando **1,5 kg para piezas rígidas, protecciones y fijaciones**.
La reserva es una decisión de presupuesto, no la masa de un arnés seleccionado o pesado.
Si el arnés nuevo necesita más, la estructura deberá bajar más o se revisará el objetivo.

## 2. Balance actual, con cantidades de cada ocurrencia

| Grupo | Masa estimada (g) | Porcentaje |
|---|---:|---:|
| Rieles | 890 | 27.8 % |
| Cuna, cartelas y refuerzos | 706 | 22.0 % |
| Yugo y anclajes de hombro | 608 | 19.0 % |
| Protecciones HDPE | 343 | 10.7 % |
| Tornilleria de referencia | 316 | 9.9 % |
| Travesanos y diagonales | 214 | 6.7 % |
| Casquillos y separadores | 76 | 2.4 % |
| Acolchados de referencia | 53 | 1.7 % |
| **Total representado** | **3206** | **100 %** |

Las piezas metálicas estructurales suman 2,494 kg **sin los herrajes**.
La tornillería de referencia suma otros 0,316 kg.
El total 3,206 kg incluye geometrías de referencia de contacto y fijaciones,
pero carece del arnés completo.

El presupuesto rígido de 1,5 kg implica reducir aproximadamente un 52 %
respecto de los 3,153 kg de elementos actuales excluyendo el acolchado representado.
Es una reducción exigente: requiere revisar la arquitectura y la fabricación,
además de espesores. La masa del equipo completo debe contrastarse con componentes reales.

## 3. Prioridades del rediseño

### A. Yugo de cintura y anclajes de hombro

Masa conjunta actual: 608 g. Las placas planas de 5 mm son candidatas a una
geometría con mayor rigidez por unidad de masa: sección conformada, nervaduras
o perfil, conservando el material y el área necesarios alrededor de las ranuras.

No se prescribe aún un espesor final. En el modelo actual, al pasar uniformemente
de 5 a 3 mm, la tensión de flexión escala aproximadamente con 1/t²:
el margen del puente de hombro bajaría de 2,39 a 0,86 y el de la raíz del yugo
de 2,43 a 0,87. Debe cambiar la geometría resistente.

Mantener compatibilidad con las cintas, radios de contacto, liberación y cuerpo del usuario.

### B. Cuna, cartelas y refuerzos

Masa actual: 706 g. Estudiar una bandeja conformada que asuma funciones de
rigidez y retención, para reducir piezas independientes, juntas y material duplicado.
El espesor y el proceso de fabricación se definirán después de calcular el detalle.

La memoria MC01 tiene prioridad sobre el cálculo inicial del generador:
el piso de 2,5 mm da margen 1,22 en el caso de borde, frente al objetivo 2,2.

Mover únicamente el refuerzo delantero para reducir el voladizo de 40 a 25 mm,
con el trasero fijo, aumenta la luz entre apoyos de 65 a 80 mm.
El margen pasa a aproximadamente 1,90 en el mismo modelo: aún queda por debajo de 2,2.
Debe revisarse toda la distribución de apoyos, la placa y el contacto.

### C. Rieles

Masa CAD actual del par perforado: 890 g.
La selección anterior tenía una preferencia de profundidad máxima de 25 mm.
Es una restricción de diseño que merece revisarse con la bolsa y la espalda reales.

Cambiar el tamaño o la proporción del perfil puede mejorar I/A.
Acercar la línea de carga y reducir el tramo sin apoyo disminuye la demanda,
si esas geometrías resultan compatibles con la bomba y el arnés reales.

Resultados parciales con las ecuaciones analíticas de MC01:
se mantienen 25 kg, 3 g verticales, 1 g horizontal, eta=0,7 y Kt=2.

| Perfil (mm) | e / L (mm) | Masa par sin agujeros (g) | Margen riel | Margen pared M8 |
|---|---:|---:|---:|---:|
| 50 x 25 x 2,5 | 100 / 400 | 902 | 2,25 | 2,68 |
| 50 x 25 x 2,0 | 100 / 400 | 739 | 1,92 | 2,15 |
| 35 x 35 x 2,5 | 100 / 400 | 834 | 2,33 | 2,68 |
| 40 x 40 x 1,5 | 100 / 400 | 608 | 2,09 | 1,61 |
| 40 x 40 x 2,0 | 100 / 400 | 793 | 2,65 | 2,15 |
| 50 x 30 x 2,0 | 100 / 400 | 793 | 2,38 | 2,15 |
| 40 x 30 x 2,0 | 100 / 400 | 685 | 1,89 | 2,15 |
| 40 x 30 x 2,0 | 80 / 350 | 685 | 2,20 | 2,53 |
| 40 x 30 x 2,0 | 75 / 300 | 685 | 2,47 | 2,64 |

La masa de los tubos sin agujeros no es idéntica a la masa CAD perforada.
No se han recalculado el resto de piezas, montaje, estabilidad local, fatiga ni contacto
para estos candidatos. Los radios se suponen ro=2t y ri=t como en MC01.
Los valores e y L son parámetros independientes de esta comparación.
Al cambiar la profundidad del tubo, hay que actualizar también e según el desplazamiento real
de la cuna y la línea de carga.

El perfil 50 x 25 x 2 mm ahorra aproximadamente 163 g en los tubos continuos,
pero su margen de riel cae a 1,92 y el de pared M8 a 2,15.
El perfil 40 x 40 x 2 mejora el margen del riel, pero su pared M8 continúa en 2,15.
Por eso cambiar solo el perfil no basta para aceptar el conjunto.

Los casos con e=80/L=350 y e=75/L=300 son sensibilidades hipotéticas,
no posiciones medidas ni cotas confirmadas. El primero supera el objetivo del riel
por muy poco; ningún candidato se declara aprobado.

### D. Protector de bolsa e interfaces

El HDPE representado suma 343 g, de los cuales 197 g están en el protector de cuna.
Su espesor de 6 mm está relacionado con cubrir las tuercas de referencia.

Revisar ubicación de cabezas y tuercas, protección del contacto y superficie realmente necesaria.
La reducción exige conservar cobertura de puntas, radios y protección de bolsa y usuario.
Los materiales de contacto siguen pendientes de calificación térmica y de desgaste.

### E. Tornillería y número de uniones

Los herrajes modelados suman 316 g, con geometría simplificada.
Contrastar catálogo y pesaje reales. Integrar funciones y corregir longitudes puede
ahorrar masa de uniones. No reducir diámetros o eliminar casquillos usando solo el
margen de cortante del tornillo: faltan tracción, apriete, apertura y aflojamiento.

## 4. Criterios para comparar variantes

- Registrar masa completa y distribución por subsistema, incluyendo elementos nuevos del arnés.
- Mantener inicialmente el mismo escenario de cargas para comparar.
- Revisar fluencia, flecha, pandeo, aplastamiento y arrancamiento.
- Evaluar radios, ranuras, agujeros y contacto de la bolsa.
- Usar modelos locales cuando los apoyos y uniones se aparten de las idealizaciones.
- Completar fatiga, fabricación y comprobaciones de arnés y entorno antes de validar uso.

La relación de flexión elástica es sigma=M/Z, con M=F*e, y la rigidez depende de E*I.
Por eso la forma y los apoyos pueden permitir ahorro sin depender únicamente del espesor.
No se afirma equivalencia entre margen analítico y seguridad de uso.

## 5. Información pendiente y trazabilidad

Faltan masa del arnés y cinturón elegidos, anchura de correas, geometría de bolsa llena,
trayectoria real de carga, zonas de contacto y capacidad de fabricación disponible.
Estos datos condicionan la selección final, pero permiten avanzar desde ahora con
alternativas y presupuesto de masa.

El CAD, la memoria MC01 y el ZIP de P2.02 no se han modificado.
Huella SHA-256 del ZIP de referencia: 9353e6ef30483065898f710e1b56b6be4a7f2c876f8e23a77ad9cce72a151f1c

Archivos de este estudio:
- BALANCE_MASAS.csv: suma por subsistema y por cantidad.
- COMPARACION_PRELIMINAR_RIELES.csv: candidatos y sensibilidades parciales.
- ESTUDIO_MASA.md: interpretación y propuesta de trabajo.

## Fuentes

- MASAS_CAD.json, BOM_MODELO.csv y MODELO_P2_02.json de la generación 15:26:25.
- Memoria_SEDAC_P2_02_MC01_EDITABLE.xmcd y REVISION_CALCULOS.md.
- [MIT: solución de flechas de vigas](https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/3533c046dafcc488f1432e92d05ec210_MIT2_080JF13_Lecture5.pdf).
- [Hydro: aleación 6061](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf):
  la soldadura puede reducir resistencia en la zona del T6. Una propuesta de pieza conformada
  o soldada debe elegir proceso, producto y propiedades correspondientes.
- [Atlas: 5052](https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf).
- [NASA RP-1228: diseño de uniones](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf).
