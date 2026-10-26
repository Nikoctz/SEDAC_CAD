"""
gen_informe.py — genera el informe editable (docx) del paquete documental SEDAC.

Reglas: separar ANTECEDENTE / MEDIDO / DATO DE FABRICANTE / SUPUESTO / HIPOTESIS / CALCULADO /
PENDIENTE. No declarar validacion fisica. Los umbrales sin respaldo quedan como pendientes de
acordar con el profesor. No se inventan mediciones, precios ni disponibilidades.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from docx_lib import Doc  # noqa: E402

OUT = HERE / "Informe_SEDAC_Memoria_y_Ensayos_v0.1.docx"

d = Doc()

# ============================================================ PORTADA
d.title("SEDAC · Memoria de cálculo y plan de ensayos")
d.para("Informe de planificación para la memoria de cálculo y los ensayos del prototipo de transporte "
       "de agua para transporte al respaldo con bomba de espalda (SEDAC).", size=11)
d.para("Base vigente: P2.04 (entregable del 16/10/2026). P2.05 abierta. Motor de cálculo: Mathcad 15 "
       "(instalación de este equipo). Registro y seguimiento: planilla Excel de este paquete.", size=10)
d.para("Versión del documento: 0.1 · Fecha: 2026-10-25 · Estado: borrador de trabajo, sujeto a revisión "
       "del profesor de biomecánica y a la medición real del equipo.", size=10, bold=True)
d.para("Qué NO es este documento: no es una validación del prototipo, no acredita resistencia, "
       "seguridad, comodidad ni cumplimiento normativo, y no autoriza ensayos con personas. Las cifras "
       "de carga que se usan son hipótesis de prediseño declaradas como tales.", size=10, bold=True,
       color="8A3B12")
d.page_break()

# ============================================================ 0. COMO LEER ESTE DOCUMENTO
d.heading("0. Cómo leer este documento", 1)
d.para("Este apartado está pensado para alguien que llega por primera vez. Si ya conoce el proyecto, "
       "puede saltarlo y empezar por el §1.")

d.heading("0.1 Qué es SEDAC, en pocas palabras", 2)
d.para("SEDAC es un arnés para llevar agua a la espalda. La bomba va en la espalda, sujetada por un "
       "arnés de correas, y el agua se transporta en la bolsa de la bomba. El problema no es la bomba: es "
       "que una persona tiene que caminar con ella durante horas, a veces corriendo o con terreno difícil, "
       "y a menudo necesita las dos manos libres.")
d.para("Para que eso sea llevadero hacen falta tres cosas al mismo tiempo, y ese es el motivo de que el "
       "prototipo sea de aluminio mecanizado y no de tela:")
d.bullet("Que el peso de la bomba no se apoye directamente sobre el cuerpo. El agua pesa y vibra: si toda "
         "esa carga la sostiene solo el arnés de tela, aparecerían zonas de presión muy altas y dolor en la piel.")
d.bullet("Que la carga se reparta en dos puntos concretos, el hombro y el cinturón, en vez de repartirse de "
         "forma difusa por toda la espalda.")
d.bullet("Que la estructura sea rígida. Un marco de aluminio reparte la carga entre los apoyos y evita que "
         "el conjunto se balancee.")
d.para("El prototipo de este proyecto es ese marco: dos canales verticales de aluminio de 32 × 24 × 3 mm y "
       "480 mm de largo, separados 190 mm, unidos abajo por una interfaz lumbar y arriba por dos yugos. "
       "Las piezas de texto (cunas, cintas, acolchados) hacen el contacto con el cuerpo; el aluminio "
       "carga.")

d.heading("0.2 Las piezas del prototipo y para qué sirve cada una", 2)
d.table([
    ["Pieza", "Para qué sirve", "Cómo lo entender"],
    ["Canal (2)", "El esqueleto vertical. Recibe el peso de la bomba y lo lleva hasta los apoyos",
     "Son dos perfiles de aluminio en U, como dos rieles verticales"],
    ["Interfaz lumbar", "Une los dos canales por abajo y recibe el apoyo de la zona lumbar",
     "Una placa horizontal que cose los dos canales abajo"],
    ["Yugo superior (2)", "La interfaz de arriba, donde se apoya el hombro",
     "Una pieza en horizontal en la parte alta de cada canal"],
    ["Mejilla", "Una placa que abraza el ala del canal por fuera y reparte la presión del tornillo",
     "Como una oreja que aprieta el canal por fuera"],
    ["Casquillo", "Un tubo corto que separa las dos alas del canal dentro de la unión",
     "Su función es topar: si no estuviera, al apretar el tornillo las alas se aplastarían"],
    ["Pasador", "Un tubo que pasa por las dos alas y transmite el esfuerzo cortante",
     "Va justo por el hueco del taladro; el tornillo de dentro lo aprieta"],
    ["Tornillo M5, arandela y tuerca", "El apriete de cada unión",
     "Cada unión es un tornillo con su arandela y su tuerca; hay 8 uniones"],
    ["Cuna, cintas y acolchados", "El contacto con el cuerpo",
     "Son las piezas textiles; no se les atribuye resistencia estructural"],
    ["Panel posterior", "La cubierta trasera de reparto",
     "Una lámina de HDPE de 1 mm, sin función portante"],
], widths=[1700, 3300, 3200])

d.heading("0.3 En qué estado está el proyecto y qué es este paquete", 2)
d.para("Hoy el prototipo existe como modelo CAD (54 piezas, 83 ocurrencias, masa medida de 1,442 kg) y "
       "como memoria de prediseño: un cálculo con hipótesis de carga que indica, para cada forma posible "
       "de fallo, cuánto margen queda. No existe ninguna revisión fabricada ni probada, no hay "
       "certificados de material y no hay ensayos. El prototipo no está liberado para llevarlo una persona.")
d.para("Este paquete es la preparación de la etapa siguiente: dejar la memoria de cálculo lista para "
       "recalcularse con datos reales, dejar una planilla donde registrar esos datos sin rehacer la "
       "documentación, y dejar escrito el protocolo con el que se medirá y se ensayará.")

d.heading("0.4 Las cuatro categorías de dato que se usan en todo el documento", 2)
d.table([
    ["Categoría", "Qué significa", "Ejemplo en este paquete"],
    ["ANTECEDENTE", "Viene de un archivo del proyecto y se puede comprobar leyendo ese archivo",
     "El ancho del canal, 32 mm, está en el modelo CAD"],
    ["MEDIDO", "Se obtuvo con un instrumento y tiene fecha, método e incertidumbre",
     "La masa de 1,442328 kg, medida por el propio Inventor sobre el modelo"],
    ["SUPUESTO o HIPÓTESIS", "Un valor que se adoptó para poder calcular, pero que nadie ha medido",
     "Los 25 kg de carga, el reparto 70/30 y la precarga de 2000 N"],
    ["PENDIENTE", "No existe el dato. Nunca se escribe un cero en su lugar",
     "La masa real de la bomba y el ancho real de las correas"],
], widths=[1700, 3700, 2800])
d.para("Cuando una cifra es hipótesis, el texto lo dice. Cuando un dato no existe, el texto lo dice. "
       "Por eso este documento se puede leer como una lista de lo que falta tanto como de lo que hay.")

d.heading("0.5 Glosario: las palabras técnicas que aparecen en el documento", 2)
d.table([
    ["Término", "Qué significa en palabras sencillas"],
    ["Prototipo funcional", "La primera versión que se puede usar de verdad, no un modelo de estudio. Este, todavía no: es un modelo con el que se calcula"],
    ["Prediseño", "Cálculo hecho antes de fabricar, con hipótesis, para decidir si vale la pena fabricar y qué forma conviene"],
    ["Cribado", "Filtro de comprobaciones que descarta las formas de fallo con poco margen. Es una criba, no una certificación"],
    ["Margen (n)", "Cuántas veces la resistencia disponible supera a la demanded por la carga. n = 2,25 significa que la pieza aguanta 2,25 veces esa carga"],
    ["Umbral de margen", "El valor mínimo de n que se acepta. En este proyecto es 2,2, y es una decisión de prediseño, no una norma"],
    ["Modo que gobierna", "La forma de fallo que deja menos margen. Si el margen lo fija el pandeo local, dice que ese es el punto débil"],
    ["Pandeo local de alas", "Que las alas del canal se doblen hacia dentro formando una onda, en vez de romperse. Es el modo que gobierna hoy"],
    ["Pandeo global (Euler)", "Que el canal entero se curvee como una barra, como una regla flexible"],
    ["Pandeo lateral torsional", "Que el canal gire sobre su eje y se deforme en planta, por la asimetría de la carga"],
    ["Flecha", "Cuánto se desplaza el canal en el punto más cargado, en milímetros"],
    ["Precarga", "El apriete que se le da al tornillo de la unión antes de que entre la carga de uso"],
    ["Apilamiento axial", "La suma de las piezas que se apilan en la dirección del tornillo: paquete, arandelas, tuerca. Determina si el tornillo llega o sobra"],
    ["Holgura axial", "El espacio que queda entre el casquillo y las caras interiores de las alas. Hoy vale 0,000 mm: el casquillo ocupa exactamente el ancho interior"],
    ["Paquete", "El conjunto de piezas que el tornillo atraviesa: canal (32 mm) más las dos mejillas (3 mm cada una) = 38 mm"],
    ["Excentricidad", "A qué distancia del eje del canal está el peso de la bomba. Esa distancia es la que hace que el canal se doble"],
    ["Reparto 70/30", "Cuánto de la carga se lleva el lado más cargado (70 %) frente al otro (30 %). Hoy es una hipótesis"],
    ["Factor 3 g / 1 g", "Cuánto se amplifica la carga de uso respecto del peso quieto: 3 veces en vertical y 1 en horizontal. Hoy es una hipótesis"],
    ["Tuerca autofrenante", "Una tuerca con un inserto que evita que se suelte sola. No está probada en este proyecto"],
    ["IMU", "Unidad de medición inercial: un sensor que mide aceleración y velocidad angular. Sirve para medir movimiento, no fuerza"],
    ["Aceleración", "Cuánto cambia la velocidad por segundo. Es lo que mide la IMU; la fuerza es otra cosa y no se obtiene sin un modelo"],
    ["Banco", "Instalación de laboratorio con apoyos y lastre para ensayar sin personas"],
    ["FEA", "Análisis por elementos finitos: la herramienta para estudiar el detalle por método numérico. Este proyecto no tiene ninguno"],
    ["Reserva de masa", "Un kg que se aparta en el presupuesto para el arnés y los textiles, porque aún no se han medido"],
], widths=[2100, 6100])
d.para("Dos palabras que se usan en sentidos distintos según el contexto: 'en cortante' significa que la "
       "carga empuja lateralmente y no que la pieza está descargada, y 'apantallamiento' o 'aplastamiento' "
       "se refieren a que una pieza recibe el esfuerzo de otra en una superficie de contacto pequeña.")
d.page_break()

# ============================================================ 1. REVISIÓN INICIAL
d.heading("1. Revisión inicial: qué está confirmado, qué es del prototipo antiguo y qué falta", 1)
d.para("En pocas palabras: se revisaron los archivos vigentes del proyecto. La geometría, las uniones y la masa están confirmadas; la memoria de cálculo anterior sirve solo como método, no como resultado; y faltan las mediciones de la bomba, las correas y las tolerancias, que son justamente lo que bloquea el cierre del diseño.")
d.para("La revisión se hizo sobre los archivos vigentes del repositorio SEDAC_CAD, en modo de solo "
       "lectura. El estado del proyecto se tomó de ESTADO_ACTUAL.md (24/10/2026) y de DECISIONES.md; "
       "no se usó ninguna versión histórica como si fuera la vigente.")

d.heading("1.1 Confirmado en el prototipo vigente", 2)
d.table([
    ["Elemento", "Valor o estado", "Fuente", "Categoría"],
    ["Geometría del canal", "Doble canal abierto 6061-T6 de 32 × 24 × 3 mm, largo 480 mm, separación 190 mm, 4 estaciones por canal a Ø10,2 con eje a z = 12 mm",
     "PARAMETROS_P2_05.json; Entrega/Inventor/MODELO_API.json", "ANTECEDENTE verificado"],
    ["Uniones", "8 uniones M5: pasador hueco Ø10/Ø5,5 × 37,6 mm, casquillo Ø12,5/Ø10,2 × 26 mm, arandela 5,3 × 16 × 3 mm (GN 6341), tornillo M5×55 ISO 4762, tuerca autofrenante M5",
     "MODELO_API.json; BOM_FIJACIONES.csv", "ANTECEDENTE verificado"],
    ["Masa rígida y protectores", "1,442328 kg, medida por MassProperties en Inventor",
     "01_CAD/Prototipo_P2/P2_04_20261016/BOM_Y_MASAS.csv", "MEDIDO en CAD"],
    ["Presupuesto del sistema", "2,212328 kg (rígida + 0,65 kg de reserva textil + 0,12 kg de reserva). Sin bomba ni agua",
     "Cálculo de prediseño del repositorio", "CALCULADO"],
    ["Cribado de prediseño", "15 verificaciones, mínimo 2,2471; gobierna el límite de fluencia bajo tensión combinada; la comprobación local empata porque está limitada por fluencia, no por pandeo elástico; flecha 0,8667 mm",
     "Analisis/V0_base_P2_05/RESULTADOS_PREDISENO.json", "CALCULADO condicionado a hipótesis"],
    ["Punto crítico abierto", "Holgura axial nominal de 0,000 mm entre casquillo y caras interiores de las alas, porque el casquillo se define como B − 2t",
     "generar_p2_05.py (línea 45) y memoria de este paquete", "CALCULADO"],
    ["Hojas de captura existentes", "Registro de medición de bomba (02_PROTOTIPO) y hoja de medición de P2.03, sin datos",
     "02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md", "ANTECEDENTE"],
], widths=[1500, 3900, 2400, 1100])

d.heading("1.2 Pertenece al prototipo antiguo y sirve solo de antecedente", 2)
d.para("Estos elementos describen versiones anteriores (P2.02 y P2.03) o estructuras de apoyo. Se auditan "
       "y se reutilizan solo en lo que sea independiente de la geometría y de las cargas actuales.")
d.table([
    ["Antecedente", "Qué era", "Qué se hace con él"],
    ["Memoria de cálculo P2.03 (MC02)", "Memoria de prediseño en Mathcad clásico (.xmcd) de la arquitectura de doble riel 50×40×1,5 con Marco X M6",
     "Se audita (§9). Sus ecuaciones se reutilizan; su geometría, cargas, materiales y resultados NO se transfieren."],
    ["Memoria de cálculo P2.02 (MC01)", "Primera memoria de prediseño, mismo formato", "Se conserva como antecedente histórico; no se actualiza."],
    ["Hoja de medición P2.03", "22 ítems de medición de bomba, arnés y correas", "Se reutiliza como estructura de formulario; sus columnas están vacías y sus cotas no aplican al prototipo actual."],
    ["Kit de montaje V0.1", "Kit geométrico de anclaje, base y separadores para impresión PLA, con lista de fijaciones",
     "Se reutiliza su lista de componentes comerciales y su apilamiento como referencia; no es la arquitectura vigente."],
    ["Hoja de registro de bomba local", "Formulario en blanco para medir la bomba real",
     "Es el formulario de referencia del anexo A.1: ya existe en el repositorio y se adopta sin duplicarlo."],
], widths=[1900, 3300, 3700])

d.heading("1.3 Falta, y bloquea el trabajo", 2)
d.bullet("La bomba de espalda real: masa vacía y llena, centro de masa, envolvente, tapa, manguera y puntos de anclaje. Sin esto no hay carga ni excentricidad verificables.")
d.bullet("Las correas y el arnés: ancho, espesor, resistencia, rigidez, recorrido y zonas de apoyo reales. Sin esto el reparto de cargas es hipótesis.")
d.bullet("La cadena de tolerancias del apilamiento: B, t y longitud real de casquillos medidos en piezas. Sin esto la holgura axial de 0,000 mm no se puede cerrar.")
d.bullet("Los materiales comprados: grado, condición, propiedades certificadas y disponibilidad de canal, casquillo, pasador, tornillo, arandela y tuerca.")
d.bullet("La instrumentación: qué IMU hay en el laboratorio, con qué software se registra y si existe celda de carga. Sin inventario no se puede elegir sensor.")
d.bullet("El acceso al laboratorio y la agenda del profesor: hoy no hay ninguna fecha comprometida en este documento.")
d.bullet("Los criterios de aceptación de los ensayos: sin umbral acordado, los resultados se registran pero no se declaran aprobados ni rechazados.")

d.heading("1.4 Tres preguntas que condicionan el trabajo", 2)
d.para("Se registran aquí en lugar de interrumpir la entrega, porque ninguna de las tres bloquea la "
       "preparación documental ya hecha.")
d.table([
    ["#", "Pregunta", "Por qué condiciona", "Qué se hace mientras no se responda"],
    ["P1", "¿El profesor pone a disposición la bomba de espalda real y las correas del prototipo, o el prototipo se evaluará con cargas simuladas?",
     "Determina si el caso de carga puede apoyarse en masa y centro de masa medidos, o seguirá siendo hipótesis de 25 kg.",
     "La memoria mantiene las hipótesis de prediseño y deja los símbolos de medición definidos al incorporarse."],
    ["P2", "¿Qué criterio de aceptación se usará para cada ensayo (tolerancia admisible, número de repeticiones y tratamiento de la dispersión)?",
     "Sin criterio, un ensayo se puede registrar pero no cerrar; y el protocolo necesita criterios de parada.",
     "La columna de criterio queda como «Por acordar» en la planilla y el protocolo propone rangos de referencia claramente marcados como propuesta."],
    ["P3", "¿Qué instrumentación hay efectivamente en el laboratorio (IMU, software de registro, celda de carga o dinamómetro) y con qué frecuencia real de muestreo?",
     "La IMU mide aceleración, no fuerza: sin celda de carga la cadena de cargas de las correas no se puede cerrar.",
     "La matriz de sensores queda con criterios de comparación y las candidatas sin datos, lista para completar en la visita al laboratorio."],
], widths=[500, 2900, 2700, 2800])

d.page_break()

# ============================================================ 2. OBJETIVO Y ALCANCE
d.heading("2. Objetivo, alcance, descripción del sistema y límites de la validación", 1)
d.heading("2.1 Objetivo", 2)
d.para("Dejar preparado, de forma que no haya que reconstruir la documentación, el camino que lleva desde el "
       "prototipo CAD vigente hasta un prototipo cuyos puntos de decisión estén apoyados en mediciones: una "
       "memoria de cálculo editable y verificada en Mathcad 15, una planilla de captura con trazabilidad "
       "completa, un protocolo de laboratorio sujeto a revisión y una matriz de decisiones lista para "
       "usarse con evidencia.")
d.heading("2.2 Alcance de este paquete", 2)
d.bullet("Documental y de soporte. No incluye CAD nuevo, no modifica el prototipo, no cierra P2.05 y no reemplaza la memoria de cálculo vigente del repositorio: la reproduce y la deja parametrizada.")
d.bullet("Incluye: informe editable, planilla de captura y seguimiento, memoria de cálculo Mathcad 15 verificada, guion de implementación, auditoría de la memoria anterior, formularios y diccionario de datos.")
d.bullet("No incluye: ensayo realizado, datos de laboratorio, análisis FEA, selección de proveedor con cotización cerrada ni liberación para uso con personas.")
d.heading("2.3 Descripción del sistema", 2)
d.para("SEDAC es un arnés de transporte de agua con bomba de espalda, pensado para que la persona que lo "
       "usa pueda moverse con las manos libres en terreno. El conjunto rígido son dos canales verticales "
       "de aluminio que forman el esqueleto y reciben la carga de la bomba; las correas transmiten esa "
       "carga al cuerpo y los textiles y acolchados distribuyen el contacto. La optimización de "
       "masa importa porque el equipo se carga y se porta, pero no puede obtenerse recortando espesores: el "
       "límite que gobierna en el caso base es la fluencia bajo tensión combinada. La tensión crítica elástica local calculada es mayor que la fluencia adoptada; el empate de márgenes no demuestra pandeo local gobernante.")
d.table([
    ["Elemento", "Función", "Material y estado", "Qué falta por medir"],
    ["Canal (Refuerzo_C_I / _D)", "Esqueleto vertical; recibe la carga de la bomba y la transmite a los apoyos",
     "6061-T6, mecanizado o extrusión certificada, 32 × 24 × 3 mm", "B y t reales, acabado superficial y radios efectivos"],
    ["Interfaz lumbar aligerada", "Une los dos canales abajo y recibe el apoyo lumbar",
     "6061-T6, cuerpo 3 mm, refuerzos hasta 6 mm; redondeo de 0,5 mm solicitado y NO aplicado", "Contorno y recortes; decisión sobre el redondeo"],
    ["Yugo superior", "Interfaz superior y apoyo de hombro", "6061-T6, placa 6 mm, mejillas 3 mm", "Contorno y posición de las mejillas"],
    ["Casquillo", "Tope de compresión entre alas: evita que las alas se aplasten al apretar", "6061-T6, Ø12,5/Ø10,2 × 26 mm", "Longitud real y holgura axial admisible"],
    ["Pasador hueco", "Transmite cortante entre mejilla y ala; aloja el M5 que aporta apriete y retención", "6061-T6, Ø10/Ø5,5 × 37,6 mm", "Tolerancias de diámetro y longitud"],
    ["Fijaciones", "Precarga de las 8 uniones", "Tornillo M5×55 ISO 4762 (A2-80 hipótesis), arandela GN 6341, tuerca autofrenante", "Par de apriete, clase y prueba de la tuerca"],
    ["Cuna, cintas y acolchados", "Contacto y transmisión de carga sobre el cuerpo", "Textiles por seleccionar; reserva de 0,65 kg", "Ancho, espesor, resistencia, rigidez, recorrido"],
    ["Panel posterior", "Cubierta de reparto", "HDPE 1 mm, sin crédito estructural", "Recortes y ranuras"],
    ["Bomba de espalda", "Carga transportada", "Scotty 4000-BP según ficha del fabricante; masa real no medida", "Masa, centro de masa, envolvente, interfaces"],
], widths=[1500, 2600, 3000, 1800])

d.heading("2.4 Límites de la validación", 2)
d.bullet("La memoria calcula un cribado de prediseño con hipótesis de carga: 25 kg de masa total, 3 g vertical, 1 g horizontal, reparto 70/30, excentricidad 107,5 mm y precarga de 2000 N. Ninguna de esas cifras está medida y el propio repositorio las marca como hipótesis.")
d.bullet("El cribado no cubre fatiga, pandeo distorsional, FEA de detalle, contacto real, abrasión, ergonomía ni liberación de emergencia.")
d.bullet("Los factores de seguridad calculados son índices de un filtro, nofactors de seguridad certificate. El umbral 2,2 es un criterio de prediseño, no un criterio normativo.")
d.bullet("Un ensayo con IMU mide movimiento, no fuerza. Convertir aceleración en fuerza exige un modelo dinámico con masa, rigidez y amortiguamiento, y sus condiciones de validez; sin esa cadena no se puede cerrar la resistencia de las correas.")
d.bullet("Los ensayos con personas solo proceden con autorización documentada, tras la prueba piloto, con consentimiento y con criterios de interrupción definidos.")
d.page_break()

# ============================================================ 3. REQUISITOS
d.heading("3. Requisitos y criterios de aceptación", 1)
d.para("En pocas palabras: esta es la lista de cosas que el prototipo tiene que cumplir. Cada línea dice de dónde sale el criterio. Los umbrales que no tienen respaldo escrito quedan como pendientes de acordar con el profesor, no se inventan.")
d.para("Cada requisito lleva su fuente. Cuando el criterio numérico no tiene respaldo documentado, se "
       "declara PENDIENTE DE ACORDAR con el profesor, sin proponer un valor como si estuviera aceptado.")
d.table([
    ["ID", "Requisito", "Criterio de aceptación", "Fuente del criterio", "Estado"],
    ["R01", "El canal no falla por pandeo local con la carga de uso",
     "n ≥ 2,2 es un umbral de prediseño por validar; en el caso base gobierna la fluencia bajo tensión combinada, no el pandeo local elástico",
     "Cálculo de prediseño vigente (D-14); umbral no validado", "Umbral PENDIENTE DE ACORDAR"],
    ["R02", "Las uniones no fallan por aplastamiento ni por cortante",
     "n ≥ 2,2 en aplastamiento de ala y mejilla, arranque y pasador; cierre de junta positivo",
     "Cálculo de prediseño vigente", "Umbral PENDIENTE DE ACORDAR"],
    ["R03", "El prototipo no cede bajo la masa de la bomba",
     "Flecha ≤ 5 mm en el apoyo; hoy 0,8667 mm con hipótesis",
     "PARAMETROS_P2_05.json (flecha_limite, supuesto)", "PENDIENTE DE ACORDAR"],
    ["R04", "Las correas reparten la carga de forma conocida",
     "Sin criterio hasta medir la correa y medir la fuerza en ella",
     "No existe criterio en el repositorio", "PENDIENTE"],
    ["R05", "El contacto no depende de aristas vivas",
     "Clasificación de zonas de contacto A/B/C y redondeo de 0,5 mm en la interfaz lumbar",
     "D-12 y registro de redondeos (E_FAIL en 0,5 mm)", "PENDIENTE"],
    ["R06", "El usuario puede liberarse del equipo con guantes",
     "Sin criterio. Requiere ensayo con guantes y acceso físico medido",
     "No existe criterio en el repositorio", "PENDIENTE"],
    ["R07", "El presupuesto de masa se sostiene con el equipo real",
     "Objetivo de 2,0 kg; hoy 2,212328 kg con reservas, brecha 0,212328 kg",
     "Reservas de masa del JSON de parámetros", "Brecha declarada"],
    ["R08", "La respuesta medida es compatible con la predicción",
     "Sin criterio. Debe fijarse diferencia y repetibilidad antes del piloto",
     "No existe criterio en el repositorio", "PENDIENTE DE ACORDAR"],
    ["R09", "El apilamiento de la unión es fabricable",
     "Holgura axial del casquillo compatible con la tolerancia de B y t medidas",
     "Cadena de tolerancias abierta (H04 en la auditoría del repositorio)", "PENDIENTE DE MEDIR"],
], widths=[500, 2300, 2400, 2400, 1300])

d.page_break()

# ============================================================ 4. PLANIFICACIÓN POR ETAPAS
d.heading("4. Planificación por etapas", 1)
d.para("En pocas palabras: el orden no es arbitrario. Primero se miden las cosas que hoy son suposiciones (bomba, correas, apoyos, tolerancias), después se elige y calibra el instrumental, luego se hace un piloto y solo después se ensaya. Ninguna etapa puede empezar antes de que la anterior esté cerrada.")
d.para("La secuencia sigue la lógica del propio repositorio: medir primero (bloquea el resto), después "
       "caracterizar la bomba y las correas, después elegir e instalar sensores, calibrar, hacer un piloto, "
       "ensayar, procesar, actualizar los cálculos y, solo al final, revisar el diseño. No hay fechas: la "
       "duración es una estimación declarada y los responsables están por asignar.")

d.table([
    ["Etapa", "Objetivo", "Qué produce", "Condición para pasar a la siguiente"],
    ["E0 · Preparación", "Fijar alcance, protocolos y criterios con el profesor; inventariar piezas; cerrar la cadena de tolerancias del apilamiento",
     "Protocolo aprobado, inventario, tabla de tolerancias medidas", "El profesor acepta el protocolo y hay criterio de aceptación escrito"],
    ["E1 · Caracterización de bomba", "Masa y centro de masa reales de la bomba, y su envolvente e interfaces",
     "Ficha de bomba con condición llena/vacía y método", "Hay masa y centro de masa con incertidumbre"],
    ["E2 · Caracterización de correas y arnés", "Ancho, espesor, resistencia, rigidez, recorrido y apoyos reales",
     "Ficha de correas y de arnés", "El reparto de cargas deja de ser hipótesis"],
    ["E3 · Sensores", "Definir las preguntas experimentales antes de elegir; inventariar el material del laboratorio; decidir si hace falta medir fuerza",
     "Ficha de selección de sensor con justificación", "Sensor e instrumentación adicional decididos"],
    ["E4 · Calibración", "Calibración estática de las IMU y verificación de sincronización con la instrumentación de fuerza",
     "Tablas de offset y de desfase, con repetibilidad", "Error de sincronización menor que el criterio acordado"],
    ["E5 · Prueba piloto", "Montaje en banco sin personas, con registro crudo, y revisión del profesor",
     "Datos del piloto y acta de revisión", "El profesor aprueba el paso a ensayo con personas"],
    ["E6 · Ensayos", "Ensayos con carga inerte y, solo con autorización, con personas",
     "Datos brutos por ensayo, con versión del prototipo y configuración", "Todos los ensayos con criterio de parada aplicado"],
    ["E7 · Procesamiento", "Corrección de sesgos, deriva y orientación; comparación con la predicción",
     "Datos procesados y tabla de cotejo predicción-ensayo", "Diferencias con causa identificada o pendiente explícita"],
    ["E8 · Actualización de cálculos", "Incorporar las mediciones a la memoria y recalcular el cribado y la sensibilidad",
     "Memoria versión 2 con entradas medidas", "Recálculo cerrado y lista de modos que fallan"],
    ["E9 · Revisión del diseño", "Decidir sobre geometría, material, unión, correa y montaje con la evidencia",
     "Matriz de decisión cerrada y expediente actualizado", "Decisiones registradas con su evidencia"],
], widths=[1500, 2700, 2700, 2000])

d.heading("4.1 Tabla de actividades", 2)
d.para("Duración estimada: unidades de trabajo de una jornada completa con una persona. No son fechas ni "
       "compromisos del profesor. El responsable queda por asignar en la planilla (hoja 01_Planificacion).")
actividades = [
    ["A01", "E0", "Inventario de piezas P2.04 y su estado físico", "", "Entrega P2.04", "Media jornada", "Acceso a la carpeta de entrega", "Lista de piezas con identificadores y disponibilidad", "Acta de inventario"],
    ["A02", "E0", "Definición de alcance y protocolo con el profesor", "", "Este informe", "1 reunión", "Profesor disponible", "Protocolo y criterios de parada acordados", "Protocolo firmado"],
    ["A03", "E0", "Cadena de tolerancias del apilamiento axial", "A01", "Canales, casquillos y pasadores reales", "Media jornada", "Piezas disponibles", "Tabla de B, t y L con incertidumbre", "Hoja de medición"],
    ["A04", "E0", "Definición del banco y de la carga inerte", "A02", "Criterios acordados", "1 reunión", "Protocolo aprobado", "Lastre, incrementos y criterio de parada", "Registro del banco"],
    ["A05", "E1", "Caracterización dimensional de la bomba", "A01", "Bomba y instrumentos", "1 jornada", "Bomba disponible", "Dimensiones con condición llena/vacía", "Registro y fotos"],
    ["A06", "E1", "Masa y centro de masa de la bomba llena", "A05", "Bomba llena y báscula", "Media jornada", "Dimensiones tomadas", "Masa y centro de masa con método", "Hoja de masa"],
    ["A07", "E2", "Medición de ancho, espesor y rigidez de correas", "A01", "Correas seleccionadas", "Media jornada", "Correas disponibles", "Valores con incertidumbre", "Hoja de correas"],
    ["A08", "E2", "Medición del arnés: masa, recorrido y apoyos", "A01", "Arnés y acolchado", "1 jornada", "Arnés disponible", "Masa y mapa de apoyos", "Hoja de arnés"],
    ["A09", "E3", "Definir las preguntas experimentales antes de elegir sensor", "A02", "Objetivos del laboratorio", "1 sesión", "Alcance acordado", "Magnitudes a medir y decisiones asociadas", "Acta de definición"],
    ["A10", "E3", "Inventario del material IMU del laboratorio", "A09", "Acceso al laboratorio", "Media jornada", "Acceso concedido", "Inventario con modelo y software", "Inventario"],
    ["A11", "E3", "Selección de sensor y de instrumentación adicional", "A09, A10", "Inventario y criterios", "1 sesión", "Inventario completo", "Sensor y accesorio de fuerza con justificación", "Ficha de selección"],
    ["A12", "E3", "Definición del sistema de coordenadas y de la fijación", "A11", "Sensor elegido", "1 sesión", "Sensor disponible", "Protocolo de ejes y fijación con fotos", "Protocolo de montaje"],
    ["A13", "E4", "Calibración estática de las IMU en seis posiciones", "A11", "IMU y girómetro de referencia", "Media jornada", "IMU instalada", "Offset por eje con repetibilidad", "Registro de calibración"],
    ["A14", "E4", "Verificación de sincronización IMU-DAQ de fuerza", "A11, A13", "IMU y adquisicion de fuerza", "Media jornada", "Ambos disponibles", "Desfase medido y corregido", "Registro de sincronización"],
    ["A15", "E5", "Prueba piloto en banco sin personas", "A04, A12, A13", "Prototipo, banco y lastre", "1 jornada", "Todo lo anterior cerrado", "Piloto con datos crudos", "Registro del piloto"],
    ["A16", "E5", "Revisión del profesor sobre el piloto", "A15", "Datos del piloto", "1 reunión", "Piloto ejecutado", "Observaciones y ajustes acordados", "Acta de revisión"],
    ["A17", "E6", "Ensayos con carga inerte", "A16", "Prototipo instrumentado", "Según protocolo", "Piloto revisado", "Serie de ensayos con criterio de parada", "Datos brutos y registro"],
    ["A18", "E6", "Ensayos con personas, solo con autorización", "A16, A17", "Consentimiento y protocolo de seguridad", "Según protocolo", "Autorización escrita", "Datos de campo con consentimiento", "Consentimientos y datos"],
    ["A19", "E7", "Procesamiento de señales IMU y corrección de sesgos", "A17", "Software del sensor", "1 jornada", "Datos brutos disponibles", "Series procesadas con método documentado", "Carpetas de datos procesados"],
    ["A20", "E7", "Comparación predicción-ensayo", "A19, A11", "Memoria y datos procesados", "1 jornada", "Ambos disponibles", "Tabla de cotejo con causas", "Hoja de comparación"],
    ["A21", "E8", "Actualización de entradas medidas en la memoria", "A03, A06, A07, A08", "Mediciones registradas", "1 jornada", "Entradas disponibles", "Memoria recalculada (versión 2)", "Memoria MC02"],
    ["A22", "E8", "Recálculo del cribado y de la sensibilidad", "A21", "Memoria actualizada", "1 jornada", "Memoria actualizada", "Márgenes nuevos y modos que fallan", "Informe de recálculo"],
    ["A23", "E9", "Matriz de decisión de diseño", "A22", "Resultados comparados", "1 sesión", "Recálculo cerrado", "Acciones propuestas y condicionadas", "Registro de decisiones"],
    ["A24", "E9", "Actualización del expediente de diseño", "A23", "Decisiones tomadas", "1 jornada", "Decisiones cerradas", "Expediente con trazabilidad", "Expediente y changelog"],
]
d.table([["ID", "Etapa", "Actividad", "Depende de", "Insumo", "Duración estimada", "Condición de inicio", "Resultado esperado", "Evidencia de cierre"]] +
         [list(a) for a in actividades], widths=[500, 500, 2200, 800, 1500, 1000, 1400, 1600, 1400], font_size=7)
d.page_break()

# ============================================================ 5. PROTOCOLO
d.heading("5. Protocolo propuesto de laboratorio", 1)
d.para("En palabras sencillas: el protocolo dice qué se mira, con qué instrumento, cómo se ancla el sensor, cuántas veces se repite y en qué momento se detiene todo. Está escrito para que el profesor lo revise y lo modifique: es una propuesta, no un procedimiento aprobado.")
d.para("Propuesta para revisión del profesor. No sustituye un protocolo aprobado y no habilita por sí "
       "mismo ensayos con personas. Los valores numéricos marcados como referencia son rangos de trabajo "
       "razonables para un banco de carga inerte, no criterios aceptados.")
d.heading("5.1 Antes de la sesión", 2)
d.bullet("Verificar el estado del prototipo: apriete de las 8 uniones, integridad de aristas, estado de las cintas y de los acolchados, y ausencia de juego en los apoyos.")
d.bullet("Registrar la versión del prototipo (P2.04) y la configuración concreta de cada ensayo: qué piezas, qué correas, qué lastre y qué anclajes.")
d.bullet("Confirmar el instrumento de medición y su calibración vigente; si el instrumento no está calibrado, el ensayo no se registra como válido.")
d.bullet("Definir por escrito el criterio de parada y el canal de comunicación para detenerlo.")
d.heading("5.2 Montaje e instrumentación", 2)
d.table([
    ["Elemento", "Criterio propuesto", "Por qué"],
    ["Colocación de la IMU", "En el canal, en el punto más cercano al apoyo de hombro, con el eje z alineado con el eje longitudinal del canal",
     "El punto de mayor desplazamiento y el de menor curvatura de la IMU dan información complementaria"],
    ["Fijación", "Soporte rígido y contínuo, sin cinta ni espuma intermedias; registering con fotos de la montaje",
     "Una IMU mal fijada mide el movimiento del soporte, no el del cuerpo"],
    ["Segunda IMU", "En el punto de la bomba o del yugo, si hay sensor disponible",
     "Permite estimar el movimiento relativo, que es el que se compara con la predicción"],
    ["Instrumentación de fuerza", "Una celda de carga en la correa de carga, si el laboratorio dispone",
     "Sin ella no hay cadena cerrada entre la IMU y las fuerzas de las correas"],
    ["Sincronización", "Un evento común visible por todas las instrumentaciones (golpe controlado o led) para medir el desfase",
     "Sin sincronización, la comparación predicción-ensayo no es interpretable"],
    ["Frecuencia y duración", "Propuesta: muestreo efectivo ≥ 100 Hz y ≥ 60 s por repetición, con la tasa real registrada",
     "Cubre el contenido de frecuencia del movimiento esperado en banco; la tasa real puede ser menor que la nominal y hay que registrarla"],
    ["Repeticiones", "Propuesta: 5 repeticiones por condición, más 3 de control sin carga",
     "Permite estimar repetibilidad y detectar deriva o changement de montaje entre repeticiones"],
], widths=[1800, 3500, 3200])

d.heading("5.3 Secuencia de un ensayo", 2)
for i, paso in enumerate([
    "Registro de la configuración y del estado del prototipo antes de cargar.",
    "Colocación del lastre en incrementos definidos por el profesor; en cada incremento, espera de estabilización y registro.",
    "Registro continuo de todas las instrumentaciones, con la marca del evento de sincronización.",
    "Medición de la holgura axial del casquillo y del estado de las uniones antes y después del ensayo, con comparador.",
    "Descenso controlado del lastre y registro del comportamiento de retorno (histeresis o juego).",
    "Registro de cualquier evento: deformación permanente, marca de desgarro, deslizamiento, pérdida de precarga, giro del pasador o ruidos.",
    "Cierre: fotografías, hoja de registro firmada y copia de los datos crudos con su carpeta de origen.",
]):
    d.bullet("%d. %s" % (i + 1, paso))

d.heading("5.4 Criterios de interrupción", 2)
d.bullet("Deformación permanente visible o marca de desgarro en cualquier pieza, union o cinta.")
d.bullet("Aumento medible de la holgura axial del casquillo o giro del pasador en una unión.")
d.bullet("Pérdida de precarga perceptible o aflojamiento de una unión durante la carga.")
d.bullet("Cualquier señal de fallo en la instrumentación o pérdida de sincronización: el registro no es válido y se repite.")
d.bullet("Alcanzar el límite de carga definido por el profesor: se detiene, se registra y no se repite sin revisión.")
d.heading("5.5 Personas, consentimiento y datos", 2)
d.bullet("Los ensayos con personas solo se realizan después del piloto y de la revisión del profesor, con autorización escrita, con consentimiento informado y con la posibilidad de detenerse en cualquier momento sin explicación.")
d.bullet("Los datos de las personas son sensibles: se almacenan de forma pseudonimizada, con la clave de identificación separada de los datos, y no se publican sin autorización expresa.")
d.bullet("El proyecto tiene una regla vigente: no introducir datos personales de terceros ni información confidencial en herramientas de IA. Los datos antropométricos de usuarios no se procesan con modelos externos.")
d.bullet("Ninguna medición aislada declara validación ergonómica, clínica o normativa. Esas declaraciones requieren un protocolo y un análisis que no forman parte de este paquete.")
d.page_break()

# ============================================================ 6. MATRIZ DE VARIABLES
d.heading("6. Matriz de variables y datos pendientes", 1)
d.para("En pocas palabras: es la lista de números que el cálculo necesita. Cada fila dice si ese número ya existe (y de dónde sale) o si hay que medirlo, y quién lo va a medir. Los símbolos que todavía no existen no están escritos en la memoria de cálculo: si alguien los usa sin definirlos, el programa los marca como error en lugar de inventarles un valor.")
d.para("La planilla (hoja 02_Variables) contiene la matriz completa con símbolo, unidad SI, fuente, método "
       "de obtención, incertidumbre, estado, cálculo que la usa y ensayo que la produce. Se reproduce aquí "
       "el núcleo: las variables que gobiernan el resultado y las que bloquean el cierre.")
d.table([
    ["ID", "Variable", "Unidad", "Valor actual", "Estado", "Fuente", "Qué falta"],
    ["V001", "B, ancho del canal", "mm", "32", "ANTECEDENTE", "PARAMETROS_P2_05.json", "Medición en 5 canales"],
    ["V002", "t, espesor de pared", "mm", "3 (mín. de cálculo 2,8)", "ANTECEDENTE", "PARAMETROS_P2_05.json", "Micrómetro en 5 puntos por canal"],
    ["V003", "L_casq, longitud del casquillo", "mm", "26 (= B − 2t)", "ANTECEDENTE", "Generador vigente", "Medir 8 casquillos"],
    ["V004", "g_ax, holgura axial", "mm", "0,000", "CALCULADO", "Esta memoria", "Decidir tras la cadena de tolerancias"],
    ["V006", "m_bomba_vacia", "kg", "—", "PENDIENTE", "Sin dato", "Báscula, 3 repeticiones"],
    ["V007", "m_bomba_llena", "kg", "—", "PENDIENTE", "Sin dato", "Báscula, 3 repeticiones"],
    ["V008", "z_cg_bomba", "mm", "—", "PENDIENTE", "Sin dato", "Paradoja de medición"],
    ["V009", "m_arnes", "kg", "—", "PENDIENTE", "Sin dato", "Báscula"],
    ["V010", "ancho_cinta", "mm", "50", "SUPUESTO", "PARAMETROS_P2_05.json", "Medir"],
    ["V011", "esp_cinta", "mm", "1,5", "SUPUESTO", "PARAMETROS_P2_05.json", "Medir"],
    ["V012", "rigidez_correa", "N/mm", "—", "PENDIENTE", "Sin dato", "Ensayo de tracción"],
    ["V013", "apoyo_hombro_y", "mm", "435", "HIPÓTESIS", "PARAMETROS_P2_05.json", "Marcar con carga"],
    ["V016", "m_total", "kg", "25", "HIPÓTESIS", "PARAMETROS_P2_05.json", "Suma medida de equipo y carga"],
    ["V017", "fv / V018 fh", "—", "3 / 1", "HIPÓTESIS", "PARAMETROS_P2_05.json", "Justificar con el profesor"],
    ["V019", "frac, reparto por lado", "—", "0,7", "HIPÓTESIS", "PARAMETROS_P2_05.json", "Deducir de la medición de apoyos"],
    ["V020", "excentricidad", "mm", "107,5", "HIPÓTESIS", "PARAMETROS_P2_05.json", "Distancia medida al centro de masa"],
    ["V021", "precarga", "N", "2000", "HIPÓTESIS", "PARAMETROS_P2_05.json", "Definir con par de montaje"],
    ["V024", "masa_CAD", "kg", "1,442328", "MEDIDO en CAD", "BOM_Y_MASAS.csv", "Regenerar si cambia el CAD"],
    ["V025", "masa_presupuesto", "kg", "2,212328", "CALCULADO", "Esta memoria", "Recalcular con masas medidas"],
    ["V027", "par_apriete", "N·m", "—", "PENDIENTE", "Sin dato", "Acordar y documentar"],
    ["V029", "zonas de contacto A/B/C", "—", "—", "PENDIENTE", "D-12", "Acordar criterios"],
    ["V030", "frecuencia propia", "Hz", "—", "PENDIENTE", "No calculada", "Ensayo de impacto"],
], widths=[500, 1500, 700, 1400, 1100, 1700, 2000], font_size=7)

d.page_break()

# ============================================================ 7. MEMORIA DE CÁLCULO
d.heading("7. Estructura y fundamentos de la memoria de cálculo", 1)
d.para("En pocas palabras: aquí se explica de dónde sale cada número de la memoria: qué cargas se suponen, cómo se reparten, cómo se calcula la resistencia de cada pieza y qué margen queda. La memoria no inventa nada: reproduce el cálculo del proyecto con la geometría vigente y deja las entradas editables para poder recalcularlo cuando lleguen las mediciones.")
d.para("El motor de cálculo es Mathcad 15, con el archivo Memoria_SEDAC_P204_MC01_EDITABLE.xmcd de este "
       "paquete. Excel registra y sigue; no recalcula resistencia. Así hay una sola fuente de verdad para "
       "cada resultado.")

d.heading("7.1 Diagrama de cuerpo libre y trayectoria de cargas", 2)
d.para("El sistema se modela como una barra vertical de longitud L entre dos apoyos: el apoyo de hombro "
       "en y = 435 mm y el apoyo de cinturón en y = 55 mm, de modo que L = 380 mm. La carga de la bomba "
       "llega al esqueleto por la interfaz lumbar y por los yugos; los apoyos reaccionan hacia el cuerpo; "
       "las correas transmiten entre esos apoyos y el arnés.")
d.bullet("Trayectoria de carga: bomba → interfaz lumbar y yugos → canales → apoyos de hombro y cinturón → correas → arnés → cuerpo.")
d.bullet("Reacción de apoyo: en cada apoyo, la fuerza vertical e el momento por excentricidad de la carga; el canal trabaja como barra simplemente apoyada entre dos apoyos ideales.")
d.bullet("En las uniones: cortante por reacción entre apoyos y tracción por el momento, más la precarga del M5; el pasador transmite cortante y el M5 aporta apriete y retención. La función del casquillo es de tope de compresión: evita que las alas se aplasten al apretar.")
d.bullet("En las correas: la tracción de la correa de carga y la del anclaje del arnés se obtienen de la componente vertical del lado cargado y del ángulo de eslinga, con la excentricidad como fuente del momento.")
d.para("Advertencia de simplificación: el modelo supone apoyos ideales efectivos y contacto ideal. No "
       "representa la rigidez real del arnés, ni la deformación de las cintas, ni la abrasión, ni el "
       "comportamiento dinámico. Esa limitación es la razón de medir antes de decidir.", size=10)

d.heading("7.2 Casos de carga", 2)
d.table([
    ["Caso", "Definición", "Cálculo", "Estado"],
    ["Fuerza vertical total", "Fv = m_total · g · fv", "25 kg × 9,81 m/s² × 3 = 735,75 N", "CALCULADO sobre hipótesis"],
    ["Fuerza horizontal total", "Fh = m_total · g · fh", "25 kg × 9,81 m/s² × 1 = 245,25 N", "CALCULADO sobre hipótesis"],
    ["Componente del lado más cargado", "N = Fv · frac; Q = Fh · frac", "N = 515,03 N; Q = 171,67 N", "CALCULADO sobre hipótesis"],
    ["Momento por excentricidad", "M0 = N · e", "55 365,2 N·mm", "CALCULADO sobre hipótesis"],
    ["Envolvente de momento", "M(x) = M0 · máx(1 − x/L, x/L) + Q · x · (L − x)/L",
     "Mmax = 55 738,6 N·mm en x = 28,975 mm", "CALCULADO"],
    ["Momento flector lateral idealizado", "mlat = Q · L / 4", "16 309 N·mm", "CALCULADO sobre hipótesis"],
    ["Precarga de unión", "f0 = 2000 N con dispersión del 25 %", "f_b = 2804,44 N", "HIPÓTESIS"],
    ["Carga dinámica", "No modelada. La variación temporal de la carga entra como factor 3 g / 1 g, no como historia de tiempo",
     "—", "PENDIENTE: el factor dinámico no es una historia de carga",
     ],
], widths=[1800, 2600, 2400, 2100])
d.para("La envolvente reúne casos alternativos: un momento único aplicado alternativamente en un extremo "
       "o en el otro, y una fuerza horizontal de posición variable a lo largo de la luz. No es un único "
       "diagrama de cargas simultáneas, y así queda declarado en la memoria.", size=10)

d.heading("7.3 Masa y centro de masa, y el efecto del contenido de la bomba", 2)
d.bullet("Masa rígida y protectores: 1,442328 kg, medida en Inventor sobre la entrega P2.04 (MEDIDO en CAD).")
d.bullet("Reservas: 0,65 kg de textiles y 0,12 kg de reserva adicional, que son reservas presupuestarias y no geometría.")
d.bullet("Presupuesto del sistema sin bomba ni agua: 2,212328 kg. Brecha hasta el objetivo de 2,0 kg: 0,212328 kg, es decir el 14,7 % de la masa rígida.")
d.bullet("La bomba no está en ese presupuesto: su masa y su centro de masa son las variables V006 a V008, hoy PENDIENTE. Cuando se incorporen, la excentricidad y la posición de la resultante cambian y con ellas M0, la flecha y la tensión del canal.")
d.bullet("Los 25 kg del caso de carga son una hipótesis de carga y no la masa de la estructura: no deben sumarse a la masa del CAD.")

d.heading("7.4 Resultados del cribado vigente reproducido en la memoria", 2)
d.para("La memoria nueva reproduce el cribado vigente del repositorio con error relativo máximo de 8·10⁻¹⁶ "
       "en las quince verificaciones y en once magnitudes: no es una reinterpretación, es la misma "
       "aritmética, ahora con entradas editables y con las verificaciones dimensionales de Mathcad.")
d.table([
    ["Verificación", "Margen n", "Cumple", "Observación"],
    ["Refuerzo combinado, pared mínima", "2,2471", "Sí", "Gobierna el caso base por fluencia bajo tensión combinada"],
    ["Comprobación local limitada por fluencia", "2,2471", "Sí", "min(240; 477,70) MPa = 240 MPa: empata con el combinado por fluencia; no gobierna el pandeo elástico"],
    ["Taladro en alas, tensión local", "2,7599", "Sí", "Cribado K = 3, no acreditación de fatiga"],
    ["M5, combinación de precarga y servicio", "2,5512", "Sí", "Precarga dispersa 25 % y palanca 1,5"],
    ["Arandela, presión bajo tuerca", "2,2584", "Sí", "No verifica roscas ni prueba de tuerca"],
    ["Arandela, flexión local", "2,2839", "Sí", "Cribado de anillo en voladizo"],
    ["Puente de anclaje arnés/cinturón", "2,3588", "Sí", "Reparto de cargas no medido"],
    ["Pasador hueco, flexión y cortante", "2,9692", "Sí", "Holguras por verificar"],
    ["Casquillo, compresión", "3,5942", "Sí", "Tolerancias ±0,1 mm exploradas en diámetro, no en longitud"],
    ["Aplastamiento de ala y de mejilla por pasador", "6,3543", "Sí", "Se admite una sola superficie efectiva"],
    ["Arrancamiento del ala", "5,1108", "Sí", "Dos ligamentos"],
    ["Pandeo Euler, eje débil", "108,58", "Sí", "Modelo ideal articulado"],
    ["Pandeo lateral torsional ideal", "26,61", "Sí", "Sin crédito de alabeo"],
    ["Puente inferior de cuna", "3,6982", "Sí", "Carga completa del lado"],
], widths=[3200, 1200, 1000, 3500])
d.para("Además: flecha de la envolvente 0,8667 mm (límite 5 mm), giro torsional ideal 3,176°, cierre residual "
       "de junta 282,2 N, cortante de unión 1046,98 N, tracción externa de unión 1522,22 N y fuerza máxima "
       "de perno 2804,44 N.")

d.para("SUPUESTOS heredados para el pasador: pin_od_eff = 10 − 0,1 = 9,9 mm y pin_id_eff = 5,6 mm. Proceden de calcular_p2_05.py, líneas 63 y 71, en 01_CAD/Prototipo_P2/P2_05_20261019/Soporte/. Se conservan para reproducir el cribado. No son mediciones ni tolerancias de fabricación aprobadas; deben revisarse con el proceso y las dimensiones reales. El taladro de 10,2 mm es una cota distinta y no sustituye al diámetro del pasador en estas expresiones.", size=10)

d.heading("7.5 Sensibilidad a los parámetros inciertos", 2)
d.para("La sensibilidad se calculó variando la profundidad del canal con el resto de entradas del caso "
       "base y con pared mínima de 2,8 mm. No son los casos OPT1 del repositorio, que usaban pared de "
       "2,5 mm: se mantienen separados para no confundirlos.")
d.table([
    ["Profundidad D", "Área (mm²)", "Inercia (mm⁴)", "σ_vm (MPa)", "σ de pandeo local (MPa)", "n del caso"],
    ["24 mm (base P2.04)", "208,32", "11 858", "106,80", "477,70", "2,2471"],
    ["26 mm", "219,52", "14 848", "92,80", "398,89", "2,5861"],
    ["28 mm", "230,72", "18 268", "81,63", "338,08", "2,9403"],
], widths=[2000, 1400, 1600, 1400, 2000, 1200])
d.bullet("Lectura: en estos casos de sensibilidad, aumentar D reduce la tensión combinada pero también reduce la tensión crítica elástica local del ala. El margen local calculado puede aumentar porque cambia la demanda; no implica que mejore la resistencia elástica al pandeo. La masa de mejillas y el reparto real deben reevaluarse.")
d.bullet("El caso base cumple el umbral con margen estrecho (2,2471 frente a 2,2): cualquier reducción de pared o de sección puede llevarla por debajo. El margen es pequeño, no cómodo.")
d.bullet("La sensibilidad a los factores de carga, al reparto 70/30, a la excentricidad y a la precarga no se recorre aquí con números, porque esos cuatro son hipótesis: barrer hipótesis no informa. Se hará cuando existan mediciones (etapa E8).")

d.heading("7.6 Materiales, uniones y factores de seguridad", 2)
d.bullet("Material del canal y uniones: 6061-T6 con E = 69 000 MPa, Sy = 240 MPa y densidad 2,70 g/cm³, todos como mínimos de prediseño condicionados al material real. La masa del constructor se valida contra volumen × densidad, así que la coherencia masa-geometría está garantizada en el modelo.")
d.bullet("Fijaciones: acero A2-80 como hipótesis, densidad 8,0 g/cm³; arandela con Sy mínimo exigido de 200 MPa. La tuerca autofrenante exige prueba de carga y par prevalente compatibles: no está verificada.")
d.bullet("Textiles y espuma: sin crédito estructural y con masa de referencia solo visual; el papel del arnés lo cubre la reserva de 0,65 kg, que no es geometría.")
d.bullet("Factores de seguridad: el cribado usa Sy/E del material declarado, coeficientes de borde 1,25, ventana 3 y cribado de taladro 3, y un factor de palanca 1,5 en las reacciones. Todos son criterios de prediseño sin respaldo normativo, y así quedan declarados.")

d.heading("7.7 Del cálculo a la decisión: qué falta para cerrar", 2)
d.table([
    ["Modo o verificación", "Hoy", "Qué lo cerraría"],
    ["Pandeo local de alas", "n = 2,2471 sobre hipótesis", "Geometría real (D, t), cargas medidas y, si el margen sigue justo, FEA de detalle"],
    ["Reparto por lado 70/30", "Hipótesis", "Medición de los apoyos reales y del centro de masa de la bomba"],
    ["Excentricidad 107,5 mm", "Hipótesis", "Distancia medida entre el eje del canal y el centro de masa de la bomba llena"],
    ["Precarga 2000 N", "Hipótesis", "Par de apriete definido y prueba de la tuerca autofrenante"],
    ["Holgura axial 0,000 mm", "Calculado", "Medición de B, t y longitud de casquillo; decisión sobre g_ax o ajuste a la dimensión real"],
    ["Fatiga", "No evaluada", "Historia de carga medida y conteo de ciclos"],
    ["Pandeo distorsional", "No evaluado", "Geometría con ranuras y FEA"],
    ["Comportamiento de las correas", "No evaluado", "Medición de rigidez y de la fuerza en la correa en ensayo"],
], widths=[2200, 2400, 4300])

d.page_break()

# ============================================================ 8. AUDITORÍA DE LA MEMORIA ANTERIOR
d.heading("8. Auditoría de la memoria de cálculo anterior (P2.03 MC02)", 1)
d.para("En pocas palabras: la memoria de cálculo que existía era de otra versión del prototipo (P2.03, con rieles de 50 × 40 mm y marco X M6). Se revisó para quedarse con su método y su formato, y se descartó todo lo numérico, porque corresponde a otra geometría y a otras cargas.")
d.para("La memoria anterior es un archivo XMCD de Mathcad 14.1 con 247 variables y 45 páginas lógicas, "
       "referida a la arquitectura de doble riel 50 × 40 × 1,5 mm con marco X M6: una geometría que ya no "
       "es la vigente. Se auditó leyéndola, no reejecutándola: no se abrió su constructor ni se "
       "recalculó, de modo que sus valores numéricos no se transfieren.")
d.table([
    ["Elemento de la memoria anterior", "Veredicto", "Justificación"],
    ["Estructura de la hoja: entradas editable, salidas con unidades, verificaciones dimensionales",
     "REUTILIZABLE", "Es la estructura que exige el proyecto y la que se reprodujo en la memoria nueva"],
    ["Convención de unidades (mm, N, MPa) y verificaciones de dimensionalidad",
     "REUTILIZABLE", "La memoria nueva trabaja en las mismas unidades y comprueba N, MPa y mm² explícitamente"],
    ["Método de envolvente de momento con momento alternado y fuerza horizontal de posición variable",
     "REUTILIZABLE CON ADAPTACIÓN", "El método es válido; los brazos y la excentricidad son los de P2.03 y hay que sustituirlos por los de P2.04"],
    ["Cribado de 15 verificaciones con su fórmula y su texto de modelo",
     "REUTILIZABLE CON ADAPTACIÓN", "Las fórmulas son las mismas; cambian los coeficientes de sección y la geometría de las piezas"],
    ["Formato XMCD y apertura con la instalación Mathcad de este equipo",
     "REUTILIZABLE", "Se comprobó: la instalación Mathcad 15 se identifica como 14.1.4.587 y abre y recalcula el formato"],
    ["Geometría de rieles 50 × 40 × 1,5, travesaños, diagonales, marco X M6",
     "DESCARTADO", "Corresponde a P2.03, ya superada por P2.04"],
    ["Cargas, brazos y excentricidades de P2.03",
     "DESCARTADO", "Son hipótesis de otro prototipo; se conservan como hipótesis, no como resultados"],
    ["Resultados numéricos y márgenes publicados de P2.03 (n mínimo 2,254)",
     "DESCARTADO", "Corresponden a otra geometría y otro modelo de carga; no son comparables"],
    ["Masa de 2,333 kg y presupuesto 2,913 kg de P2.03",
     "DESCARTADO", "Historia; el valor vigente es 1,442328 kg medido en P2.04"],
    ["Guía en PDF con teoría y referencias a páginas de la hoja",
     "REUTILIZABLE COMO REFERENCIA", "Buena práctica de presentación; el contenido hay que rehacerlo para el prototipo vigente"],
], widths=[3000, 1500, 4400])
d.para("Conclusión de la auditoría: de la memoria anterior se conserva el método y el formato, y se "
       "descarta todo lo numérico. La memoria de este paquete es una hoja nueva sobre la geometría "
       "vigente, no una edición de la anterior.")

d.page_break()

# ============================================================ 9. MATERIALES
d.heading("9. Comparación de materiales y procesos de fabricación", 1)
d.para("En pocas palabras: el aluminio 6061 es el material de la estructura porque combina poca masa con buena rigidez y se puede mecanizar; el HDPE sirve solo de cubierta; el acero, solo para la tornillería; y el textil, para el contacto con el cuerpo. Los pesos de la tabla son propuestas para revisar, no criterios.")
d.para("Los pesos de la matriz son propuestas revisables, no criterios. La comparación se hace sobre las "
       "propiedades que gobiernan el comportamiento del conjunto: densidad (masa que se porta), módulo y "
       "límite elástico (rigidez y resistencia), fabricabilidad (proceso viable en el taller o en "
       "mecanizado), disponibilidad y contacto con el usuario cuando la pieza toca el cuerpo.")
d.table([
    ["Criterio", "Peso propuesto", "6061-T6 mecanizado o extrusión", "6061-T6 fundido", "HDPE", "Acero (fijaciones)", "PLA (maqueta)"],
    ["Densidad (g/cm³)", "Alto", "2,70", "2,70", "0,953", "8,0", "1,24"],
    ["Módulo E (GPa)", "Alto", "69", "69", "— (sin crédito)", "193–210", "3,5"],
    ["Límite elástico Sy (MPa)", "Muy alto", "240 (mínimo de prediseño)", "240", "—", "600 (A2-80, hipótesis)", "50"],
    ["Fabricabilidad", "Alto", "Mecanizado CNC o extrusión con certification", "Molde y coste alto", "Lámina cortada y perforada", "Comprado", "Impresión 3D"],
    ["Uniones y montaje", "Alto", "Atornillado, sin soldadura creditada", "Atornillado", "Remaches o tornillos", "Atornillado", "Atornillado"],
    ["Contacto con el usuario", "Medio", "No toca el cuerpo directamente", "No toca el cuerpo", "Toca el cuerpo", "No", "No"],
    ["Temperatura de servicio", "Medio", "Adecuado con acolchado", "Adecuado", "Adecuado", "Adecuado", "Insuficiente"],
    ["Disponibilidad", "Alto", "Local, por confirmar", "Baja", "Local", "Alta", "Propia"],
    ["Costo", "Medio", "Por cotizar", "Alto", "Bajo", "Bajo", "Muy bajo"],
    ["Veredicto provisional", "", "Opción vigente", "Descartada por costo y proceso", "Solo espaldera", "Solo fijaciones", "Solo ajuste de encaje"],
], widths=[1800, 1100, 1700, 1500, 1300, 1400, 1200], font_size=7)
d.para("Dos observaciones de coherencia con el repositorio: el constructor del CAD ya crea materiales con "
       "la densidad del JSON y rechaza la pieza si la masa nativa no coincide con volumen × densidad, de "
       "modo que la coherencia entre geometría y masa está garantizada en el modelo; y la ficha del "
       "proyecto prohíbe la soldadura creditada y el doblado severo, lo que deja el mecanizado y la "
       "extrusión certificada como únicas vías para la estructura.", size=10)

d.page_break()

# ============================================================ 10. SENSORES
d.heading("10. Selección justificada de sensores e instrumentación", 1)
d.para("En palabras sencillas: primero se decide qué hay que medir y para qué decisión sirve cada medición, y solo después se elige el sensor. La IMU mide movimiento, no fuerza: por eso se pregunta si el laboratorio tiene una celda de carga, porque sin ella no se puede cerrar la cadena de cargas de las correas.")
d.heading("10.1 Qué queremos medir y para qué decisión", 2)
d.para("La pregunta experimental se define antes del sensor. Si no, se elige el instrumento disponible y "
       "luego se busca una pregunta que encaje con él, que es el error que este plan debe evitar.")
d.table([
    ["ID", "Pregunta experimental", "Magnitud que la responde", "Decisión de diseño que depende de ella"],
    ["Q1", "¿El esqueleto se deflecta más de lo previsto en la zona de la bomba?", "Aceleración lineal y velocidad angular en el canal", "Si la flecha real supera la predicción, revisar sección, unión o apoyo"],
    ["Q2", "¿La bomba y el esqueleto se mueven de forma acoplada?", "Aceleración relativa entre la IMU del canal y la de la bomba", "Si el acoplamiento es alto, la interfaz lumbar tiene que absorber más"],
    ["Q3", "¿El reparto entre correas es el supuesto?", "Fuerza en la correa de carga", "Si el reparto real difiere del 70/30, cambia el cálculo de anclajes y de puente de cuna"],
    ["Q4", "¿El conjunto tiene una frecuencia propia que excite resonancia?", "Frecuencia propia por excitación conocida", "Si la frecuencia propia cae en la banda de la marcha, hay que cambiar rigidez o masa"],
    ["Q5", "¿El usuario puede liberarse del equipo con guantes?", "Tiempo y fuerza de desenganche, acceso físico", "Geometría de apertura y de la interfaz lumbar"],
], widths=[500, 3200, 2600, 2600])

d.heading("10.2 Qué mide una IMU y qué no", 2)
d.bullet("La IMU mide aceleración lineal y velocidad angular. No mide fuerza, ni tensión, ni par, ni desplazamiento directo.")
d.bullet("Convertir aceleración en fuerza exige un modelo dinámico con masa, rigidez y amortiguamiento, y sus condiciones de validez: sin ese modelo no hay fuerza, hay una magnitud mal rotulada. Es el error más probable de este trabajo y por eso la planilla separa el dato bruto del procesado.")
d.bullet("Limitaciones que deben documentarse en el postproceso: orientación respecto de la gravedad (un error de 5° en la instalación introduce un sesgo del orden de g · sen 5°), deriva del giroscopio (crece con el tiempo, comparable a la señal en reposo), doble integración del acelerómetro (el error crece con el cuadrado del tiempo) y perturbación magnética (afecta al magnetómetro y, con él, a la estimación de orientación).")
d.bullet("Consecuencia práctica: la IMU es un sensor de movimiento relativo. Sirve para comparar el comportamiento medido con el predicho y para detectar modos; no reemplaza la celda de carga.")
d.heading("10.3 ¿Hace falta instrumentación adicional?", 2)
d.para("Sí, y es la recomendación central de este apartado: para cerrar la cadena de cargas de las "
       "correas (pregunta Q3) hace falta al menos un canal de fuerza, con celda de carga o dinamómetro, en "
       "la correa de carga. Sin él, la IMU mide movimiento sin fuerza asociada y la comparación con la "
       "predicción se queda en el plano cualitativo. La alternativa —un modelo dinámico con masa y "
       "rigidez medidas— es posible, pero solo para modos bien identificados y exige la calibración del "
       "modelo que hoy no existe.")
d.heading("10.4 Comparación de candidatas", 2)
d.para("El laboratorio no ha sido inventariado todavía, así que la comparación se deja con los criterios "
       "completos y las candidatas sin datos, lista para completar en la visita. Se prioriza lo que ya "
       "esté en el laboratorio; el costo se usa solo como criterio de desempate entre equipos "
       "disponibles, no como razón principal de compra.")
d.table([
    ["Criterio", "Qué se compara", "Por qué pesa", "Cómo se verifica en la visita"],
    ["Magnitudes", "Aceleración 3 ejes, giro 3 ejes, magnetómetro", "Si no hay magnetómetro, la estimación de orientación depende del filtro", "Ficha del modelo"],
    ["Rango", "Rango del acelerómetro y del giroscopio", "Rango insuficiente satura y produce una señal plausible pero falsa", "Ficha del modelo"],
    ["Ruido y resolución", "Ruido en la banda de interés", "El ruido integrado es la fuente principal de deriva", "Ruido en reposo registrado"],
    ["Frecuencia real de muestreo", "Tasa efectiva del software, no la del sensor", "Una tasa efectiva de 50 Hz no sirve para contenido de 60 Hz", "Registro de la tasa con el software"],
    ["Sincronización", "Desfase entre IMU y DAQ de fuerza", "Sin esto no hay comparación interpretable", "Evento común medido"],
    ["Registro", "Formato bruto con metadatos y marca de tiempo", "Un CSV sin metadatos no es auditable", "Exportación de prueba"],
    ["Autonomía", "Duración de batería frente al ensayo", "Un ensayo de 60 s con 5 repeticiones necesita margen", "Hoja de datos"],
    ["Montaje", "Rigididad del soporte y facilidad de fijación", "Una IMU con base flexible mide el soporte", "Prueba de fijación"],
    ["Compatibilidad", "Software de registro y de postproceso, y exportación", "Sin postproceso no hay correction de sesgos", "Instalación de prueba"],
    ["Costo", "Precio o disponibilidad", "Solo desempate", "Cotización si se decide comprar"],
], widths=[1600, 2400, 2900, 2000], font_size=7)
d.table([
    ["ID", "Candidata", "Origen", "Magnitudes", "Rango", "Ruido", "Muestreo", "Sincronización", "Registro", "Autonomía", "Montaje", "Costo", "Estado"],
    ["S01", "Equipo IMU del laboratorio", "Inventario pendiente", "", "", "", "", "", "", "", "", "", "PENDIENTE"],
    ["S02", "Celda de carga o dinamómetro de correa", "Laboratorio o alquiler", "", "", "", "", "", "", "", "", "", "PENDIENTE"],
    ["S03", "Referencia angular para calibración", "Laboratorio", "", "", "", "", "", "", "", "", "", "PENDIENTE"],
    ["S04", "Sistema de video para sincronización", "Laboratorio", "", "", "", "", "", "", "", "", "", "PENDIENTE"],
], widths=[400, 1500, 1200, 700, 500, 500, 700, 700, 600, 600, 600, 500, 800], font_size=7)

d.page_break()

# ============================================================ 11. PRESUPUESTO
d.heading("11. Presupuesto y cotizaciones", 1)
d.para("En pocas palabras: la tabla de cotizaciones quedó preparada y vacía. No se consultaron proveedores en esta tarea, y no se rellenó con precios inventados: la estructura exige proveedor, fecha, moneda, impuestos, despacho y disponibilidad, y se distingue una cotización formal de un precio de lista o de una estimación interna.")
d.para("No se han realizado compras ni consultas de precio en este paquete: no hay acceso verificado a "
       "fuentes de proveedores en este momento. La tabla de cotizaciones queda preparada, con la "
       "estructura completa que exige el registro, y cada línea marcada como PENDIENTE DE COTIZAR. "
       "Completarla exige distinguir tres cosas distintas: cotización formal, precio publicado y "
       "estimación interna; solo la primera obliga.")
d.table([
    ["ID", "Ítem", "Especificación", "Proveedor", "Fecha", "Moneda", "Cant.", "Impuestos", "Despacho", "Disponibilidad", "Tipo de dato", "Estado"],
    ["C01", "Plancha de aluminio 6061 T6", "32 × 24 × 3 mm", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C02", "Barra de aluminio 6061", "Para pasadores y casquillos", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C03", "Lámina de HDPE 1 mm", "Panel 270 × 472 mm", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C04", "Tornillo M5×55 ISO 4762", "Cabeza Ø8,5 × 5, acero A2-80", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C05", "Tuerca M5 autofrenante", "Envolvente DIN 980", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C06", "Arandela M5 5,3 × 16 × 3", "Envolvente GN 6341", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C07", "Cinta de polipropileno 50 mm", "Ancho 50 mm, espesor por medir", "Por consultar en Chile", "", "CLP", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C08", "Sensores IMU", "Por definir en A11", "Laboratorio o proveedor", "", "", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
    ["C09", "Instrumentación de fuerza", "Por definir en A11", "Laboratorio o alquiler", "", "", "", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"],
], widths=[400, 1500, 1700, 1200, 700, 600, 500, 800, 800, 900, 1300, 900], font_size=7)
d.para("Reglas de registro, ya incorporadas en la planilla: una cotización formal exige proveedor "
       "identificado, fecha, moneda, cantidad, especificación, impuestos, despacho y disponibilidad "
       "declarada; un precio publicado se marca como PRECIO PUBLICADO y no como cotización; una "
       "estimación interna se marca como ESTIMACIÓN y no se usa para decidir compras. El precio de las "
       "piezas ya dibujadas no es una partida del proyecto: el prototipo no se fabrica, y el presupuesto "
       "de masa no es un presupuesto de dinero.", size=10)

d.page_break()

# ============================================================ 12. MATRIZ DE DECISIÓN
d.heading("12. Matriz de actualización posterior del diseño", 1)
d.para("En palabras sencillas: cada resultado que salga de un ensayo se enlaza con lo que se podría hacer después: dejar el diseño como está, revisar la geometría, cambiar la sección, el material, la unión, la correa o el montaje. Son propuestas condicionadas a la evidencia; en esta tarea no se ejecuta ningún cambio de diseño.")
d.para("Cada resultado del proyecto se enlaza con la acción que podríavaldo, condicionada a la evidencia "
       "que la respalde. En esta tarea no se ejecuta ningún cambio de diseño: esta matriz es la que se "
       "usará después de los ensayos.")
d.table([
    ["ID", "Resultado que lo dispara", "Evidencia que lo respalda", "Acción posible (condicionada)"],
    ["T01", "Flecha medida en el apoyo de hombro", "Diferencia y repetibilidad frente a la predicción de 0,8667 mm",
     "Si la flecha supera el límite acordado: conservar / revisar geometría (D, t) / revisar unión / cambiar material"],
    ["T02", "Desplazamiento por masa de la bomba", "Medición de masa y centro de masa más ensayo",
     "Si es mayor que lo previsto: conservar / revisar interfaz lumbar / revisar apoyo / cambiar distribución de masa"],
    ["T03", "Giro del conjunto", "Comparación con los 3,176° predichos",
     "Si excede: conservar / aumentar rigidez torsional (sección o uniones) / revisar correa"],
    ["T04", "Desplazamiento lateral", "Ensayo con carga lateral",
     "Si excede: conservar / revisar arriostramiento / revisar unión"],
    ["T05", "Desplazamiento local de la cuna", "Ensayo de la cuna",
     "Si excede: conservar / revisar espesor o puente / cambiar la solución textil"],
    ["T06", "Frecuencia propia medida", "Ensayo de excitación conocida",
     "Si cae en la banda de excitación de la marcha: conservar / cambiar masa o rigidez / modificar el uso"],
    ["T07", "Holgura axial del casquillo tras apriete", "Medición con comparador antes y después",
     "Si hay juego: conservar / introducir g_ax / ajustar el casquillo a la dimensión real / cambiar el proceso del canal"],
    ["T08", "Fuerza medida en la correa", "Celda de carga en la correa de carga",
     "Si el reparto difiere del supuesto: conservar / cambiar reparto de correas / cambiar longitud de correa / revisar anclaje"],
    ["V002", "Espesor real medido", "Micrómetro en 5 puntos por canal",
     "Si t < 2,8 mm: conservar / rehacer el cribado con el valor medido / ajustar el proceso de suministro"],
    ["V003", "Longitud real de casquillo", "Medición de 8 casquillos",
     "Si L_casq > W: conservar / corregir la longitud / redefinir el ajuste de fabricación"],
    ["V022", "Propiedades certificadas del material", "Certificado del proveedor o ensayo",
     "Si Sy < 240 MPa: conservar / cambiar material / aumentar sección"],
    ["V027", "Par de apriete y comportamiento de la tuerca", "Par medido y prueba de la tuerca",
     "Si hay aflojamiento: conservar / cambiar de tuerca / cambiar el método de apriete / añadir seguro mecánico"],
], widths=[500, 2300, 2800, 3300])

d.page_break()

# ============================================================ 13. RIESGOS
d.heading("13. Riesgos, limitaciones, decisiones pendientes y próximos pasos", 1)
d.para("En pocas palabras: qué puede salir mal, qué no se hizo todavía, qué decisiones quedan abiertas y por dónde conviene empezar. Lo más importante: el riesgo mayor es que las hipótesis de carga sobrevivan a las mediciones, y la forma más barata de evitarlo es medir antes de decidir.")
d.heading("13.1 Riesgos", 2)
d.table([
    ["ID", "Riesgo", "Origen", "Impacto", "Mitigación"],
    ["RK1", "Que las hipótesis de carga sobrevivan a las mediciones", "El modelo completo está construido sobre 25 kg, 3 g, 1 g, 70/30, e = 107,5 mm y 2000 N",
     "Alta: todos los márgenes se mueven", "Medir antes de decidir (etapa E1 y E2) y reescribir la memoria con las entradas reales"],
    ["RK2", "Que la holgura axial de 0,000 mm se materialice en la pieza", "L_casq = B − 2t define el casquillo exactamente igual al ancho interior",
     "Media: la unión podría no montar o apretar contra el ala", "Medir B, t y L de casquillo (A03) y decidir g_ax o ajuste a la dimensión real"],
    ["RK3", "Confundir movimiento con fuerza", "Uso de IMU como si midiera cargas de correa",
     "Alta: conclusiones erróneas sobre la resistencia de las correas", "Separar dato bruto y procesado; exigir celda de fuerza para Q3; declarar el modelo dinámico"],
    ["RK4", "Que el margen de 2,2471 sea demasiado justo", "En el caso base gobierna la fluencia bajo tensión combinada; comprobar también estabilidad local al variar la geometría",
     "Media: cualquier reducción de pared rompe el umbral", "Recalcular con t medido y, si sigue justo, FEA de detalle"],
    ["RK5", "Que el texto de la memoria quede desalineado con el CAD", "Cambios geométricos sin regenerar ni recalcular",
     "Media: documenta un modelo que no existe", "Regla del proyecto: tras cambio geométrico, regenerar, remedir masa y recalcular la memoria"],
    ["RK6", "Que el piloto se ejecute sin criterios de parada", "Sin acuerdo previo con el profesor",
     "Alta para la seguridad de las personas", "A02 antes de cualquier ensayo; criterios de interrupción escritos"],
    ["RK7", "Datos de personas en herramientas de IA", "Regla vigente del proyecto",
     "Alta para las personas y para el proyecto", "Procesar datos antropométricos solo con herramientas autorizadas y sin datos personales en sistemas externos"],
    ["RK8", "Que el presupuesto de masa se cierre recortando espesores", "La brecha de 212 g tempta el atajo",
     "Alta: contradice las decisiones de no aligerar a ciegas", "Recordar que OPT1, con -9,55 g, empeoró el margen; masa y resistencia van juntas"],
], widths=[500, 2200, 2500, 1900, 2800], font_size=7)

d.heading("13.2 Limitaciones de este paquete", 2)
d.bullet("No se ejecutó ningún ensayo ni se tomó ninguna medición: el paquete es documental.")
d.bullet("No se hizo FEA, ni análisis de fatiga, ni análisis de pandeo distorsional.")
d.bullet("No se cotizó con proveedores: la tabla de cotizaciones queda vacía y estructurada.")
d.bullet("No se inventarió el material del laboratorio: la selección de sensores queda con criterios y sin datos.")
d.bullet("La memoria reproduce el cribado vigente; no lo amplía. Modos que hoy no se evalúan (fatiga, distorsional, contacto) siguen sin evaluarse.")
d.bullet("La auditoría de la memoria anterior es documental: se leyó el archivo y su soporte, sin reejecutar su constructor.")

d.heading("13.3 Decisiones pendientes", 2)
d.bullet("Criterios de aceptación de cada ensayo y de cada modo de fallo (P2).")
d.bullet("Uso de la bomba real o de cargas simuladas en la evaluación (P1).")
d.bullet("Instrumentación disponible y necesidad de celda de fuerza (P3).")
d.bullet("g_ax del casquillo: mantener 0, introducir holgura o ajustar a la dimensión real.")
d.bullet("Longitud del pasador: mantener 37,6 mm o estudiar el pasador con cabeza integrada, que cambia la ruta de carga de la precarga.")
d.bullet("Profundidad del canal: mantener 24 mm o pasar a 26/28 mm, con el incremento de masa de las mejillas.")
d.bullet("Selección del material y del proceso del canal, con su cotización real.")
d.bullet("Selección de la correa: ancho, espesor, resistencia y proceso de terminación.")

d.heading("13.4 Próximos pasos", 2)
d.bullet("A01 y A02: inventario de piezas y reunión de alcance con el profesor. Sin esto no arranca el resto.")
d.bullet("A03: medir B, t y longitud de casquillo en las piezas disponibles. Es la measurement más barata y la que cierra el hallazgo de la holgura axial.")
d.bullet("A09 y A10: definir las preguntas experimentales y hacer el inventario del laboratorio antes de elegir sensor.")
d.bullet("Cuando existan las primeras mediciones: incorporarlas a la memoria (A21) y recalcular (A22); el cambio de P2.04 a P2.05 se justifica con esa comparación, no antes.")

d.page_break()

# ============================================================ 14. ANEXOS
d.heading("14. Anexos", 1)
d.heading("14.1 Anexo A · Formularios de captura", 2)
d.para("Los formularios completos están como archivos sueltos en 04_Anexos_Formularios y como hojas de la "
       "planilla. El formulario de bomba ya existe en el repositorio (02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md) "
       "y se adopta sin duplicarlo.", size=10)
d.table([
    ["Formulario", "Archivo", "Campos clave", "Origen"],
    ["A.1 Registro de medición de bomba", "04_Anexos_Formularios/Formulario_Registro_Bomba_y_Correas.md",
     "Identificación, condición de llenado, 13 cotas con dos medidas, footnotes de método", "Adopta el registro existente del repositorio"],
    ["A.2 Protocolo de laboratorio", "04_Anexos_Formularios/Formulario_Protocolo_Laboratorio.md",
     "Montaje, variables controladas, instrumentación, criterios de parada, registro de datos", "Nuevo en este paquete"],
    ["A.3 Ficha de ensayo", "04_Anexos_Formularios/Formulario_Ficha_de_Ensayo.md",
     "Identificador, fecha, versión del prototipo, configuración, datos crudos, eventos", "Nuevo en este paquete"],
    ["A.4 Diccionario de datos", "04_Anexos_Formularios/Diccionario_de_Datos.md",
     "Símbolo, descripción, unidad SI, estado, fuente, método, incertidumbre", "Nuevo en este paquete"],
], widths=[1800, 3200, 2600, 2300])

d.heading("14.2 Anexo B · Memoria de cálculo", 2)
d.table([
    ["Archivo", "Contenido", "Estado"],
    ["03_Memoria_Calculo/Memoria_SEDAC_P204_MC01_EDITABLE.xmcd", "Memoria de cálculo en formato XMCD clásico, abierta, recalculada y guardada por la instalación Mathcad 15 de este equipo",
     "VERIFICADO: 177 variables cotejadas contra el control numérico, 0 fuera de tolerancia"],
    ["03_Memoria_Calculo/Soporte/Memoria_SEDAC_P204_MC01_FUENTE.xmcd", "Archivo fuente generado con el generador de este paquete", "Generado; sirve para regenerar la memoria"],
    ["03_Memoria_Calculo/Soporte/VERIFICACION_MATHCAD.json", "Resultado variable por variable de la verificación en Mathcad", "Evidencia de verificación"],
    ["03_Memoria_Calculo/Soporte/COMPARACION_CONTROL_VS_REPO.json", "Cotejo del control numérico contra el cribado publicado del repositorio", "Peor error relativo 8,06·10⁻¹⁶"],
    ["03_Memoria_Calculo/Soporte/Guion_Implementacion_Mathcad15.md", "Guion de implementación: qué se declaró, en qué orden y con qué unidades, para rehacer o extender la memoria",
     "Documento de referencia"],
    ["03_Memoria_Calculo/Soporte/construir_memoria.py", "Generador de la hoja de trabajo XMCD", "Herramienta del paquete"],
], widths=[3300, 3700, 2400])
d.para("El anexo de la memoria dentro de este informe queda PENDIENTE de exportación: la memoria está "
       "verificada y guardada por la aplicación, pero no se ha generado un PDF de su hoja de trabajo para "
       "incrustarlo. La exportación desde Mathcad queda como tarea pendiente.", size=10, bold=True)

d.heading("14.3 Anexo C · Trazabilidad y verificación", 2)
d.bullet("Requisito → ensayo → dato → cálculo → decisión: hoja 10_Trazabilidad de la planilla.")
d.bullet("Cada variable de la memoria lleva su estado y su origen; los símbolos de medición de laboratorio no se definen en la hoja, de modo que cualquier uso indebido queda marcado como error por Mathcad.")
d.bullet("Las unidades se declaran en cada entrada y el verificador dimensional de Mathcad rechaza las combinaciones incompatibles; la hoja incluye cuatro comprobaciones explícitas de dimensionalidad.")
d.bullet("El control numérico se genera con las mismas expresiones que la hoja, de modo que la comparación entre control y aplicación verifica el motor y no reescribe las fórmulas.")
d.bullet("El cotejo contra los resultados publicados del repositorio verifica además el modelo, no solo el motor.")

path = d.save(OUT)
print("informe escrito:", path, path.stat().st_size, "bytes")

