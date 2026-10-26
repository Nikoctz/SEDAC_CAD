"""
gen_planilla.py — genera la planilla de captura y seguimiento del prototipo SEDAC.

Estructura de identificadores:
  R-xx  requisito
  V-xx  variable de entrada
  E-xx  ensayo
  I-xx  instrumento
  M-xx  material
  S-xx  sensor
  C-xx  cotizacion
  A-xx  actividad
  D-xx  decision
  T-xx  resultado

Reglas:
- Las mediciones quedan VACIAS. Nunca se usa 0 como sustituto de un dato desconocido.
- Cada formula comprueba entradas incompletas y devuelve PENDIENTE en vez de un numero enganoso.
- Se separa dato bruto (03_Registro_Ensayos) de dato procesado (08_Resultados).
"""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xlsx_lib import (Sheet, write_xlsx, STYLE_HEADER, STYLE_TITLE, STYLE_INPUT,  # noqa: E402
                      STYLE_NORMAL, STYLE_DATE, STYLE_CALC)

OUT = HERE / "Planilla_SEDAC_Captura_y_Seguimiento_v0.1.xlsx"

H = STYLE_HEADER
T = STYLE_TITLE
I_ = STYLE_INPUT
N = STYLE_NORMAL
D = STYLE_DATE
C = STYLE_CALC


def hdr(row):
    return [(v, H) for v in row]


def build():
    sheets = []

    # ---------------------------------------------------------------- 00 Portada
    s = Sheet("00_Portada", widths=[34, 62, 30, 26])
    s.add_row([("SEDAC · Planilla de captura, seguimiento y trazabilidad", T)])
    s.add_row([("Prototipo SEDAC · base P2.04 vigente · parametrización P2.05 · versión de la planilla 0.1", N)])
    s.add_row([("Fecha de emisión", N), ("2026-10-25", N)])
    s.add_row([("Estado del paquete", N),
               ("Documental. No contiene mediciones: las mediciones de laboratorio, correas, bomba y sensores "
                "aún no existen y quedan como PENDIENTE. No declara validación física ni técnica.", N)])
    s.blank()
    s.add_row([("Uso previsto", H), ("Cómo se usa", H)])
    for a, b in [
        ("Registro de datos", "03_Registro_Ensayos guarda el dato bruto tal como se observa; 08_Resultados guarda el procesado."),
        ("Control de completitud", "Las celdas de medición quedan vacías y las fórmulas devuelven PENDIENTE."),
        ("Trazabilidad", "10_Trazabilidad enlaza requisito → ensayo → dato → cálculo → decisión."),
        ("Cálculo", "El motor de cálculo es la memoria Mathcad 15 de 03_Memoria_Calculo; esta planilla NO recalcula resistencia."),
        ("Estados", "Cada fila lleva su estado. Ver 11_Diccionario para el significado."),
    ]:
        s.add_row([(a, N), (b, N)])
    s.blank()
    s.add_row([("Indicador", H), ("Valor", H), ("Fórmula", H)])
    s.add_row([("Variables de entrada en la planilla", N),
               ("=COUNTIF('02_Variables'!A3:A400,\"V*\")", C),
               ("Cuenta filas con identificador", N)])
    s.add_row([("Variables con estado PENDIENTE", N),
               ("=COUNTIF('02_Variables'!H3:H400,\"PENDIENTE*\")", C),
               ("Cuenta estados que empiezan por PENDIENTE", N)])
    s.add_row([("Variables medidas (MEDIDO)", N),
               ("=COUNTIF('02_Variables'!H5:H200,\"MEDIDO*\")", C),
               ("Solo se cuentan si el dato se registro como medido", N)])
    s.add_row([("Ensayos registrados", N),
               ("=COUNTIF('03_Registro_Ensayos'!A3:A400,\"E*\")", C),
               ("Filas de ensayo con identificador", N)])
    s.add_row([("Ensayos con resultado en bruto", N),
               ("=COUNTIF('03_Registro_Ensayos'!N3:N400,\"REGISTRADO*\")", C),
               ("No cuenta los ensayos planificados", N)])
    s.add_row([("Resultados procesados", N),
               ("=COUNTIF('08_Resultados'!A3:A400,\"T*\")", C),
               ("Cada resultado con dato y prediccion comparables", N)])
    s.add_row([("Decisiones cerradas", N),
               ("=COUNTIF('09_Decisiones'!I3:I400,\"CERRADA*\")", C),
               ("Decisiones con cierre documentado", N)])
    s.add_row([("Cotizaciones formales", N),
               ("=COUNTIF('07_Cotizaciones'!L3:L400,\"COTIZACION FORMAL\")", C),
               ("Solo cotizaciones formales; no precios de lista", N)])
    s.blank()
    s.add_row([("Advertencia", H)])
    s.add_row([("El cero no es un dato. Ninguna celda de medición debe completarse con 0 para represents "
                "cero; si la magnitud es realmente nula, se escribe 0 en el resultado procesado y se deja "
                "constancia del método. Las hipótesis de carga (25 kg, 3 g, 1 g, 70/30, e = 107,5 mm, "
                "precarga 2000 N) NO son mediciones y no deben mezclarse con los datos de la planilla.", N)])
    sheets.append(s)

    # ------------------------------------------------------- 01 Planificación
    s = Sheet("01_Planificacion", widths=[7, 16, 30, 12, 26, 20, 14, 22, 26, 26, 14], freeze=4)
    s.add_row([("Planificación por etapas", T)])
    s.add_row([("Identificador", H), ("Etapa", H), ("Actividad", H), ("Depende de", H), ("Insumo", H),
               ("Responsable (por asignar)", H), ("Duración estimada", H), ("Condición de inicio", H),
               ("Resultado esperado", H), ("Evidencia de cierre", H), ("Estado", H)])
    actividades = [
        ("A01", "Preparación", "Inventario de piezas P2.04 disponibles y su estado físico", "", "Entrega P2.04", "", "Media jornada", "Acceso a la carpeta de entrega", "Lista de piezas con identifiers y disponibilidad", "Acta de inventario firmada", "PLANIFICADA"),
        ("A02", "Preparación", "Definición de alcance y protocolo con el profesor de biomecánica", "", "Este informe", "", "1 reunión", "Profesor disponible", "Protocolo aprobado y criterios de parada acordados", "Documento de protocolo firmado", "PLANIFICADA"),
        ("A03", "Preparación", "Verificación de la cadena de tolerancias del apilamiento axial", "A01", "Piezas reales de canales, casquillos y pasadores", "", "Media jornada", "Piezas disponibles", "Tabla de B, t y L medidas con su incertidumbre", "Hoja de medición firmada", "PLANIFICADA"),
        ("A04", "Preparación", "Selección del banco y definición de la carga inerte", "A02", "Criterios acordados", "", "1 reunión", "Protocolo aprobado", "Definición de lastre, incrementos y criterio de parada", "Registro del banco", "PLANIFICADA"),
        ("A05", "Caracterización de bomba", "Caracterización dimensional de la bomba de espalda", "A01", "Bomba, cinta métrica, calibre, báscula", "", "1 jornada", "Bomba disponible", "Hoja de dimensiones con condición llena/vacía", "Registro + fotografías", "PLANIFICADA"),
        ("A06", "Caracterización de bomba", "Determinación de masa y centro de masa de la bomba llena", "A05", "Bomba llena, báscula, paradoja de medición", "", "Media jornada", "Dimensiones tomadas", "Masa y centro de masa con método declarado", "Hoja de masa con fotografías", "PLANIFICADA"),
        ("A07", "Caracterización de correas", "Medición de ancho, espesor y rigidez de las correas", "A01", "Correas seleccionadas", "", "Media jornada", "Correas disponibles", "Valores con incertidumbre y método de rigidez", "Hoja de correas", "PLANIFICADA"),
        ("A08", "Caracterización de correas", "Medición del arnés: masa, recorrido y puntos de apoyo", "A01", "Arnés y acolchado", "", "1 jornada", "Arnés disponible", "Masa del arnés y mapa de apoyos", "Hoja de arnés", "PLANIFICADA"),
        ("A09", "Sensores", "Definición de las preguntas experimentales antes de elegir sensor", "A02", "Objetivos del laboratorio", "", "1 sesión", "Alcance acordado", "Lista de magnitudes a medir y decisiones asociadas", "Acta de definición", "PLANIFICADA"),
        ("A10", "Sensores", "Inventario del material IMU disponible en el laboratorio", "A09", "Acceso al laboratorio", "", "Media jornada", "Acceso concedido", "Inventario con modelo, firmware y software", "Inventario del laboratorio", "PLANIFICADA"),
        ("A11", "Sensores", "Selección de sensores y de la instrumentación adicional", "A09, A10", "Inventario y criterios", "", "1 sesión", "Inventario completo", "Sensor y accesorio de fuerza elegidos con justificación", "Ficha de selección", "PLANIFICADA"),
        ("A12", "Sensores", "Definición del sistema de coordenadas y de la fijación", "A11", "Sensor elegido", "", "1 sesión", "Sensor disponible", "Protocolo de ejes y fijación con fotografías", "Protocolo de montaje", "PLANIFICADA"),
        ("A13", "Calibración", "Calibración estática de las IMU en seis posiciones", "A11", "IMU, mesa, girómetro de referencia", "", "Media jornada", "IMU instalada", "Tabla de offset por eje con repetibilidad", "Registro de calibración", "PLANIFICADA"),
        ("A14", "Calibración", "Verificación de sincronización entre IMU yDAQ de fuerza", "A11, A13", "IMU y采集 de fuerza", "", "Media jornada", "Ambos disponibles", "Desfase medido y corregido", "Registro de sincronización", "PLANIFICADA"),
        ("A15", "Prueba piloto", "Montaje y montaje en banco sin personas", "A04, A12, A13", "Prototipo, banco, lastre", "", "1 jornada", "Todo lo anterior cerrado", "Ensayo piloto ejecutado con datos crudos", "Registro de ensayo piloto", "PLANIFICADA"),
        ("A16", "Prueba piloto", "Revisión del profesor sobre el piloto antes de ensayo con personas", "A15", "Datos del piloto", "", "1 reunión", "Piloto ejecutado", "Observaciones y ajustes acordados", "Acta de revisión", "PLANIFICADA"),
        ("A17", "Ensayos", "Ensayos con carga inerte en banco", "A16", "Prototipo instrumentado", "", "Según protocolo", "Piloto revisado", "Serie de ensayos con criterio de parada aplicado", "Datos brutos + registro de ensayos", "PLANIFICADA"),
        ("A18", "Ensayos", "Ensayos con personas, solo con autorización documentada", "A16, A17", "Consentimiento y protocolo de seguridad", "", "Según protocolo", "Autorización escrita y criterios de parada", "Datos de campo con consentimiento registrado", "Consentimientos + datos", "PLANIFICADA"),
        ("A19", "Procesamiento", "Procesamiento de señales IMU y corrección de sesgos", "A17", "Software del sensor", "", "1 jornada", "Datos brutos disponibles", "Series procesadas con método documentado", "Carpetas de datos procesados", "PLANIFICADA"),
        ("A20", "Procesamiento", "Comparación entre predicción de la memoria y ensayo", "A19, A11", "Memoria Mathcad, datos procesados", "", "1 jornada", "Ambos disponibles", "Tabla de cotejo con diferencias y su causa", "Hoja de comparación", "PLANIFICADA"),
        ("A21", "Actualización de cálculos", "Actualización de las entradas medidas en la memoria", "A03, A06, A07, A08", "Mediciones registradas", "", "1 jornada", "Entradas disponibles", "Memoria recalculada con valores medidos", "Memoria versión MC02", "PLANIFICADA"),
        ("A22", "Actualización de cálculos", "Recálculo del cribado y de la sensibilidad con datos reales", "A21", "Memoria actualizada", "", "1 jornada", "Memoria actualizada", "Márgenes nuevos y lista de modos que fallan", "Informe de recálculo", "PLANIFICADA"),
        ("A23", "Revisión del diseño", "Matriz de decisión: conservar, revisar geometría, material o unión", "A22", "Resultados comparados", "", "1 sesión", "Recálculo cerrado", "Acciones propuestas y condicionadas a evidencia", "Registro de decisiones", "PLANIFICADA"),
        ("A24", "Revisión del diseño", "Actualización del expediente de diseño del proyecto", "A23", "Decisiones tomadas", "", "1 jornada", "Decisiones cerradas", "Expediente actualizado con trazabilidad", "Expediente y changelog", "PLANIFICADA"),
    ]
    ini_a = len(s.rows) + 1
    for a in actividades:
        s.add_row(list(a))
    s.blank()
    s.add_row([("Duración total estimada", N),
               ("=SUMPRODUCT((G%d:G%d<>\"\")*1)" % (ini_a, ini_a + len(actividades) - 1), C),
               ("Conteo de actividades con duración declarada; no es un compromiso de fechas", N)])
    s.add_row([("Actividades planificadas", N), ("=COUNTA(A%d:A%d)" % (ini_a, ini_a + len(actividades) - 1), C), ("", N)])
    s.add_row([("Actividades cerradas", N), ("=COUNTIF(K%d:K%d,\"CERRADA*\")" % (ini_a, ini_a + len(actividades) - 1), C), ("", N)])
    sheets.append(s)

    # ----------------------------------------------------------- 02 Variables
    s = Sheet("02_Variables", widths=[7, 18, 34, 12, 14, 14, 26, 16, 22, 20, 24, 12, 12], freeze=4)
    s.add_row([("Matriz de variables y datos pendientes", T)])
    s.add_row([("Identificador", H), ("Símbolo", H), ("Descripción", H), ("Unidad SI", H),
               ("Valor registrado", H), ("Valor en cálculo", H), ("Fuente del valor en cálculo", H),
               ("Estado", H), ("Método de obtención", H), ("Incertidumbre o tolerancia", H),
               ("Cálculo que la usa", H), ("Ensayo", H), ("Control", H)])
    variables = [
        ("V001", "B", "Ancho exterior del canal", "mm", 32, "P2.04 CAD (PARAMETROS_P2_05.json)", "ANTECEDENTE", "Medir en 5 canales con calibre", "por determinar", "A_min, A_sec", "A03", "MEDIR"),
        ("V002", "t", "Espesor de pared del canal", "mm", 3, "P2.04 CAD", "ANTECEDENTE", "Medir con micrómetro en 5 puntos por canal", "por determinar", "A_min, pandeo local", "A03", "MEDIR"),
        ("V003", "L_casq", "Longitud del casquillo", "mm", 26, "Generador vigente: B - 2t", "ANTECEDENTE", "Medir 8 casquillos", "por determinar", "holgura_axial", "A03", "MEDIR"),
        ("V004", "g_ax", "Holgura axial nominal del casquillo", "mm", None, "No adoptado", "PENDIENTE", "Decidir tras la cadena de tolerancias de A03", "por determinar", "holgura_axial", "A03", "PENDIENTE"),
        ("V005", "D", "Profundidad del canal", "mm", 24, "P2.04 CAD", "ANTECEDENTE", "Medir con calibre", "por determinar", "A_min, sensibilidad", "A03", "MEDIR"),
        ("V006", "m_bomba_vacia", "Masa de la bomba de espalda vacía, con manguera", "kg", None, "Sin dato", "PENDIENTE", "Báscula calibrada, 3 repeticiones", "por determinar", "Fv, presupuesto", "A05", "MEDIR"),
        ("V007", "m_bomba_llena", "Masa de la bomba llena en la condición de uso", "kg", None, "Sin dato", "PENDIENTE", "Báscula calibrada, 3 repeticiones", "por determinar", "Fv, centro de masa", "A06", "MEDIR"),
        ("V008", "z_cg_bomba", "Centro de masa de la bomba llena, coordenada Z", "mm", None, "Sin dato", "PENDIENTE", "Paradoja de medición, 3 repeticiones", "por determinar", "M0, excentricidad", "A06", "MEDIR"),
        ("V009", "m_arnes", "Masa del arnés con acolchado", "kg", None, "Sin dato", "PENDIENTE", "Báscula calibrada", "por determinar", "reserva textil", "A08", "MEDIR"),
        ("V010", "ancho_cinta", "Ancho de la correa de carga", "mm", 50, "PARAMETROS_P2_05.json", "SUPUESTO", "Medir con cinta métrica y calibre", "por determinar", "Tinterface, puente", "A07", "MEDIR"),
        ("V011", "esp_cinta", "Espesor de la correa", "mm", 1.5, "PARAMETROS_P2_05.json", "SUPUESTO", "Medir con micrómetro en 3 puntos", "por determinar", "Z_bridge", "A07", "MEDIR"),
        ("V012", "rigidez_correa", "Rigidez axial de la correa", "N/mm", None, "Sin dato", "PENDIENTE", "Ensayo de tracción axial, 3 repeticiones", "por determinar", "reparto de cargas", "A07", "MEDIR"),
        ("V013", "apoyo_hombro_y", "Posición del apoyo de hombro", "mm", 435, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Marcar sobre el prototipo con carga", "por determinar", "L_luz", "A08", "MEDIR"),
        ("V014", "apoyo_cinturon_y", "Posición del apoyo de cinturón", "mm", 55, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Marcar sobre el prototipo con carga", "por determinar", "L_luz", "A08", "MEDIR"),
        ("V015", "ancho_apoyo_hombro", "Ancho efectivo del apoyo de hombro", "mm", None, "Sin dato", "PENDIENTE", "Medir la zona de contacto con carga", "por determinar", "reparto de cargas", "A08", "MEDIR"),
        ("V016", "m_total", "Masa total considerada en el caso de carga", "kg", 25, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Reemplazar por suma medida de equipo más carga", "por determinar", "Fv, Fh", "A06, A08", "REEMPLAZAR"),
        ("V017", "fv", "Factor de carga vertical", "-", 3, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Justificar con el profesor según dinámica de la tarea", "por determinar", "Fv", "A02", "JUSTIFICAR"),
        ("V018", "fh", "Factor de carga horizontal", "-", 1, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Justificar con el profesor", "por determinar", "Fh", "A02", "JUSTIFICAR"),
        ("V019", "frac", "Reparto de carga entre el lado más cargado y el otro", "-", 0.7, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Deducir de la medición de apoyos", "por determinar", "N_lado, Q_lado", "A08", "REEMPLAZAR"),
        ("V020", "excentricidad", "Excentricidad de la carga respecto del eje", "mm", 107.5, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Reemplazar por la distancia medida al centro de masa", "por determinar", "M0", "A06", "REEMPLAZAR"),
        ("V021", "precarga", "Precarga de estudio de las uniones", "N", 2000, "PARAMETROS_P2_05.json", "HIPÓTESIS", "Definir con el par de montaje y la prueba de tuerca", "por determinado", "n_casquillo, n_perno", "A02", "JUSTIFICAR"),
        ("V022", "E_al", "Módulo de Youngs del material del canal", "MPa", 69000, "PARAMETROS_P2_05.json", "SUPUESTO", "Certificado del proveedor o ensayo", "por determinar", "todas las verificaciones", "A24", "REEMPLAZAR"),
        ("V023", "Sy_al", "Límite elástico del material del canal", "MPa", 240, "PARAMETROS_P2_05.json", "SUPUESTO", "Certificado del proveedor o ensayo", "por determinar", "todas las verificaciones", "A24", "REEMPLAZAR"),
        ("V024", "masa_CAD", "Masa rígida y protectores del conjunto P2.04", "kg", 1.442328, "01_CAD/Prototipo_P2/P2_04_20261016/BOM_Y_MASAS.csv (masa de modelo en Inventor)", "MEDIDO", "Regenerar si cambia el CAD", "±0,001 kg (modelo)", "presupuesto", "A24", "REVISAR"),
        ("V025", "masa_presupuesto", "Presupuesto del sistema sin bomba ni agua", "kg", 2.212328, "Cálculo", "CALCULADO", "Recalcular con masas medidas", "según entradas", "brecha a 2 kg", "A21", "REVISAR"),
        ("V026", "Sy_arandela", "Límite elástico mínimo exigido a la arandela", "MPa", 200, "PARAMETROS_P2_05.json", "SUPUESTO", "Certificado del proveedor", "por determinar", "n_arb_flex, n_arb_tuerca", "A24", "REEMPLAZAR"),
        ("V027", "par_apriete", "Par de apriete de las uniones M5", "N·m", None, "Sin dato", "PENDIENTE", "Acordar con el profesor y el fabricante", "por determinar", "precarga real", "A02", "PENDIENTE"),
        ("V028", "recorrido_cinta", "Recorrido real de las cintas", "mm", None, "Sin dato", "PENDIENTE", "Medir con topes de recorrido", "por determinar", "Tinterface", "A08", "MEDIR"),
        ("V029", "zonas_contacto", "Clasificación de zonas de contacto A/B/C", "-", None, "D-12 pendiente", "PENDIENTE", "Acordar criterios con el profesor", "por determinar", "criterio funcional", "A02", "PENDIENTE"),
        ("V030", "frecuencia_propia", "Frecuencia propia del conjunto", "Hz", None, "No calculada", "PENDIENTE", "Ensayo de impacto con registro de IMU", "por determinar", "comparación con ensayo", "A17", "MEDIR"),
    ]
    ini_v = len(s.rows) + 1
    for v in variables:
        vid, sym, desc, unit, valor_calc, fuente, estado, metodo, incert, calc, ensayo, control = v
        s.add_row([(vid, N), (sym, N), (desc, N), (unit, N), (None, I_), (valor_calc, N), (fuente, N),
                   (estado, N), (metodo, N), (incert, N), (calc, N), (ensayo, N), (control, C)])
    # formulas de control por fila (columna M) y estado efectivo
    for row in range(ini_v, ini_v + len(variables)):
        s.rows[row - 1].append(("=IF(E%d=\"\",\"PENDIENTE: sin medición\",IF(H%d=\"MEDIDO\",\"OK\",\"REVISAR: valor sin marcar MEDIDO\"))" % (row, row), C))
    s.blank()
    s.add_row([("Nota", H)])
    s.add_row([("La columna 'Valor registrado' queda vacía hasta que exista una medición. Las fórmulas de la "
                "columna de control devuelven PENDIENTE mientras eso ocurra: no hay ceros sustitutos. "
                "El 'Valor en cálculo' es el número que hoy usa la memoria Mathcad, con su estado al lado.", N)])
    sheets.append(s)

    # --------------------------------------------------- 03 Registro de ensayos
    s = Sheet("03_Registro_Ensayos", widths=[7, 12, 14, 16, 26, 22, 20, 14, 12, 12, 10, 26, 18, 14, 10], freeze=4)
    s.add_row([("Registro de ensayos (dato bruto)", T)])
    s.add_row([("Identificador", H), ("Fecha", H), ("Versión del prototipo", H), ("Configuración", H),
               ("Objetivo", H), ("Montaje", H), ("Variables controladas", H), ("Instrumentación", H),
               ("Frecuencia (Hz)", H), ("Duración (s)", H), ("Repeticiones", H), ("Criterio de aceptación", H),
               ("Dato bruto obtenido", H), ("Estado", H), ("Control de entrada", H)])
    ensayos = [
        ("E01", "P04", "Canal solo, sin bomba", "Comprobar la rigidez del canal en flexión", "Banco con apoyo de hombro y cinturón", "Carga inerte, sin personas", "Sin definir", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E02", "P04", "Canal + bomba de agua", "Medir desplazamiento por peso y por balanceo de la bomba", "Ídem E01", "Ídem E01", "Ídem E01", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E03", "P04", "Conjunto completo con arnés", "Medir la respuesta global del prototipo con correas", "Banco o simulador de marcha", "Carga inerte primero", "Ídem E01", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E04", "P04", "Conjunto con carga lateral", "Caracterizar la respuesta a fuerzas horizontales", "Ídem E01", "Ídem E01", "Ídem E01", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E05", "P04", "Cuna y puente inferior", "Medir desplazamiento local de la cuna", "Ídem E01", "Ídem E01", "Ídem E01", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E06", "P04", "Conjunto completo", "Medir la respuesta con personas, solo tras autorización", "Banco con arnés", "Personas, con consentimiento", "Ídem E01", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E07", "P04", "Unión aislada", "Medir el desplazamiento axial del casquillo con apriete", "Banco de uniones", "Precarga controlada", "Precarga y par", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
        ("E08", "P04", "Banco", "Obtener la frecuencia propia del conjunto", "Banco con excitación conocida", "Impacto controlado", "Masa e inercia", "Pendiente de A11", "Pendiente", "Pendiente", "Por acordar", "PENDIENTE"),
    ]
    ini_e = len(s.rows) + 1
    for e in ensayos:
        eid, ver, conf, obj, mont, varc, instr, freq, dur, rep, crit, estado = e
        s.add_row([(eid, N), (None, D), (ver, N), (conf, N), (obj, N), (mont, N), (varc, N), (instr, N),
                   (None, I_), (None, I_), (None, I_), (crit, N), (None, I_), (estado, N), ("", C)])
    for row in range(ini_e, ini_e + len(ensayos)):
        s.rows[row - 1][14] = ("=IF(B%d=\"\",\"PENDIENTE: sin fecha\",IF(N%d=\"REGISTRADO\",\"OK\",\"PENDIENTE\"))" % (row, row), C)
    s.blank()
    s.add_row([("Regla", H)])
    s.add_row([("El dato bruto se registra sin procesar. Frecuencia, duración y repeticiones quedan vacías "
                "hasta que se defina el protocolo con el profesor: se proponemos valores, pero no se fijan "
                "sin ese acuerdo.", N)])
    sheets.append(s)

    # ------------------------------------------ 04 Instrumentos y calibración
    s = Sheet("04_Instrumentos_Calibracion", widths=[7, 26, 16, 20, 12, 16, 14, 14, 14, 26, 14, 12], freeze=4)
    s.add_row([("Instrumentos y calibración", T)])
    s.add_row([("Identificador", H), ("Instrumento", H), ("Tipo", H), ("Marca y modelo", H),
               ("Resolución", H), ("Incertidumbre", H), ("Fecha de calibración", H), ("Próxima", H),
               ("Certificado", H), ("Uso previsto", H), ("Estado", H), ("Control", H)])
    instrumentos = [
        ("I01", "Báscula", "Masa", "", "", "", "", "", "", "Masa de bomba y arnés", "PENDIENTE"),
        ("I02", "Cálmetro digital", "Longitud", "", "", "", "", "", "", "B, t, longitudes de casquillo", "PENDIENTE"),
        ("I03", "Micrómetro", "Longitud", "", "", "", "", "", "", "Espesor de pared y de correa", "PENDIENTE"),
        ("I04", "Cinta métrica", "Longitud y recorrido", "", "", "", "", "", "", "Recorrido de cintas", "PENDIENTE"),
        ("I05", "Paradoja de medición", "Centro de masa", "", "", "", "", "", "", "Centro de masa de bomba", "PENDIENTE"),
        ("I06", "Célula de carga", "Fuerza", "", "", "", "", "", "", "Fuerza en correas", "PENDIENTE"),
        ("I07", "IMU (unidad)", "Aceleración y giro", "", "", "", "", "", "", "Movimiento del conjunto", "PENDIENTE"),
        ("I08", "Registrador de fuerza", "Adquisición", "", "", "", "", "", "", "Sincronización con IMU", "PENDIENTE"),
        ("I09", "Girómetro de referencia", "Referencia angular", "", "", "", "", "", "", "Calibración angular", "PENDIENTE"),
        ("I10", "Banco de ensayo", "Carga inerte y apoyos", "", "", "", "", "", "", "Ensayos E01 a E05", "PENDIENTE"),
    ]
    ini_i = len(s.rows) + 1
    for i in instrumentos:
        iid, nombre, tipo, marca, res, incert, fc, prox, cert, uso, estado = i
        s.add_row([(iid, N), (nombre, N), (tipo, N), (marca, N), (res, N), (incert, N), (fc, D), (prox, D),
                   (cert, N), (uso, N), (estado, N), ("", C)])
    for row in range(ini_i, ini_i + len(instrumentos)):
        s.rows[row - 1][11] = ("=IF(OR(G%d=\"\",H%d=\"\"),\"PENDIENTE: sin calibración\",\"OK\")" % (row, row), C)
    sheets.append(s)

    # ------------------------------------------------------------ 05 Materiales
    s = Sheet("05_Materiales", widths=[7, 20, 16, 22, 12, 12, 14, 14, 14, 20, 20, 26, 16, 12, 12], freeze=4)
    s.add_row([("Matriz de materiales y procesos", T)])
    s.add_row([("Identificador", H), ("Material", H), ("Grado y condición", H), ("Propiedad medida", H),
               ("Valor", H), ("Unidad", H), ("Fuente", H), ("Estado", H), ("Ambiente de uso", H),
               ("Comodidad de contacto", H), ("Fabricación", H), ("Disponibilidad", H), ("Costo", H),
               ("Uso en el prototipo", H), ("Control", H)])
    materiales = [
        ("M01", "Aluminio 6061", "T6,certificate", "Densidad", 2.7, "g/cm³", "PARAMETROS_P2_05.json", "SUPUESTO", "Interior, sin contacto directo con agua", "No aplica (estructura interna)", "Mecanizado o extrusión certificada, sin soldadura creditada", "Proveedor nacional por consultar", "", "Canales, casquillos, pasadores, uniones", ""),
        ("M02", "Aluminio 6061", "T6,certificate", "Límite elástico", 240, "MPa", "PARAMETROS_P2_05.json", "SUPUESTO", "", "", "", "", "", "Canal y uniones", ""),
        ("M03", "Aluminio 6061", "T6,certificate", "Módulo de Young", 69000, "MPa", "PARAMETROS_P2_05.json", "SUPUESTO", "", "", "", "", "", "Canal y uniones", ""),
        ("M04", "HDPE", "Panel 1 mm", "Densidad", 0.953, "g/cm³", "PARAMETROS_P2_05.json", "SUPUESTO", "Exterior, humedad", "No aplica (sin crédito estructural)", "Lámina cortada y perforada", "Proveedor nacional por consultar", "", "Espaldera", ""),
        ("M05", "Acero de fijación", "A2-80 (hipótesis)", "Densidad", 8.0, "g/cm³", "PARAMETROS_P2_05.json", "SUPUESTO", "Interior", "No aplica", "Comprado", "Catálogo común", "", "Tornillos y arandelas", ""),
        ("M06", "Textil de correa", "Por seleccionar", "Resistencia a la tracción", "", "N", "", "PENDIENTE", "Interior, humedad y roce", "Alta: es la superficie de contacto con el usuario", "Cinta tejida con costura", "Por consultar", "", "Correas de carga y estabilización", ""),
        ("M07", "Textil de correa", "Por seleccionar", "Ancho y espesor", "", "mm", "", "PENDIENTE", "", "", "", "", "", "Correas", ""),
        ("M08", "Espuma de acolchado", "Por seleccionar", "Densidad", 0.06, "g/cm³", "PARAMETROS_P2_05.json", "SUPUESTO", "Contacto con el usuario", "Alta: confort y protección de arista", "Espuma cortada", "Por consultar", "", "Acolchados lumbar y dorsal", ""),
        ("M09", "PLA", "Maqueta de ajuste", "Densidad", 1.24, "g/cm³", "Antecedente de Automatizacion", "SUPUESTO", "Solo para ajuste de encaje", "No aplica", "Impresión 3D, escala de referencia", "Impresora propia", "", "No usar como material estructural", ""),
        ("M10", "Aleación de aluminio alternativa", "Por comparar", "Densidad", "", "g/cm³", "", "PENDIENTE", "", "", "", "", "", "Candidata a comparar en la matriz de decisión", ""),
    ]
    ini_m = len(s.rows) + 1
    for m in materiales:
        mid, mat, grado, prop, val, unit, fuente, estado, amb, com, fab, disp, costo, uso, ctrl = m
        s.add_row([(mid, N), (mat, N), (grado, N), (prop, N), (val, I_ if val == "" else N), (unit, N),
                   (fuente, N), (estado, N), (amb, N), (com, N), (fab, N), (disp, N), (costo, N),
                   (uso, N), ("", C)])
    for row in range(ini_m, ini_m + len(materiales)):
        s.rows[row - 1][14] = ("=IF(H%d=\"PENDIENTE\",\"PENDIENTE: sin dato\",\"OK\")" % row, C)
    sheets.append(s)

    # -------------------------------------------------------------- 06 Sensores
    s = Sheet("06_Sensores", widths=[7, 26, 14, 22, 20, 22, 20, 14, 20, 22, 14, 14, 14], freeze=4)
    s.add_row([("Selección de sensores e instrumentación", T)])
    s.add_row([("Identificador", H), ("Magnitud u opción", H), ("Tipo", H), ("Rango", H),
               ("Ruido o resolución", H), ("Frecuencia real de muestreo", H), ("Sincronización", H),
               ("Registro", H), ("Autonomía", H), ("Montaje", H), ("Compatibilidad", H), ("Costo", H),
               ("Estado", H)])
    s.blank()
    s.add_row([("Criterios de comparación (aplicables a cualquier IMU)", H)])
    for t in ["Magnitudes medidas: aceleración lineal de 3 ejes, velocidad angular de 3 ejes, Magnetómetro (para corregir la deriva por磁场, si el modelo lo permite).",
              "Rango: suficiente para el movimiento esperado en banco y en uso; hay que verificar saturación con el acelerómetro.",
              "Ruido: ruido en la banda de interés; la IMU integra ruido y la deriva crece con el tiempo.",
              "Frecuencia real de muestreo: la nominal del sensor y la del software de registro pueden diferir; hay que registrar la tasa efectiva.",
              "Sincronización: indispensable para comparar IMU con célula de carga; se mide el desfase con una excitación común.",
              "Registro: archivo原始 con metadatos de calibración y marca de tiempo por muestra.",
              "Autonomía: duración de la batería frente a la duración del ensayo.",
              "Montaje: rigidez del soporte; una IMU mal fijada mide el movimiento del soporte, no el del cuerpo.",
              "Compatibilidad: software de registro y de postproceso, y formato de exportación.",
              "Costo: solo como criterio de desempate entre equipos ya disponibles."]:
        s.add_row([(t, N)])
    s.blank()
    s.add_row([("Identificador", H), ("Candidata", H), ("Origen", H), ("Magnitudes", H), ("Rango", H),
               ("Ruido", H), ("Muestreo", H), ("Sincronización", H), ("Registro", H), ("Autonomía", H),
               ("Montaje", H), ("Costo", H), ("Estado", H)])
    candidatas = [
        ("S01", "Equipo IMU del laboratorio (a inventariar)", "Laboratorio de biomecánica", "", "", "", "", "", "", "", "", "", "PENDIENTE"),
        ("S02", "Celda de carga o dinamómetro de correa", "Laboratorio o alquiler", "", "", "", "", "", "", "", "", "", "PENDIENTE"),
        ("S03", "Instrumentación de video para sincronizar", "Laboratorio", "", "", "", "", "", "", "", "", "", "PENDIENTE"),
        ("S04", "Acelerómetro de juicio (referencia)", "Laboratorio", "", "", "", "", "", "", "", "", "", "PENDIENTE"),
    ]
    for c in candidatas:
        s.add_row(list(c))
    s.blank()
    s.add_row([("Advertencia", H)])
    s.add_row([("La IMU mide aceleración y velocidad angular, no fuerza. Convertir aceleración en fuerza "
                "exige un modelo dinámico con masa, rigidez y amortiguamiento, y sus condiciones de "
                "validez. Para cerrar la cadena de cargas de las correas hace falta instrumentación de "
                "fuerza o tensión. La orientación respecto de la gravedad, la deriva del giroscopio, la "
                "integración del acelerómetro y las perturbaciones magnéticas son fuentes de error "
                "conocidas: deben documentarse en el postproceso, no ignorarse.", N)])
    sheets.append(s)

    # ---------------------------------------------------------- 07 Cotizaciones
    s = Sheet("07_Cotizaciones", widths=[7, 26, 22, 34, 14, 10, 12, 26, 14, 18, 24, 22, 12], freeze=4)
    s.add_row([("Cotizaciones y precios", T)])
    s.add_row([("Identificador", H), ("Ítem", H), ("Proveedor", H), ("Enlace o referencia", H),
               ("Fecha de consulta", H), ("Moneda", H), ("Cantidad", H), ("Especificación", H),
               ("Impuestos", H), ("Despacho", H), ("Disponibilidad declarada", H),
               ("Tipo de dato", H), ("Estado", H)])
    cotizaciones = [
        ("C01", "Plancha de aluminio 6061 T6", "Proveedor chileno por consultar", "", "", "CLP", "", "Plancha 32 x 24 x 3 mm o equivalente", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C02", "Barra de aluminio 6061", "Proveedor chileno por consultar", "", "", "CLP", "", "Para pasadores y casquillos", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C03", "Lámina de HDPE 1 mm", "Proveedor chileno por consultar", "", "", "CLP", "", "Panel 270 x 472 mm", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C04", "Tornillo M5x55 ISO 4762 A2-80", "Proveedor chileno por consultar", "", "", "CLP", "", "Cabeza cilíndrica 8,5 x 5", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C05", "Tuerca M5 autofrenante", "Proveedor chileno por consultar", "", "", "CLP", "", "Envolvente DIN 980", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C06", "Arandela M5 5,3 x 16 x 3", "Proveedor chileno por consultar", "", "", "CLP", "", "Envolvente GN 6341", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C07", "Cinta de polipropileno 50 mm", "Proveedor chileno por consultar", "", "", "CLP", "", "Ancho 50 mm, espesor por medir", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C08", "Sensores IMU", "Laboratorio / proveedor", "", "", "", "", "Por definir en A11", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
        ("C09", "Instrumentación de fuerza", "Laboratorio / alquiler", "", "", "", "", "Por definir en A11", "", "", "", "PENDIENTE DE COTIZAR", "PENDIENTE"),
    ]
    for c in cotizaciones:
        cid, item, prov, link, fecha, mon, cant, esp, imp, desp, disp, tipo, estado = c
        s.add_row([(cid, N), (item, N), (prov, N), (link, N), (fecha, D), (mon, N), (cant, I_), (esp, N),
                   (imp, N), (desp, N), (disp, N), (tipo, N), (estado, N)])
    s.blank()
    s.add_row([("Regla", H)])
    s.add_row([("Solo se registra una cotización formal con proveedor identificado, fecha, moneda, "
                "especificación, impuestos, despacho y disponibilidad declarada. Un precio publicado en "
                "sitio web se marca como PRECIO PUBLICADO y no como cotización. Una estimación interna se "
                "marca como ESTIMACION y no se usa para decidir compras.", N)])
    sheets.append(s)

    # ------------------------------------------------------------ 08 Resultados
    s = Sheet("08_Resultados", widths=[7, 10, 30, 14, 14, 14, 16, 16, 16, 18, 14, 12], freeze=4)
    s.add_row([("Resultados procesados y comparación con la predicción", T)])
    s.add_row([("Identificador", H), ("Ensayo", H), ("Magnitud", H), ("Valor medido", H),
               ("Unidad", H), ("Incertidumbre", H), ("Predicción (memoria)", H), ("Diferencia", H),
               ("Diferencia relativa", H), ("Método de procesamiento", H), ("Criterio de aceptación", H),
               ("Estado", H)])
    resultados = [
        ("T01", "E01", "Flecha en el apoyo de hombro", "mm", "", "", "", "Por acordar"),
        ("T02", "E02", "Desplazamiento por masa de bomba", "mm", "", "", "", "Por acordar"),
        ("T03", "E03", "Giro del conjunto", "grados", "", "", "", "Por acordar"),
        ("T04", "E04", "Desplazamiento lateral", "mm", "", "", "", "Por acordar"),
        ("T05", "E05", "Desplazamiento local de la cuna", "mm", "", "", "", "Por acordar"),
        ("T06", "E08", "Frecuencia propia del conjunto", "Hz", "", "", "", "Por acordar"),
        ("T07", "E07", "Holgura axial del casquillo tras apriete", "mm", "", "", "", "Por acordar"),
        ("T08", "E03", "Fuerza en la correa de carga", "N", "", "", "", "Por acordar"),
    ]
    ini_r = len(s.rows) + 1
    for r in resultados:
        tid, ens, mag, unit, metodo, crit = r[0], r[1], r[2], r[3], r[6], r[7]
        s.add_row([(tid, N), (ens, N), (mag, N), (None, I_), (unit, N), (None, I_), (None, I_),
                   (None, C), (None, C), (metodo, N), (crit, N), ("", C)])
    for row in range(ini_r, ini_r + len(resultados)):
        s.rows[row - 1][7] = ("=IF(OR(D%d=\"\",G%d=\"\"),\"PENDIENTE\",D%d-G%d)" % (row, row, row, row), C)
        s.rows[row - 1][8] = ("=IF(OR(D%d=\"\",G%d=\"\",G%d=0),\"PENDIENTE\",ABS(D%d-G%d)/ABS(G%d))" % (row, row, row, row, row, row), C)
        s.rows[row - 1][11] = ("=IF(D%d=\"\",\"PENDIENTE: sin dato medido\",IF(G%d=\"\",\"SIN PREDICCIÓN\",\"COMPARABLE\"))" % (row, row), C)
    s.blank()
    s.add_row([("Nota", H)])
    s.add_row([("La diferencia solo se calcula cuando existe dato medido y predicción: mientras tanto "
                "devuelve PENDIENTE. La predicción se toma de la memoria Mathcad, no de esta planilla.", N)])
    sheets.append(s)

    # ------------------------------------------------------------ 09 Decisiones
    s = Sheet("09_Decisiones", widths=[7, 26, 30, 26, 26, 26, 18, 14, 14, 12], freeze=4)
    s.add_row([("Registro de decisiones", T)])
    s.add_row([("Identificador", H), ("Tema", H), ("Evidencia (resultado o ensayo)", H),
               ("Opciones consideradas", H), ("Decisión", H), ("Condición o impacto", H),
               ("Responsable", H), ("Fecha", H), ("Estado", H), ("Control", H)])
    decisiones = [
        ("D01", "Holgura axial del casquillo", "A03: medición de B, t y L de casquillo", "g_ax = 0 / ajuste a la dimensión real / otro", "Pendiente", "Decidir con la cadena de tolerancias cerrada", "", "", "ABIERTA", ""),
        ("D02", "Longitud del pasador", "A03 y A07", "Mantener 37,6 / pasador con cabeza integrada", "Pendiente", "B cambia la ruta de carga de la precarga: requiere análisis de detalle", "", "", "ABIERTA", ""),
        ("D03", "Profundidad del canal", "A22: sensibilidad con datos reales", "D = 24 / 26 / 28", "Pendiente", "Condicionada al modo que gobierne con cargas reales", "", "", "ABIERTA", ""),
        ("D04", "Selección de material del canal", "V022, V023: certificado del proveedor", "6061-T6 / otro", "Pendiente", "Condicionada a disponibilidad y costo", "", "", "ABIERTA", ""),
        ("D05", "Selección de correa", "A07 y T08", "Ancho, espesor y resistencia por tejido", "Pendiente", "Condicionada a medición y a la fuerza medida en ensayo", "", "", "ABIERTA", ""),
        ("D06", "Instrumentación de fuerza", "A09 y A11", "IMU sola / IMU más celda de carga", "Pendiente", "La IMU no mide fuerza: condiciona qué se puede concluir", "", "", "ABIERTA", ""),
        ("D07", "Clasificación de zonas de contacto A/B/C", "A02 y A08", "Criterio funcional", "Pendiente", "D-12 sigue pendiente: bloquea el cierre del ajuste físico", "", "", "ABIERTA", ""),
        ("D08", "Cierre de la memoria de cálculo", "A21 y A22", "Memoria con entradas medidas", "Pendiente", "Requiere las mediciones de bomba, correas, apoyos y tolerancias", "", "", "ABIERTA", ""),
    ]
    ini_d = len(s.rows) + 1
    for d in decisiones:
        did, tema, ev, opc, dec, cond, resp, fecha, estado, _ctrl = d
        s.add_row([(did, N), (tema, N), (ev, N), (opc, N), (dec, N), (cond, N), (resp, N), (fecha, D),
                   (estado, N), ("", C)])
    for row in range(ini_d, ini_d + len(decisiones)):
        s.rows[row - 1][9] = ("=IF(AND(I%d=\"CERRADA\",E%d=\"\"),\"REVISAR: cerrada sin decisión escrita\",\"OK\")" % (row, row), C)
    sheets.append(s)

    # ------------------------------------------------------------ 10 Trazabilidad
    s = Sheet("10_Trazabilidad", widths=[7, 30, 12, 12, 12, 14, 14, 30, 14], freeze=4)
    s.add_row([("Trazabilidad requisito → ensayo → dato → cálculo → decisión", T)])
    s.add_row([("Identificador", H), ("Requisito", H), ("Ensayo", H), ("Dato", H), ("Variable", H),
               ("Cálculo (memoria)", H), ("Decisión", H), ("Evidencia de cierre", H), ("Estado", H)])
    trazabilidad = [
        ("R01", "El canal no falla por pandeo local con la carga de uso", "E01, E04", "T01, T04", "V002, V005, V016", "n_local, vm", "D03", "Serie de ensayos + memoria recalculada", "PENDIENTE"),
        ("R02", "Las uniones no fallan por aplastamiento ni por cortante", "E07", "T07", "V003, V021", "n_aplast_ala, n_pasador, n_casquillo", "D01, D02", "Ensayo de unión + memoria", "PENDIENTE"),
        ("R03", "El prototipo no cede bajo la masa de la bomba", "E02, E03", "T02, T03", "V006, V007, V008", "Fv, M0, flecha", "D08", "Medición de bomba + ensayos", "PENDIENTE"),
        ("R04", "Las correas reparten la carga de forma conocida", "E03, E05", "T05, T08", "V010, V011, V012, V028", "Tinterface, Tstrap", "D05", "Medición de correas + fuerza medida", "PENDIENTE"),
        ("R05", "El confort de contacto no depende de aristas vivas", "E03", "T03", "V029", "No modelado", "D07", "Clasificación de zonas de contacto", "PENDIENTE"),
        ("R06", "El usuario puede liberarse del equipo con guantes", "E06", "T03", "V029", "No modelado", "D07", "Ensayo con gloves y consentimiento, si se autoriza", "PENDIENTE"),
        ("R07", "El presupuesto de masa se sostiene con el equipo real", "A05, A08", "T02", "V006, V009, V016, V024, V025", "masa_presupuesto", "D08", "Mediciones de masa y presupuesto recalculado", "PENDIENTE"),
        ("R08", "La respuesta medida es compatible con la predicción", "E01 a E05", "T01 a T06", "V001 a V005", "Memoria completa", "D08", "Tabla de comparación con diferencias y su causa", "PENDIENTE"),
    ]
    for t in trazabilidad:
        s.add_row(list(t))
    s.blank()
    s.add_row([("Control", H)])
    s.add_row([("Cada línea exige que exista ensayo, dato, variable, cálculo y decisión antes de cerrarla. "
                "Mientras alguna de esas piezas sea PENDIENTE, la línea no se cierra.", N)])
    sheets.append(s)

    # -------------------------------------------------------- 11 Diccionario
    s = Sheet("11_Diccionario", widths=[26, 70])
    s.add_row([("Diccionario de datos y estados", T)])
    s.add_row([("Término", H), ("Definición", H)])
    definiciones = [
        ("ANTECEDENTE", "Valor tomado de un archivo del repositorio SEDAC_CAD o de un antecedente verificable de otro prototipo. No es una medición de la pieza actual."),
        ("MEDIDO", "Valor obtenido con un instrumento identificado, con registro y con su incertidumbre asociada."),
        ("DATO DE FABRICANTE", "Valor declarado por el proveedor en su ficha o catálogo, con referencia y fecha."),
        ("SUPUESTO", "Valor adoptado por decisión de ingeniería sin medición, con motivo declarado."),
        ("HIPÓTESIS", "Condición de carga o de uso todavía no comprobada."),
        ("CALCULADO", "Resultado de la memoria de cálculo a partir de entradas con estado declarado."),
        ("PENDIENTE", "Sin dato. Nunca se sustituye por cero."),
        ("PENDIENTE: sin medición", "La celda de medición está vacía y el valor en cálculo sigue siendo el supuesto o antecedente anterior."),
        ("COTIZACIÓN FORMAL", "Oferta de proveedor identificado, con fecha, moneda, especificación, impuestos, despacho y disponibilidad declarada."),
        ("PRECIO PUBLICADO", "Precio visible en un sitio web o catálogo, sin oferta formal. No obliga a comprar ni fija condiciones."),
        ("ESTIMACIÓN", "Valor interno aproximado. No es un precio y no se usa para decidir compras."),
        ("Dato bruto", "Registro de lo observado en el ensayo, sin procesar."),
        ("Dato procesado", "Resultado de aplicar el método de procesamiento declarado al dato bruto."),
        ("Dificación de unidades", "El motor de cálculo trabaja en mm, N, MPa y kg; el verificador dimensional de Mathcad rechaza combinaciones incompatibles."),
        ("Criterio de aceptación", "Umbral con el que se juzga un resultado. Mientras no exista, el resultado se registra pero no se declara aprobado ni rechazado."),
        ("Estado de un ensayo", "PLANIFICADA → EN CURSO → REGISTRADO (con dato bruto) → PROCESADO (con resultado comparado)."),
    ]
    for d in definiciones:
        s.add_row([(d[0], N), (d[1], N)])
    sheets.append(s)

    write_xlsx(OUT, sheets)
    return OUT


if __name__ == "__main__":
    path = build()
    print("planilla escrita:", path, path.stat().st_size, "bytes")

