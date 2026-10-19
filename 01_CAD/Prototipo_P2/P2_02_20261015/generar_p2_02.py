from pathlib import Path
import json,math,csv,hashlib,sys
import numpy as np
BASE=Path(__file__).resolve().parent
O=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'Precalculo'
O.mkdir(parents=True,exist_ok=True)
C=json.loads((BASE/'PARAMETROS_P2_02.json').read_text(encoding='utf-8-sig'))
G=C['geometria'];L=C['cargas'];MAT=C['materiales']
H=G['altura_riel'];S=G['separacion_rieles'];W=G['ancho_cuna'];D=G['fondo_cuna'];Y=G['altura_piso'];tf=G['espesor_piso'];tg=G['espesor_cartela']
assert 450<=H<=650 and 180<=S<=240 and W>=S+80 and 110<=D<=160 and 110<=Y<=150
F=L['masa_total_referencia_kg']*9.81*L['factor_vertical'];Q=L['masa_total_referencia_kg']*9.81*L['factor_horizontal'];share=L['fraccion_lado_mas_cargado'];e=L['brazo_carga_desde_eje_riel'];ell=max(L['altura_fuerza_sobre_sujecion'],H-100);K=L['factor_concentracion_provisional'];E=MAT['E_aluminio_MPa']
def rrpts(w,h,r):
 p=[]
 for cx,cy,a in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for q in np.linspace(a,a+90,65):p.append((cx+r*math.cos(math.radians(q)),cy+r*math.sin(math.radians(q))))
 return np.array(p)
def polyprops(p):
 x,y=p.T;X,Y=np.roll(p,-1,axis=0).T;c=x*Y-X*y
 return c.sum()/2,((y*y+y*Y+Y*Y)*c).sum()/12,((x*x+x*X+X*X)*c).sum()/12
rows=[]
for b,d,t in C['candidatos_riel']:
 A,Ix,Iz=np.array(polyprops(rrpts(b,d,2*t)))-np.array(polyprops(rrpts(b-2*t,d-2*t,t)))
 Zx=Ix/(d/2);Zz=Iz/(b/2)
 normal=share*(F/A+F*e/Zx+Q*ell*math.sqrt(1/Zx**2+1/Zz**2))
 Am=(b-t)*(d-t)-(4-math.pi)*(1.5*t)**2
 tau=share*Q*(S/2)/(2*Am*t)+share*math.hypot(F,Q)/A
 vm=K*math.sqrt(normal**2+3*tau**2);n=MAT['fluencia_6061_MPa']/vm
 deflection=share*Q*ell**3/(3*E*min(Ix,Iz))+share*F*e*ell**2/(2*E*Ix)
 euler=math.pi**2*E*min(Ix,Iz)/(2*ell)**2
 local=4*math.pi**2*E/(12*(1-MAT['nu_aluminio']**2))*(t/(max(b,d)-4*t))**2
 rows.append(dict(b=b,d=d,t=t,A=A,Ix=Ix,Iz=Iz,Zx=Zx,Zz=Zz,masa_rieles_kg=2*H*A*2.7e-6,tension_VM_MPa=vm,margen=n,flecha_mm=deflection,margen_Euler=euler/(share*F),tension_pandeo_local_MPa=local,cumple_precriterios=bool(n>=L['margen_fluencia_objetivo'] and deflection<=L['flecha_limite_preliminar_mm'])))
valid=[r for r in rows if r['cumple_precriterios']]
assert valid,'Ninguna seccion satisface las hipotesis; revisar parametros'
preferred=[r for r in valid if r['d']<=C['preferencia_optimizacion']['profundidad_max_preferida'] and r['masa_rieles_kg']<=C['preferencia_optimizacion']['masa_max_par_rieles_kg']]
assert preferred,'No hay perfil dentro de los limites de masa y profundidad con margen objetivo'
R=min(preferred,key=lambda a:a['masa_rieles_kg']);b,d,t=R['b'],R['d'],R['t']
with (O/'COMPARACION_RIELES.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
checks=[]
def check(name,stress,sy,scope):checks.append(dict(elemento=name,tension_MPa=stress,limite_MPa=sy,margen=sy/stress,alcance=scope))
# Dos tornillos M8 por cartela, situados a Y-85 e Y-40 => separacion 45.
boltPitch=45
V=share*math.hypot(F,Q)
M=share*(F*e+Q*(Y-(Y-62.5)))
boltforce=1.2*math.hypot(V/2,M/boltPitch)
check('M8_cartela_cortante',math.sqrt(3)*boltforce/36.6,MAT['fluencia_A2_70_MPa'],'Rosca en plano de corte, A_s=36.6 mm2; sin acreditar friccion')
check('Pared_riel_aplastamiento_M8',boltforce/(8*t),MAT['fluencia_6061_MPa'],'Una pared; espesor nominal; cilindro de apoyo interior')
check('Cartela_aplastamiento_M8',boltforce/(8*tg),MAT['fluencia_5052_MPa'],'Sin credito de reparto por friccion')
check('Cartela_arrancamiento_borde',math.sqrt(3)*boltforce/(2*(min(15,d/2)-8.6/2)*tg),MAT['fluencia_5052_MPa'],'Borde centro-agujero minimo min(15, profundidad/2) mm')
rootH=Y-20-20
check('Cartela_raiz_VM',2*math.sqrt((6*M/(tg*rootH**2))**2+3*(V/(tg*rootH))**2),MAT['fluencia_5052_MPa'],'Idealizacion de viga; factor local 2, sin sustituir FEA del recorte')
# Piso con dos refuerzos cerrados a 20 y D-40 desde borde posterior.
gap=max(0,(D-40-10)-(20+10));overhang=30
q=2*F/(W*D)
floorM=max(q*gap**2/8,q*overhang**2/2)+100*gap/(4*50)
check('Piso_carga_repartida_y_parche_100N',6*floorM/tf**2,MAT['fluencia_5052_MPa'],'2x presion media + 100 N sobre franja de 50 mm; supuesto de contacto flexible')
rb=G['ancho_refuerzo_cuna'];rt=G['espesor_refuerzo_cuna'];Ir=(rb**4-(rb-2*rt)**4)/12
check('Refuerzo_cuna_flexion',(.7*F*(S+b)/4)/(Ir/(rb/2)),MAT['fluencia_6061_MPa'],'70% de F en un tubo, carga puntual centrada entre cartelas')
ta=G['espesor_anclaje_hombro']
check('Puente_ranura_hombro',1.5*6*(share*F*52/4)/(24*ta**2),MAT['fluencia_6061_MPa'],'Carga fuera del plano sobre puente, viga apoyada; concentracion 1.5 provisional')
tb=G['espesor_yugo_cinturon']
check('Puente_ranura_cinturon',1.5*6*(share*F*52/4)/(26*tb**2),MAT['fluencia_6061_MPa'],'Viga apoyada del puente exterior, fuerza fuera del plano')
check('Yugo_cinturon_flexion_lateral',2*(share*F*40)/(100*tb**2/6),MAT['fluencia_6061_MPa'],'Voladizo 40 mm desde riel, sin utilizar ventana central como apoyo')
brace_force=Q*math.hypot(S,H-30-(Y+30))/S
check('Diagonal_trabajando_a_traccion',brace_force/(2*(24-6.6)),MAT['fluencia_5052_MPa'],'Solo la diagonal traccionada; sin credito a la comprimida')
check('M6_uniones_VM',math.sqrt(3)*1.2*share*F/2/20.1,MAT['fluencia_A2_70_MPa'],'Solo cortante externo; pretension, apertura y palanca pendientes')
calc=dict(hipotesis=C,seleccion=R,fuerza_vertical_N=F,fuerza_horizontal_N=Q,reaccion_tornillo_cartela_N=boltforce,altura_efectiva_calculo_mm=ell,comprobaciones=checks,criterio_interno=L['margen_fluencia_objetivo'],validacion_global=False,pendientes=['FEA de uniones y rigidez real del arnes','Fatiga y espectro de pasos/impactos','Aflojamiento, pretension, aplastamiento bajo arandelas y palanca','Ensayo de bolsa flexible llena y salida inferior','Ambiente termico, abrasion, bordes y liberacion rapida'])
(O/'CALCULOS_PRELIMINARES.json').write_text(json.dumps(calc,indent=2,ensure_ascii=False),encoding='utf-8')
# Geometria declarativa: operaciones prismas (perfil y extrusion) y taladros reales.
parts=[];instances=[];bolts=[];interfaceX=min(70,S/2-b/2-5)
colors={'6061':(159,184,200),'5052':(118,150,166),'anclaje':(227,151,65),'hdpe':(41,99,108),'pad':(48,62,74),'herrajes':(85,96,106)}
def rect(x,y,w,h,r=0):return dict(kind='rr',x=x,y=y,w=w,h=h,r=r)
def circle(x,y,r):return dict(kind='circle',x=x,y=y,r=r)
def poly(pts):return dict(kind='poly',pts=pts)
def op(axis,start,depth,loops,cut=False,label='Forma'):return dict(axis=axis,start=start,depth=depth,loops=loops,cut=cut,label=label)
def part(name,ops,mat='6061',ref=False):
 parts.append(dict(name=name,ops=ops,material=mat,color=colors[mat],reference=ref))
 instances.append(dict(part=name,name=name,axis='z',position=[0,0,0]))
 return parts[-1]
def bolt(axis,pos,diam,grip,tag):bolts.append(dict(axis=axis,pos=pos,diam=diam,grip=grip,tag=tag))
zholes=[Y-70,Y-25,Y+30,H-30,H-180,H-160,H-140,H-120,H-100]
# Rieles cerrados; taladros Z M6 y X M8.
for side,cx in [('I',-S/2),('D',S/2)]:
 ops=[op('y',0,H,[rect(0,cx-b/2,d,b,2*t)],label='Tubo_exterior'),op('y',-.1,H+.2,[rect(t,cx-b/2+t,d-2*t,b-2*t,t)],True,'Vaciado_tubo'),
 op('z',-.1,d+.2,[circle(cx,y,3.3) for y in zholes],True,'Patron_M6'),
 op('x',cx-b/2-.1,b+.2,[circle(Y-85,d/2,4.3),circle(Y-40,d/2,4.3)],True,'Cartela_M8')]
 part('Riel_'+side,ops)
 # Casquillos anticompresion dentro del tubo, instalados por extremo abierto.
 for yy in [Y-70,Y-25,Y+30,H-30,H-140,H-100]:
  part('Casquillo_Z_'+side+'_'+str(int(yy)),[op('z',t,d-2*t,[circle(cx,yy,5),circle(cx,yy,3.3)])],ref=False)
 for yy in [Y-85,Y-40]:
  part('Casquillo_X_'+side+'_'+str(int(yy)),[op('x',cx-b/2+t,b-2*t,[circle(yy,d/2,6.5),circle(yy,d/2,4.3)])])
 # Cartela lateral exterior con ala superior hacia dentro; tubo separa verticales M6/M8.
 xweb=cx-b/2-tg if side=='I' else cx+b/2
 web=poly([[Y-100,0],[Y-20,0],[Y-20,d+D],[Y-50,d+D*.60],[Y-100,d]])
 ops=[op('x',xweb,tg,[web],label='Alma_cartela'),
 op('y',Y-24,4,[rect(d,xweb if side=='I' else xweb-16,D,16+tg)],label='Ala_apoyo'),
 op('x',xweb-.1,tg+.2,[circle(Y-85,d/2,4.3),circle(Y-40,d/2,4.3),circle(Y-43,d+35,10)],True,'Taladros_alivio')]
 xb=xweb+tg+8 if side=='I' else xweb-8
 # Ala central de contacto con refuerzos: agujeros M5 eje Y.
 ops.append(op('y',Y-24-.1,4.2,[circle(d+20,xb,2.75),circle(d+D-40,xb,2.75)],True,'Tornillos_piso'))
 part('Cartela_'+side,ops,'5052')
 for yy in [Y-85,Y-40]:bolt('x',[cx-b/2-tg if side=='I' else cx-b/2,yy,d/2],8,b+tg,'Cartela_'+side)
 # Apoyos de la cuna sobre el ala.
 for zz in [d+20,d+D-40]:
  part('Casquillo_refuerzo_'+side+'_'+str(int(zz)),[op('y',Y-20+rt,20-2*rt,[circle(zz,xb,4.5),circle(zz,xb,2.75)])])
  bolt('y',[xb,Y-24,zz],5,24+tf,'Piso_'+side)
# Travesanos posteriores y diagonales en dos planos.
for tag,cy in [('Bajo',Y+30),('Alto',H-30)]:
 ops=[op('z',-2,2,[rect(-S/2-30,cy-20,S+60,40,6)]),op('z',-2.1,2.2,[circle(-S/2,cy,3.3),circle(S/2,cy,3.3),circle(-interfaceX,cy,2.25),circle(interfaceX,cy,2.25)],True,'Taladros')]
 part('Travesano_'+tag,ops,'5052')
for idx,sign in enumerate([1,-1]):
 a=np.array([-S/2,Y+30]);c=np.array([S/2,H-30])
 if sign<0:a[0]*=-1;c[0]*=-1
 tangent=(c-a)/np.linalg.norm(c-a);normal=np.array([-tangent[1],tangent[0]])
 pts=[(a-tangent*12+normal*12).tolist(),(a-tangent*12-normal*12).tolist(),(c+tangent*12-normal*12).tolist(),(c+tangent*12+normal*12).tolist()]
 zz=-4-idx*2
 part('Diagonal_'+str(idx+1),[op('z',zz,2,[poly(pts)]),op('z',zz-.1,2.2,[circle(*a,3.3),circle(*c,3.3)],True,'Extremos')],'5052')
 for xx,yy in [a,c]:
  if idx:part('Calce_diagonal_'+str(int(xx))+'_'+str(int(yy)),[op('z',-4,2,[circle(xx,yy,7),circle(xx,yy,3.3)])],'5052')
  bolt('z',[xx,yy,zz],6,d-zz+(2.5 if abs(yy-(Y+30))<.01 else 0),'Diagonal')
# Dos perfiles cerrados bajo la cuna.
for i,zz in enumerate([d+20,d+D-40]):
 ops=[op('x',-W/2,W,[rect(Y-20,zz-10,20,20,3)]),op('x',-W/2-.1,W+.2,[rect(Y-20+rt,zz-10+rt,20-2*rt,20-2*rt,1.5)],True,'Hueco')]
 xb=S/2+b/2-8
 ops.append(op('y',Y-20-.1,20.2,[circle(zz,-xb,2.75),circle(zz,xb,2.75)],True,'Paso_tornillos'))
 part('Refuerzo_cuna_'+str(i+1),ops)
# Piso con escotadura circular abierta hacia frente. Ranuras drenaje lejos de fijaciones.
ops=[op('y',Y,tf,[rect(d,-W/2,D,W,8)],label='Piso'),
 op('y',Y-.1,tf+.2,[circle(d+D-5,0,25)],True,'Salida_manguera'),
 op('z',d,2.5,[rect(-W/2+8,Y+tf,W-16,50,5)],label='Respaldo_cuna')]
# laterales de retencion como labios unidos al piso
for xx in [-W/2,W/2-2.5]:ops.append(op('x',xx,2.5,[rect(Y+tf,d+8,16,D-16,4)],label='Labio_lateral'))
for u in [d+45,d+75]:ops.append(op('y',Y-.1,tf+.2,[rect(u-3,-70,6,25,3),rect(u-3,45,6,25,3)],True,'Drenajes'))
xb=S/2+b/2-8
ops.append(op('y',Y-.1,tf+.2,[circle(zz,xx,2.75) for zz in [d+20,d+D-40] for xx in [-xb,xb]],True,'Fijacion_M5'))
ops.append(op('z',d-.1,2.7,[circle(xx,Y+30,3.3) for xx in [-S/2,S/2]],True,'Union_posterior_M6'))
part('Cuna_modular',ops,'5052')
# Hombros: agujeros indexados, sin depender de friccion de ranuras.
for side,cx in [('I',-S/2),('D',S/2)]:
 ops=[op('z',d,ta,[rect(cx-38,H-160,76,120,10)]),
 op('z',d-.1,ta+.2,[circle(cx,H-140,3.3),circle(cx,H-100,3.3),rect(cx-26,H-72,52,8,4)],True,'Correa_y_tornillos')]
 part('Anclaje_hombro_'+side,ops,'anclaje')
 for yy in [H-140,H-100]:bolt('z',[cx,yy,0],6,d+ta,'Hombro_'+side)
# Yugo de cadera: distribuidor amplio y desmontable. Ventana central de aligeramiento.
hipW=S+140
ops=[op('z',-tb,tb,[rect(-hipW/2,Y-105,hipW,100,14)]),
 op('z',-tb-.1,tb+.2,[rect(-50,Y-80,100,50,12),rect(-S/2-44,Y-81,8,52,4),rect(S/2+36,Y-81,8,52,4)]+[circle(xx,yy,3.3) for xx in [-S/2,S/2] for yy in [Y-70,Y-25]],True,'Cinturon_y_anclajes')]
part('Yugo_cinturon',ops,'anclaje')
for xx in [-S/2,S/2]:
 for yy in [Y-70,Y-25]:bolt('z',[xx,yy,-tb],6,d+tb,'Cinturon')
# Interfaz posterior en dos modulos desmontables, canal central abierto, cabezas aisladas de espalda.
for side,x in [('I',-130),('D',20)]:
 part('REF_Interfaz_'+side,[op('z',-14,2,[rect(x,130,110,H-150,18)]),op('z',-14.1,2.2,[circle(-interfaceX if side=='I' else interfaceX,cy,2.25) for cy in [Y+30,H-30]],True,'Fijacion_independiente')],'hdpe',True)
 part('REF_Pad_'+side,[op('z',-26,12,[rect(x+8,160,94,H-210,20)])],'pad',True)
part('REF_Pad_lumbar',[op('z',-26,12,[rect(-120,20,240,85,20)])],'pad',True)
# Separadores de interfaz, sin introducir plastico en las uniones primarias.
for xx in [-interfaceX,interfaceX]:
 for cy in [Y+30,H-30]:
  part('Separador_interfaz_'+str(xx)+'_'+str(int(cy)),[op('z',-12,10,[circle(xx,cy,4),circle(xx,cy,2.25)])])
  bolt('z',[xx,cy,-14],4,14,'Interfaz')
# Protector de bolsa con cavidades inferiores que cubren tuercas M5.
ops=[op('y',Y+tf,6,[rect(d+2.5,-W/2+3,D-2.5,W-6,8)]),
 op('y',Y+tf-.1,6.2,[circle(d+D-5,0,25)],True,'Salida_manguera'),
 op('y',Y+tf-.1,4.6,[circle(zz,xx,4.8) for xx in [-xb,xb] for zz in [d+20,d+D-40]],True,'Alojamiento_tuercas')]
part('REF_Protector_bolsa_cuna',ops,'hdpe',True)
# Herrajes esquematicos reutilizables: volumen de tornillo, arandela y tuerca sin rosca.
hardware={}
for i,bb in enumerate(bolts):
 key='REF_M'+str(bb['diam'])+'_Agarre_'+str(round(bb['grip'],2)).replace('.','p')
 if key not in hardware:
  dd=bb['diam'];ll=bb['grip'];rr=dd*.82
  ops=[op('z',0,ll,[circle(0,0,dd/2)]),op('z',-dd*.7,dd*.7,[circle(0,0,rr)]),op('z',ll,dd*.8,[poly([[rr*math.cos(a*math.pi/3),rr*math.sin(a*math.pi/3)] for a in range(6)])])]
  parts.append(dict(name=key,ops=ops,material='herrajes',color=colors['herrajes'],reference=True));hardware[key]=True
 instances.append(dict(part=key,name=bb['tag']+'_'+str(i+1),axis=bb['axis'],position=bb['pos']))
manifest=dict(version='P2.02',units='mm',parameters=C,rail=R,parts=parts,instances=instances,bolts=bolts)
(O/'MODELO_P2_02.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
(O/'PARAMETROS_UTILIZADOS.json').write_text(json.dumps(C,indent=2,ensure_ascii=False),encoding='utf-8')
with (O/'BOM_MODELO.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Archivo','Cantidad','Material_candidato','Referencia'])
 for p in parts:w.writerow([p['name']+'.ipt',sum(i['part']==p['name'] for i in instances),p['material'],p['reference']])
print(json.dumps(dict(output=str(O),riel=[b,d,t],margen_riel=R['margen'],masa_rieles=R['masa_rieles_kg'],min_margen_comprobaciones=min(c['margen'] for c in checks),piezas=len(parts),ocurrencias=len(instances))))

