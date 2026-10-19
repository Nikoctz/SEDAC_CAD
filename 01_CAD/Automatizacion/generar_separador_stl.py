"""Generate and check a watertight cylindrical spacer in millimetres.

Independent mesh construction, NOT an Inventor export. Standard library only.
Run once; refuses to replace existing artifacts. Geometry matches iLogic defaults.
"""
import collections
import json
import math
from pathlib import Path
import struct


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def generate():
    n, outer, inner, height = 128, 9.0, 2.75, 6.0
    vertices = []
    for radius, z in ((outer, 0), (outer, height), (inner, 0), (inner, height)):
        for i in range(n):
            angle = 2*math.pi*i/n
            vertices.append((radius*math.cos(angle), radius*math.sin(angle), z))
    faces = []
    for i in range(n):
        j = (i+1) % n
        for a, b, c, d in ((i, j, n+j, n+i),
                            (2*n+j, 2*n+i, 3*n+i, 3*n+j),
                            (n+i, n+j, 3*n+j, 3*n+i),
                            (j, i, 2*n+i, 2*n+j)):
            faces.extend(((a, b, c), (a, c, d)))
    # Closed manifold and consistent directed edge orientation.
    edges = collections.Counter()
    directions = collections.Counter()
    volume = 0.0
    records = []
    for face in faces:
        a, b, c = (vertices[k] for k in face)
        normal = cross(tuple(b[k]-a[k] for k in range(3)), tuple(c[k]-a[k] for k in range(3)))
        norm = math.sqrt(dot(normal, normal))
        if norm <= 1e-10:
            raise ValueError("Degenerate triangle")
        normal = tuple(v/norm for v in normal)
        records.append(struct.pack("<12fH", *normal, *a, *b, *c, 0))
        volume += dot(a, cross(b, c))/6
        for u, v in zip(face, face[1:]+face[:1]):
            edges[tuple(sorted((u, v)))] += 1
            directions[(u, v)] += 1
    if any(count != 2 for count in edges.values()):
        raise ValueError("Open/nonmanifold mesh")
    if any(directions[(v, u)] != count for (u, v), count in directions.items()):
        raise ValueError("Inconsistent winding")
    expected_volume = n*math.sin(2*math.pi/n)/2*(outer**2-inner**2)*height
    if abs(volume-expected_volume) > 1e-6:
        raise ValueError("Wrong enclosed volume")
    mins = [min(v[k] for v in vertices) for k in range(3)]
    maxs = [max(v[k] for v in vertices) for k in range(3)]
    size = [maxs[k]-mins[k] for k in range(3)]
    if any(abs(a-b) > 1e-8 for a, b in zip(size, [18,18,6])):
        raise ValueError("Wrong envelope")
    report = {
        "units": "mm (select millimetres on STL import)",
        "origin": "Independent mesh generator, not exported from Inventor",
        "outer_diameter_mm": 18,
        "nominal_bore_mm": 5.5,
        "minimum_faceted_bore_mm": 2*inner*math.cos(math.pi/n),
        "height_mm": 6,
        "bounding_box_mm": size,
        "triangles": len(faces),
        "watertight_manifold": True,
        "consistent_orientation": True,
        "volume_mm3": volume,
        "fits_40_40_70_geometrically": all(a <= b for a,b in zip(size,[40,40,70])),
        "limitations": "Not sliced or printed. Fit, strength and tightening not validated. Print one sample first."
    }
    outdir = Path(__file__).resolve().parents[2] / "01_CAD" / "Exportaciones"
    outdir.mkdir(parents=True, exist_ok=True)
    stl = outdir / "SEDAC_Separador_18x5p5x6_V01.stl"
    audit = outdir / "SEDAC_Separador_18x5p5x6_V01_verificacion.json"
    if stl.exists() or audit.exists():
        raise FileExistsError("Existing output; choose a new version before rerunning")
    with stl.open("xb") as f:
        f.write(b"SEDAC spacer 18x5.5x6 mm; GEOMETRIC PROTOTYPE".ljust(80,b" "))
        f.write(struct.pack("<I",len(faces)))
        f.write(b"".join(records))
    with audit.open("x",encoding="utf-8") as f:
        json.dump(report,f,indent=2)
    print(json.dumps({"stl":str(stl),"verification":report},indent=2))


if __name__ == "__main__":
    generate()
