"""Trade study de sección del canal (P2.04/P2.05 -> Optimizacion_Real).

Cada alternativa se evalúa ejecutando la COPIA DEL CÁLCULO REAL
(calcular_p2_05.py) con su propio JSON de parámetros. No se reimplementan
ecuaciones: se comparan las salidas del mismo código.

Solo se modifican los campos de sección del canal y la pared mínima de
estudio (nominal - 0.2 mm, mismo criterio que 3 -> 2.8 en P2.05).
Todo lo demás (cargas, materiales, hipótesis) queda idéntico.
"""
from pathlib import Path
import json, subprocess, sys, csv

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PY = sys.executable
CALC = HERE / 'calcular_p2_05.py'

variantes = {
    'V0_base_P2_05': dict(ancho_refuerzo=32, profundidad_refuerzo=24, pared_refuerzo=3.0, pared_minima=2.8),
    'V1_30x26x2.5': dict(ancho_refuerzo=30, profundidad_refuerzo=26, pared_refuerzo=2.5, pared_minima=2.3),
    'V2_32x26x2.5': dict(ancho_refuerzo=32, profundidad_refuerzo=26, pared_refuerzo=2.5, pared_minima=2.3),
    'V3_32x24x2.5': dict(ancho_refuerzo=32, profundidad_refuerzo=24, pared_refuerzo=2.5, pared_minima=2.3),
    'V4_32x28x2.5': dict(ancho_refuerzo=32, profundidad_refuerzo=28, pared_refuerzo=2.5, pared_minima=2.3),
}

base = json.loads((BASE / 'PARAMETROS_BASE.json').read_text(encoding='utf-8-sig'))
out = []

for nombre, sec in variantes.items():
    p = json.loads(json.dumps(base))
    p['geometria'].update(sec)
    pf = BASE / 'Analisis' / f'PARAMETROS_{nombre}.json'
    pf.write_text(json.dumps(p, indent=2, ensure_ascii=False), encoding='utf-8')
    od = BASE / 'Analisis' / nombre
    od.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([PY, str(CALC), str(pf), str(od)], capture_output=True, text=True)
    if r.returncode != 0:
        print(nombre, 'FALLO', r.stderr[-800:])
        continue
    res = json.loads((od / 'RESULTADOS_PREDISENO.json').read_text(encoding='utf-8'))
    s = res['seccion_minima']
    filas = {q['nombre']: q['margen'] for q in res['verificaciones']}
    masa_canal = s['A'] * p['geometria']['alto_refuerzo'] * 2.7e-6
    out.append(dict(
        variante=nombre,
        B=p['geometria']['ancho_refuerzo'], D=p['geometria']['profundidad_refuerzo'],
        t=p['geometria']['pared_refuerzo'], t_min=p['geometria']['pared_minima'],
        area_mm2=round(s['A'], 2), I_mm4=round(s['I'], 1), Z_mm3=round(s['Z'], 1),
        Ix_mm4=round(s['Ix'], 1), J_mm4=round(s['J'], 1),
        masa_canal_kg=round(masa_canal, 6), masa_2canales_kg=round(2 * masa_canal, 6),
        delta_vs_base_g=round((masa_canal - out[0]['masa_canal_kg']) * 2000, 2) if out else 0.0,
        minimo_margen=round(res['minimo_margen'], 4),
        cumple_cribado=res['cumple_cribado'],
        sigma_vm=round(res['sigma_VM_MPa'], 2),
        flecha_mm=round(res['flecha_envolvente_mm'], 3),
        giro_grados=round(res['giro_torsion_ideal_grados'], 3),
        margen_pandeo_local=round(filas.get('Pandeo local de alas', 0), 4),
        margen_pandeo_lt=round(filas.get('Pandeo lateral torsional ideal', 0), 4),
        margen_aplastamiento_ala=round(filas.get('Aplastamiento ala por pasador', 0), 4),
        margen_arrancamiento=round(filas.get('Arrancamiento ala', 0), 4),
        margen_pasador=round(filas.get('Pasador hueco flexion y cortante', 0), 4),
        margen_M5=round(filas.get('M5 combinacion precarga y servicio', 0), 4),
        margen_casquillo=round(filas.get('Casquillo compresion', 0), 4),
        fallos=', '.join(q['nombre'] for q in res['verificaciones'] if not q['cumple']),
    ))
    print(nombre, 'ok')

with (BASE / 'Analisis' / 'COMPARACION_ALTERNATIVAS.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)
(BASE / 'Analisis' / 'COMPARACION_ALTERNATIVAS.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
for o in out:
    print(f"{o['variante']:16s} A={o['area_mm2']:6.1f} Z={o['Z_mm3']:6.1f} 2canales={o['masa_2canales_kg']:.4f}kg "
          f"margen={o['minimo_margen']:.3f} cumple={o['cumple_cribado']} {o['fallos']}")
