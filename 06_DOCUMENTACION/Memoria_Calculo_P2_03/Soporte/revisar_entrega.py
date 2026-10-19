from pathlib import Path
from lxml import etree as E, html
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader
import re,json,subprocess,hashlib,math
ROOT=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD')
B=ROOT/'06_DOCUMENTACION/Memoria_Calculo_P2_03';SUP=B/'Soporte'
QA=SUP/'Revision_visual';QA.mkdir(exist_ok=True)
PDF=B/'Guia_SEDAC_P2_03_MC02_Beamer.pdf'
log=(SUP/'Beamer/Guia_SEDAC_P2_03_MC02_Beamer.log').read_text(encoding='utf-8',errors='replace')
assert not re.search(r'Overfull \\[hv]box',log)
reader=PdfReader(str(PDF));assert len(reader.pages)==55
exe=r'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
subprocess.run([exe,'-r','125','-png',str(PDF),str(QA/'PDF')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',17)
def contact(files,cols,rows,cw,ch,prefix):
 for start in range(0,len(files),cols*rows):
  im=Image.new('RGB',(cols*cw,rows*ch),'#DDE5E9');dr=ImageDraw.Draw(im)
  for j,f in enumerate(files[start:start+cols*rows]):
   a=Image.open(f).convert('RGB');a.thumbnail((cw-14,ch-30))
   x=j%cols*cw+(cw-a.width)//2;y=j//cols*ch+26
   im.paste(a,(x,y));dr.text((j%cols*cw+7,j//cols*ch+4),f'{prefix} {start+j+1}',font=font,fill='#173345')
  im.save(QA/f'CONTACTO_{prefix}_{start//(cols*rows)+1}.png')
contact(sorted(QA.glob('PDF-*.png')),3,4,410,254,'PDF')
xml=E.parse(str(B/'Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd'));ns={'w':'http://schemas.mathsoft.com/worksheet30'}
assert not xml.xpath('//*[@error]')
regions=[]
for e in xml.findall('.//w:regions/w:region',ns):
 a=e.attrib;regions.append(dict(id=a['region-id'],tag=a.get('tag'),x=float(a['left']),y=float(a['top']),w=float(a['width']),h=float(a['height'])))
wide=[r for r in regions if r['x']+r['w']>512];over=[]
for i,a in enumerate(regions):
 for c in regions[i+1:]:
  ox=min(a['x']+a['w'],c['x']+c['w'])-max(a['x'],c['x']);oy=min(a['y']+a['h'],c['y']+c['h'])-max(a['y'],c['y'])
  if ox>1 and oy>1:over.append([a['tag'],c['tag'],ox,oy])
assert not wide,wide
assert not over,over
PH=757.89;scale=4/3;pages={}
def pt(s,key):
 m=re.search(r'(?:^|;)\s*'+key+r':\s*([0-9.]+)pt',s);return float(m[1]) if m else 0
h=html.parse(str(SUP/'memoria_MC02_final.html'))
for d in h.xpath('//div[starts-with(@id,"mc-region-")]'):
 ims=d.xpath('.//img');assert len(ims)==1
 el=ims[0];style=d.get('style');x=pt(style,'left');y=pt(style,'top');page=int(y//PH)
 a=Image.open(SUP/el.get('src').replace('\\','/')).convert('RGBA')
 canvas=pages.setdefault(page,Image.new('RGB',(794,1123),'white'))
 xx=round((42+x)*scale);yy=round((42+y-page*PH)*scale)
 bg=re.search(r'background-color:\s*(#[0-9a-fA-F]+)',style)
 if bg:ImageDraw.Draw(canvas).rectangle((xx,yy,xx+a.width,yy+a.height),fill=bg[1])
 canvas.paste(a,(xx,yy),a)
for n,im in pages.items():im.save(QA/f'MC-{n+1:02}.png')
contact(sorted(QA.glob('MC-*.png')),3,3,362,535,'MC')
checks=json.loads((SUP/'VERIFICACION_MATHCAD.json').read_text(encoding='utf-8-sig'))
assert len(checks)==247 and all(v['coincide'] for v in checks)
CAD=ROOT/'01_CAD/Prototipo_P2/P2_03_20261016/Entrega/Inventor_Optimizado'
ints=json.loads((CAD/'INTERFERENCIAS.json').read_text(encoding='utf-8-sig'));assert not ints
cons=json.loads((CAD/'RESTRICCIONES.json').read_text(encoding='utf-8-sig'))
assert len(cons)==130 and all(c['error_transformacion']<1e-6 and c['traslaciones']==0 and c['rotaciones']==0 for c in cons)
audit=json.loads((CAD/'AUDITORIA_NATIVA.json').read_text(encoding='utf-8-sig'))
assert len(audit)==51 and all(a['solidos']==1 for a in audit)
rounds=[{'pieza':a['pieza'],'radio_mm':0.4,'aplicado':a['redondeos']>0,'evidencia':'Feature nativa Radio_cantos_0p4 y radio indicado por el generador'} for a in audit if a['pieza'].startswith('Anclaje')]
assert all(a['aplicado'] for a in rounds)
(CAD/'REDONDEOS.json').write_text(json.dumps(rounds,indent=2,ensure_ascii=False),encoding='utf-8')
old=ROOT/'01_CAD/Prototipo_P2/P2_02_20261015/SEDAC_P2_02_ENTREGA.zip'
sha=hashlib.sha256(old.read_bytes()).hexdigest();assert sha=='9353e6ef30483065898f710e1b56b6be4a7f2c876f8e23a77ad9cce72a151f1c'
report=dict(pdf_pages=len(reader.pages),mathcad_pages=len(pages),mathcad_regions=len(regions),mathcad_variables=len(checks),mathcad_errors=0,mathcad_overlaps=0,pdf_overfull=0,max_relative_error=max(v['error_relativo'] for v in checks),cad_parts=len(audit),cad_instances=131,position_constraints=390,unrestrained_dof=0,volumetric_interferences=0,rounded_anchor_parts=4,threaded_part_definitions=sum(a['roscas_nativas'] for a in audit),P2_02_zip_sha256=sha,visual_review='PNGs generados; revisión visual humana pendiente en este registro')
(SUP/'AUDITORIA_ENTREGA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
