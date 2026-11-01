"""
Calculos de prediseno P0 (v2, pivote con tornillo de hombro ISO 7379 M6).
Resistencia de materiales con formulas simplificadas. NO es FEA, NO es una
validacion y NO establece un factor de seguridad admisible.

Salida: EVIDENCIAS/calculos_p0.json
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVI = ROOT / "EVIDENCIAS"
EVI.mkdir(parents=True, exist_ok=True)

g = 9.81
m_sup = 20.0
F_tot = m_sup * g          # 196.2 N (masa SUPUESTA)
F_2 = F_tot / 2            # 98.1 N (reparto IDEAL entre 2 conexiones)
k_dyn = 2.0                # SUPUESTO de prediseno, NO normativo
F_d = F_tot * k_dyn        # 392.4 N (carga concentrada en una conexion)

# --- geometria (debe coincidir con modelo_p0.py) ---
T = 9.0                    # espesor de las placas
ARM_SPINE_B = 9.0          # ancho del refuerzo de la espina (X)
ARM_BASE_B = 6.0           # brazo basico
SEC_H = 9.0                # profundidad de seccion en Y
BORE = 6.2                 # agujero del cubo y tetones
HUB_H = 9.0                # longitud de apoyo del cubo
LUG_T = 3.3                # espesor de cada teton (segun modelo P0)
LUG_W = 11.0               # ancho del teton (X)
E_AXLE = 6.5               # excentricidad eje de giro - centro de canasta (SUPUESTO por geometria)
R_BASKET = 7.5
PIN_D = 4.0                # pasador de cierre
PIN_B = 6.0                # espesor de material atravesado por el pasador

# --- resistencias de referencia (fichas, NO admisibles) ---
REF = dict(
    petg_xy=39.0,     # MPa Prusament PETG V0, probeta impresa horizontal
    petg_z=16.4,      # MPa Prusament PETG V0, adherencia interlaminar
    pa6cf_xy=105.0,   # MPa Fiberon PA6-CF20
    pa6cf_z=67.7,     # MPa Fiberon PA6-CF20
    a2_shear=0.6 * 210.0,   # MPa, criterio elastico aprox. acero A2 (no admisible)
)

res = []


def add(modo, F, geom, sigma, tipo, nota, controla=False):
    res.append(dict(
        modo=modo, F_N=round(F, 2), geometria=geom,
        sigma_MPa=round(sigma, 2), tipo=tipo, nota=nota, controla=controla,
    ))


# 1. tornillo de hombro en cortante doble
A_ds = 2 * math.pi / 4 * BORE**2
add("Tornillo Ø6 (hombro) en cortante doble", F_d, f"A = 2·π/4·{BORE}² = {A_ds:.1f} mm²",
    F_d / A_ds, "cortante",
    "El herraje es acero A2; el tornillo no es el elemento critico. Se muestra "
    "solo para descartar el modo.")

# 2. presion de contacto en el cubo impreso
A_bear_hub = BORE * HUB_H
add("Presion de contacto cubo (PETG) sobre hombro Ø6", F_d,
    f"A = {BORE}·{HUB_H} = {A_bear_hub:.1f} mm²", F_d / A_bear_hub, "contacto",
    "Presion proyectada; supone contacto uniforme en toda la longitud.")

# 3. presion en cada teton (la carga se reparte entre dos tetones)
A_bear_lug = BORE * LUG_T
add("Presion de contacto por teton (2 tetones)", F_d / 2,
    f"A = {BORE}·{LUG_T} = {A_bear_lug:.1f} mm²", (F_d / 2) / A_bear_lug,
    "contacto", "Reparto 50/50 entre tetones, supuesto.")

# 4. seccion neta del teton (arrancamiento)
A_net = (LUG_W - BORE) * LUG_T
add("Seccion neta del teton (arrancamiento por el agujero)", F_d / 2,
    f"A = ({LUG_W}-{BORE})·{LUG_T} = {A_net:.1f} mm²", (F_d / 2) / A_net,
    "traccion", "Traccion sobre la seccion debilitada por el agujero; "
                "no incluye concentracion de esfuerzo (Kt > 1).")

# 5. flexion de la espina por excentricidad del eje de giro
M_sp = F_tot * E_AXLE
W_sp = ARM_SPINE_B * SEC_H**2 / 6
add("Flexion de la espina por excentricidad e = 6,5 mm (carga estatica)", F_tot,
    f"M = {F_tot:.1f}·{E_AXLE} = {M_sp:.0f} N·mm; W = {ARM_SPINE_B}·{SEC_H}²/6 "
    f"= {W_sp:.1f} mm³", M_sp / W_sp, "flexion",
    "Seccion 9 x 9 mm (con refuerzo). Modelo de viga; no incluye entallas.",
    controla=True)

M_spd = F_d * E_AXLE
add("Flexion de la espina, caso conservador (k = 2)", F_d,
    f"M = {F_d:.1f}·{E_AXLE} = {M_spd:.0f} N·mm", M_spd / W_sp, "flexion",
    "Mismo modelo con la carga concentrada y factor dinamico supuesto.",
    controla=True)

# 6. arco de canasta (media circunferencia cargada en la clave)
M_arch = 0.32 * F_tot * R_BASKET
W_arm = ARM_BASE_B * SEC_H**2 / 6
sig_arch = M_arch / W_arm + F_tot / (ARM_BASE_B * SEC_H)
add("Arco de canasta (media circunferencia, apoyo en brazos)", F_tot,
    f"M = 0,32·{F_tot:.1f}·{R_BASKET} = {M_arch:.0f} N·mm; W = {W_arm:.1f} mm³",
    sig_arch, "flexion+axial",
    "Coeficiente 0,32 para arco semicircular con carga en la clave: aproximado. "
    "Superpone flexion y compresion de forma conservadora.")

# 7. pasador de cierre en cortante doble
A_pin = 2 * math.pi / 4 * PIN_D**2
add("Pasador de cierre Ø4 en cortante doble", F_d, f"A = 2·π/4·4² = {A_pin:.1f} mm²",
    F_d / A_pin, "cortante", "Acero; solo trabaja si la argolla de la bolsa "
                             "empuja el cierre desde el interior.")

# 8. torsion si la cinta no queda alineada con el eje
e_tors = 10.0
Tq = F_tot * e_tors
tau = 16 * Tq / (math.pi * (SEC_H**3))
add("Torsion del cuello de la argolla (e supuesta 10 mm)", F_tot,
    f"T = {Tq:.0f} N·mm; seccion circular equiv. Ø{SEC_H}", tau,
    "torsion", "Excentricidad SUPUESTA; indica que la cinta debe quedar "
               "centrada sobre el eje de giro.")

out = dict(
    entradas=dict(masa_sup_kg=m_sup, g=g, F_total_N=round(F_tot, 2),
                  F_dos_conexiones_N=round(F_2, 2), k_dinamico_supuesto=k_dyn,
                  F_diseno_N=round(F_d, 2),
                  excentricidad_eje_mm=E_AXLE),
    resistencias_referencia_MPa=REF,
    resultados=res,
    factor_seguridad="PENDIENTE: no hay admisibles trazables para la pieza "
                     "impresa (dependen de orientacion, relleno, temperatura y "
                     "proceso). No se declara.",
    aviso="Calculos de prediseno con formulas simplificadas. No sustituyen "
          "ensayos ni FEA. Ningun valor aqui es una validacion del producto.",
)
(EVI / "calculos_p0.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                     encoding="utf-8")

print(f"{'Modo':62s}{'F [N]':>8s}{'sigma [MPa]':>13s}")
print("-" * 83)
for r in res:
    print(f"{r['modo'][:61]:62s}{r['F_N']:8.1f}{r['sigma_MPa']:13.2f}"
          + ("   <-- controla" if r["controla"] else ""))
print()
print(f"F_estatica = {F_tot:.1f} N | F_conservadora (k={k_dyn}) = {F_d:.1f} N")
print("Referencia PETG XY %.1f MPa / Z %.1f MPa (NO admisibles)" %
      (REF['petg_xy'], REF['petg_z']))
for r in res:
    if r["controla"]:
        print(f"  {r['modo']}: sigma_z/ref_XY = {REF['petg_xy']/r['sigma_MPa']:.2f} "
              f"| ref_Z/sigma = {REF['petg_z']/r['sigma_MPa']:.2f}")
