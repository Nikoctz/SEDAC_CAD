"""
comparar_control.py — coteja el control numerico de la memoria nueva (SI) contra los
resultados publicados del cribado vigente en el repositorio SEDAC_CAD (V0_base_P2_05).

Solo lectura del repositorio. Genera COMPARACION_CONTROL_VS_REPO.json y una tabla por consola.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(r"C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD")
V0 = (REPO / "01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Optimizacion_Real_20261023_014225"
      / "Analisis/V0_base_P2_05/RESULTADOS_PREDISENO.json")

control = json.loads((HERE / "VALORES_ESPERADOS_SI.json").read_text(encoding="utf-8"))
repo = json.loads(V0.read_text(encoding="utf-8"))

# nombre del control -> (nombre en el JSON del repo, factor para pasar de SI a la unidad del repo)
MAPA = {
    "Mmax": ("Mmax_Nmm", 1000.0),
    "vm": ("sigma_VM_MPa", 1e-6),
    "flecha": ("flecha_envolvente_mm", 1000.0),
    "giro": ("giro_torsion_ideal_grados", 1.0),
    "cierre_residual": ("cierre_residual_junta_N", 1.0),
    "V_union": ("cortante_union_N", 1.0),
    "R": ("traccion_externa_union_N", 1.0),
    "fb": ("fuerza_max_perno_N", 1.0),
    "pin_vm": ("pasador_sigma_VM_MPa", 1e-6),
    "Tstrap": ("T_por_rama_cuna_N", 1.0),
    "Tinterface": ("T_anclaje_arnes_cinturon_N", 1.0),
    "masa_presupuesto": (None, 1.0),
}

MARGENES = {
    "n_combinado": "Refuerzo combinado, pared minima",
    "n_euler": "Pandeo Euler, eje debil",
    "n_local": "Pandeo local de alas",
    "n_ltb": "Pandeo lateral torsional ideal",
    "n_taladro": "Taladro en alas, tension local",
    "n_perno": "M5 combinacion precarga y servicio",
    "n_aplast_ala": "Aplastamiento ala por pasador",
    "n_aplast_mejilla": "Aplastamiento mejilla por pasador",
    "n_arranc": "Arrancamiento ala",
    "n_casquillo": "Casquillo compresion",
    "n_pasador": "Pasador hueco flexion y cortante",
    "n_arb_flex": "Arandela gruesa flexion local",
    "n_arb_tuerca": "Arandela presion bajo tuerca",
    "n_puente_anclaje": "Puente anclaje arnes/cinturon biaxial",
    "n_puente_cuna": "Puente inferior de cuna",
}

repo_margenes = {v["nombre"]: v["margen"] for v in repo.get("verificaciones", [])}

filas = []
for clave, (nombre_repo, factor) in MAPA.items():
    if nombre_repo is None or clave not in control:
        continue
    c = control[clave] * factor
    r = repo[nombre_repo]
    filas.append(dict(tipo="magnitud", variable=clave, control=c, repo=r,
                      error_relativo=abs(c - r) / max(1e-12, abs(r))))

for clave, nombre_repo in MARGENES.items():
    if clave not in control or nombre_repo not in repo_margenes:
        continue
    c = control[clave]
    r = repo_margenes[nombre_repo]
    filas.append(dict(tipo="margen", variable=clave, control=c, repo=r,
                      error_relativo=abs(c - r) / max(1e-12, abs(r))))

peor = max(filas, key=lambda f: f["error_relativo"])
print("%-22s %18s %18s %12s" % ("variable", "control", "repo", "error rel."))
for f in filas:
    print("%-22s %18.9g %18.9g %12.3g" % (f["variable"], f["control"], f["repo"], f["error_relativo"]))
print()
print("peor error relativo: %.3g (%s)" % (peor["error_relativo"], peor["variable"]))
print("todas las magnitudes dentro de 1e-9:", all(f["error_relativo"] < 1e-9 for f in filas))

(HERE / "COMPARACION_CONTROL_VS_REPO.json").write_text(
    json.dumps({"cotejo": filas, "peor_error_relativo": peor["error_relativo"],
                "referencia": str(V0)}, indent=2, ensure_ascii=False), encoding="utf-8")
