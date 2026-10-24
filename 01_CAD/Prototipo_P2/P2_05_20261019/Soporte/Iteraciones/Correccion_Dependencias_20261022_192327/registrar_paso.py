"""Registra esta corrección documental; no ejecuta el generador ni Inventor."""
from pathlib import Path
import difflib
import hashlib
import json

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[2]
ROOT=BASE.parents[2]
GEN=BASE/'Soporte/generar_p2_05.py'
assert not (HERE/'DOCUMENTACION_AGREGADA.json').exists(),'El registro ya se realizó'
old=(HERE/'generar_p2_05_ANTES.py').read_bytes()
now=GEN.read_bytes()
if b'\r\n' in old:
    now=now.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
    GEN.write_bytes(now)
patch=''.join(difflib.unified_diff(old.decode('utf-8-sig').splitlines(True),now.decode('utf-8-sig').splitlines(True),fromfile='generar_p2_05_ANTES.py',tofile='Soporte/generar_p2_05.py'))
(HERE/'CAMBIO_GENERADOR.diff').write_text(patch,encoding='utf-8')
newrel=HERE.relative_to(BASE).as_posix()
doc={}
section='''

## 12. Primera corrección de dependencias — 2026-10-22

**hecho de implementación:** el generador deriva de `espesor_mejilla` las posiciones exteriores, el agarre y la longitud del pasador (H03); las capas lumbares y cortes derivan de sus caras de referencia (parte de H13). El JSON de parámetros y el cálculo resistente no se modificaron. No se ejecutó el generador modificado ni Inventor, ni se añadieron o ejecutaron pruebas; la invariancia de las salidas queda pendiente.

**hecho:** fuente anterior, diff, ficha, alcance y estado: [Corrección de dependencias](REL/INFORME.md). La auditoría de §11 describe la fuente anterior; no se interpreta como verificación de este cambio. Se conserva intacta.

**pendiente:** comparación de descripciones antes/después y propagación de parámetros. H02/H04/H05 y el vínculo del espesor de cuna con el mínimo analítico siguen abiertos; también las hipótesis físicas y D-12. No se autoriza cambiar valores ni cerrar P2.05 por esta edición.
'''.replace('REL',newrel)
state='''## Seguimiento de coherencia y dependencias — 2026-10-22, 19:23

- **hecho:** la auditoría de parámetros/cálculo/descripción del modelo sí se realizó después del encargo de cierre: 13 hallazgos propuestos, con regeneración descriptiva idéntica antes de esta corrección. Ver `P2_05_20261019/LEEME_P2_05.md` §11. Las menciones previas a «revisión no ejecutada» quedan como historial del encargo anterior.
- **hecho de implementación:** primera corrección del generador: dependencias de mejillas/pasador (H03) y referencias de capas/cortes (parte de H13), con nominales conservados en el JSON. Fuente anterior y diff guardados en `REL/`. No se ejecutó el generador modificado, Inventor ni pruebas. No se declara invariancia comprobada después de esta edición.
- **pendiente:** verificar las salidas y variaciones; resolver H02/H04/H05, el espesor local de cuna y los supuestos físicos. P2.04 continúa como entrega vigente y P2.05 sigue abierta. No hay commit nuevo.

'''.replace('REL',HERE.relative_to(ROOT).as_posix())
changelog='- **hecho (2026-10-22):** primera corrección de dependencias del generador P2.05 (H03 y parte de H13), conservando parámetros y ecuaciones; sin ejecución del generador modificado, pruebas, CAD ni commit. Evidencia: `'+HERE.relative_to(ROOT).as_posix()+'/INFORME.md`; comparación posterior pendiente.\n'
for path,text,where in [(BASE/'LEEME_P2_05.md',section,'final'),(ROOT/'ESTADO_ACTUAL.md',state,'antes_seccion'),(ROOT/'CHANGELOG_SEDAC.md',changelog,'despues_auditoria')]:
    data=path.read_bytes()
    eol='\r\n' if b'\r\n' in data else '\n'
    text=text.replace('\n',eol)
    if where=='final':position=len(data)
    elif where=='antes_seccion':position=data.index(b'## ')
    else:
        anchor=data.index(b'- **hecho (2026-10-22):** auditor')
        position=data.index(b'\n',anchor)+1
    rel=path.relative_to(ROOT).as_posix()
    doc[rel]=dict(antes_sha256=hashlib.sha256(data).hexdigest(),contenido_antes_hex=data.hex(),posicion=position,texto_agregado=text)
    path.write_bytes(data[:position]+text.encode('utf-8')+data[position:])
(HERE/'DOCUMENTACION_AGREGADA.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
print('Diff y tres inserciones documentales registrados; sin ejecutar el generador.')
