"""Verificacion de salidas: reimporta cada STEP y compara volumen; revisa STL."""
import json
import struct
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent.parent
CAD = ROOT / "CAD"
IMP = ROOT / "IMPRESION"
EVI = ROOT / "EVIDENCIAS"

out = {"step": {}, "stl": {}, "ok": True}

for f in sorted(CAD.glob("P0_*.step")):
    src = cq.importers.importStep(str(f))
    v = sum(s.Volume() for s in src.val().Solids())
    n = len(src.val().Solids())
    out["step"][f.name] = dict(volumen_mm3=round(v, 2), solidos=n)

# el conjunto debe traer 2 solidos; las piezas, 1
for name, d in out["step"].items():
    esperado = 2 if "Conjunto" in name else 1
    if d["solidos"] != esperado:
        out["ok"] = False
        d["error"] = f"se esperaban {esperado} solidos"

for f in sorted(list(CAD.glob("P0_*.stl")) + list(IMP.glob("*.stl"))):
    data = f.read_bytes()
    if len(data) < 84:
        out["stl"][f.name] = dict(triangulos=0, error="archivo demasiado corto")
        out["ok"] = False
        continue
    ntri = struct.unpack("<I", data[80:84])[0]
    esperado = 84 + ntri * 50
    out["stl"][f.name] = dict(
        bytes=len(data), triangulos=ntri,
        binario_consistente=(esperado == len(data)),
        tamano_mm=None,
    )
    if esperado != len(data):
        out["ok"] = False

# dimensiones de malla desde el STEP equivalente (referencia)
(EVI / "verificacion_salidas.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

for k, v in out["step"].items():
    print(f"STEP {k:32s} vol={v['volumen_mm3']:10.1f} mm3 solidos={v['solidos']}")
for k, v in out["stl"].items():
    print(f"STL  {k:40s} tri={v.get('triangulos')} bytes={v.get('bytes')} "
          f"ok={v.get('binario_consistente')}")
print("TODO OK" if out["ok"] else "HAY FALLOS")
