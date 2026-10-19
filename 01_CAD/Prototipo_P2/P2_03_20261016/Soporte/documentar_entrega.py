from pathlib import Path
import json,csv,collections
ROOT=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD')
B=ROOT/'01_CAD/Prototipo_P2/P2_03_20261016';CAD=B/'Entrega/Inventor_Optimizado'
M=ROOT/'06_DOCUMENTACION/Memoria_Calculo_P2_03'
ms=json.loads((CAD/'MASAS_CAD.json').read_text(encoding='utf-8-sig'))
calc=json.loads((M/'Soporte/RESUMEN_CALCULO.json').read_text(encoding='utf-8-sig'))
rigid=calc['mCAD_kg'];total=calc['mTotal_kg'];old=3.2062576846-.0532007361
foam=sum(x['cantidad']*x['masa_candidata_kg'] for x in ms if x['material']=='pad')
saving=100*(1-rigid/old)
def fmt(x,n=3):return f'{x:.{n}f}'.replace('.',',')
def group(x):
 n=x['pieza']
 if x['material']=='pad':return 'Acolchado de referencia (dentro de reserva textil)'
 if x['material']=='herrajes':return 'Tornillos, tuercas y arandelas'
 if x['material']=='hdpe':return 'Protector HDPE'
 if n.startswith('Riel_'):return 'Dos rieles'
 if n.startswith('Anclaje'):return 'Anclajes de hombro y cinturón'
 if n.startswith('Cartela'):return 'Dos cartelas'
 if n.startswith(('Cuna_','Refuerzo_cuna')):return 'Piso y tres refuerzos de cuna'
 if n.startswith(('Travesano','Diagonal')):return 'Travesaños y diagonales'
 return 'Casquillos, pasadores, apoyos y calces'
groups=collections.defaultdict(float)
for x in ms:groups[group(x)]+=x['cantidad']*x['masa_candidata_kg']
rows='\n'.join(f'| {k} | {fmt(v)} |' for k,v in groups.items())
summary=f'''# SEDAC P2.03 - entrega de prediseño

**Revisión:** 16/10/2026. **Escala maestra:** 1:1. **Carpeta de trabajo:** Documentos/SEDAC_CAD.

## Qué abrir

1. **Inventor:** [SEDAC_P2_03.iam](Entrega/Inventor_Optimizado/SEDAC_P2_03.iam). Todos los IPT necesarios están en la misma carpeta. Abrir el IAM, no cada pieza por separado.
2. **Vista previa:** [frente](Entrega/Inventor_Optimizado/VISTA_FRENTE.png), [espalda](Entrega/Inventor_Optimizado/VISTA_ESPALDA.png) y [estructura sin protector](Entrega/Inventor_Optimizado/VISTA_ESTRUCTURA.png).
3. **Intercambio CAD:** [STEP](Entrega/Inventor_Optimizado/SEDAC_P2_03_REVISION.step).
4. **Mathcad y PDF:** [guía de archivos](../../../06_DOCUMENTACION/Memoria_Calculo_P2_03/LEEME_MEMORIA.md). Usar el archivo que termina en **MC02_FINAL_EDITABLE.xmcd**.
5. **Resultados y decisiones:** [informe](INFORME_DISENO_P2_03.md).

## Resultado del aligeramiento

- Estructura, protector y herrajes: **{fmt(rigid)} kg**.
- Reducción equivalente respecto de P2.02: **{fmt(saving,1)} %**, aproximadamente **{fmt(old-rigid)} kg**.
- Presupuesto completo con 0,50 kg de textiles y 0,08 kg de accesorios: **{fmt(total)} kg**.
- El objetivo conceptual de 2 kg **no se alcanza**. Las reservas no son masas medidas.
- Menor margen de los 33 modelos analíticos revisados: **2,254**, en el M6 del marco/X. No es un factor de seguridad global.
- Riel: margen nominal **2,447**, mínimo de pared **2,305** y flecha **2,038 mm**.

## Qué hay en cada carpeta

| Carpeta/archivo | Uso |
|---|---|
| Entrega/Inventor_Optimizado | Única revisión CAD final de P2.03; 51 IPT, IAM, STEP, vistas y registros |
| Soporte | Generadores y comprobaciones; archivos de trabajo, no otra entrega |
| Soporte/Iteraciones | Intentos intermedios conservados; no abrirlos como diseño vigente |
| PARAMETROS_P2_03.json | Dimensiones principales, cargas, materiales y reservas |
| ESPECIFICACION_P2_03.md | Alcance geométrico y datos pendientes |
| INFORME_DISENO_P2_03.md | Razones de diseño, masas, uniones y límites |

## Alcance

Los 25 kg del escenario son **masa total de equipo transportado**, incluyendo soporte y mochila. Se mantienen 3 g verticales totales, 1 g horizontal y reparto 70/30. Si cambia la masa, el brazo de carga o la posición del arnés, hay que recalcular.

El ensamblaje tiene 131 ocurrencias, 390 restricciones de posición y cero interferencias volumétricas nominales detectadas. Las restricciones a planos de referencia no simulan contacto ni apriete. Roscas nativas cosméticas: no hay una hélice sólida en el STEP.

**Sigue siendo un prediseño.** Faltan bomba real, arnés, tolerancias, referencias comerciales certificadas, contacto local, fatiga, temperatura y ensayos. La escotadura para la manguera cambió. No es una orden de fabricación para uso sobre una persona.

## Cómo modificarlo

Trabajar en una copia de revisión nueva. Las dimensiones principales están en el JSON; los detalles de la plantilla están en los generadores de Soporte. No todos los brazos ni las posiciones del arnés se deducen automáticamente de una dimensión general. Una modificación exige comprobar CAD y memoria juntos.

El generador usa Inventor 2027 instalado en este equipo. El cálculo usa Mathcad clásico de la instalación Mathcad 15. Editar el XMCD por sí solo no actualiza el IAM; editar el IAM por sí solo no actualiza la masa de la memoria.

P2.02 y su ZIP histórico se conservan sin cambios. No se publicó esta entrega en Notion ni se envió por correo.
'''
(B/'LEEME.md').write_text(summary,encoding='utf-8')
spec='''# Especificación final SEDAC P2.03 / 16-10-2026

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
'''
(B/'ESPECIFICACION_P2_03.md').write_text(spec,encoding='utf-8')
report=f'''# Informe de diseño y comprobación P2.03

Fecha: 16/10/2026. Revisión de P2.02 conservada por separado.

## 1. Resultado y criterio de comparación

La masa rígida estimada baja de **{fmt(old)} a {fmt(rigid)} kg**, una reducción de **{fmt(saving,1)} %**. Se descuenta del modelo anterior su espuma de referencia (0,053201 kg) para comparar con el mismo alcance.

La nueva masa representada en Inventor es **{fmt(rigid+foam,6)} kg**: incluye **{fmt(foam,6)} kg** de espuma de referencia. Para el sistema completo se suma a la masa rígida una reserva de 0,50 kg que ya incluye todo el acolchado, más 0,08 kg de accesorios. Resultado: **{fmt(total)} kg**, sin bomba ni líquido. Con las mismas reservas, el equivalente anterior sería {fmt(old+.58)} kg.

El objetivo de 2 kg no se alcanzó. Este trabajo no acredita un mínimo global de masa. Reducir más requiere datos reales que permitan revisar dimensiones, brazos, cargas e interfaces.

## 2. Desglose de masa

| Grupo | Masa estimada (kg) |
|---|---:|
{rows}

Densidades usadas: 6061 y anclajes 2700 kg/m³; 5052 2680; inoxidable 8000; HDPE 953; espuma 60. Las masas nativas se contrastaron contra volumen por densidad. No sustituyen pesaje ni certificado. La rosca cosmética no resta el volumen de una hélice y la tuerca no reproduce su deformación de bloqueo.

## 3. Decisiones de aligeramiento

- **Riel:** pared de 2,5 a 1,5 mm; profundidad de 25 a 40 mm. Se aumenta e a 107,5 y L a 423 para incorporar el desplazamiento de la carga. La masa de los dos rieles taladrados es {fmt(groups['Dos rieles'])} kg.
- **Anclajes:** alma de 2 mm con retornos hasta 18. Se calcula flexión asimétrica de los puentes L, raíz C y pandeo local, con pared mínima 1,8. No se sustituyen por placas planas de 2 mm.
- **Interfaz posterior:** se retiran paneles rígidos y fijaciones secundarias; el arnés y su soporte textil quedan por definir. La espuma es una referencia, no una interfaz validada por sí sola.
- **Protector:** HDPE hueco, cara superior de 2 mm y espacio inferior de 12 mm. El paquete de apriete primario es metálico.
- **Cuna:** se conserva el piso de 2,5 mm y se añade un tercer apoyo. Así se reduce la luz a 45 mm y el voladizo delantero a 20 mm. El apoyo cambia la escotadura de manguera: se debe medir.
- **Material que se conserva:** diagonales en X, altura de refuerzos, ala de cartela de 5 mm y apoyos contra aplastamiento. Adelgazarlos uniformemente no conserva los márgenes.

## 4. Escenario y resultados

Se mantienen **25 kg de masa total transportada**, 3 g verticales totales y 1 g horizontal, con 70 % en el lado más cargado. Incluye estructura, mochila, bomba y líquido. Quedan aproximadamente {fmt(25-total,2)} kg del presupuesto para bomba/líquido y elementos no incluidos. Esto no es una carga de uso autorizada.

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

Total: 22 tornillos, 44 arandelas y 22 tuercas; todos se representan como piezas separadas. M6: arandelas 6,4/12/1,6, tuerca AF10 y altura6. M5: 5,3/10/1, tuerca AF8 y altura5. Rosca parcial nominal b=2d+12; verificar la longitud efectiva del producto comprado. La clase geométrica 6g/6H no es la clase resistente A2-80.

Se orientan las cabezas de hombro y cartela derecha para cubrir el plano crítico con vástago liso. Los pasadores de cartela tienen exterior10/interior6,6 y longitud53; se insertan en taladros10,2. Los M6 restantes tienen casquillos interiores; los M5 llevan apoyos con contorno igual al interior redondeado de sus refuerzos.

Las tuercas son autofrenantes metálicas derivadas DIN980; se requiere confirmar un producto de clase80 y carga de prueba compatible. No se ha modelado la deformación del autofreno ni demostrado que nunca se afloje. Las arandelas distribuyen presión; no son el mecanismo de bloqueo.

Se incluyen tracción por precarga y palanca, cortante y flexión local de perno, compresión de apoyos, presión de asiento, punzonamiento nominal y reserva contra apertura. Precargas de estudio: 1500/1400/1800/1000 N, dispersión25 %. El ejemplo T=K F0 d con K=0,20 **no es una instrucción de apriete**: falta par prevalente, fricción y calibración.

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
- [Bossard, inoxidable ISO3506](https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf).
- [NASA RP-1228, Fastener Design Manual](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf).
- [MIT OCW, Structural Mechanics](https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/).
- [Autodesk, ThreadFeatures](https://help.autodesk.com/cloudhelp/2024/ENU/Inventor-API/files/ThreadFeatures.htm).

El PDF amplía las referencias de tornillería, arandelas, fractura y representación. Las fuentes respaldan conceptos y propiedades; no aprueban este diseño particular.
'''
(B/'INFORME_DISENO_P2_03.md').write_text(report,encoding='utf-8')
with (CAD/'BOM_PIEZAS_Y_MASAS.csv').open('w',newline='',encoding='utf-8-sig') as f:
 cols=['pieza','cantidad','material','masa_unidad_kg','masa_grupo_kg','grupo','incluida_reserva_textil'];w=csv.DictWriter(f,cols);w.writeheader()
 for x in ms:w.writerow(dict(pieza=x['pieza'],cantidad=x['cantidad'],material=x['material'],masa_unidad_kg=x['masa_candidata_kg'],masa_grupo_kg=x['masa_candidata_kg']*x['cantidad'],grupo=group(x),incluida_reserva_textil=x['material']=='pad'))
with (CAD/'RESUMEN_MASAS.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['grupo','masa_kg']);w.writerows(groups.items());w.writerow(['CAD sin espuma de referencia',rigid]);w.writerow(['Sistema con reservas',total])
mem=f'''# Memoria SEDAC P2.03 / MC02

## Archivos principales

- **[Mathcad editable final](Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd)**: 247 variables, resultados numéricos guardados por la aplicación, 45 páginas lógicas.
- **[Guía PDF Beamer](Guia_SEDAC_P2_03_MC02_Beamer.pdf)**: 55 diapositivas con teoría, desarrollos y referencias a páginas/secciones del Mathcad.
- [Fuente LaTeX](Guia_SEDAC_P2_03_MC02_Beamer.tex): editable, independiente y compilable.
- [CAD e informe](../../01_CAD/Prototipo_P2/P2_03_20261016/LEEME.md).

## Lectura

Abrir primero el XMCD que contiene **FINAL_EDITABLE** en su nombre. Recalcular con Ctrl+F9. Las entradas con fondo azul son editables; las funciones utilizan argumentos locales. := define y = evalúa. El valor absoluto es el operador nativo con barras.

La aplicación instalada bajo Mathcad15 se identifica por automatización como versión14.1.4.587. El documento se creó en formato clásico XMCD y fue abierto, recalculado y guardado mediante esa instalación; no es formato de MathcadPrime.

La masa CAD actual es **{fmt(rigid)} kg** sin espuma de referencia; el presupuesto completo es **{fmt(total)} kg**. Los 25 kg de cálculo incluyen todo el equipo. No sumar una bomba de25 kg a esta estructura conservando los márgenes actuales.

## Coherencia

Cambiar Mathcad no modifica el CAD. La masa mCAD es una lectura guardada de geometría y densidad. Después de cambios geométricos hay que regenerar, medir masa y recalcular; conservar las revisiones previas. Los archivos dentro de Soporte son fuentes, exportaciones y registros, no versiones alternativas para usar.

Los 33 márgenes listados superan2,2 bajo los modelos parciales; el mínimo2,254 corresponde al M6delmarco. El conjunto no está validado para fabricación/uso: faltan medidas, tolerancias, materiales comprados, fatiga, contacto, FEA y ensayos.
'''
mem=mem.replace('de25','de 25').replace('superan2,2','superan 2,2').replace('mínimo2,254','mínimo 2,254').replace('M6delmarco','M6 del marco').replace('Mathcad15','Mathcad 15').replace('versión14','versión 14').replace('MathcadPrime','Mathcad Prime')
(M/'LEEME_MEMORIA.md').write_text(mem,encoding='utf-8')
measurements=['Modelo exacto y accesorios de bomba','Masa de bomba vacía con manguera','Volumen de agua de trabajo','Masa de bomba llena','Altura llena','Ancho máximo lleno','Profundidad máxima llena','Ancho de huella inferior','Profundidad de huella inferior','Perfil/curvatura inferior','Posición lateral de salida de manguera','Altura y profundidad de salida','Diámetro y giro mínimo de manguera','Tapa: posición y espacio de apertura','Costuras y zonas sin contacto','Posiciones de anclajes existentes','Ancho y espesor de cintas','Dimensiones de cinturón/arnés','Masa de arnés completo y acolchado','Centro de masa: posición estimada y método','Cambio de forma llena/vacía','Acceso de herramientas y secuencia de montaje']
measurement='''# Hoja personal de medición SEDAC / P2.03

Fecha: ______  Modelo: ______  Persona que mide: ______  Instrumentos/resolución: ______

Registrar condición llena/vacía y volumen. Repetir cada cota y conservar fotografías con regla en el mismo plano. Indicar si el dato es medido o estimado; no completar con un supuesto sin marcarlo.

| Nº | Dato | Medida 1 | Medida 2 | Unidad | Condición / foto / observación |
|---:|---|---|---|---|---|
'''+ '\n'.join(f'| {i} | {t} | | | | |' for i,t in enumerate(measurements,1))+'''

## Fotografías

Frente: ___; espalda: ___; lado izquierdo: ___; lado derecho: ___; arriba: ___; base: ___; salida y costuras: ___. Repetir llenado/vaciado cuando cambie la forma.

## Comparación con CAD

| Parámetro | P2.03 supuesto | Valor medido | Cambio propuesto | Recalcular |
|---|---:|---:|---|---|
| Masa total transportada | 25 kg | | | Sí |
| Excentricidad desde eje de riel | 107,5 mm | | | Sí |
| Longitud equivalente | 423 mm | | | Sí |
| Cuna | 300 x 125 mm | | | Sí |
| Reserva completa textil | 0,50 kg | | | Masa y cargas |

Conservar el archivo junto a las fotografías. Esta hoja es personal y no se publica automáticamente en Notion.
'''
(B/'HOJA_MEDICION_P2_03.md').write_text(measurement,encoding='utf-8')
guide=ROOT/'00_GUIA_PERSONAL_SEDAC.md';oldtext=guide.read_text(encoding='utf-8-sig')
if '## Estado actual - 16/10/2026' not in oldtext:
 new=f'''# Guía personal de continuidad - SEDAC

## Estado actual - 16/10/2026

La revisión local actual es **P2.03**, prediseño aligerado a escala1:1. [Abrir entrega e instrucciones](01_CAD/Prototipo_P2/P2_03_20261016/LEEME.md). Masa rígida estimada{fmt(rigid)} kg, aproximadamente{fmt(saving,1)} % menor que P2.02; con reserva de mochila y accesorios,{fmt(total)} kg. Aún no cumple el objetivo de2 kg ni está validada para uso.

- [Mathcad final y PDF Beamer](06_DOCUMENTACION/Memoria_Calculo_P2_03/LEEME_MEMORIA.md).
- [Hoja personal de medición](01_CAD/Prototipo_P2/P2_03_20261016/HOJA_MEDICION_P2_03.md).
- P2.02 y su ZIP histórico siguen intactos. Los borradores P2.03 están dentro de Soporte/Iteraciones.
- Próximo paso: conseguir la bomba, medirla llena/vacía y seleccionar/pesar el arnés. No se ha actualizado Notion en esta entrega.

## Historial conservado hasta el 15/10/2026

Lo que sigue registra estados anteriores; las fechas previstas de octubre6/7 pertenecen a ese historial.

'''
 for a,c in [('escala1:1','escala 1:1'),('estimada'+fmt(rigid),'estimada '+fmt(rigid)),('aproximadamente'+fmt(saving,1),'aproximadamente '+fmt(saving,1)),('accesorios,'+fmt(total),'accesorios, '+fmt(total)),('de2','de 2'),('octubre6/7','octubre 6/7')]:new=new.replace(a,c)
 guide.write_text(new+oldtext,encoding='utf-8')
# Keep JSON-driven preload edits consistent for subsequent revisions; current values are unchanged.
p=B/'Soporte/calcular_y_mathcad.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace("D('scatter','0.25','',True);D('prying','1.5','',True)","D('scatter',str(JU['dispersion']),'',True);D('prying',str(JU['prying']),'',True)")
s=s.replace("[('F0C',1500),('F0F',1400),('F0H',1800),('F05',1000)]","[('F0C',JU['preload_cartela']),('F0F',JU['preload_frame']),('F0H',JU['preload6']),('F05',JU['preload5'])]")
p.write_text(s,encoding='utf-8-sig')
print(json.dumps({'masa_rigida':rigid,'masa_completa_reservada':total,'ahorro_porcentaje':saving,'desglose':groups},ensure_ascii=False,indent=2))
