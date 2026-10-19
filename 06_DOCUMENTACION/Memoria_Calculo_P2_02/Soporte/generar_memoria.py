from pathlib import Path
from lxml import etree as E
from copy import deepcopy
import ast,math,json,textwrap,sys
sys.stdout.reconfigure(encoding='utf-8')
O=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02')
SUP=O/'Soporte';SUP.mkdir(parents=True,exist_ok=True)
B=Path(r'C:\Program Files (x86)\Mathcad\Mathcad 15')
W='http://schemas.mathsoft.com/worksheet30';M='http://schemas.mathsoft.com/math30'
NS={'w':W,'m':M};q=lambda s:'{'+M+'}'+s;w=lambda s:'{'+W+'}'+s
T=E.parse(str(B/'Resource Center/EN/qsheet/about_qs.xmcd')).getroot()
settings=deepcopy(T.find('w:settings',NS))
for x in settings.findall('.//w:textStyle',NS):
 for e in x.findall('.//w:inlineAttr',NS):e.set('font-family','Arial');e.set('font-size','10')
for e in settings.findall('.//w:mathStyle',NS):e.set('font-size','10')
pg=settings.find('.//w:pageModel',NS)
pg.set('paper-code','9');pg.set('page-width','595.276');pg.set('page-height','841.89');pg.set('print-single-page-width','true')
mar=pg.find('w:margins',NS)
for a in ['left','right','top','bottom']:mar.set(a,'42')
pg.set('show-page-frame','true')
settings.find('.//w:language',NS).set('math','EN')
settings.find('.//w:general',NS).set('precision','4')
settings.find('.//w:fileFormat',NS).set('save-numeric-results','true')
settings.find('.//w:fileFormat',NS).set('save-text-images','true')
hand=settings.find('.//w:handbook',NS)
if hand is not None:hand.set('file-permission-mask','4294967295')
root=E.Element(w('worksheet'),nsmap={None:W,'ml':M},version='3.0.3')
meta=E.SubElement(root,w('metadata'));E.SubElement(meta,w('generator')).text='SEDAC - Memoria MC15 - 2026-10-15'
ud=E.SubElement(meta,w('userData'))
for k,v in [('title','SEDAC P2.02 - Memoria de cálculo preliminar'),('description','Prediseño; entradas editables y verificaciones dimensionales. Rev. MC01. Sin validación física.')]:E.SubElement(ud,w(k)).text=v
root.append(settings);regions=E.SubElement(root,w('regions'))
records=[];pages=[];inputs={};values={};env={'mm':.001,'m':1,'s':1,'kg':1,'N':1,'MPa':1e6,'Pa':1,'pi':math.pi}
units={}
def ident(n):
 e=E.Element(q('id'));e.set('{http://www.w3.org/XML/1998/namespace}space','preserve');e.text='π' if n=='pi' else n;return e
def tree(n):
 if isinstance(n,ast.Constant):
  e=E.Element(q('str' if isinstance(n.value,str) else 'real'));e.text=str(n.value);return e
 if isinstance(n,ast.Name):return ident(n.id)
 if isinstance(n,ast.BinOp):
  e=E.Element(q('apply'));E.SubElement(e,q({ast.Add:'plus',ast.Sub:'minus',ast.Mult:'mult',ast.Div:'div',ast.Pow:'pow'}[type(n.op)]))
  pr={ast.Add:10,ast.Sub:10,ast.Mult:20,ast.Div:20,ast.Pow:30}
  for side,ch in [('left',n.left),('right',n.right)]:
   ce=tree(ch)
   if isinstance(ch,ast.BinOp):
    need=pr[type(ch.op)]<pr[type(n.op)] or (side=='right' and isinstance(n.op,ast.Sub) and pr[type(ch.op)]==10) or (isinstance(n.op,ast.Pow) and side=='left')
    if need:
     pe=E.Element(q('parens'));pe.append(ce);ce=pe
   e.append(ce)
  return e
 if isinstance(n,ast.UnaryOp):
  e=E.Element(q('apply'));E.SubElement(e,q('neg'));e.append(tree(n.operand));return e
 if isinstance(n,ast.Call):
  e=E.Element(q('apply'))
  if n.func.id=='sqrt':E.SubElement(e,q('sqrt'));e.append(tree(n.args[0]));return e
  e.append(ident(n.func.id))
  if len(n.args)>1:
   seq=E.SubElement(e,q('sequence'))
   for a in n.args:seq.append(tree(a))
  else:e.append(tree(n.args[0]))
  return e
 if isinstance(n,ast.Compare):
  e=E.Element(q('apply'));E.SubElement(e,q({ast.GtE:'greaterOrEqual',ast.LtE:'lessOrEqual',ast.Gt:'greaterThan',ast.Lt:'lessThan'}[type(n.ops[0])]))
  e.append(tree(n.left));e.append(tree(n.comparators[0]));return e
 raise TypeError(ast.dump(n))
def expr(s):return tree(ast.parse(s,mode='eval').body)
env.update(sqrt=math.sqrt,max=max,min=min)
def calc(s):return eval(compile(ast.parse(s,mode='eval'),'<equation>','eval'),{'__builtins__':{}},env)
P=-1;Y=0;PH=757.89
def reg(tag,height=30,left=16,width=490,color='inherit'):
 global Y
 ri=len(records)+1
 e=E.SubElement(regions,w('region'),{'region-id':str(ri),'left':str(left),'top':str(P*PH+Y),'width':str(width),'height':str(height),'align-x':str(left),'align-y':str(P*PH+Y+height*.65),'show-border':'false','show-highlight':('true' if color!='inherit' else 'false'),'is-protected':'false','z-order':'0','background-color':color,'tag':tag})
 records.append(dict(id=ri,page=P+1,y=Y,height=height,left=left,width=width,tag=tag))
 return e
def txt(s,size=10,bold=False,color='#253746',height=None):
 global Y
 lines=[]
 for a in s.split('\n'):lines+=textwrap.wrap(a,92 if size<=10 else 70,break_long_words=False) or ['']
 ht=height or (len(lines)*(size+3)+6)
 e=reg('texto',ht)
 tx=E.SubElement(e,w('text'),{'use-page-width':'false','push-down':'false','lock-width':'true'})
 for ln in lines:
  pp=E.SubElement(tx,w('p'),style='Normal')
  f=E.SubElement(pp,w('f'),family='Arial',charset='0',size=str(size))
  if bold:f=E.SubElement(f,w('b'))
  cc=E.SubElement(f,w('c'),val=color);cc.text=ln
 records[-1].update(kind='text',text=s)
 Y+=ht+6
def page(title,subtitle=''):
 global P,Y
 P+=1;Y=16;pages.append(title)
 txt('SEDAC / P2.02 / MC01',9,True,'#687A88',20)
 txt(title,14,True,'#123B54',28)
 if subtitle:txt(subtitle,9,color='#687A88')
def mathnode(e):return E.SubElement(e,w('math'),optimize='false',**{'disable-calc':'false'})
def output(name,unit='',left=355,y=None,height=34):
 global Y
 old=Y
 if y is not None:Y=y
 e=reg('eval_'+name,height,left,150)
 ev=E.SubElement(mathnode(e),q('eval'));ev.append(ident(name))
 if unit:un=E.SubElement(ev,q('unitOverride'));un.append(expr(unit))
 records[-1].update(kind='eval',name=name,unit=unit)
 Y=old
def define(name,s,unit='',height=48,wide=False,input=False):
 global Y
 top=Y
 e=reg(name,height,width=490 if wide else 330,color='#F0F6FC' if input else 'inherit')
 de=E.SubElement(mathnode(e),q('define'));de.append(ident(name));de.append(expr(s))
 val=calc(s);env[name]=val;values[name]=val;units[name]=unit
 records[-1].update(kind='define',name=name,expression=s,unit=unit,value=val,input=input)
 if input:inputs[name]=s
 if not wide:output(name,unit,y=top,height=height)
 Y=top+height+4
 if wide:
  output(name,unit,left=20,y=Y);Y+=35
def fun(name,args,s,height=56):
 global Y
 e=reg(name,height)
 de=E.SubElement(mathnode(e),q('define'));fn=E.SubElement(de,q('function'));fn.append(ident(name));bv=E.SubElement(fn,q('boundVars'))
 for a in args:E.SubElement(bv,q('id')).text=a
 de.append(expr(s))
 env[name]=lambda *v,ss=s,aa=args:eval(compile(ast.parse(ss,mode='eval'),'<function>','eval'),{'__builtins__':{}},dict(env,**dict(zip(aa,v))))
 records[-1].update(kind='function',name=name,args=args,expression=s)
 Y+=height+5
def gap(n=8):
 global Y
 Y+=n

page('1. Alcance y escenario de carga','Memoria editable en Mathcad clásico. Diseño de referencia: P2.02, 15/10/2026.')
txt('Se estudia un sistema auxiliar para apoyar y estabilizar una bomba de espalda. Se revisan rieles, cuna, cartelas, anclajes y uniones con modelos analíticos simplificados.')
txt('Las entradas azules son hipótesis de prediseño. La bomba real, el arnés, la temperatura y el espectro de fatiga siguen pendientes. Un margen calculado no acredita la seguridad del conjunto.',color='#8A4A12')
define('Mass','25*kg','kg',input=True)
define('grav','9.81*m/s**2','m/s**2',input=True)
define('av','3',input=True);define('ah','1',input=True);define('eta','0.7',input=True)
define('Fv','Mass*grav*av','N');define('Fh','Mass*grav*ah','N')
txt('av = 3 representa 3 g verticales totales, incluida gravedad. Fh es una fuerza horizontal resultante de dirección variable. Se asigna 70% al lado más cargado.')

page('2. Geometría y propiedades de referencia')
define('H','500*mm','mm',input=True);define('Sep','200*mm','mm',input=True)
define('b','50*mm','mm',input=True);define('d','25*mm','mm',input=True);define('t','2.5*mm','mm',input=True)
define('ecc','100*mm','mm',input=True);define('Linput','400*mm','mm',input=True)
define('Le','max(Linput,H-100*mm)','mm')
define('nReq','2.2',input=True);define('deltaLim','5*mm','mm',input=True)
txt('b es ancho y d profundidad del tubo. El brazo ecc se mide desde el eje del riel hasta la línea de acción de carga; debe medirse con la bolsa llena.')

page('3. Materiales y factores provisionales')
define('SyR','240*MPa','MPa',input=True);define('SyS','130*MPa','MPa',input=True)
define('SyB','450*MPa','MPa',input=True);define('Emod','69000*MPa','MPa',input=True)
define('nu','0.33',input=True);define('rho','2700*kg/m**3','kg/m**3',input=True)
define('Kt','2',input=True);define('Kslot','1.5',input=True);define('Kb','1.2',input=True)
txt('SyR: 6061-T6 sin soldar; SyS: 5052-H32, valor conservador adoptado; SyB: tornillos A2-70. Confirmar aleación, temple, producto y certificado.')
txt('Kt y Kslot son amplificaciones provisionales: no son factores de concentración determinados por FEA. El margen objetivo es una decisión del proyecto.',color='#8A4A12')

page('4. Propiedades exactas de la sección redondeada')
txt('Se resta el contorno interior del exterior, con radios ro = 2t y ri = t. Las funciones siguientes permiten cambiar b, d y t manteniendo las unidades.')
define('c0','1-pi/4');define('c1','1/3-pi/16')
fun('Jc',['c','r'],'c0*c**2*r**2+c*r**3/3+c1*r**4')
fun('Ar',['B','D','R'],'B*D-(4-pi)*R**2')
fun('Ir',['B','D','R'],'B*D**3/12-4*Jc(D/2-R,R)')
define('ro','2*t','mm');define('ri','t','mm')
define('Area','Ar(b,d,ro)-Ar(b-2*t,d-2*t,ri)','mm**2')
define('Ix','Ir(b,d,ro)-Ir(b-2*t,d-2*t,ri)','mm**4')
define('Iz','Ir(d,b,ro)-Ir(d-2*t,b-2*t,ri)','mm**4')
txt('Ir(B,D,R) es el segundo momento alrededor del eje paralelo a B. Este desarrollo analítico sustituye el contorno discretizado del cálculo anterior.')

page('5. Riel: solicitaciones normales')
define('Zx','Ix/(d/2)','mm**3');define('Zz','Iz/(b/2)','mm**3')
define('MassR','2*H*Area*rho','kg')
define('Nr','eta*Fv','N');define('Me','eta*Fv*ecc','N*mm')
define('SigAx','Nr/Area','MPa');define('SigEc','Me/Zx','MPa')
define('SigH','eta*Fh*Le*sqrt(1/Zx**2+1/Zz**2)','MPa',height=60,wide=True)
define('SigN','SigAx+SigEc+SigH','MPa')
txt('SigH maximiza la suma de flexiones para una fuerza horizontal resultante de módulo Fh. Se usa una idealización de riel en voladizo.')

page('6. Riel: torsión, fluencia y flecha')
define('Am','(b-t)*(d-t)-(4-pi)*(1.5*t)**2','mm**2')
define('Tr','eta*Fh*Sep/2','N*mm')
define('TauT','Tr/(2*Am*t)','MPa')
define('TauV','eta*sqrt(Fv**2+Fh**2)/Area','MPa')
txt('TauV reproduce una envolvente conservadora del prediseño: incluye la fuerza vertical en cortante medio aunque el riel también la recibe axialmente. No es un campo local de tensiones.')
define('SigVM','Kt*sqrt(SigN**2+3*(TauT+TauV)**2)','MPa',wide=True)
define('nR','SyR/SigVM')
define('deltaH','eta*Fh*Le**3/(3*Emod*min(Ix,Iz))','mm',height=58)
define('deltaE','Me*Le**2/(2*Emod*Ix)','mm')
define('deltaR','deltaH+deltaE','mm')
txt('Contrastar nR con nReq y deltaR con deltaLim. La suma de flechas es una cota orientativa, dependiente de las condiciones reales del arnés.')

page('7. Riel: estimaciones de estabilidad')
define('Kcol','2',input=True)
define('Pcr','pi**2*Emod*min(Ix,Iz)/(Kcol*Le)**2','N',height=60)
define('nEuler','Pcr/Nr')
define('bp','max(b,d)-4*t','mm')
define('kplate','4',input=True)
define('SigCr','kplate*pi**2*Emod/(12*(1-nu**2))*(t/bp)**2','MPa',height=65,wide=True)
define('SigCap','min(SyR,SigCr)','MPa')
txt('Euler supone una columna ideal con longitud efectiva 2Le. El pandeo local supone una pared apoyada y sin agujeros. Si SigCr supera SyR, la fluencia ocurre antes que ese pandeo elástico.')
txt('No se han calculado pandeo flexotorsional, imperfecciones ni estabilidad de las uniones. No se interpreta nEuler como seguridad global.',color='#8A4A12')

page('8. Cartelas: tornillos M8 y reparto de esfuerzos')
define('pitch','45*mm','mm',input=True);define('armH','62.5*mm','mm',input=True)
define('As8','36.6*mm**2','mm**2',input=True);define('dia8','8*mm','mm',input=True)
define('Vy','eta*Fv','N');define('Vz','eta*Fh','N')
define('MomC','eta*(Fv*ecc+Fh*armH)','N*mm',height=58)
define('R8old','Kb*sqrt((sqrt(Vy**2+Vz**2)/2)**2+(MomC/pitch)**2)','N',height=66,wide=True)
define('R8','Kb*sqrt((Vy/2)**2+(Vz/2+MomC/pitch)**2)','N',height=66,wide=True)
txt('Corrección: la fuerza horizontal directa y el esfuerzo producido por el momento se suman en el tornillo crítico antes de obtener la resultante. R8old se conserva solo para comparar.',color='#8A4A12')

page('9. Cartelas: cortante, aplastamiento y arrancamiento')
define('tg','4*mm','mm',input=True)
define('VM8','sqrt(3)*R8/As8','MPa');define('nBolt8','SyB/VM8')
define('BearR','R8/(dia8*t)','MPa');define('nBearR','SyR/BearR')
define('BearG','R8/(dia8*tg)','MPa');define('nBearG','SyS/BearG')
define('edge','min(15*mm,d/2)','mm')
define('hole8','8.6*mm','mm',input=True)
define('TearG','sqrt(3)*R8/(2*(edge-hole8/2)*tg)','MPa',height=62)
define('nTearG','SyS/TearG')
txt('Se usa una sola pared del tubo para aplastamiento y sección resistente de rosca para cortante del tornillo. Sin crédito de fricción ni reparto por la segunda pared.')

page('10. Cartela: raíz y límites de la unión')
define('hRoot','80*mm','mm',input=True)
define('Vcart','sqrt(Vy**2+Vz**2)','N')
define('SigRoot','6*MomC/(tg*hRoot**2)','MPa')
define('TauRoot','Vcart/(tg*hRoot)','MPa')
define('VMroot','2*sqrt(SigRoot**2+3*TauRoot**2)','MPa')
define('nRoot','SyS/VMroot')
txt('Modelo de sección rectangular idealizada con amplificación local 2. El recorte de aligeramiento, el pliegue y el ala requieren un análisis local.')
txt('El cálculo anterior revisa cortante externo del M8; no verifica tracción por palanca, apertura, precarga, aplastamiento bajo cabeza/arandela ni pérdida de apriete. Los casquillos deben ajustar al tubo real.')
txt('La posición de las fijaciones principales evita depender de plástico comprimido para sostener la precarga. La longitud y tolerancia de casquillos aún deben especificarse.')

page('11. Cuna: apoyo del piso y cargas locales')
define('Width','300*mm','mm',input=True);define('Depth','125*mm','mm',input=True)
define('tf','2.5*mm','mm',input=True);define('spanF','Depth-60*mm','mm')
define('over','40*mm','mm',input=True)
define('Ppatch','100*N','N',input=True);define('strip','50*mm','mm',input=True)
define('qfloor','2*Fv/(Width*Depth)','MPa')
define('Mspan','qfloor*spanF**2/8+Ppatch*spanF/(4*strip)','N')
define('Medge','qfloor*over**2/2+Ppatch*over/strip','N')
txt('Se usan ejes de refuerzos como líneas de apoyo: separación 65 mm y voladizo 40 mm. El piso se idealiza por franjas de ancho unitario. Mspan y Medge son momentos por unidad de ancho, de unidad N. La carga localizada se coloca por separado entre apoyos y en el extremo del voladizo.')

page('12. Cuna: resultado del caso de borde')
define('Mfloor','max(Mspan,Medge)','N')
define('SigFloor','6*Mfloor/tf**2','MPa')
define('nFloor','SyS/SigFloor')
define('tNeed','sqrt(6*Mfloor*nReq/SyS)','mm')
define('tfProp','3.5*mm','mm',input=True)
define('SigProp','6*Mfloor/tfProp**2','MPa')
define('nProp','SyS/SigProp')
txt('Con las entradas iniciales, el caso de carga localizada en el borde no alcanza el margen objetivo para el piso de 2,5 mm. La memoria propone comparar 3,5 mm o reducir el voladizo.',color='#A02B21',bold=True)
txt('La alternativa tfProp es una evaluación de cálculo. El CAD P2.02 conserva 2,5 mm: esta memoria no modifica automáticamente el modelo.')
txt('El contacto real de una bolsa flexible puede distribuir la fuerza de otra forma. El parche de 100 N y su ancho son hipótesis que deben contrastarse.')

page('13. Refuerzos inferiores y puente del anclaje de hombro')
define('br','20*mm','mm',input=True);define('tr','1.5*mm','mm',input=True)
define('Irib','Ir(br,br,2*tr)-Ir(br-2*tr,br-2*tr,tr)','mm**4')
define('Zrib','Irib/(br/2)','mm**3')
define('Lrib','Sep+b','mm')
define('SigRib','eta*Fv*Lrib/(4*Zrib)','MPa')
define('nRib','SyR/SigRib')
define('slot','52*mm','mm',input=True);define('bridgeS','24*mm','mm',input=True)
define('ta','5*mm','mm',input=True)
define('SigSlot','Kslot*6*(eta*Fv*slot/4)/(bridgeS*ta**2)','MPa',height=58)
define('nSlot','SyR/SigSlot')
txt('Se usa un tubo inferior con esquinas redondeadas y carga puntual equivalente. El puente de la cinta se aproxima como viga apoyada bajo fuerza fuera del plano.')

page('14. Yugo de cinturón y diagonales')
define('tb','5*mm','mm',input=True);define('bridgeB','26*mm','mm',input=True)
define('SigBelt','Kslot*6*(eta*Fv*slot/4)/(bridgeB*tb**2)','MPa',height=58)
define('nBelt','SyR/SigBelt')
define('Zbelt','100*mm*tb**2/6','mm**3')
define('SigYoke','2*eta*Fv*40*mm/Zbelt','MPa')
define('nYoke','SyR/SigYoke')
define('riseX','H-30*mm-(120*mm+30*mm)','mm')
define('LenX','sqrt(Sep**2+riseX**2)','mm')
define('ForceX','Fh*LenX/Sep','N')
define('NetX','2*mm*(24*mm-6.6*mm)','mm**2')
define('nX','SyS/(ForceX/NetX)')
txt('Solo se acredita la diagonal traccionada; la opuesta puede pandear. Falta verificar herrajes del cinturón, costuras, liberación y transferencia real a la cadera.')

page('15. M6, criterios y verificaciones que siguen abiertas')
define('As6','20.1*mm**2','mm**2',input=True)
define('R6','Kb*eta*Fv/2','N')
define('VM6','sqrt(3)*R6/As6','MPa')
define('nM6','SyB/VM6')
define('MinYield','min(nR,nBolt8,nBearR,nBearG,nTearG,nRoot,nFloor,nRib,nSlot,nBelt,nYoke,nX,nM6)',wide=True)
txt('MinYield reúne márgenes de modelos parciales para localizar el resultado menor. No representa un factor de seguridad global del sistema.')
txt('Fatiga: falta espectro de ciclos y curvas S-N del detalle real. No se asigna vida útil.\nUniones: faltan tracción, precarga, aflojamiento y palanca.\nTemperatura: materiales de contacto sin calificación para fuego.\nErgonomía: faltan mediciones de bomba, cuerpo, arnés y presión de contacto.')
txt('El criterio de Von Mises se aplica como aproximación a fluencia de materiales dúctiles. No sustituye criterios de fractura, fatiga ni ensayos de los textiles.',color='#8A4A12')

page('16. Resumen calculado y comparación con P2.02')
txt('Para aceptar cada precriterio de fluencia: n >= nReq. Para flecha: deltaR <= deltaLim. Los resultados se recalculan al modificar las entradas de páginas anteriores.')
for name,unit in [('nReq',''),('nR',''),('deltaR','mm'),('nBolt8',''),('nBearR',''),('nBearG',''),('nTearG',''),('nRoot',''),('nFloor',''),('nRib',''),('nSlot',''),('nBelt',''),('nYoke',''),('nX',''),('nM6','')]:
 output(name,unit,left=22,y=Y);Y+=30
txt('La revisión corrige dos aspectos del cálculo previo: suma vectorial en M8 y parche en el borde del piso. Con entradas iniciales, la cuna requiere revisión para alcanzar el margen objetivo.',color='#A02B21',bold=True)

page('17. Estado del modelo, fuentes y uso de la memoria')
txt('Modelo geométrico de referencia: 54 diseños de piezas, 70 ocurrencias y cero interferencias volumétricas en Inventor. Masa representada aproximada: 3,206 kg, sin arnés completo. Estos datos son registros del CAD; no se recalculan al editar esta hoja.')
txt('Las dimensiones oficiales de bolsa vacía no describen la forma de la bolsa llena. La masa de referencia de 25 kg y los factores de carga fueron elegidos para prediseño.')
txt('Fuentes técnicas:\n[1] Scotty Firefighter, catálogo oficial, Alpha Backpack 4000-BP: capacidad 19 L y conexión inferior central.\n[2] Hydro, Alloy 6061, ficha de extrusión: propiedades según temple y producto.\n[3] Atlas Steels, ficha 5052 y Technical Note 14: propiedades y diferencias entre especificaciones.\n[4] Bossard, Stainless steel fasteners, ISO 3506: clase A2-70.\n[5] NASA RP-1228, Fastener Design Manual, 1990: revisión de grupos de tornillos y cargas combinadas.')
gap(50)
txt('Enlaces completos y auditoría: LEEME_MEMORIA.md y REVISION_CALCULOS.md, junto a esta hoja. No se declara conformidad con normas aeroespaciales.')
txt('Uso: editar entradas azules, recalcular la hoja y revisar los márgenes y unidades. La modificación de esta memoria no actualiza el CAD ni sus archivos JSON. Al cambiar la geometría deben revisarse apoyos, brazos y cargas.')
txt('Fecha de revisión: 15/10/2026. Versión documental MC01. Documento de trabajo sujeto a revisión técnica y pruebas de banco.',9)

# Validar que nada cae fuera de la página antes de abrir en Mathcad.
for r in records:
 assert r['y']+r['height']<=PH-10,(r['page'],r['tag'],r['y'],r['height'])
source=SUP/'fuente_memoria_MC01f.xmcd'
E.ElementTree(root).write(str(source),encoding='UTF-8',xml_declaration=True)
# XSD oficial de la instalación.
schema=E.XMLSchema(E.parse(str(B/'schema/worksheet30.xsd')))
assert schema.validate(E.parse(str(source))),str(schema.error_log)
(SUP/'REGIONES.json').write_text(json.dumps(dict(pages=pages,page_height=PH,records=records),ensure_ascii=False,indent=2),encoding='utf-8')
(SUP/'VALORES_ESPERADOS_SI.json').write_text(json.dumps([dict(name=k,value=v) for k,v in values.items()],indent=2),encoding='utf-8')
(SUP/'ENTRADAS.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
print(json.dumps(dict(pages=len(pages),regions=len(records),variables=len(values),R8_N=env['R8'],nFloor=env['nFloor'],tNeed_mm=env['tNeed']/.001,nR=env['nR'],nProp=env['nProp']),ensure_ascii=False))

