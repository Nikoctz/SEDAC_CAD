from pathlib import Path
from lxml import html
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image,ImageOps,ImageDraw
from pypdf import PdfReader
import json,re,math,subprocess
B=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02');S=B/'Soporte'
layout=json.loads((S/'REGIONES.json').read_text(encoding='utf-8'));PH=layout['page_height'];byid={r['id']:r for r in layout['records']}
doc=html.fromstring((S/'memoria_final.html').read_bytes())
def props(s):return {a.strip():float(re.search(r'[-\d.]+',b)[0]) for a,b in re.findall(r'([\w-]+)\s*:\s*([^;]+)',s) if re.search(r'[-\d.]+',b)}
files={p.name:p for p in S.rglob('*.PNG')};placed=[]
for div in doc.xpath('//div[starts-with(@id,"mc-region-")]'):
 rid=int(div.get('id').split('-')[-1]);r=byid[rid]
 dp=props(div.get('style',''));img=div.xpath('.//img')[0];ip=props(img.get('style',''))
 basename=img.get('src').replace('\\','/').split('/')[-1];f=files[basename]
 box=dict(id=rid,page=r['page'],x=dp['left'],y=dp['top']-(r['page']-1)*PH,width=ip['width'],height=ip['height'],image=str(f))
 assert box['x']+box['width']<=512 and box['y']>=-1 and box['y']+box['height']<=PH,(r,box)
 placed.append(box)
over=[]
for i,a in enumerate(placed):
 for b in placed[i+1:]:
  if a['page']!=b['page']:continue
  if min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x'])>.8 and min(a['y']+a['height'],b['y']+b['height'])-max(a['y'],b['y'])>.8:over.append([a['id'],b['id']])
assert not over,over
out=B/'Memoria_SEDAC_P2_02_MC01.pdf'
c=canvas.Canvas(str(out),pagesize=(595.276,841.89),pageCompression=1)
c.setTitle('SEDAC P2.02 - Memoria de calculo MC01');c.setAuthor('Proyecto SEDAC');c.setSubject('Copia de consulta de ecuaciones recalculadas en Mathcad. Prediseno provisional.')
for p,title in enumerate(layout['pages'],1):
 c.bookmarkPage('p'+str(p));c.addOutlineEntry(title,'p'+str(p),0,False)
 for a in placed:
  if a['page']!=p:continue
  c.drawImage(a['image'],42+a['x'],841.89-42-a['y']-a['height'],width=a['width'],height=a['height'],mask='auto')
 c.setStrokeColor(HexColor('#D8E1E8'));c.line(42,37,553,37)
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#617587'))
 c.drawString(42,24,'SEDAC P2.02 / MC01 / Prediseno - 15/10/2026')
 c.drawRightString(553,24,f'{p} / {len(layout["pages"])}')
 if p==17:
  links=[
   ('Scotty - catalogo oficial','https://scottyfire.com/wp-content/uploads/2017/04/2017ScottyFireCatalogue_LR.pdf'),
   ('Hydro - ficha 6061','https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf'),
   ('Atlas - ficha 5052','https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf'),
   ('Bossard - tornilleria inoxidable','https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf'),
   ('NASA RP-1228 - Fastener Design Manual','https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf')]
  c.setFont('Helvetica',9);c.setFillColor(HexColor('#175873'))
  for j,(label,url) in enumerate(links):
   yy=165-j*15;c.drawString(58,yy,label);c.linkURL(url,(58,yy-2,400,yy+10),relative=0)
 c.showPage()
c.save()
assert len(PdfReader(out).pages)==17
(S/'VERIFICACION_MAQUETACION.json').write_text(json.dumps(dict(pages=17,regions=len(placed),overlaps=over,horizontal_overflow=0,source='Renderizado por Mathcad, exportacion HTML de hoja calculada'),ensure_ascii=False,indent=2),encoding='utf-8')
pop=Path(r'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')
render=S/'Revision_PDF';render.mkdir(exist_ok=True)
subprocess.run([str(pop),'-scale-to','1400','-png',str(out),str(render/'pagina')],check=True,capture_output=True)
images=[]
for f in sorted(render.glob('pagina-*.png')):
 im=Image.open(f).convert('RGB');im.thumbnail((300,425));card=Image.new('RGB',(320,450),'#dce4eb');card.paste(im,((320-im.width)//2,8));ImageDraw.Draw(card).text((12,430),f.stem,fill='#253746');images.append(card)
cols=4;rows=math.ceil(len(images)/cols);contact=Image.new('RGB',(cols*320,rows*450),'white')
for i,im in enumerate(images):contact.paste(im,((i%cols)*320,(i//cols)*450))
contact.save(render/'CONTACTO.png')
print(json.dumps(dict(pdf=str(out),pages=17,regions=len(placed),bytes=out.stat().st_size,contact=str(render/'CONTACTO.png')),ensure_ascii=False))

