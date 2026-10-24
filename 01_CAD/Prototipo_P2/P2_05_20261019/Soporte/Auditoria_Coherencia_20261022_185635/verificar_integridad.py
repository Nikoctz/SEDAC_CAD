"""Cotejo de archivos previos; no abre all.png ni escribe fuera de la auditoría."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

AUDIT=Path(__file__).resolve().parent
BASE=AUDIT.parents[1]
ROOT=BASE.parents[2]
def sha(data):return hashlib.sha256(data).hexdigest()
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
before=json.loads((AUDIT/'INTEGRIDAD_ANTES.json').read_text(encoding='utf-8-sig'))
audit_rel=AUDIT.relative_to(ROOT).as_posix()+'/'
names=set(subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT).decode('utf-8').strip('\0').split('\0'))
names={n.replace('\\','/') for n in names if n and n!='all.png' and not n.replace('\\','/').startswith(audit_rel)}
current={n:sha((ROOT/n).read_bytes()) for n in sorted(names) if (ROOT/n).is_file()}
old=before['archivos']
changed=[n for n in sorted(old) if n in current and old[n]!=current[n]]
added=sorted(set(current)-set(old));removed=sorted(set(old)-set(current))
allowed={str((BASE/'LEEME_P2_05.md').relative_to(ROOT)).replace('\\','/'),'CHANGELOG_SEDAC.md'}
unexpected=[n for n in changed if n not in allowed]
png=(ROOT/'all.png').stat()
pngmeta=dict(bytes=png.st_size,mtime_ns=png.st_mtime_ns)
prefix='01_CAD/Prototipo_P2/P2_05_20261019/Soporte/'
foreign=[prefix+'Pruebas/cierre/Ejecuciones/'+x+'/' for x in ['Nueva_20261022_183218_837','Calculo_20261022_183238_628']]
cad={n for n in old if Path(n).suffix.lower() in {'.ipt','.iam','.step','.stl','.3mf'}}
historical={n for n in old if n.startswith(prefix+'Iteraciones/Nueva_20261019_060807/')}
foreign_sets={p:{n for n in old if n.startswith(p)} for p in foreign}
reproductions={}
for path in sorted(AUDIT.glob('Ejecucion_*/REGISTRO_GENERACION.json')):
    reg=json.loads(path.read_text(encoding='utf-8-sig'))
    comp=json.loads((path.parent/'COMPARACION_GENERACION.json').read_text(encoding='utf-8-sig'))
    reproductions[path.parent.name]=dict(powershell=reg['powershell_invocador'],retorno=reg['retorno'],igualdad_bytes=comp['igualdad_bytes'])
documentation={}
docfile=AUDIT/'REGISTRO_DOCUMENTACION.json'
if docfile.exists():
    docreg=json.loads(docfile.read_text(encoding='utf-8'))
    for n,record in docreg.items():
        raw=(ROOT/n).read_bytes()
        content=bytes.fromhex(record['contenido_antes_hex'])
        extra=record['texto_agregado'].encode('utf-8')
        position=record['posicion']
        documentation[n]=dict(antes_sha256=sha(content),antes_coincide_linea_base=sha(content)==old[n],despues_solo_insercion_autorizada=raw==content[:position]+extra+content[position:])
result=dict(etiqueta='hecho',fecha=datetime.datetime.now().astimezone().isoformat(),archivos_previos=len(old),archivos_previos_modificados=changed,nuevos_fuera_de_auditoria=added,borrados=removed,cambios_no_autorizados=unexpected,CAD=dict(comparados=len(cad),modificados=sorted(cad&set(changed))),corrida_historica=dict(comparados=len(historical),modificados=sorted(historical&set(changed))),evidencia_ajena={p:dict(comparados=len(s),modificados=sorted(s&set(changed))) for p,s in foreign_sets.items()},all_png_solo_metadatos=dict(antes=before['all_png_solo_metadatos'],despues=pngmeta,intacto=pngmeta==before['all_png_solo_metadatos']),documentacion=documentation,regeneraciones=reproductions,inventor_ejecutado=False,commit=False)
result['integridad_cumple']=not(added or removed or unexpected) and result['all_png_solo_metadatos']['intacto'] and all(x['despues_solo_insercion_autorizada'] and x['antes_coincide_linea_base'] for x in documentation.values())
dump(AUDIT/'VERIFICACION_INTEGRIDAD.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
assert result['integridad_cumple'],'Cambio ajeno o no autorizado detectado: detenerse'
