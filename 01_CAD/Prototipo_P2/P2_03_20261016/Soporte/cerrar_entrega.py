from pathlib import Path
import json,re,hashlib,zipfile
ROOT=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD')
B=ROOT/'01_CAD/Prototipo_P2/P2_03_20261016';M=ROOT/'06_DOCUMENTACION/Memoria_Calculo_P2_03';CAD=B/'Entrega/Inventor_Optimizado'
p=M/'Soporte/AUDITORIA_ENTREGA.json';j=json.loads(p.read_text(encoding='utf-8-sig'));j['visual_review']='Revisión visual por el asistente de las 55 diapositivas PDF, las 45 páginas Mathcad y las tres vistas CAD; sin recortes ni solapamientos observados. Detalles ampliados revisados en PDF25/37 y Mathcad12/43.';p.write_text(json.dumps(j,indent=2,ensure_ascii=False),encoding='utf-8')
for p in [B/'INFORME_DISENO_P2_03.md',M/'LEEME_MEMORIA.md']:
 s=p.read_text(encoding='utf-8')
 for a,c in [('altura6','altura 6'),('altura5','altura 5'),('exterior10/interior6,6','exterior 10/interior 6,6'),('longitud53','longitud 53'),('taladros10,2','taladros 10,2'),('DIN980','DIN 980'),('clase80','clase 80'),('dispersión25','dispersión 25'),('ISO3506','ISO 3506')]:s=s.replace(a,c)
 p.write_text(s,encoding='utf-8')
p=M/'LEEME_MEMORIA.md';s=p.read_text(encoding='utf-8');s+='\n## Borrador abierto en otra instancia\n\nEl archivo sin la palabra FINAL es un borrador generado durante esta tarea. Quedó bloqueado por otra instancia de Mathcad y no se pudo trasladar a Soporte. No se incluye en el ZIP de entrega. Usar únicamente **MC02_FINAL_EDITABLE.xmcd**; el borrador podrá archivarse después de cerrar esa ventana.\n';p.write_text(s,encoding='utf-8')
p=B/'Soporte/REGENERAR_P2_03.ps1';s=p.read_text(encoding='utf-8-sig')
s=s.replace('$priorParts=@{};$priorMass=@{};$priorThreads=@()','$priorParts=@{};$priorMass=@{};$priorThreads=@();$priorRounding=@()')
s=s.replace("$pd=Get-Content -Raw -LiteralPath (Join-Path $Desde 'MODELO_API.json') | ConvertFrom-Json", "if(Test-Path -LiteralPath (Join-Path $Desde 'REDONDEOS.json')){$priorRounding=Get-Content -Raw -LiteralPath (Join-Path $Desde 'REDONDEOS.json') | ConvertFrom-Json}\n $pd=Get-Content -Raw -LiteralPath (Join-Path $Desde 'MODELO_API.json') | ConvertFrom-Json")
s=s.replace('$threads+=@($priorThreads | Where-Object {$_.pieza -eq $p.name})','$threads+=@($priorThreads | Where-Object {$_.pieza -eq $p.name})\n    $rounding+=@($priorRounding | Where-Object {$_.pieza -eq $p.name})')
p.write_text(s,encoding='utf-8-sig')
# Capture every final deliverable, not the iterations or caches.
files=[]
for p in CAD.iterdir():
 if p.is_file() and p.suffix.lower() in {'.ipt','.iam','.step','.png','.json','.csv','.txt'} and p.name!='ERROR.txt':files.append(p)
for n in ['LEEME.md','INFORME_DISENO_P2_03.md','ESPECIFICACION_P2_03.md','PARAMETROS_P2_03.json','HOJA_MEDICION_P2_03.md']:files.append(B/n)
for n in ['generar_p2_03.py','REGENERAR_P2_03.ps1','calcular_y_mathcad.py','mathcad_base.py'] :files.append(B/'Soporte'/n)
for n in ['LEEME_MEMORIA.md','Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd','Guia_SEDAC_P2_03_MC02_Beamer.tex','Guia_SEDAC_P2_03_MC02_Beamer.pdf']:files.append(M/n)
for n in ['RESUMEN_CALCULO.json','VERIFICACION_MATHCAD.json','ERRORES_MATHCAD.json','AUDITORIA_ENTREGA.json','ENTRADAS.json','REGIONES.json','VALORES_ESPERADOS_SI.json','crear_beamer.py','comprobar_mathcad.ps1']:files.append(M/'Soporte'/n)
manifest=[]
for p in sorted(files):
 assert p.exists(),str(p)
 manifest.append({'ruta':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'HUELLAS_ENTREGA.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
files.append(B/'HUELLAS_ENTREGA.json')
z=B/'SEDAC_P2_03_ENTREGA.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in sorted(files):f.write(p,p.relative_to(ROOT).as_posix())
 f.writestr('ABRIR_PRIMERO.txt','SEDAC P2.03 / 16-10-2026\n\nExtraer todo el ZIP conservando carpetas.\nCAD e instrucciones: 01_CAD/Prototipo_P2/P2_03_20261016/LEEME.md\nMathcad y PDF: 06_DOCUMENTACION/Memoria_Calculo_P2_03/LEEME_MEMORIA.md\nAbrir el IAM con los 51 IPT en su misma carpeta.\nAbrir la memoria que termina MC02_FINAL_EDITABLE.xmcd.\nPrediseno pendiente de mediciones y validacion fisica.\n')
with zipfile.ZipFile(z) as f:
 for e in manifest:assert hashlib.sha256(f.read(e['ruta'])).hexdigest()==e['sha256']
old=ROOT/'01_CAD/Prototipo_P2/P2_02_20261015/SEDAC_P2_02_ENTREGA.zip'
assert hashlib.sha256(old.read_bytes()).hexdigest()=='9353e6ef30483065898f710e1b56b6be4a7f2c876f8e23a77ad9cce72a151f1c'
status={'version':'P2.03','fecha':'2026-10-16','estado':'Entrega de prediseño completa','cad':'Entrega/Inventor_Optimizado/SEDAC_P2_03.iam','mathcad':'06_DOCUMENTACION/Memoria_Calculo_P2_03/Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd','pdf_diapos':55,'masa_rigida_kg':2.3331284134369037,'masa_reservada_kg':2.913128413437,'zip_bytes':z.stat().st_size,'archivos_zip':len(files)+1,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'pendientes_ingenieria':['mediciones','tolerancias y productos comerciales','FEA','fatiga','ensayos y arnes'],'organizacion':'CAD intermedios archivados. Un XMCD borrador quedó bloqueado por otra instancia; excluido del ZIP y señalado en LEEME.'}
(B/'ESTADO_ENTREGA.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(status,ensure_ascii=False,indent=2))
