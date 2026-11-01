"""
Mosqueton giratorio P0 — modelo parametrico de prediseno (v2)
Proyecto SEDAC. Borrador de laboratorio. NO validado para uso con personas.

Topologia (continuidad con el modelo previo):
  El giro es un PIVOTE alrededor de un eje transversal (Y), no un giro libre
  de 360 grados alrededor de la linea de carga. Se resuelve el montaje que en
  el modelo previo quedaba abierto: en vez de cabezales integrales de Ø15 que
  no pasan por el alojamiento de Ø8, se usa un TORNILLO DE HOMBRO comercial
  ISO 7379 M6x16 (hombro Ø6 h9) con tuerca autoblocante M5 y arandelas.

  Eje de giro: Y, en (-6.5, 0, 28).  Eje de carga previsto: Z.
  Juego axial del cubo entre tetones: 0.2 mm (verificable con galga).

Piezas impresas: 2 (cuerpo del gancho, argolla).
Herrajes: tornillo ISO 7379 M6x16 A2; tuerca M5 nyloc A2; 2 arandelas
DIN 125 M5 A2; pasador de horquilla Ø4x30 con clip (cierre del gancho).

Todas las cotas en milimetros.

Salidas: CAD/*.step, CAD/*.stl, CAD/P0_Conjunto_Montaje.step,
         EVIDENCIAS/verificacion_modelo.json
"""

import json
import math
from pathlib import Path  # noqa: F401

import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

ROOT = Path(__file__).resolve().parent.parent
CAD = ROOT / "CAD"
IMP = ROOT / "IMPRESION"
EVI = ROOT / "EVIDENCIAS"
for d in (CAD, IMP, EVI):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# PARAMETROS
# ---------------------------------------------------------------------------
P = dict(
    # cuerpo del gancho
    T=9.0,              # espesor de placa (Y) del cuerpo y de la argolla
    IN_W=7.5,           # semiluz interior del gancho  -> garganta 15 mm
    BASKET_R=7.5,       # radio interior de la canasta
    ARM_T=6.0,          # espesor de brazo (la espina se refuerza a 9 con 'butt')
    ARM_TOP=21.0,       # cara superior plana del brazo
    CAP_R=3.0,          # casquete de extremo (ARM_T/2)
    # horquilla (fork) del pivote
    FORK_X0=-14.0,      # borde izquierdo del bloque de horquilla
    FORK_X1=-3.0,       # borde derecho
    FORK_Z0=19.5,       # base del bloque (solapa 1,5 mm en el brazo)
    FORK_Z1=34.5,       # tope del bloque = tope de tetones
    FORK_Y=16.0,        # ancho total en Y (2 tetones de 3,3 + hueco 9,4)
    SLOT_Y=9.4,         # hueco entre tetones: paso 16,0 = ISO 7379 M6x16
    SLOT_Z0=21.4,       # fondo del hueco (1,1 mm bajo el cubo)
    # eje del pivote
    AX_X=-6.5,
    AX_Z=28.0,
    BORE_D=6.2,         # agujero del cubo y de los tetones (hombro Ø6 h9)
    # cierre (pasador de horquilla)
    PIN_Z=17.5,
    PIN_D=4.2,
    PIN_X0=-15.5,
    PIN_X1=15.5,
    # argolla
    HUB_D=11.0,
    RING_W=22.0,
    RING_H=20.0,
    SLOT_W=12.0,
    SLOT_H=11.0,
    RING_GAP=2.0,       # luz entre tope de tetones y base de la anilla
    # material
    DENSITY=1.27,       # g/cm3 PETG (Prusament PETG V0)
)

G_ACC = 9.81
F_TOT = 20.0 * G_ACC


def r2(v):
    return round(float(v), 4)


def inter_vol(a, b):
    """Volumen de interseccion robusto (0 si no hay)."""
    try:
        r = a.intersect(b)
        if r is None:
            return 0.0
        v = r.val()
        if v is None:
            return 0.0
        try:
            return float(v.Volume())
        except Exception:
            return float(sum(s.Volume() for s in v.Solids()))
    except Exception:
        return 0.0


def puntos_interiores(verts, tris, ang, centro, solido, tol=0.001):
    """Cuenta vertices de la malla que quedan DENTRO del otro solido tras
    girar alrededor del eje Y que pasa por 'centro'. Metodo independiente de
    booleanos y de distancias minimas."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt

    cx, cz = centro[0], centro[1]
    th = math.radians(ang)
    c, s = math.cos(th), math.sin(th)
    cl = BRepClass3d_SolidClassifier(solido.val().wrapped)
    n = 0
    for v in verts:
        x, z = v.x - cx, v.z - cz
        xr, zr = x * c + z * s, -x * s + z * c
        cl.Perform(gp_Pnt(xr + cx, v.y, zr + cz), tol)
        if cl.State() == TopAbs_IN:
            n += 1
    return n


def min_dist(a, b):
    """Distancia minima entre dos solidos (independiente de booleanos)."""
    d = BRepExtrema_DistShapeShape(a.val().wrapped, b.val().wrapped)
    d.Perform()
    return float(d.Value()) if d.IsDone() else float("nan")


def center_y(shape, t):
    bb = shape.val().BoundingBox()
    return shape.translate((0, -(bb.ymin + bb.ymax) / 2.0, 0))


# ---------------------------------------------------------------------------
# 1. CUERPO DEL GANCHO
# ---------------------------------------------------------------------------
def cuerpo_gancho():
    wi, ri, arm, zt, cap = P["IN_W"], P["BASKET_R"], P["ARM_T"], P["ARM_TOP"], P["CAP_R"]
    wo, ro = wi + arm, ri + arm
    cx = (wi + wo) / 2.0
    zc = zt - cap
    d = math.sqrt(2) / 2

    prof = (
        cq.Workplane("XZ")
        .moveTo(-wi, zc)
        .threePointArc((-cx, zt), (-wo, zc))                     # casquete izq.
        .lineTo(-wo, ri)
        .threePointArc((-ro * d, ri - ro * d), (0, ri - ro))      # canasta ext. izq
        .threePointArc((ro * d, ri - ro * d), (wo, ri))           # canasta ext. der
        .lineTo(wo, zc)
        .threePointArc((cx, zt), (wi, zc))                        # casquete der
        .lineTo(wi, ri)
        .threePointArc((ri * d, ri - ri * d), (0, 0))             # canasta int. der
        .threePointArc((-ri * d, ri - ri * d), (-wi, ri))         # canasta int. izq
        .lineTo(-wi, zc)
        .close()
    )
    body = prof.extrude(-P["T"])
    body = center_y(body, P["T"])      # centrar ANTES de unir el bloque

    # bloque de horquilla sobre el brazo izquierdo
    fx0, fx1 = P["FORK_X0"], P["FORK_X1"]
    fz0, fz1 = P["FORK_Z0"], P["FORK_Z1"]
    block = (
        cq.Workplane("XY")
        .workplane(offset=fz0)
        .moveTo((fx0 + fx1) / 2, 0)
        .rect(fx1 - fx0, P["FORK_Y"])
        .extrude(fz1 - fz0)
    )
    # redondeo de esquinas verticales del bloque (aristas |Z)
    try:
        block = block.edges("|Z").fillet(min(3.0, (fx1 - fx0) / 2 - 0.6))
    except Exception:
        pass
    # refuerzo exterior del brazo izquierdo (espina): lleva la seccion de 6 a 9
    # mm en la zona cargada, sin tocar la cara interior de la garganta
    butt = (
        cq.Workplane("XY")
        .workplane(offset=0.0)
        .moveTo(-15.0, 0)
        .rect(3.2, P["T"])
        .extrude(21.0)
    )
    body = body.union(butt)
    body = body.union(block)

    # hueco entre tetones
    # el hueco se centra en el eje del pivote y se dimensiona para que el cubo
    # Ø11 pueda girar sin tocar los tetones (barrido del cubo = Ø11)
    slot = (
        cq.Workplane("XY")
        .workplane(offset=P["SLOT_Z0"])
        .moveTo(P["AX_X"], 0)
        .rect(14.0, P["SLOT_Y"])
        .extrude(fz1 - P["SLOT_Z0"] + 1)
    )
    body = body.cut(slot)

    # agujero del eje (Y) en los dos tetones: se corta con solape en ambos
    # sentidos para no dejar caras coplanares
    ax_tool = (
        cq.Workplane("XZ").moveTo(P["AX_X"], P["AX_Z"])
        .circle(P["BORE_D"] / 2).extrude(40, both=True)
    )
    body = body.cut(ax_tool)
    # agujero del pasador de cierre (X)
    pin_tool = (
        cq.Workplane("YZ").moveTo(0, P["PIN_Z"])
        .circle(P["PIN_D"] / 2).extrude(40, both=True)
    )
    body = body.cut(pin_tool)
    return body


# ---------------------------------------------------------------------------
# 2. ARGOLLA (cubo + cuello + anilla)
# ---------------------------------------------------------------------------
def argolla():
    hub_r = P["HUB_D"] / 2
    hub_bot = P["AX_Z"] - hub_r
    ring_bot = P["FORK_Z1"] + P["RING_GAP"]      # base de la anilla
    ring_top = ring_bot + P["RING_H"]
    ring_cz = (ring_bot + ring_top) / 2

    # cubo (eje Y) + placa (plano XZ)
    hub = (
        cq.Workplane("XZ")
        .moveTo(P["AX_X"], P["AX_Z"])
        .circle(hub_r)
        .extrude(-P["T"])
    )
    # cuello esbelto: 6 mm de ancho, arranca sobre el eje del pivote para que
    # el giro no lo haga chocar con la horquilla
    neck_z0 = P["AX_Z"] - 1.0
    neck_z1 = ring_bot + 1.0
    neck = (
        cq.Workplane("XZ")
        .moveTo(P["AX_X"], (neck_z0 + neck_z1) / 2)
        .rect(6.0, neck_z1 - neck_z0)
        .extrude(-P["T"])
    )
    # la placa de la anilla, con esquinas redondeadas (limitado para no fallar)
    ring = (
        cq.Workplane("XZ")
        .moveTo(P["AX_X"], ring_cz)
        .rect(P["RING_W"], P["RING_H"])
        .extrude(-P["T"])
    )
    try:
        ring = ring.edges("|Y").fillet((min(P["RING_W"], P["RING_H"]) - max(
            P["SLOT_W"], P["SLOT_H"])) / 2.0 - 0.05)
    except Exception:
        pass

    body = hub.union(neck).union(ring)
    body = center_y(body, P["T"])

    # agujero del eje (Y)
    body = body.cut(
        cq.Workplane("XZ").moveTo(P["AX_X"], P["AX_Z"])
        .circle(P["BORE_D"] / 2).extrude(40, both=True)
    )
    # hueco de la anilla (Y)
    slot = (
        cq.Workplane("XZ")
        .moveTo(P["AX_X"], ring_cz)
        .rect(P["SLOT_W"], P["SLOT_H"])
        .extrude(P["T"] + 4, both=True)     # pasar de lado a lado
    )
    body = body.cut(slot)
    return body


def info(solids):
    out = {}
    for name, s in solids.items():
        v = s.val()
        bb = v.BoundingBox()
        vol = v.Volume()
        out[name] = dict(
            bbox=[r2(bb.xlen), r2(bb.ylen), r2(bb.zlen)],
            bbox_min=[r2(bb.xmin), r2(bb.ymin), r2(bb.zmin)],
            bbox_max=[r2(bb.xmax), r2(bb.ymax), r2(bb.zmax)],
            volume_mm3=r2(vol),
            mass_g=r2(vol / 1000.0 * P["DENSITY"]),
            n_solids=len(v.Solids()),
            valido=bool(v.isValid()),
        )
    return out


def main():
    gancho = cuerpo_gancho()
    arg = argolla()

    parts = {"P0_Cuerpo_Gancho": gancho, "P0_Argolla": arg}

    for name, s in parts.items():
        cq.exporters.export(s, str(CAD / f"{name}.step"))
        cq.exporters.export(s, str(CAD / f"{name}.stl"),
                            tolerance=0.02, angularTolerance=0.1)
    asm = cq.Compound.makeCompound([gancho.val(), arg.val()])
    cq.exporters.export(asm, str(CAD / "P0_Conjunto_Montaje.step"))

    # STL de impresion (misma orientacion del modelo: Z vertical)
    cq.exporters.export(gancho, str(IMP / "P0_Cuerpo_Gancho.stl"),
                        tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(arg, str(IMP / "P0_Argolla.stl"),
                        tolerance=0.02, angularTolerance=0.1)

    meta = info(parts)

    # --- interferencia en montaje ---
    v_mont = inter_vol(gancho, arg)

    # --- holgura del cubo entre tetones ---
    holgura_axial = P["SLOT_Y"] - P["T"]

    # --- barrido de giro del pivote por DISTANCIA MINIMA ---
    # El booleano de interseccion produce volumenes con caras casi tangentes
    # (holguras de 0,2 mm); la distancia minima no depende del booleano.
    verts, tris = arg.val().tessellate(0.2)
    centro = (P["AX_X"], P["AX_Z"])
    sweep = []
    for ang in range(-90, 91, 2):
        n_in = puntos_interiores(verts, tris, ang, centro, gancho)
        rot = arg.rotate(cq.Vector(P["AX_X"], 0, P["AX_Z"]),
                         cq.Vector(0, 1, 0), ang)
        sweep.append(dict(ang=ang, puntos_dentro=n_in,
                          dist_mm=round(min_dist(rot, gancho), 4),
                          vol_inf=r2(inter_vol(rot, gancho))))
    umbral = 0
    libres = [s["ang"] for s in sweep if s["puntos_dentro"] <= umbral]
    pos = [a for a in libres if a >= 0]
    neg = [a for a in libres if a <= 0]
    rango = dict(
        positivo_max=max(pos) if pos else 0,
        negativo_min=min(neg) if neg else 0,
        paso=2,
        criterio="sin vertices de la argolla dentro del solido del gancho "
                 "(muestreo de malla, paso 0,2 mm)",
        dist_min_montaje=round(min_dist(arg, gancho), 4),
        puntos_dentro_en_montaje=puntos_interiores(
            *arg.val().tessellate(0.2), 0, centro, gancho),
        ADVERTENCIA="El rango de +-90 grados sale de un muestreo de vertices "
                    "grueso y NO se considera validado: el booleano de "
                    "interseccion y la distancia minima dan resultados "
                    "contradictorios con holguras de 0,2-2,0 mm. Ver informe S8.",
        limite_calculado_grados=round(math.degrees(math.asin(2.0 / 7.5)), 1),
        limite_calculo_nota="Primer contacto previsto anilla-horquilla por luz "
                            "de 2,0 mm y brazo 7,5 mm: CALCULO, no verificado.",
    )

    lim = (40.0, 40.0, 70.0)
    fit = {n: all(a <= b for a, b in zip(m["bbox"], lim)) for n, m in meta.items()}
    bb_asm = asm.BoundingBox()

    res = dict(
        parametros=P,
        piezas=meta,
        masa_impresa_total_g=r2(sum(m["mass_g"] for m in meta.values())),
        montaje=dict(
            volumen_interferencia_mm3=v_mont,
            holgura_axial_cubo_tetones=r2(holgura_axial),
            agujero_y_hombro=P["BORE_D"],
            nota="Hombro ISO 7379 Ø6 h9 en agujero Ø6,2: juego radial 0,1 mm.",
        ),
        giro=rango,
        giro_detalle=sweep,
        conjunto=dict(
            bbox=[r2(bb_asm.xlen), r2(bb_asm.ylen), r2(bb_asm.zlen)],
            z_min=r2(bb_asm.zmin), z_max=r2(bb_asm.zmax),
            alto_total=r2(bb_asm.zlen),
        ),
        sobre_referencia_no_confirmado=list(lim),
        cabe_en_referencia=fit,
        aviso="40x40x70 es referencia historica del proyecto, NO confirmada "
              "para este servicio ni para este material.",
    )
    (EVI / "verificacion_modelo.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({k: res[k] for k in
                      ("masa_impresa_total_g", "montaje", "giro", "conjunto")},
                     indent=2, ensure_ascii=False))
    for n, m in meta.items():
        print(f"{n:22s} bbox={m['bbox']} vol={m['volume_mm3']:.0f} "
              f"m={m['mass_g']:.2f} g valido={m['valido']}")
    print("cabe en 40x40x70:", fit)
    print("sweep dentro:", [(s['ang'], s['puntos_dentro']) for s in sweep
                            if s['ang'] % 10 == 0])


if __name__ == "__main__":
    main()
