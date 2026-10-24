"""Inserciones documentales autorizadas, conservando todos los bytes anteriores."""
from pathlib import Path
import hashlib
import json

AUDIT=Path(__file__).resolve().parent
BASE=AUDIT.parents[1]
ROOT=BASE.parents[2]
record=AUDIT/'REGISTRO_DOCUMENTACION.json'
assert not record.exists(),'Las inserciones ya se registraron; no repetirlas'
baseline=json.loads((AUDIT/'INTEGRIDAD_ANTES.json').read_text(encoding='utf-8'))['archivos']
readme=BASE/'LEEME_P2_05.md'
changelog=ROOT/'CHANGELOG_SEDAC.md'
readme_data=readme.read_bytes();change_data=changelog.read_bytes()
eol='\r\n' if b'\r\n' in readme_data else '\n'
section=eol.join(['','','## 11. Auditoría de coherencia — 2026-10-22','','**hecho:** se revisaron parámetros, literales, cálculo y descripción del modelo, sin corregir las fuentes. La regeneración JSON/CSV coincide byte por byte con `Nueva_20261019_060807`; no se ejecutó Inventor. Se documentaron 13 hallazgos con severidad propuesta (10 informativos, 3 a conservar), incluidos el recuento 8+4 frente al 10+4 histórico y dependencias geométricas parciales.','','**hecho:** informe, tablas, scripts y registros: [Auditoría de coherencia](Soporte/'+AUDIT.name+'/AUDITORIA.md). Fuera de esa carpeta solo se añadió esta sección y una línea al changelog.','','**pendiente:** resolver las propuestas antes de variar parámetros, justificar los supuestos locales y validar la integración nativa/física. Esta revisión no cierra P2.05 ni sustituye D-12.',''])
change_eol='\r\n' if b'\r\n' in change_data else '\n'
line='- **hecho (2026-10-22):** auditoría de coherencia P2.05, 88 nodos/78 hojas; 13 hallazgos propuestos (10 I/3 C), regeneración JSON/BOM idéntica en Windows PowerShell 5.1, sin correcciones de fuentes, CAD ni commit. Evidencia: `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/'+AUDIT.name+'/AUDITORIA.md`.'+change_eol
anchor=change_data.index(b'- **Evidencia:**')
position=change_data.index(b'\n',anchor)+1
plan={}
for path,content,pos,text in [(readme,readme_data,len(readme_data),section),(changelog,change_data,position,line)]:
    rel=path.relative_to(ROOT).as_posix()
    assert hashlib.sha256(content).hexdigest()==baseline[rel],'Cambio ajeno en documentación; detenerse'
    plan[rel]=dict(contenido_antes_hex=content.hex(),posicion=pos,texto_agregado=text)
record.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
for rel,entry in plan.items():
    content=bytes.fromhex(entry['contenido_antes_hex']);pos=entry['posicion']
    (ROOT/rel).write_bytes(content[:pos]+entry['texto_agregado'].encode('utf-8')+content[pos:])
print('Dos inserciones documentales registradas; sin cambios adicionales a las fuentes.')
