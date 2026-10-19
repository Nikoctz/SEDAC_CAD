from pathlib import Path
import subprocess, json
from PIL import Image, ImageOps, ImageDraw, ImageFont
base=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02')
out=base/'Soporte'/'Revision_Guia_PDF'
out.mkdir(exist_ok=True)
exe=r'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
pdf=base/'Guia_Explicada_Memoria_SEDAC_P2_02_MC01.pdf'
subprocess.run([exe,'-r','90','-png',str(pdf),str(out/'pagina')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
files=sorted(out.glob('pagina-*.png'))
font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',17)
for start in range(0,len(files),9):
    contact=Image.new('RGB',(1080,1575),'#DDE5E9')
    for j,file in enumerate(files[start:start+9]):
        im=Image.open(file).convert('RGB')
        im.thumbnail((338,477))
        x=11+(j%3)*360+(338-im.width)//2
        y=34+(j//3)*525
        contact.paste(im,(x,y))
        ImageDraw.Draw(contact).text((11+(j%3)*360,y-24),'Página '+str(start+j+1),font=font,fill='#173345')
    contact.save(out/f'CONTACTO_{start//9+1}.png')
print(json.dumps(dict(rendered=len(files),contacts=3),ensure_ascii=False))

