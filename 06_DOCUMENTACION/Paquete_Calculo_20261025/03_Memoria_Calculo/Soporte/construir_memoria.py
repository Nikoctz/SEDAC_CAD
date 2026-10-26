"""
construir_memoria.py — construye la memoria de calculo del prototipo SEDAC (base P2.04,
parametrizacion P2.05) en formato clasico XMCD para Mathcad 15.

Reglas del proyecto aplicadas:
- Las cifras que provienen de archivos del repositorio SEDAC_CAD se declaran como antecedente
  con su ruta; las que son hipotesis se declaran como hipotesis; las medidas de laboratorio
  NO se inventan: quedan como simbolo pendiente, sin definir.
- Las expresiones se escriben una sola vez (aqui) y se usan para dos fines:
  (1) emitirlas como regiones de Mathcad, (2) evaluarlas en Python como control numerico.
- No se modifica nada del repositorio SEDAC_CAD: solo lectura.

Salida: 03_Memoria_Calculo/Soporte/Memoria_SEDAC_P204_MC01_FUENTE.xmcd
        03_Memoria_Calculo/Soporte/VALORES_ESPERADOS_SI.json  (control numerico, SI)
        03_Memoria_Calculo/Soporte/MANIFIESTO_MEMORIA.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mathcad_gen import Worksheet  # noqa: E402

OUT_DIR = HERE
FUENTE = OUT_DIR / "Memoria_SEDAC_P204_MC01_FUENTE.xmcd"
CONTROL = OUT_DIR / "VALORES_ESPERADOS_SI.json"
MANIFIESTO = OUT_DIR / "MANIFIESTO_MEMORIA.json"

# --- Origen de los datos (solo lectura del repositorio) ---------------------------
REPO = r"C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD"
ORIGEN = {
    "parametros": "01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json",
    "calculo": "01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py",
    "resultados_v0": "01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Optimizacion_Real_20261023_014225/Analisis/V0_base_P2_05/RESULTADOS_PREDISENO.json",
    "masas_cad": "01_CAD/Prototipo_P2/P2_04_20261016/BOM_Y_MASAS.csv",
    "modelo_api": "01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/MODELO_API.json",
    "bom_fij": "01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/BOM_FIJACIONES.csv",
}

# --- Entradas: (nombre, expresion, unidad, es_entrada, nota) ---------------------
ENTRADAS = [
    ("L_canal", "480*mm", "mm", True, "P2.04 CAD: alto_refuerzo. Antecedente verificado."),
    ("B", "32*mm", "mm", True, "P2.04 CAD: ancho_refuerzo. Antecedente verificado."),
    ("D", "24*mm", "mm", True, "P2.04 CAD: profundidad_refuerzo. Antecedente verificado."),
    ("t_nom", "3*mm", "mm", True, "P2.04 CAD: pared_refuerzo nominal."),
    ("t_min", "2.8*mm", "mm", True, "PARAMETROS_P2_05.json: pared_minima. Es un minimo de calculo, no gobierna la geometria."),
    ("r_raiz", "2*mm", "mm", True, "P2.04 CAD: radio de raiz."),
    ("sep_canales", "190*mm", "mm", True, "P2.04 CAD: separacion_refuerzos."),
    ("z_eje", "12*mm", "mm", True, "PARAMETROS_P2_05.json: eje_pernos_z."),
    ("d_taladro", "10.2*mm", "mm", True, "PARAMETROS_P2_05.json: taladro_union."),
    ("esp_mejilla", "3*mm", "mm", True, "PARAMETROS_P2_05.json: espesor_mejilla."),
    ("esp_anclaje", "6*mm", "mm", True, "PARAMETROS_P2_05.json: espesor_anclaje."),
    ("esp_anclaje_min", "5.8*mm", "mm", True, "PARAMETROS_P2_05.json: espesor_minimo_anclaje."),
    ("casquillo_od", "12.5*mm", "mm", True, "PARAMETROS_P2_05.json: casquillo_od."),
    ("pasador_od", "10*mm", "mm", True, "PARAMETROS_P2_05.json: pasador_od."),
    ("pasador_id", "5.5*mm", "mm", True, "PARAMETROS_P2_05.json: pasador_id."),
    ("L_pasador", "37.6*mm", "mm", True, "Modelo P2.04: longitud de pasador."),
    ("arandela_od", "16*mm", "mm", True, "Envolvente GN 6341 declarada en el modelo."),
    ("arandela_id", "5.3*mm", "mm", True, "Envolvente GN 6341 declarada en el modelo."),
    ("arandela_esp", "3*mm", "mm", True, "Envolvente GN 6341 declarada en el modelo."),
    ("arandela_esp_min", "2.9*mm", "mm", True, "PARAMETROS_P2_05.json: espesor_arandela_minimo."),
    ("separacion_pernos", "60*mm", "mm", True, "PARAMETROS_P2_05.json: separacion_pernos."),
    ("dist_borde_perno", "12*mm", "mm", True, "PARAMETROS_P2_05.json: distancia_borde_perno."),
    ("apoyo_hombro_y", "435*mm", "mm", True, "PARAMETROS_P2_05.json: apoyo_hombro_y. Su efectividad no esta confirmada fisicamente."),
    ("apoyo_cinturon_y", "55*mm", "mm", True, "PARAMETROS_P2_05.json: apoyo_cinturon_y."),
    ("alto_puente_cinta", "18*mm", "mm", True, "PARAMETROS_P2_05.json: alto_puente_cinta."),
    ("luz_puente_cinta", "52*mm", "mm", True, "PARAMETROS_P2_05.json: luz_puente_cinta."),
    ("m_total", "25*kg", "kg", True, "PARAMETROS_P2_05.json: masa_total_kg. HIPOTESIS: incluye el sistema auxiliar, no es masa de estructura."),
    ("g", "9.81*m/s**2", "m/s**2", True, "PARAMETROS_P2_05.json: cargas.g."),
    ("fv", "3", "", True, "HIPOTESIS: factor_vertical. No validado."),
    ("fh", "1", "", True, "HIPOTESIS: factor_horizontal. No validado."),
    ("frac", "0.7", "", True, "HIPOTESIS: fraccion_lado. Reparto 70/30 no medido."),
    ("excentricidad", "107.5*mm", "mm", True, "HIPOTESIS: excentricidad_mm. No medida."),
    ("precarga", "2000*N", "N", True, "HIPOTESIS: precarga_estudio_N. No es un par de montaje."),
    ("angulo_eslinga", "35*pi/180", "", True, "HIPOTESIS: angulo_eslinga_grados."),
    ("margen_objetivo", "2.2", "", True, "HIPOTESIS: margen_objetivo. Umbral pendiente de acordar con el profesor."),
    ("flecha_limite", "5*mm", "mm", True, "SUPUESTO: flecha_limite_mm."),
    ("K_borde", "1.25", "", True, "SUPUESTO: K_borde."),
    ("K_ventana", "3", "", True, "SUPUESTO: K_ventana."),
    ("brazo_torsion", "12*mm", "mm", True, "PARAMETROS_P2_05.json: brazo_torsion_mm."),
    ("E_al", "69000*MPa", "MPa", True, "SUPUESTO de prediseno: E 6061-T6. Condicionado al material real."),
    ("Sy_al", "240*MPa", "MPa", True, "SUPUESTO de prediseno: Sy 6061-T6. Condicionado al material real."),
    ("Sy_perno", "600*MPa", "MPa", True, "SUPUESTO de prediseno: Sy perno A2-80."),
    ("Sy_arandela", "200*MPa", "MPa", True, "SUPUESTO de prediseno: Sy minimo exigido a la arandela."),
    ("nu", "0.33", "", True, "Poisson 6061."),
    ("As_M5", "14.2*mm**2", "mm**2", True, "Seccion resistente de rosca M5 (antecedente de la memoria anterior)."),
    ("longitud_tornillo", "55*mm", "mm", True, "Tornillo M5x55 ISO 4762 declarado en el modelo."),
    ("altura_tuerca", "5*mm", "mm", True, "Tuerca autofrenante M5 representada en el modelo: 5 mm de alto."),
    ("factor_palanca", "1.5", "", True, "Constante heredada del cribado vigente (R = 1,5*reaccion)."),
    ("masa_CAD", "1.442328*kg", "kg", True, "MEDIDO en Inventor: masa rigida + protectores P2.04."),
    ("reserva_textil", "0.65*kg", "kg", True, "Reserva presupuestaria de textiles. No es geometria."),
    ("reserva_adicional", "0.12*kg", "kg", True, "Reserva presupuestaria adicional."),
]

# --- Funciones: (nombre, argumentos, expresion) -----------------------------------
FUNCIONES = [
    ("A_sec", ["b", "d", "t"], "b*t + 2*t*(d-t)"),
    ("z_sec", ["b", "d", "t"], "(b*t*t/2 + 2*t*(d-t)*(t+d)/2)/A_sec(b,d,t)"),
    ("I_sec", ["b", "d", "t"], "b*t**3/12 + b*t*(t/2 - z_sec(b,d,t))**2 + 2*(t*(d-t)**3/12 + t*(d-t)*((t+d)/2 - z_sec(b,d,t))**2)"),
    ("Ix_sec", ["b", "d", "t"], "t*b**3/12 + 2*((d-t)*t**3/12 + t*(d-t)*((b-t)/2)**2)"),
    ("Z_sec", ["b", "d", "t"], "I_sec(b,d,t)/max(z_sec(b,d,t), d-z_sec(b,d,t))"),
    ("J_sec", ["b", "d", "t"], "(b + 2*(d-t))*t**3/3"),
    ("M_env", ["x"], "M0*max(1-x/L_luz, x/L_luz) + Q_lado*x*(L_luz-x)/L_luz"),
]

# --- Derivadas y comprobaciones: (nombre, expresion, unidad, nota) ---------------
DERIVADAS = [
    ("L_luz", "apoyo_hombro_y - apoyo_cinturon_y", "mm", "Luz entre apoyos: hombro menos cinturon."),
    ("Fv", "m_total*g*fv", "N", "Fuerza vertical total (hipotesis 3 g)."),
    ("Fh", "m_total*g*fh", "N", "Fuerza horizontal total (hipotesis 1 g)."),
    ("N_lado", "Fv*frac", "N", "Componente vertical del lado mas cargado (reparto 70/30 no medido)."),
    ("Q_lado", "Fh*frac", "N", "Componente horizontal del lado mas cargado."),
    ("M0", "N_lado*excentricidad", "N*mm", "Momento por excentricidad."),
    ("step", "L_luz/800", "mm", "Paso de la malla de 801 puntos usada por el cribado vigente."),
    ("x_cont", "(L_luz - M0/Q_lado)/2", "mm", "Abscisa del maximo continuo de la envolvente."),
    ("i_cont", "floor(x_cont/step)", "", "Indice de malla del maximo continuo."),
    ("x_a", "i_cont*step", "mm", "Punto de malla inmediatamente anterior."),
    ("x_b", "(i_cont+1)*step", "mm", "Punto de malla inmediatamente posterior."),
    ("Mmax", "max(M_env(x_a), M_env(x_b))", "N*mm", "Maximo de la envolvente de momento, misma malla que el cribado vigente."),
    ("x_max", "x_a + (M_env(x_b) > M_env(x_a))*(x_b - x_a)", "mm", "Posicion del maximo."),
    ("GG", "E_al/(2*(1+nu))", "MPa", "Modulo de cortante."),
    ("A_min", "A_sec(B, D, t_min)", "mm**2", "Area de la seccion con pared minima."),
    ("z_min", "z_sec(B, D, t_min)", "mm", "Centroide de la seccion minima."),
    ("I_min", "I_sec(B, D, t_min)", "mm**4", "Inercia principal de la seccion minima."),
    ("Ix_min", "Ix_sec(B, D, t_min)", "mm**4", "Inercia secundaria de la seccion minima."),
    ("Z_min", "Z_sec(B, D, t_min)", "mm**3", "Modulo elastico de la seccion minima."),
    ("J_min", "J_sec(B, D, t_min)", "mm**4", "Constante de torsion de seccion abierta de pared delgada, sin credito de alabeo."),
    ("mlat", "Q_lado*L_luz/4", "N*mm", "Momento flector lateral idealizado; no es una fuerza."),
    ("sig", "N_lado/A_min + K_borde*Mmax/Z_min", "MPa", "Tension axial + flexion."),
    ("sig_biax", "sig + K_borde*mlat*(B/2)/Ix_min", "MPa", "Tension con flexion lateral."),
    ("T", "Q_lado*brazo_torsion", "N*mm", "Par torsionico idealizado."),
    ("tau", "T*t_min/J_min + Q_lado/A_min", "MPa", "Cortante de Saint-Venant + cortante por torsion."),
    ("vm", "sqrt(sig_biax**2 + 3*tau**2)", "MPa", "Tension equivalente de von Mises."),
    ("n_combinado", "Sy_al/vm", "", "Factor de seguridad del refuerzo combinado."),
    ("n_euler", "pi**2*E_al*min(I_min, Ix_min)/(L_luz**2*N_lado)", "", "Pandeo de Euler en el eje debil (ideal articulado)."),
    ("sig_placa", "0.43*pi**2*E_al/(12*(1-nu**2))*(t_min/(D-t_min))**2", "MPa", "Tension de pandeo local del ala sobresaliente (k = 0,43)."),
    ("n_local", "min(Sy_al, sig_placa)/vm", "", "Comprobacion local limitada por min(Sy_al, sig_placa). En el caso base gobierna Sy_al; no demuestra pandeo elastico gobernante."),
    ("Mcr", "pi/L_luz*sqrt(E_al*Ix_min*GG*J_min)", "N*mm", "Momento critico de pandeo lateral torsional ideal."),
    ("n_ltb", "Mcr/Mmax", "", "Pandeo lateral torsional ideal."),
    ("netA", "A_min - 2*t_min*d_taladro", "mm**2", "Area neta en el plano del taladro."),
    ("sig_local", "N_lado/netA + Mmax*abs(z_eje - z_min)/I_min + mlat*(B/2)/Ix_min", "MPa", "Tension local en el taladro."),
    ("n_taladro", "Sy_al/(3*sig_local)", "", "Taladro en alas con K = 3 de cribado."),
    ("reaction", "Mmax/separacion_pernos + Q_lado/2", "N", "Reaccion por union."),
    ("R", "factor_palanca*reaction", "N", "Traccion externa en la union con factor de palanca."),
    ("V_union", "sqrt((N_lado/2)**2 + reaction**2)", "N", "Cortante en la union."),
    ("fb", "1.25*precarga + 0.2*R", "N", "Fuerza maxima en el perno (precarga dispersa 25 %)."),
    ("sb", "fb/As_M5", "MPa", "Tension por precarga en el perno."),
    ("tb", "V_union/As_M5", "MPa", "Tension por cortante en el perno."),
    ("bolt_vm", "sqrt(sb**2 + 3*tb**2)", "MPa", "Tension equivalente en el perno."),
    ("n_perno", "Sy_perno/bolt_vm", "", "Combinacion de precarga y servicio en el M5."),
    ("pin_od_eff", "pasador_od - 0.1*mm", "mm", "SUPUESTO heredado de calcular_p2_05.py:63 y 71: OD nominal 10 menos 0,1 = 9,9 mm. Extremo de estudio; no es medida ni tolerancia de fabricacion aprobada."),
    ("pin_id_eff", "5.6*mm", "mm", "SUPUESTO heredado de calcular_p2_05.py:63 y 71: ID de estudio 5,6 mm frente a nominal 5,5 mm. No es medida ni tolerancia de fabricacion aprobada."),
    ("n_aplast_ala", "Sy_al/(V_union/(t_min*pin_od_eff))", "", "Aplastamiento de una sola ala efectiva."),
    ("n_aplast_mejilla", "Sy_al/(V_union/(t_min*pin_od_eff))", "", "Aplastamiento de una sola mejilla efectiva (3 mm nominal / 2,8 minima)."),
    ("n_arranc", "0.577*Sy_al/(V_union/(2*t_min*(dist_borde_perno - d_taladro/2)))", "", "Arrancamiento del ala en el taladro (dos ligamentos)."),
    ("n_casquillo", "Sy_al/((1.25*precarga)/(pi/4*((casquillo_od-0.1*mm)**2 - (d_taladro+0.1*mm)**2)))", "", "Aplastamiento del casquillo separador por precarga."),
    ("pin_area", "pi/4*(pin_od_eff**2 - pin_id_eff**2)", "mm**2", "Area del pasador hueco."),
    ("pin_Z", "pi/32*(pin_od_eff**4 - pin_id_eff**4)/pin_od_eff", "mm**3", "Modulo elastico del pasador hueco."),
    ("pin_vm", "sqrt((V_union*3.4*mm/pin_Z)**2 + 3*(2*V_union/pin_area)**2)", "MPa", "Tension equivalente del pasador (brazo local 3,4 mm)."),
    ("n_pasador", "Sy_al/pin_vm", "", "Pasador hueco: flexion y cortante."),
    ("washer_sigma", "6*(fb/(2*pi*4*mm))*max(0, d_taladro/2 - 4*mm)/(arandela_esp_min**2)", "MPa", "Flexion local de la arandela en voladizo."),
    ("n_arb_flex", "Sy_arandela/washer_sigma", "", "Arandela: flexion local."),
    ("washer_contact", "sqrt(3)/2*(8*mm)**2 - pi/4*(5.5*mm)**2", "mm**2", "Area de apoyo hexagonal bajo tuerca."),
    ("n_arb_tuerca", "Sy_arandela/(fb/washer_contact)", "", "Arandela: presion bajo tuerca."),
    ("Tstrap", "N_lado/(2*cos(angulo_eslinga))", "N", "Traccion por rama de cuna."),
    ("Tinterface", "max(N_lado/cos(angulo_eslinga), sqrt(N_lado**2 + (Q_lado + M0/L_luz)**2))", "N", "Traccion en el anclaje de arnes/cinturon."),
    ("bridge_M", "Tinterface*luz_puente_cinta/4", "N*mm", "Momento en el puente de anclaje."),
    ("Z_bridge", "esp_anclaje_min*alto_puente_cinta**2/6", "mm**3", "Modulo del puente en la direccion de la correa."),
    ("Z_bridge_out", "alto_puente_cinta*esp_anclaje_min**2/6", "mm**3", "Modulo del puente en la direccion del espesor."),
    ("sbri", "factor_palanca*bridge_M*(cos(angulo_eslinga)/Z_bridge + sin(angulo_eslinga)/Z_bridge_out)", "MPa", "Tension biaxial en el puente de anclaje."),
    ("n_puente_anclaje", "Sy_al/sbri", "", "Puente de anclaje arnes/cinturon."),
    ("cuna_Zin", "esp_anclaje_min*(15*mm)**2/6", "mm**3", "Modulo del puente inferior de cuna."),
    ("cuna_Zout", "(15*mm)*esp_anclaje_min**2/6", "mm**3", "Modulo del puente inferior de cuna (espesor)."),
    ("cuna_sigma", "factor_palanca*(Tstrap*luz_puente_cinta/4)*(cos(angulo_eslinga)/cuna_Zin + sin(angulo_eslinga)/cuna_Zout)", "MPa", "Tension en el puente inferior de cuna."),
    ("n_puente_cuna", "Sy_al/cuna_sigma", "", "Puente inferior de cuna."),
]

RESUMEN = [
    ("n_min", "min(n_combinado, n_euler, n_local, n_ltb, n_taladro, n_perno, n_aplast_ala, n_aplast_mejilla, n_arranc, n_casquillo, n_pasador, n_arb_flex, n_arb_tuerca, n_puente_anclaje, n_puente_cuna)", "", "Minimo de los 15 factores de seguridad del cribado."),
    ("cumple_cribado", "(n_min >= margen_objetivo) and (cierre_residual > 0) and (flecha <= flecha_limite)", "", "Veredicto del cribado: margen objetivo, cierre de junta y flecha."),
    ("flecha", "M0*L_luz**2/(9*sqrt(3)*E_al*I_min) + Q_lado*L_luz**3/(48*E_al*I_min)", "mm", "Flecha de la envolvente."),
    ("giro", "T*L_luz/(GG*J_min)*180/pi", "grados", "Giro torsional ideal."),
    ("cierre_residual", "0.75*precarga - 0.8*R", "N", "Reserva de cierre de junta de la union."),
]

MASA = [
    ("masa_presupuesto", "masa_CAD + reserva_textil + reserva_adicional", "kg", "Presupuesto del sistema sin bomba ni agua."),
    ("masa_brecha_2kg", "masa_presupuesto - 2*kg", "kg", "Brecha hasta el objetivo de 2 kg."),
    ("paquete", "B + 2*esp_mejilla", "mm", "Paquete apilado entre caras exteriores de mejillas."),
    ("L_casq", "B - 2*t_nom", "mm", "Longitud del casquillo tal como la define el generador vigente (B - 2t)."),
    ("holgura_axial", "(B - 2*t_nom) - L_casq", "mm", "Holgura axial nominal entre casquillo y caras interiores de las alas. Resultado: 0,000 mm."),
    ("bajo_cabeza", "paquete + 2*arandela_esp + altura_tuerca", "mm", "Apilado desde debajo de la cabeza del tornillo hasta la cara exterior de la tuerca."),
    ("saliente", "longitud_tornillo - bajo_cabeza", "mm", "Saliente geometrica del tornillo."),
]

# --- Casos de sensibilidad de profundidad (D-14) ----------------------------------
CASOS_D = [("D24", "D"), ("D26", "26*mm"), ("D28", "28*mm")]

CASO_D_DEFS = [
    ("A_{s}", "A_sec(B, {d}, t_min)", "mm**2"),
    ("z_{s}", "z_sec(B, {d}, t_min)", "mm"),
    ("I_{s}", "I_sec(B, {d}, t_min)", "mm**4"),
    ("Ix_{s}", "Ix_sec(B, {d}, t_min)", "mm**4"),
    ("Z_{s}", "Z_sec(B, {d}, t_min)", "mm**3"),
    ("J_{s}", "J_sec(B, {d}, t_min)", "mm**4"),
    ("sig_{s}", "N_lado/A_{s} + K_borde*Mmax/Z_{s}", "MPa"),
    ("sig_biax_{s}", "sig_{s} + K_borde*mlat*(B/2)/Ix_{s}", "MPa"),
    ("tau_{s}", "T*t_min/J_{s} + Q_lado/A_{s}", "MPa"),
    ("vm_{s}", "sqrt(sig_biax_{s}**2 + 3*tau_{s}**2)", "MPa"),
    ("sig_placa_{s}", "0.43*pi**2*E_al/(12*(1-nu**2))*(t_min/({d}-t_min))**2", "MPa"),
    ("n_comb_{s}", "Sy_al/vm_{s}", ""),
    ("n_local_{s}", "min(Sy_al, sig_placa_{s})/vm_{s}", ""),
    ("n_caso_{s}", "min(n_comb_{s}, n_local_{s})", ""),
]


def build():
    ws = Worksheet(
        "SEDAC P2.04-P2.05 - Memoria de calculo de prediseno y preparacion de ensayos",
        "MC01 - 2026-10-25. Prediseno con entradas editables. No es validacion fisica ni tecnica. "
        "Los simbolos de medicion de laboratorio quedan sin definir a proposito.",
    )

    ws.page("0. Como usar esta memoria (para quien llega por primera vez)",
            "Una hoja de calculo que responde: aguanta, y cuanto margen le queda.")
    ws.txt(
        "QUE ES: la memoria de calculo del prototipo SEDAC. Toma la geometria vigente (P2.04), las cargas "
        "de uso y las propiedades del material, y calcula para cada pieza y para cada forma de fallo cuanto "
        "margen queda antes de que algo ceda.\n"
        "QUE NO ES: no es una validacion. No hay ensayos, no hay analisis por elementos finitos y no hay "
        "material comprado. Las cargas que se usan son hipotesis de prediseño declaradas como tales.\n"
        "COMO SE LEE: las celdas con fondo azul son ENTRADAS: se pueden cambiar y todo lo de abajo se "
        "recalcula. A la derecha de cada entrada aparece el valor con su unidad. Las paginas siguen el "
        "orden en que se lee el problema: primero los datos, despues la forma de las piezas, despues las "
        "cargas, despues la resistencia y al final el resumen.\n"
        "COMO SE USA: para cambiar un dato, se edita la entrada, se recalcula con Ctrl+F9 y se vuelve a "
        "mirar el margen minimo de la pagina 9. El archivo entrega guarda los resultados ya calculados, "
        "de modo que se puede revisar sin recalcular.\n"
        "SI FALTA UN DATO: los simbolos que dependen de mediciones de laboratorio (masa de la bomba, centro "
        "de masa, ancho de correa, medidas reales de las piezas) NO estan definidos. Si alguien los usa "
        "sin definirlos, Mathcad marca la expresion como error: es la manera de que la hoja no produzca "
        "un numero inventado. Al definirlos en la pagina 13, se activan los resultados que dependen de "
        "ellos.\n"
        "UNIDADES: se trabaja en mm, N, MPa y kg. Cada constante lleva su unidad escrita para que el "
        "verificador dimensional de Mathcad detecte cualquier mezcla.\n"
        "RESULTADO ACTUAL: con las entradas de hoy, el margen minimo del conjunto es 2,247 y el modo que "
        "gobierna es la fluencia bajo tension combinada: Sy_al = 240 MPa es menor que sig_placa = 477,699 MPa. n_local empata porque usa min(Sy_al, sig_placa), no porque gobierne el pandeo elastico.")

    ws.page("0.1 Glosario de simbolos: que significa cada variable",
            "Todos los simbolos que aparecen en las paginas siguientes, explicados en lenguaje sencillo.")
    glosario = [
        ("L_canal", "mm", "Largo del canal vertical, de la punta de arriba a la de abajo."),
        ("B", "mm", "Ancho exterior del canal, medido de cara a cara."),
        ("D", "mm", "Profundidad del canal: cuanto se hunde la pieza hacia el lado de la bomba."),
        ("t_nom", "mm", "Espesor nominal de la pared del canal, tal como se mecaniza."),
        ("t_min", "mm", "Espesor minimo de pared que se admite para el calculo. Es mas conservador que el nominal y no cambia la pieza."),
        ("z_eje", "mm", "A que altura dentro del canal esta el eje de los taladros de union."),
        ("d_taladro", "mm", "Diametro del agujero por el que pasa el pasador."),
        ("esp_mejilla", "mm", "Espesor de la placa que abraza el canal por fuera."),
        ("L_casq", "mm", "Longitud del casquillo. El generador la define como B - 2t, es decir, exactamente el ancho interior del canal."),
        ("holgura_axial", "mm", "Espacio que queda entre el casquillo y las caras interiores de las alas. Hoy vale cero."),
        ("m_total", "kg", "Masa total que se supone que lleva el sistema. Es una hipotesis de carga, no la masa de la estructura."),
        ("fv, fh", "-", "Cuanto se amplifica la carga de uso respecto del peso quieto: 3 veces en vertical y 1 en horizontal."),
        ("frac", "-", "Parte de la carga que lleva el lado mas cargado (70 %) frente al otro (30 %)."),
        ("excentricidad", "mm", "Distancia entre el eje del canal y el peso de la bomba. Es lo que hace que el canal se doble."),
        ("precarga", "N", "Apriete que se aplica al tornillo de la union antes de que entre la carga de uso."),
        ("margen_objetivo", "-", "Margen minimo que se acepta en el filtro de prediseno. Es un criterio del proyecto, no una norma."),
        ("A_min, Z_min", "mm2, mm3", "Area y modulo elastico de la seccion del canal calculados con la pared minima."),
        ("I_min, Ix_min, J_min", "mm4", "Inercia en los dos planos y constante de torsion de esa seccion."),
        ("N_lado", "N", "Componente vertical de la carga en el lado mas cargado."),
        ("Q_lado", "N", "Componente horizontal de la carga en el lado mas cargado."),
        ("L_luz", "mm", "Distancia entre los dos apoyos: hombro y cinturón."),
        ("M0", "N*mm", "Momento que produce la excentricidad del peso de la bomba."),
        ("Mmax", "N*mm", "Momento maximo al que se ve sometida el canal en el caso de carga mas desfavorable."),
        ("vm", "MPa", "Tension equivalente que resume la combinacion de flexion, cortante y torsion."),
        ("n_min", "-", "El menor de los quince margenes calculados: el que manda."),
        ("flecha", "mm", "Cuanto se desplaza el canal en el punto mas cargado."),
        ("cierre_residual", "N", "Cuanta precarga queda despues de absorber la traccion de la union."),
        ("masa_CAD", "kg", "Masa de la parte rigida, medida en Inventor sobre el modelo entregado."),
        ("masa_presupuesto", "kg", "Masa del sistema sin bomba ni agua, contando las reservas de textiles."),
        ("bajo_cabeza, saliente", "mm", "Apilado de la union por debajo de la cabeza del tornillo, y cuanto sobra de tornillo."),
    ]
    for simbolo, unidad, descripcion in glosario:
        ws.txt("   " + simbolo + "  [" + unidad + "]  -  " + descripcion, 9, color="#253746")

    ws.page("0.2 Glosario de conceptos: que se esta calculando",
            "Las ideas que hay que tener presentes para leer los resultados de la memoria.")
    ws.txt(
        "CRIBado o filtro de prediseño: una lista de comprobaciones que descarta las formas de fallo con "
        "poco margen. Es una criba, no una certificacion: si un margen sale bajo, el diseño se revisa; si "
        "todos salen bien, todavia no se ha probado nada.\n"
        "margen o factor de seguridad: cuantas veces la resistencia disponible supera a la que pide la carga. "
        "Un margen de 2,25 significa que la pieza aguanta 2,25 veces la carga de calculo.\n"
        "modo que gobierna: la forma de fallo que deja menos margen. Si el margen lo fija el pandeo local de "
        "las alas, significa que el punto debil del canal es que las alas se doblen hacia dentro, y no que "
        "se rompan.\n"
        "envolvente de momento: no se calcula un unico caso de carga, sino el peor de una familia de casos "
        "alternativos (el momento puesto en un extremo o en el otro, y la fuerza horizontal en cualquier punto "
        "de la luz). Por eso el resultado es un maximo, no un valor unico.\n"
        "pandeo: que una pieza se deforme por el efecto de una carga de compresion. El pandeo local ocurre "
        "dentro de la pieza (las alas del canal formando una onda) y el pandeo global, cuando la pieza "
        "entera se curva como una barra.\n"
        "precarga: el apriete del tornillo. En una union precargada las piezas no se mueven mientras la carga "
        "de uso es pequeña, y por eso el reparto de fuerzas depende de la rigidez relativa de las piezas, no "
        "solo de sus resistencias.\n"
        "apilamiento axial: la suma de los espesores que el tornillo tiene que atravesar. Si el apilamiento "
        "es mayor que el tornillo, no monta; si es menor, sobra longitud, y esa sobra hay que controlarla.\n"
        "holgura axial: el espacio entre dos piezas que se tocan en la direccion del tornillo. Con cero "
        "holgura, cualquier variacion de fabricacion hace que las piezas se interfieran o que dejen de "
        "apoyar; por eso hay que cerrar la cadena de tolerancias con medidas reales.\n"
        "resistencia frente a rigidez: la resistencia dice cuanto aguanta; la rigidez, cuanto se deforma. Un "
        "material mas rgido puede ser mas pesado y ese es el compromiso central de este prototipo.")

    ws.page("1. Alcance, unidades y estados de los datos",
            "Base P2.04 vigente, parametrizacion P2.05 abierta. Motor de calculo: Mathcad 15 (XMCD clasico).")
    ws.txt(
        "QUE ES ESTE DOCUMENTO: una memoria de calculo de prediseno, editable, del prototipo SEDAC en su "
        "geometria vigente P2.04, con la parametrizacion P2.05 y el mismo modelo analitico que el cribado "
        "vigente del repositorio SEDAC_CAD. Sirve para recalcular el conjunto cuando se incorporen "
        "mediciones reales y para decidir cambios de geometria, material y componentes.\n"
        "QUE NO ES: no es validacion del prototipo. No hay ensayo, no hay FEA, no hay certificacion de "
        "material y no hay liberacion para uso con personas. Los factores de seguridad que se calculan son "
        "de prediseno y dependen de hipotesis de carga no medidas.\n"
        "ESTADOS USADOS: HECHO = verificable con un archivo del repositorio o un comando. MEDIDO = medido en "
        "instrumento, con registro. DATO DE FABRICANTE = declarado por el proveedor. SUPUESTO = valor adoptado "
        "sin medir. HIPOTESIS = condicion aun no comprobada. CALCULADO = resultado de esta hoja. PENDIENTE = sin dato.\n"
        "UNIDADES: se trabaja en mm, N, MPa y kg. Las constantes de entrada llevan su unidad escrita para que "
        "el verificador dimensional de Mathcad actue. Los resultados se muestran en la unidad de lectura propia.\n"
        "MEDIDAS DE LABORATORIO: no existen. Los simbolos que dependerian de ellas NO se definen; definirlos "
        "activa los bloques de verificacion que se describen en las ultimas paginas.")
    ws.txt("ORIGEN DE LOS DATOS DE ENTRADA (solo lectura del repositorio SEDAC_CAD):")
    for ruta in ORIGEN.values():
        ws.txt(ruta, 8, color="#687A88")
    ws.gap(6)
    ws.txt("Verificaciones dimensionales explicitas:", 10, True)
    for nombre, expr, unidad, nota in [
        ("u_fuerza", "1*kg*m/s**2", "N", "Debe equivaler exactamente a 1 N."),
        ("u_fuerza_ratio", "u_fuerza/(1*N)", "", "Debe valer 1 (adimensional)."),
        ("u_presion_ratio", "(1*MPa)/(1*N/mm**2)", "", "Debe valer 1: MPa equivale a N/mm2."),
        ("u_area", "1*mm**2", "mm**2", "Unidad de area."),
        ("u_momento", "1*N*1*mm", "N*mm", "Unidad de momento."),
    ]:
        ws.define(nombre, expr, unit=unidad, height=40, wide=True, note=nota)

    ws.page("2. Entradas geometricas del prototipo vigente",
            "Todas editables. Las marcadas como entrada editable tienen fondo azul en Mathcad.")
    for name, expr, unit, is_in, note in ENTRADAS:
        if name in ("m_total", "g", "fv", "fh", "frac", "excentricidad", "precarga",
                    "angulo_eslinga", "margen_objetivo", "flecha_limite", "K_borde",
                    "K_ventana", "E_al", "Sy_al", "Sy_perno", "Sy_arandela", "masa_CAD",
                    "reserva_textil", "reserva_adicional", "factor_palanca"):
            continue
        ws.define(name, expr, unit=unit, input=is_in, height=40, note=note)

    ws.page("3. Entradas de carga y de material (hipotesis y supuestos)",
            "Ninguna de estas cifras esta medida. D-14 ordena reemplazarlas por masa, reparto y apoyos reales.")
    for name, expr, unit, is_in, note in ENTRADAS:
        if name in ("m_total", "g", "fv", "fh", "frac", "excentricidad", "precarga",
                    "angulo_eslinga", "margen_objetivo", "flecha_limite", "K_borde",
                    "K_ventana", "E_al", "Sy_al", "Sy_perno", "Sy_arandela", "masa_CAD",
                    "reserva_textil", "reserva_adicional", "factor_palanca"):
            ws.define(name, expr, unit=unit, input=is_in, height=40, note=note)

    grupos = {
        "seccion": ("A_min", "z_min", "I_min", "Ix_min", "Z_min", "J_min"),
        "carga": ("L_luz", "Fv", "Fh", "N_lado", "Q_lado", "M0", "step", "x_cont", "i_cont",
                  "x_a", "x_b", "Mmax", "x_max", "GG"),
        "tension": ("mlat", "sig", "sig_biax", "T", "tau", "vm", "n_combinado", "n_euler",
                    "sig_placa", "n_local", "Mcr", "n_ltb", "netA", "sig_local", "n_taladro"),
        "union": ("reaction", "R", "V_union", "fb", "sb", "tb", "bolt_vm", "n_perno",
                  "pin_od_eff", "pin_id_eff", "n_aplast_ala", "n_aplast_mejilla", "n_arranc",
                  "n_casquillo", "pin_area", "pin_Z", "pin_vm", "n_pasador", "washer_sigma",
                  "n_arb_flex", "washer_contact", "n_arb_tuerca"),
        "puente": ("Tstrap", "Tinterface", "bridge_M", "Z_bridge", "Z_bridge_out", "sbri",
                   "n_puente_anclaje", "cuna_Zin", "cuna_Zout", "cuna_sigma", "n_puente_cuna"),
    }
    por_nombre = {nombre: (expr, unit, nota) for nombre, expr, unit, nota in DERIVADAS}

    ws.page("4. Propiedades de la seccion transversal del canal",
            "Seccion en U con alas de 32 x 3 y alma de 24, calculada con pared minima de 2,8 mm (caso conservador).")
    for name, args, expr in FUNCIONES:
        if name == "M_env":
            continue
        ws.fun(name, args, expr, height=52)
    ws.txt("Las funciones A_sec, z_sec, I_sec, Ix_sec, Z_sec y J_sec operan en mm y devuelven mm2, mm, mm4, mm4, mm3 y mm4.")
    ws.gap(4)
    for nombre in grupos["seccion"]:
        expr, unit, nota = por_nombre[nombre]
        ws.define(nombre, expr, unit=unit, height=40, note=nota)

    ws.page("5. Caso de carga y envolvente de momento",
            "Envolvente: momento unico alternado en un extremo y fuerza horizontal de posicion variable en la luz.")
    for nombre in ("L_luz", "Fv", "Fh", "N_lado", "Q_lado", "M0"):
        expr, unit, nota = por_nombre[nombre]
        ws.define(nombre, expr, unit=unit, height=40, note=nota)
    ws.txt(
        "La envolvente reune casos alternativos, no un unico diagrama de cargas simultaneas. La funcion "
        "M_env se declara despues de las cargas porque usa M0, Q_lado y L_luz: en Mathcad una funcion se "
        "evalua en el momento de declararse y no se resuelve si sus variables todavia no existen.")
    for name, args, expr in FUNCIONES:
        if name == "M_env":
            ws.fun(name, args, expr, height=52)
    for nombre in ("step", "x_cont", "i_cont", "x_a", "x_b", "Mmax", "x_max", "GG"):
        expr, unit, nota = por_nombre[nombre]
        ws.define(nombre, expr, unit=unit, height=40, note=nota)
    ws.txt(
        "El maximo se evalua sobre la misma malla de 801 puntos que usa el cribado vigente del repositorio: "
        "se calcula el punto critico continuo y se comparan los dos puntos de malla vecinos, de modo que el "
        "resultado coincide con el barrido numerico sin depender de vectores.")

    ws.page("6. Tensiones, estabilidad y pandeo del refuerzo", "Caso base: seccion con pared minima de 2,8 mm.")
    for nombre in grupos["tension"]:
        expr, unit, nota = por_nombre[nombre]
        ws.define(nombre, expr, unit=unit, height=40, note=nota)
    ws.txt(
        "En el caso base gobierna la fluencia bajo tension combinada; el margen local coincide por el limite de fluencia. El pandeo lateral torsional es ideal y no "
        "acredita pandeo distorsional ni alabeo. Ninguno de estos modos sustituye un analisis de detalle "
        "con las geometrias reales y las ranuras.")

    ws.page("7. Uniones: pasador, casquillo, arandelas y perno M5",
            "Cargas de union deducidas de la envolvente; precarga de estudio hipotetica.")
    for nombre in grupos["union"]:
        expr, unit, nota = por_nombre[nombre]
        ws.define(nombre, expr, unit=unit, height=40, note=nota)
    ws.txt(
        "El pasador transmite cortante; la precarga la aporta el M5 interior. El casquillo es un tope de "
        "compresion entre alas: su funcion depende de la longitud ajustada al interior real. Ninguna de estas "
        "verificaciones cubre roscas, par de apriete, prueba de tuerca autofrenante ni desgaste. "
        "SUPUESTOS heredados de calcular_p2_05.py:63,71: OD efectivo 9,9 mm e ID 5,6 mm. "
        "No son medidas ni tolerancias aprobadas. El taladro de 10,2 mm es otra cota.")

    ws.page("8. Puentes de anclaje y puente inferior de cuna",
            "Cargas de correa con el angulo de eslinga hipotetico y reparto de carga no medido.")
    for nombre in grupos["puente"]:
        expr, unit, nota = por_nombre[nombre]
        ws.define(nombre, expr, unit=unit, height=40, note=nota)
    ws.txt(
        "Se toma la carga completa del lado, no la mitad de la cuna. El reparto real entre ramas de correa "
        "y la rigidez del arnes no estan medidos: son la fuente mas probable de error de este bloque.")

    ws.page("9. Resumen del cribado", "Quince verificaciones, umbral de margen objetivo y cierre de junta.")
    for name, expr, unit, nota in RESUMEN:
        ws.define(name, expr, unit=unit, height=44, note=nota)
    ws.txt(
        "El cribado es un filtro de prediseno, no una verificacion de seguridad. No cubre fatiga, pandeo "
        "distorsional, FEA de detalle, contacto real, abrasion, ergonomia ni liberacion de emergencia.")

    ws.page("10. Masa del conjunto y presupuesto",
            "Masa medida en el CAD de P2.04. La bomba y el arnes real siguen sin medir.")
    for name, expr, unit, nota in MASA[:3]:
        ws.define(name, expr, unit=unit, height=44, note=nota)
    ws.txt(
        "La masa de 1,442328 kg es rigida + protectores, medida por MassProperties en Inventor. El presupuesto "
        "de 2,212328 kg anade la reserva textil de 0,65 kg y 0,12 kg de reserva adicional. NO incluye la bomba "
        "ni el agua. Los 25 kg del caso de carga son hipotesis de carga, no masa de la estructura: no deben "
        "agregarse a la masa del CAD.")

    ws.page("11. Apilamiento axial de la union y cadena de holguras",
            "Revision de la longitud nominal del tornillo y de la holgura axial del casquillo.")
    for name, expr, unit, nota in MASA[3:]:
        ws.define(name, expr, unit=unit, height=44, note=nota)
    ws.txt(
        "La longitud nominal de un tornillo de cabeza cilindrica se mide desde debajo de la cabeza hasta la "
        "punta: la altura de la cabeza no se descuenta del largo disponible. El apilamiento bajo cabeza hasta "
        "la cara exterior de la tuerca es paquete + 2 arandelas + tuerca; la diferencia con la longitud "
        "nominal es la saliente geometrica. La holgura axial del casquillo sale de la definicion vigente "
        "L_casq = B - 2t, es decir, ocupa exactamente el ancho interior: con t > 3 mm aparece holgura negativa. La funcion "
        "documentada del casquillo es actuar como tope de compresion y evitar aplastar las alas durante el "
        "apriete; acortarlo cambia esa funcion y no se justifica sin cerrar la cadena de tolerancias con "
        "medidas reales de B y t.")

    for etiqueta, valor in CASOS_D:
        ws.page("12. Sensibilidad de la profundidad del canal (caso %s)" % etiqueta,
                "D-14 pide sensibilidad a los parametros inciertos antes de FEA, fatiga y pandeo.")
        ws.txt("Profundidad evaluada: " + valor + ". Se mantienen el resto de entradas del caso base.", 9, color="#687A88")
        for plantilla, expr, unit in CASO_D_DEFS:
            nombre = plantilla.replace("{s}", etiqueta)
            cuerpo = expr.replace("{s}", etiqueta).replace("{d}", valor)
            ws.define(nombre, cuerpo, unit=unit, height=40)
    ws.txt(
        "Lectura: aumentar D reduce la tension combinada y tambien la tension critica elastica local del ala. Un margen local mayor no demuestra mayor resistencia elastica al pandeo. El cambio exige reevaluar la altura de mejilla "
        "y desplaza el reparto de cargas entre las uniones. El caso base ya cumple el umbral con "
        "margen estrecho; "
        "cualquier reduccion de pared o de seccion puede llevarla por debajo. La sensibilidad completa, "
        "incluyendo factores de carga, reparto y excentricidad, se hace sobre las cifras medidas, no sobre "
        "hipotesis: por eso las entradas de carga siguen marcadas como hipotesis.")

    ws.page("13. Datos de laboratorio pendientes (simbolos NO definidos)",
            "Definir estos simbolos activa los bloques de verificacion posterior.")
    ws.txt(
        "Simbolos que deben definirse cuando existan mediciones, con su unidad:\n"
        "  m_bomba_vacia, m_bomba_llena   (kg)  masa de la bomba de espalda con y sin agua, con manguera\n"
        "  z_cg_bomba, x_cg_bomba, y_cg_bomba (mm) centro de masa de la bomba llena, medido\n"
        "  m_arnes, z_cg_arnes (kg, mm)      masa y centro de masa del arnes con acolchado\n"
        "  B_med, t_med (mm)                 ancho exterior y espesor real de pared de los canales\n"
        "  L_casq_med (mm)                   longitud real de los casquillos ya ajustados\n"
        "  ancho_cinta, esp_cinta (mm)       ancho y espesor real de las correas\n"
        "  rigidez_correa (N/mm)             rigidez axial medida de la correa\n"
        "  ancho_apoyo_hombro, ancho_apoyo_cinturon (mm)  zonas de apoyo efectiva\n"
        "  recorrido_cinta (mm)              recorrido real de las cintas\n"
        "  IMU_1, IMU_2, ... (datos de sensor) series de IMU crudas con su calibracion\n"
        "Ninguno de estos valores se inventa ni se aproxima con ceros. Si un simbolo permanece indefinido, "
        "cualquier expresion que lo use quedara marcada como error por Mathcad: esa es la deteccion de "
        "entradas incompletas en el motor de calculo.")
    ws.txt(
        "Orden recomendado de incorporacion (D-14 y D-15): 1) masa y centro de masa reales de bomba y arnes; "
        "2) apoyos y zonas de contacto; 3) rigidez y recorrido de correas; 4) B, t y longitudes reales de las "
        "piezas; 5) incorporar los datos de IMU para comparar la respuesta medida contra la respuesta "
        "predicha.")

    ws.page("14. Comparacion entre prediccion y ensayo",
            "Plantilla de cotejo. Los campos de izquierda se llenan con la memoria; los de derecha, con el ensayo.")
    ws.txt(
        "Magnitudes a cotejar tras un ensayo instrumentado:\n"
        "  desplazamiento o flecha en el punto de apoyo        predicho por esta hoja   medido en ensayo   diferencia\n"
        "  inclinacion o giro del conjunto                        predicho                  medido             diferencia\n"
        "  desplazamiento relativo bomba-arnes                    predicho                  medido             diferencia\n"
        "  frecuencia propia del conjunto (ensayo de impacto)     no calculada             medido             -\n"
        "  carga en correa en el punto de anclaje                 predicho por Tinterface   medido con celda   diferencia\n"
        "La prediccion exige un modelo dinamico valido: una IMU con acelerometro y giroscopio entrega fuerza especifica y velocidad angular; no mide directamente "
        "fuerzas. Convertir aceleracion en fuerza exige un modelo dinamico (masa, rigidez, amortiguamiento) "
        "y sus condiciones de validez. La instrumentacion adicional de fuerza o tension es la que permite "
        "cerrar esa cadena; sin ella, la IMU no valida la resistencia del prototipo.")
    ws.txt(
        "Criterio de aceptacion de la comparacion: PENDIENTE de acordar con el profesor de biomecanica. "
        "Debe fijarse antes del ensayo piloto: tolerancia admisible, numero de repeticiones y tratamiento de "
        "la dispersion.")

    ws.page("15. Limites de uso de esta memoria",
            "Lo que la hoja permite y lo que no.")
    ws.txt(
        "PERMITE: recalcular el cribado al cambiar geometria, material, uniones o cargas; obtener el factor "
        "de seguridad de cada modo con la misma hipotesis; ver la sensibilidad a la profundidad; y dejar "
        "registro de que valores se usaron.\n"
        "NO PERMITE: declarar seguridad, resistencia, comodidad o cumplimiento normativo; extrapolar a "
        "personas sin ensayo autorizado; sustituir una FEA de detalle; sustituir la medicion de la bomba, "
        "el arnes, las correas o el contacto.\n"
        "Advertencia sobre la version: esta hoja reproduce el modelo del cribado vigente del repositorio "
        "SEDAC_CAD con la geometria P2.04. Si el generador del CAD cambia, hay que regenerar, volver a medir "
        "la masa en Inventor y recalcular esta hoja; la coherencia entre CAD, memoria y documentos no es "
        "automatica.")

    ws.save(FUENTE)
    control = ws.evaluate_all()
    valores = {}
    for rec in ws.records:
        if rec.get("kind") == "define" and rec["name"] in control and control[rec["name"]] is not None:
            valores[rec["name"]] = control[rec["name"]]
    CONTROL.write_text(json.dumps(valores, indent=2, ensure_ascii=False), encoding="utf-8")
    with (OUT_DIR / "VALORES_ESPERADOS_SI.csv").open("w", encoding="utf-8", newline="") as fh:
        import csv as _csv
        wtr = _csv.writer(fh)
        wtr.writerow(["variable", "valor_SI"])
        for k, v in valores.items():
            if isinstance(v, bool):
                continue
            wtr.writerow([k, repr(v)])
    MANIFIESTO.write_text(json.dumps({
        "memoria": FUENTE.name,
        "formato": "XMCD clasico (worksheet30). Se abre con la instalacion Mathcad 15 de este equipo, "
                   "que se identifica por automatizacion como 14.1.4.587.",
        "manifest": ws.manifest(),
        "entradas_editables": sorted(ws.inputs.keys()),
        "origen_datos": ORIGEN,
        "control_numerico": CONTROL.name,
        "nota": "Sin validacion fisica. Los simbolos de medicion de laboratorio no se definen a proposito.",
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(ws.manifest(), ensure_ascii=False, indent=1))
    print("variables de control:", len(valores))
    for clave in ("Mmax", "vm", "n_min", "n_combinado", "n_local", "flecha", "holgura_axial", "saliente"):
        print("  %-14s = %r" % (clave, valores.get(clave)))


if __name__ == "__main__":
    build()






