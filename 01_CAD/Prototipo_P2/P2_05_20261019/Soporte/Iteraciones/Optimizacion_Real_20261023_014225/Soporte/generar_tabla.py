"""Genera TABLA_MASAS.md desde datos, sin aritmetica manual.

Antes  : P2_04_20261016/BOM_Y_MASAS.csv (masas CAD nativas de la entrega vigente)
Despues: Build/MASAS_CAD.json (masas nativas de esta corrida)
"""
from pathlib import Path
import csv, json

BASE = Path(__file__).resolve().parent.parent
P204 = BASE.parents[3] / 'P2_04_20261016'

antes = {}
for r in csv.DictReader((P204 / 'BOM_Y_MASAS.csv').open(encoding='utf-8-sig')):
    antes[r['pieza']] = dict(m=float(r['masa_unitaria_kg']), n=float(r['cantidad']),
                             mat=r['material'], grupo=r['grupo'], ref=(r['referencia'].strip().lower()=='true'))

desp = {}
for d in json.loads((BASE / 'Build' / 'MASAS_CAD.json').read_text(encoding='utf-8-sig')):
    desp[d['pieza']] = dict(m=float(d['masa_candidata_kg']), n=float(d['cantidad']),
                            mat=d['material'], grupo=d['grupo'], ref=bool(d['referencia']))

def total(d, ref=False):
    return sum(v['m'] * v['n'] for v in d.values() if v['ref'] == ref)

grupos = sorted({v['grupo'] for v in list(antes.values())+list(desp.values())})
ga = {g: sum(v['m'] * v['n'] for v in antes.values() if v['grupo'] == g and not v['ref']) for g in grupos}
gd = {g: sum(v['m'] * v['n'] for v in desp.values() if v['grupo'] == g and not v['ref']) for g in grupos}

ra, rd = total(antes), total(desp)
va, vd = total(antes, True), total(desp, True)
TEXTIL, RESERVA = 0.65, 0.12

L = []
L.append('# Tabla de masa — antes / después (masas nativas de Inventor)')
L.append('')
L.append('**Antes:** `P2_04_20261016/BOM_Y_MASAS.csv` — masa CAD nativa de la entrega vigente.')
L.append('**Después:** `Build/MASAS_CAD.json` — masa nativa medida en esta corrida.')
L.append('**Materiales:** 6061-T6 (ρ = 2,7 g/cm³) en estructura, anclajes y uniones; HDPE 0,953 g/cm³ en la')
L.append('espaldera; acero en fijaciones; textil 0,75 y espuma en las referencias visuales. El constructor crea un')
L.append('material `SEDAC_<material>` con la densidad del JSON y **rechaza la pieza si la masa nativa no coincide**')
L.append('con volumen × densidad, de modo que no se usó el material predeterminado de Inventor.')
L.append('')
L.append('## 1. Masa rígida y protectores por grupo')
L.append('')
L.append('| Grupo | Antes (kg) | Después (kg) | Δ (g) | n piezas |')
L.append('|---|---:|---:|---:|---:|')
for g in sorted([x for x in grupos if ga.get(x,0) or gd.get(x,0)], key=lambda x: -ga[x]):
    na = int(sum(v['n'] for v in antes.values() if v['grupo'] == g and not v['ref']))
    L.append(f'| {g} | {ga[g]:.6f} | {gd[g]:.6f} | {(gd[g]-ga[g])*1000:+.2f} | {na} |')
L.append(f'| **Total rígida + protectores** | **{ra:.6f}** | **{rd:.6f}** | **{(rd-ra)*1000:+.2f}** | 54 |')
L.append('')
L.append(f'Referencias visuales (textiles, acolchados, herrajes textiles): {va:.6f} → {vd:.6f} kg.')
L.append('No se suman al presupuesto: ese papel lo cumple la reserva textil de 0,65 kg.')
L.append('')
L.append('## 2. Presupuesto del sistema auxiliar (sin bomba ni agua)')
L.append('')
L.append('| Concepto | Antes (kg) | Después (kg) | Δ (g) |')
L.append('|---|---:|---:|---:|')
L.append(f'| Rígida + protectores | {ra:.6f} | {rd:.6f} | {(rd-ra)*1000:+.2f} |')
L.append(f'| Arnés / textiles (reserva) | {TEXTIL:.6f} | {TEXTIL:.6f} | 0,00 |')
L.append(f'| Reserva adicional | {RESERVA:.6f} | {RESERVA:.6f} | 0,00 |')
L.append(f'| **Total** | **{ra+TEXTIL+RESERVA:.6f}** | **{rd+TEXTIL+RESERVA:.6f}** | **{(rd-ra)*1000:+.2f}** |')
L.append('')
L.append('## 3. Piezas que cambian (el resto es idéntico)')
L.append('')
L.append('| Pieza | n | Material | Antes (kg/u) | Después (kg/u) | Δ total (g) |')
L.append('|---|---:|---|---:|---:|---:|')
cambios = [(p, (desp[p]['m'] - antes[p]['m']) * antes[p]['n']) for p in antes
           if p in desp and abs(desp[p]['m'] - antes[p]['m']) > 1e-9]
for p, d in sorted(cambios, key=lambda x: x[1]):
    L.append(f'| {p} | {int(antes[p]["n"])} | {antes[p]["mat"]} | {antes[p]["m"]:.6f} | {desp[p]["m"]:.6f} | {d*1000:+.2f} |')
L.append(f'| **Suma de los cambios** | | | | | **{sum(d for _, d in cambios)*1000:+.2f}** |')
L.append('')
L.append('## 4. Lectura')
L.append('')
canal = (desp['Refuerzo_C_I']['m'] + desp['Refuerzo_C_D']['m']) - (antes['Refuerzo_C_I']['m'] + antes['Refuerzo_C_D']['m'])
anc = gd['anclajes'] - ga['anclajes']
L.append(f'- El canal aporta {canal*1000:+.2f} g. El resto del conjunto aporta {(rd-ra-canal)*1000:+.2f} g, casi todo en')
L.append(f'  **anclajes ({anc*1000:+.2f} g)**: las mejillas del lumbar y de los yugos derivan su altura de la')
L.append('  profundidad del canal y crecen con él.')
L.append(f'- Neto real del sistema: **{(rd-ra)*1000:+.2f} g** ({(rd-ra)/ra*100:+.2f} % de la masa rígida).')
L.append('- El cálculo por sección predecía −42,8 g en los dos canales. La masa nativa del conjunto da un')
L.append('  resultado **4,5 veces menor**: la métrica válida es la masa del ensamblaje, no la de la sección.')
L.append('- Estos valores son masas de modelo, no pesajes físicos. No incluyen bomba ni agua.')
L.append('')

(BASE / 'TABLA_MASAS.md').write_text('\n'.join(L), encoding='utf-8')
print('\n'.join(L[10:24]))
print('neto', round((rd - ra) * 1000, 3), 'g')
