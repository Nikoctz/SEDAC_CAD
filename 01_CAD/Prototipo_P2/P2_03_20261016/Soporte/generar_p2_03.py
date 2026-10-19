from pathlib import Path
import json,math,csv,sys
BASE=Path(__file__).resolve().parent.parent
O=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'CAD'
O.mkdir(parents=True,exist_ok=True)
C=json.loads((BASE/'PARAMETROS_P2_03.json').read_text(encoding='utf-8-sig'))
G=C['geometria'];globals().update(G)
parts=[];instances=[];bolts=[]
colors={'6061':(162,185,196),'5052':(124,154,169),'anclaje':(218,149,63),'hdpe':(31,92,100),'herrajes':(105,114,124),'pad':(43,59,66)}
def rect(x,y,w,h,r=0):return dict(kind='rr',x=x,y=y,w=w,h=h,r=r)
def circle(x,y,r):return dict(kind='circle',x=x,y=y,r=r)
def poly(p):return dict(kind='poly',pts=p)
def op(axis,start,depth,loops,cut=False,label='Forma'):return dict(axis=axis,start=start,depth=depth,loops=loops,cut=cut,label=label)
def part(name,ops,mat='6061',ref=False,**kw):
 p=dict(name=name,ops=ops,material=mat,color=colors[mat],reference=ref,**kw);parts.append(p)
 instances.append(dict(part=name,name=name,axis='z',position=[0,0,0]));return p
def bolt(axis,pos,diam,grip,tag):bolts.append(dict(axis=axis,pos=pos,diam=diam,grip=grip,tag=tag))
def hexagon(af):return poly([[af/math.sqrt(3)*math.cos(a*math.pi/3),af/math.sqrt(3)*math.sin(a*math.pi/3)] for a in range(6)])
xb=S/2+b/2-8
zholes=hip_y+shoulder_y+brace_y
for side,cx in [('I',-S/2),('D',S/2)]:
 ops=[op('y',0,H,[rect(0,cx-b/2,d,b,2*t)],label='Perfil_exterior'),
      op('y',-.1,H+.2,[rect(t,cx-b/2+t,d-2*t,b-2*t,t)],True,'Vaciado'),
      op('z',-.1,d+.2,[circle(cx,yy,3.3) for yy in zholes],True,'M6_pasantes'),
      op('x',cx-b/2-.1,b+.2,[circle(yy,d/2,5.1) for yy in bolt8_y],True,'M8_pasantes')]
 part('Riel_'+side,ops)
 for yy in zholes:
  part(f'Casquillo_M6_{side}_{yy}',[op('z',t,d-2*t,[circle(cx,yy,5),circle(cx,yy,3.3)])])
 for yy in bolt8_y:
  part(f'Pasador_hueco_M6_{side}_{yy}',[op('x',cx-b/2-tg if side=='I' else cx-b/2,b+tg,[circle(yy,d/2,5),circle(yy,d/2,3.3)])])
 xweb=cx-b/2-tg if side=='I' else cx+b/2
 web=poly([[0,0],[Y-20,0],[Y-20,d+D],[Y-50,d+D*.60],[0,d]])
 ops=[op('x',xweb,tg,[web],label='Alma'),
      op('y',Y-20-tflange,tflange,[rect(d,xweb if side=='I' else xweb-16,D,16+tg)],label='Ala_de_apoyo'),
      op('x',xweb-.1,tg+.2,[circle(yy,d/2,5.1) for yy in bolt8_y],True,'M8'),
      op('x',xweb-.1,tg+.2,[rect(Y-62,d+22,20,28,8)],True,'Aligeramiento'),
      op('y',Y-20-tflange-.1,tflange+.2,[circle(d+z, -xb if side=='I' else xb,2.75) for z in support_depths],True,'M5')]
 part('Cartela_'+side,ops,'6061')
 for yy in bolt8_y:bolt('x',[cx-b/2-tg if side=='I' else cx-b/2,yy,d/2],6,b+tg,'Cartela_'+side)
 for z in support_depths:
  xx=-xb if side=='I' else xb;zz=d+z
  part(f'Apoyo_interior_M5_{side}_{z}',[op('x',xx-5,10,[rect(Y-rib_h+rib_t,zz-rib_d/2+rib_t,rib_h-2*rib_t,rib_d-2*rib_t,rib_t)]),op('y',Y-rib_h-0.1,rib_h+0.2,[circle(zz,xx,2.75)],True,'M5')])
  bolt('y',[xx,Y-rib_h-tflange,zz],5,rib_h+tflange+tf,'Cuna_'+side)
# Three narrow-depth cross tubes. The front one ends exactly behind hose opening.
for i,z in enumerate(support_depths):
 zz=d+z
 ops=[op('x',-W/2,W,[rect(Y-rib_h,zz-rib_d/2,rib_h,rib_d,2*rib_t)]),
      op('x',-W/2-.1,W+.2,[rect(Y-rib_h+rib_t,zz-rib_d/2+rib_t,rib_h-2*rib_t,rib_d-2*rib_t,rib_t)],True,'Vaciado'),
      op('y',Y-rib_h-.1,rib_h+.2,[circle(zz,xx,2.75) for xx in [-xb,xb]],True,'M5')]
 part('Refuerzo_cuna_'+str(i+1),ops)
hose=circle(d+D+hose_offset,0,hose_radius)
ops=[op('y',Y,tf,[rect(d,-W/2,D,W,6)],label='Piso'),
     op('y',Y-.1,tf+.2,[hose],True,'Salida_frontal_manguera'),
     op('z',d,tf,[rect(-W/2+6,Y+tf,W-12,12,3)],label='Respaldo')]
for xx in [-W/2,W/2-tf]:ops.append(op('x',xx,tf,[rect(Y+tf,d+6,12,D-12,3)],label='Labio_lateral'))
ops += [op('y',Y-.1,tf+.2,[circle(d+z,xx,2.75) for z in support_depths for xx in [-xb,xb]],True,'M5')]
part('Cuna_modular',ops,'5052')
# Narrower transverse bars and X remain structural.
for tag,cy in [('Bajo',brace_y[0]),('Alto',brace_y[1])]:
 ops=[op('z',-2,2,[rect(-S/2-16,cy-14,S+32,28,5)]),
      op('z',-2.1,2.2,[circle(xx,cy,3.3) for xx in [-S/2,S/2]],True,'Fijaciones')]
 part('Travesano_'+tag,ops,'6061')
for idx,sign in enumerate([1,-1]):
 a=[-sign*S/2,brace_y[0]];c=[sign*S/2,brace_y[1]]
 ll=math.dist(a,c);vx=(c[0]-a[0])/ll;vy=(c[1]-a[1])/ll;nx=-vy;ny=vx;hw=10
 pts=[[a[0]-vx*12+nx*hw,a[1]-vy*12+ny*hw],[a[0]-vx*12-nx*hw,a[1]-vy*12-ny*hw],
      [c[0]+vx*12-nx*hw,c[1]+vy*12-ny*hw],[c[0]+vx*12+nx*hw,c[1]+vy*12+ny*hw]]
 zz=-4-idx*2
 part('Diagonal_'+str(idx+1),[op('z',zz,2,[poly(pts)]),op('z',zz-.1,2.2,[circle(*a,3.3),circle(*c,3.3)],True,'M6')],'5052')
 for xx,yy in [a,c]:
  if idx:part(f'Calce_X_{int(xx)}_{int(yy)}',[op('z',-4,2,[circle(xx,yy,7),circle(xx,yy,3.3)])],'6061')
  bolt('z',[xx,yy,zz],6,d-zz,'Marco')
# Tapered shoulder fittings retain original 5 mm load bridges.
for side,cx in [('I',-S/2),('D',S/2)]:
 outline=poly([[cx-18,350],[cx+18,350],[cx+38,400],[cx+38,440],[cx-38,440],[cx-38,400]])
 ops=[op('z',d,ta,[outline]),
      op('z',d-.1,ta+.2,[circle(cx,yy,3.3) for yy in shoulder_y]+[rect(cx-26,408,52,8,4)],True,'Correa_M6')]
 for sign in [-1,1]:
  edge=[[cx+sign*18,350],[cx+sign*38,400],[cx+sign*38,440],[cx+sign*(38-ta),440],[cx+sign*(38-ta),400],[cx+sign*(18-ta),350]]
  ops.append(op('z',d+ta,pan_depth-ta,[poly(edge)],label='Retorno_lateral'))
 ops.append(op('z',d+ta,pan_depth-ta,[rect(cx-38,440-ta,76,ta)],label='Retorno_puente'))
 part('Anclaje_hombro_'+side,ops,'anclaje')
 for yy in shoulder_y:bolt('z',[cx,yy,0],6,d+ta,'Hombro_'+side)
# Independent hip fittings: retain 100 mm root height, 26 mm strap bridge.
for side,sign in [('I',-1),('D',1)]:
 x0=80 if sign==1 else -155
 slotx=121 if sign==1 else -129
 ops=[op('z',-tb,tb,[rect(x0,15,75,100,4)]),
      op('z',-tb-.1,tb+.2,[circle(sign*100,yy,3.3) for yy in hip_y]+[rect(slotx,37,8,52,4)],True,'Cinturon_M6')]
 ops.append(op('z',-pan_depth,pan_depth-tb,[rect(x0,15,75,tb),rect(x0,115-tb,75,tb),rect(155-tb if sign==1 else -155,15+tb,tb,100-2*tb)],label='Retornos_cinturon'))
 part('Anclaje_cinturon_'+side,ops,'anclaje')
 for yy in hip_y:bolt('z',[sign*100,yy,-tb],6,d+tb,'Cinturon_'+side)
# Foam references; included in the textile allowance, not rigid added mass.
for side,cx in [('I',-100),('D',100)]:
 part('REF_Acolchado_'+side,[op('z',-28,12,[rect(cx-30,145,60,345,15)])],'pad',True)
# Hollow tray protector: continuous smooth top, underside pocket clears nuts/washers.
ztop=Y+tf+cover_gap
ops=[op('y',ztop,2,[rect(d+tf,-W/2+3,D-tf,W-6,6)],label='Cara_lisa'),
     op('y',Y+tf,cover_gap,[rect(d+tf,-W/2+3,D-tf,W-6,6),rect(d+tf+2,-W/2+5,D-tf-4,W-10,4)],label='Perimetro')]
# Supports run between bolt rows, avoiding hose and fasteners.
for xx in [-80,-40,40,80]:
 ops.append(op('y',Y+tf,cover_gap,[rect(d+tf+2,xx-1,D-tf-4,2)],label='Nervio_polimero'))
ops.append(op('y',Y+tf-.1,cover_gap+2.2,[hose],True,'Salida_manguera'))
part('Protector_bolsa_aligerado',ops,'hdpe',True)
# Real purchasing geometry, individual washer/nut/bolt definitions, cosmetic threads.
sizes={4:dict(p=.7,head=7,k=4,socket=3,wh=.8,wi=4.3,wo=9,nut=4,af=7,As=8.78),
       5:dict(p=.8,head=8.5,k=5,socket=4,wh=1,wi=5.3,wo=10,nut=5,af=8,As=14.2),
       6:dict(p=1,head=10,k=6,socket=5,wh=1.6,wi=6.4,wo=12,nut=6,af=10,As=20.1),
       8:dict(p=1.25,head=13,k=8,socket=6,wh=1.6,wi=8.4,wo=16,nut=8,af=13,As=36.6)}
created=set();standard_lengths=[10,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]
def hp(name,ops,thread=None,desc=''):
 if name in created:return
 created.add(name);parts.append(dict(name=name,ops=ops,material='herrajes',color=colors['herrajes'],reference=False,thread=thread,description=desc))
def instance(name,axis,pos,tag):instances.append(dict(part=name,name=tag,axis=axis,position=pos))
for j,bb in enumerate(bolts,1):
 dd=bb['diam'];q=sizes[dd];gr=bb['grip'];pitch=q['p']
 need=gr+2*q['wh']+q['nut']+2*pitch
 ln=next(z for z in standard_lengths if z>=need)
 bn=f'Tornillo_ISO4762_M{dd}x{ln}_A2_80'
 wn=f'Arandela_ISO7089_M{dd}'
 nn=f'Tuerca_autofrenante_M{dd}_DIN980'
 hp(bn,[op('z',0,ln,[circle(0,0,dd/2)],label='Vastago'),
        op('z',-q['k'],q['k'],[circle(0,0,q['head']/2)],label='Cabeza'),
        op('z',-q['k']-.1,q['k']*.6,[hexagon(q['socket'])],True,'Hexagono_interior')],
    dict(d=dd,pitch=pitch,internal=False,length=min(ln,2*dd+12)),f'ISO 4762; M{dd}x{pitch}; L={ln}; rosca b={min(ln,2*dd+12)}; A2-80; comprar con certificado')
 hp(wn,[op('z',0,q['wh'],[circle(0,0,q['wo']/2),circle(0,0,q['wi']/2)])],desc='ISO 7089; arandela plana, no dispositivo de bloqueo')
 # Bore at nominal major diameter avoids false clashes from cosmetic thread cylinders.
 hp(nn,[op('z',0,q['nut'],[hexagon(q['af']),circle(0,0,dd/2)])],
    dict(d=dd,pitch=pitch,internal=True,length=q['nut']),f'Derivada DIN 980, autofrenante metalica; altura {q["nut"]}; verificar clase y par prevalente del proveedor')
 axis=bb['axis'];ia={'x':0,'y':1,'z':2}[axis]
 reverse=bb['tag'].startswith('Hombro') or bb['tag']=='Cartela_D'
 if reverse:axis='n'+axis
 origin=bb['pos'].copy()
 if reverse:origin[ia]+=gr
 def shifted(delta):
  v=origin.copy();v[ia]+=(-delta if reverse else delta);return v
 instance(bn,axis,shifted(-q['wh']),f'{bb["tag"]}_{j}_Tornillo')
 instance(wn,axis,shifted(-q['wh']),f'{bb["tag"]}_{j}_Arandela_cabeza')
 instance(wn,axis,shifted(gr),f'{bb["tag"]}_{j}_Arandela_tuerca')
 instance(nn,axis,shifted(gr+q['wh']),f'{bb["tag"]}_{j}_Tuerca')
 bb.update(id=j,longitud=ln,paso=pitch,arandela=q['wh'],altura_tuerca=q['nut'],protrusion=ln-need+2*pitch,
           tornillo=bn,tuerca=nn,washer=wn,rosca_longitud=min(ln,2*dd+12),vastago_liso=ln-min(ln,2*dd+12),sentido=axis)
manifest=dict(version='P2.03',units='mm',parameters=C,parts=parts,instances=instances,bolts=bolts)
(O/'MODELO_API.json').write_text(json.dumps(dict(parts=parts,instances=instances,bolts=bolts),indent=2),encoding='utf-8')
(O/'MODELO_P2_03.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
with (O/'BOM_FIJACIONES.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,['id','tag','diam','paso','grip','arandela','altura_tuerca','longitud','protrusion','tornillo','tuerca'])
 w.writeheader();w.writerows([{k:x[k] for k in w.fieldnames} for x in bolts])
print(json.dumps(dict(piezas=len(parts),ocurrencias=len(instances),uniones=len(bolts))))

