from pathlib import Path
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont
import subprocess,json,re,hashlib,shutil
base=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02')
support=base/'Soporte'/'Beamer'
pdf=support/'Guia_SEDAC_P2_02_MC01_Beamer.pdf'
dest=base/pdf.name
shutil.copy2(pdf,dest)
log=(support/'Guia_SEDAC_P2_02_MC01_Beamer.log').read_text(encoding='utf-8',errors='replace')
bad=[s for s in log.splitlines() if 'Overfull' in s or s.startswith('!')]
r=PdfReader(str(dest))
assert len(r.pages)==44,len(r.pages)
assert not bad,bad
source=base/'Guia_SEDAC_P2_02_MC01_Beamer.tex'
text='\n'.join(p.extract_text() or '' for p in r.pages)
assert '100' in text and '130' in text
out=support/'Revision_PDF'
out.mkdir(exist_ok=True)
exe=r'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
subprocess.run([exe,'-r','125','-png',str(dest),str(out/'diapositiva')],check=True,capture_output=True)
files=sorted(out.glob('diapositiva-*.png'))
font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',17)
for start in range(0,len(files),12):
    contact=Image.new('RGB',(1620,940),'#DDE5E9')
    d=ImageDraw.Draw(contact)
    for j,file in enumerate(files[start:start+12]):
        im=Image.open(file).convert('RGB');im.thumbnail((390,220))
        x=12+(j%4)*405;y=34+(j//4)*310
        contact.paste(im,(x,y));d.text((x,y-24),'Diapositiva '+str(start+j+1),font=font,fill='#173345')
    contact.save(out/f'CONTACTO_{start//12+1}.png')
audit=dict(pdf=str(dest),source=str(source),pages=len(r.pages),aspect_ratio=round(float(r.pages[0].mediabox.width)/float(r.pages[0].mediabox.height),5),rendered=len(files),overfull=bad,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),native_compiler='success',bytes=dest.stat().st_size)
(support/'AUDITORIA_BEAMER.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False))

