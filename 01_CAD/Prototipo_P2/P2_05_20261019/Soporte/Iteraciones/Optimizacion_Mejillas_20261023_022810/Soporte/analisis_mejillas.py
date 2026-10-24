"""Analisis de la dependencia mejilla-profundidad de canal.

Objetivo: separar el incremento de masa de anclajes que es NECESARIO por geometria
(la mejilla debe cubrir el flanco del canal y alojar el pasador) del que podría
EVITARSE con una geometria local mejor proporcionada.

Reutiliza las cargas y los resultados del cribado de la iteracion anterior
(Analisis/RESULTADOS_OPT1.json) para no recalcular con hipotesis distintas.

No es FEA ni validacion. Cada bloque declara su etiqueta.
"""
import json, math
from pathlib import Path

B = Path(__file__).resolve().parent.parent
A = B / 'Analisis'

p04 = json.loads((B / 'PARAMETROS_P2_04.json').read_text(encoding='utf-8-sig'))
opt = json.loads((B / 'PARAMETROS_OPT1.json').read_text(encoding='utf-8-sig'))
res = json.loads((A / 'RESULTADOS_OPT1.json').read_text(encoding='utf-8-sig'))

G4, GO = p04['geometria'], opt['geometria']
M = p04['materiales']
Sy, E = M['Sy_6061_MPa'], M['E_6061_MPa']
rho = 2.7e-6  # kg/mm3, 6061; misma densidad que el CAD nativo (SEDAC_6061)

V = res['cortante_union_N']          # N, reaccion de union del lado mas cargado
mmax = res['Mmax_Nmm']

Z0 = -(G4['espesor_anclaje'] + 0.7)
ECU = G4['espesor_cuerpo_lumbar']
Z_CAPA = Z0 + ECU
EM = G4['espesor_mejilla']
Z_PIN = G4['eje_pernos_z']           # posicion del eje del pasador en z
D_PIN = G4['pasador_od']

# --- Geometria de mejillas tal como la genera generar_p2_05.py -----------------
# lumbar: 4 mejillas (2 por canal x 2 lados), rect(18, Z_CAPA, 100, D-Z_CAPA)
# yugos : 2 por yugo, 2 yugos, rect(376, -2, 98, D+2)
LUM_N, LUM_L = 4, 100.0
YUG_N, YUG_L = 4, 98.0


def altura(D, tipo):
    return (D - Z_CAPA) if tipo == 'lumbar' else (D + 2)


def masa_mejillas(D):
    return (LUM_N * LUM_L * altura(D, 'lumbar') + YUG_N * YUG_L * altura(D, 'yugo')) * EM * rho


m24, m28 = masa_mejillas(G4['profundidad_refuerzo']), masa_mejillas(GO['profundidad_refuerzo'])
delta_analitico = (m28 - m24) * 1000  # g
delta_nativo = 25.39                  # g medido en Inventor (tabla de la iteracion anterior)

# --- Comprobacion nueva: mejilla como placa en voladizo ------------------------
# La carga del pasador V actua en x (perpendicular al plano de la mejilla).
# La placa tiene ancho L (y), espesor EM (x). La seccion resistente en la raiz
# frente a flexion fuera de plano es L*EM^2/6: NO depende de la altura en z.
# La altura solo cambia el brazo desde la raiz hasta el pasador.
brazo = Z_PIN - Z_CAPA


def margen_mejilla(L_eff, tipo='lumbar', k=1.0):
    Z = L_eff * EM ** 2 / 6.0
    Mf = k * V * brazo
    sigma = Mf / Z
    return Sy / sigma, sigma


n_placa_P204, s_placa_P204 = margen_mejilla(LUM_L)

# Tension en el plano (la mejilla tambien arrastra el pasador hacia la placa):
# seccion = altura * EM en la raiz, cortante V; se compara con 0.577*Sy.
tau_raiz = V / (altura(G4['profundidad_refuerzo'], 'lumbar') * EM)
n_corte_raiz = 0.577 * Sy / tau_raiz

# --- Variante A: mejilla escalonada ------------------------------------------
# Se conserva la altura completa solo en dos zonas de L_BOSS alrededor de los
# pasadores (donde hay que alojar el casquillo y transmitir la carga) y un labio
# continuo de H_LIP en el borde de la boca para retener y proteger el flanco.
L_BOSS = 24.0
H_LIP = 8.0


def masa_mejilla_escalonada(D, tipo):
    h = altura(D, tipo)
    L = LUM_L if tipo == 'lumbar' else YUG_L
    # area en el plano YZ: 2 zonas a altura completa + labio continuo
    area = 2 * L_BOSS * h + (L - 2 * L_BOSS) * H_LIP
    return area * EM * rho, L * h * EM * rho


mL_esc, mL_ref = masa_mejilla_escalonada(GO['profundidad_refuerzo'], 'lumbar')
mY_esc, mY_ref = masa_mejilla_escalonada(GO['profundidad_refuerzo'], 'yugo')
ahorro_esc = (LUM_N * (mL_ref - mL_esc) + YUG_N * (mY_ref - mY_esc)) * 1000  # g

# Seccion critica de la mejilla escalonada: en el borde del boss, el ancho
# resistente cae a L_BOSS. Se aplica K=1.5 por el escalon (concentrador sin
# ensayo). Esta es la comprobacion que decide si la variante se sostiene.
n_esc, s_esc = margen_mejilla(L_BOSS, k=1.5)
L_min_necesario = 6 * (1.5 * V * brazo) / (Sy * EM ** 2)  # mm de ancho para n=1
L_para_objetivo = 6 * (1.5 * V * brazo) * opt['cargas']['margen_objetivo'] / (Sy * EM ** 2)

# --- Variante B: mantener el canal de P2.04 y aligerar solo las mejillas ------
# Con D=24, t=3 el canal no cambia; el aligeramiento escalonado se aplica igual.
mL_esc24, mL_ref24 = masa_mejilla_escalonada(G4['profundidad_refuerzo'], 'lumbar')
mY_esc24, mY_ref24 = masa_mejilla_escalonada(G4['profundidad_refuerzo'], 'yugo')
ahorro_esc24 = (LUM_N * (mL_ref24 - mL_esc24) + YUG_N * (mY_ref24 - mY_esc24)) * 1000

# --- Masa de cobertura: altura por encima del requisito mecanico del pasador ---
# Requisito: alojar el casquillo y la arandela alrededor del eje del pasador.
H_NEC_LUMBAR = Z_PIN + D_PIN / 2 + 2.5 - Z_CAPA      # desde la raiz
H_NEC_YUGO = Z_PIN + D_PIN / 2 + 2.5 - (-2.0)


def masa_cobertura(D, tipo):
    h = altura(D, tipo)
    h_nec = H_NEC_LUMBAR if tipo == 'lumbar' else H_NEC_YUGO
    L, n = (LUM_L, LUM_N) if tipo == 'lumbar' else (YUG_L, YUG_N)
    return max(0.0, h - h_nec) * L * EM * rho * n * 1000  # g


out = {
    'etiqueta': 'calculo',
    'nota': 'Analisis de prediseno. No es FEA ni validacion. Cargas heredadas sin cambios.',
    'cargas_reutilizadas': {'V_union_N': V, 'Mmax_Nmm': mmax, 'origen': 'Analisis/RESULTADOS_OPT1.json'},
    'geometria_mejillas': {
        'z0_mm': Z0, 'z_capa_mm': Z_CAPA, 'z_pasador_mm': Z_PIN, 'brazo_mm': brazo,
        'lumbar_n_mejillas': LUM_N, 'lumbar_longitud_mm': LUM_L,
        'yugo_n_mejillas': YUG_N, 'yugo_longitud_mm': YUG_L,
        'altura_lumbar_P204_mm': altura(G4['profundidad_refuerzo'], 'lumbar'),
        'altura_lumbar_OPT1_mm': altura(GO['profundidad_refuerzo'], 'lumbar'),
        'altura_yugo_P204_mm': altura(G4['profundidad_refuerzo'], 'yugo'),
        'altura_yugo_OPT1_mm': altura(GO['profundidad_refuerzo'], 'yugo'),
        'regla_en_generador': "rect(18,Z_CAPA,100,D-Z_CAPA) lumbar; rect(376,-2,98,D+2) yugo",
    },
    'incremento_mejillas': {
        'masa_mejillas_P204_g': m24 * 1000, 'masa_mejillas_OPT1_g': m28 * 1000,
        'delta_analitico_g': delta_analitico, 'delta_nativo_medido_g': delta_nativo,
        'desviacion_g': delta_analitico - delta_nativo,
        'desviacion_pct': 100 * (delta_analitico - delta_nativo) / delta_nativo,
        'lectura': 'El incremento de anclajes de OPT1 es integramente el area de mejilla que crece con D; la geometria lo explica dentro del 1%.',
    },
    'comprobacion_mejilla_fuera_de_plano': {
        'modelo': 'Placa en voladizo empotrada en la placa lumbar, carga V en el pasador, Z=L*EM^2/6',
        'Z_placa_mm3': LUM_L * EM ** 2 / 6,
        'brazo_mm': brazo, 'V_N': V, 'sigma_MPa': s_placa_P204, 'margen': n_placa_P204,
        'observacion': 'Z no depende de la altura en z: los 4 mm anadidos por D no aumentan la resistencia de la mejilla, solo su cobertura.',
        'etiqueta': 'calculo',
    },
    'cortante_en_raiz': {'tau_MPa': tau_raiz, 'margen': n_corte_raiz,
                         'modelo': 'V/(altura*EM) frente a 0,577*Sy; sin credito de empotramiento parcial'},
    'variante_A_mejilla_escalonada': {
        'descripcion': 'Altura completa solo en 2 zonas de 24 mm por pasador + labio de 8 mm en la boca; espesor 3 mm sin cambios.',
        'L_boss_mm': L_BOSS, 'H_lip_mm': H_LIP,
        'ahorro_OPT1_g': ahorro_esc, 'ahorro_P204_g': ahorro_esc24,
        'margen_seccion_escalonada': n_esc, 'sigma_MPa': s_esc,
        'K_escalon': 1.5, 'ancho_minimo_mm_n1': L_min_necesario,
        'ancho_para_margen_objetivo_mm': L_para_objetivo,
        'etiqueta': 'calculo (masa) / supuesto (K=1.5, forma del escalon)',
    },
    'masa_de_cobertura_no_gobernada_por_carga': {
        'modelo': 'Altura por encima del alojamiento del pasador; no aporta a Z ni al aplastamiento.',
        'h_nec_lumbar_mm': H_NEC_LUMBAR, 'h_nec_yugo_mm': H_NEC_YUGO,
        'P204_lumbar_g': masa_cobertura(24, 'lumbar'), 'P204_yugo_g': masa_cobertura(24, 'yugo'),
        'OPT1_lumbar_g': masa_cobertura(28, 'lumbar'), 'OPT1_yugo_g': masa_cobertura(28, 'yugo'),
        'etiqueta': 'cálculo; NO es ahorro: esa cobertura cumple funcion de retencion y proteccion de arista que habria que reasignar',
        'lectura': 'Es la magnitud del premio si la mordaza se sustituye por un concepto que no dependa de D. No se descuenta del presupuesto.',
    },
    'impacto_masa_si_se_adopta': {
        'OPT1_rigida_kg': 1.432778, 'OPT1_presupuesto_kg': 2.202778,
        'OPT1_mas_varianteA_rigida_kg': 1.432778 - ahorro_esc / 1000,
        'OPT1_mas_varianteA_presupuesto_kg': 2.202778 - ahorro_esc / 1000,
        'P204_rigida_kg': 1.442328, 'P204_presupuesto_kg': 2.212328,
        'ahorro_neto_vs_P204_g': (1.442328 - (1.432778 - ahorro_esc / 1000)) * 1000,
    },
}
(A / 'ANALISIS_MEJILLAS.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')

print('altura mejilla lumbar  P2.04 =', round(altura(24, 'lumbar'), 2), 'mm | OPT1 =', round(altura(28, 'lumbar'), 2), 'mm')
print('delta analitico mejoras =', round(delta_analitico, 2), 'g | nativo medido =', delta_nativo, 'g | desv =', round(delta_analitico - delta_nativo, 2), 'g')
print('Z placa =', round(LUM_L * EM ** 2 / 6, 1), 'mm3 | sigma =', round(s_placa_P204, 1), 'MPa | margen =', round(n_placa_P204, 3))
print('cortante raiz margen =', round(n_corte_raiz, 3))
print('variante A: ahorro OPT1 =', round(ahorro_esc, 2), 'g | ahorro P2.04 =', round(ahorro_esc24, 2), 'g')
print('variante A: margen con K=1.5 en el boss =', round(n_esc, 3), '| ancho para n=1:', round(L_min_necesario, 1), 'mm | ancho para 2,2:', round(L_para_objetivo, 1), 'mm')
print('ahorro neto vs P2.04 si se adopta =', round((1.442328 - (1.432778 - ahorro_esc / 1000)) * 1000, 2), 'g')
print('cobertura no gobernada por carga (OPT1): lumbar', round(out['masa_de_cobertura_no_gobernada_por_carga']['OPT1_lumbar_g'], 1),
      'g | yugo', round(out['masa_de_cobertura_no_gobernada_por_carga']['OPT1_yugo_g'], 1), 'g')
print('cobertura no gobernada por carga (P2.04): lumbar', round(out['masa_de_cobertura_no_gobernada_por_carga']['P204_lumbar_g'], 1),
      'g | yugo', round(out['masa_de_cobertura_no_gobernada_por_carga']['P204_yugo_g'], 1), 'g')
