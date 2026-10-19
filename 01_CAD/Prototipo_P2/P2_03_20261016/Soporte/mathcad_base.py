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
  if n.func.id in ('sqrt','abs'):E.SubElement(e,q('sqrt' if n.func.id=='sqrt' else 'absval'));e.append(tree(n.args[0]));return e
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

