from pathlib import Path
import json, math, csv, sys
BASE=Path(__file__).resolve().parent.parent
O=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'Entrega'/'Inventor'; O.mkdir(parents=True,exist_ok=True)
P=json.loads((BASE/'PARAMETROS_P2_05.json').read_text(encoding='utf-8-sig'))
G=P['geometria']; H=G['alto_refuerzo']; S=G['separacion_refuerzos']; B=G['ancho_refuerzo']; D=G['profundidad_refuerzo']; t=G['pared_refuerzo']
ECU=G['espesor_cuerpo_lumbar']; EM=G['espesor_mejilla']; ECI=G['espesor_cinta']; ACI=G['ancho_cinta']
ANC=G['ancho_cuna']; HM=G['hueco_manguera']; AP=G['ancho_panel']; ALP=G['alto_panel']; Z0=-(G['espesor_anclaje']+0.7)
parts=[]; instances=[]; bolts=[]
colors={'6061':(175,188,197),'hdpe':(66,88,99),'textil':(49,65,75),'espuma':(73,82,89),'herrajes':(106,118,128),'hebilla_ref':(220,143,53),'bolsa_ref':(245,191,39)}
rho={'6061':2.7e-6,'hdpe':.953e-6,'textil':.75e-6,'espuma':.06e-6,'herrajes':8e-6,'hebilla_ref':1.25e-6,'bolsa_ref':.00001e-6}
def rect(x,y,w,h,r=0): return dict(kind='rr',x=x,y=y,w=w,h=h,r=r)
def circle(x,y,r): return dict(kind='circle',x=x,y=y,r=r)
def poly(pts): return dict(kind='poly',pts=pts)
def op(axis,start,depth,loops,cut=False,label='Forma',**kw): return dict(axis=axis,start=start,depth=depth,loops=loops,cut=cut,label=label,**kw)
def part(name,ops,mat='6061',ref=False,group='estructura',**kw):
    p=dict(name=name,ops=ops,material=mat,color=colors[mat],density=rho[mat],reference=ref,group=group,**kw);parts.append(p)
    if not kw.get('no_instance'): instances.append(dict(part=name,name=name,axis='z',position=[0,0,0],reference=ref,group=group))
    return p
def bolt(axis,pos,grip,tag):bolts.append(dict(axis=axis,pos=pos,diam=5,grip=grip,tag=tag))
def strap_segment(x0,width,a,b,th=1.5,label='Tramo'):
    dy=b[0]-a[0];dz=b[1]-a[1];ll=math.hypot(dy,dz);ny=-dz/ll*th/2;nz=dy/ll*th/2
    return op('x',x0,width,[poly([[a[0]+ny,a[1]+nz],[b[0]+ny,b[1]+nz],[b[0]-ny,b[1]-nz],[a[0]-ny,a[1]-nz]])],label=label)
def ribbon_path(x0,width,pts,th):
    # A continuous planar ribbon with averaged normals. Native extruded sketch.
    left=[];right=[]
    for i,p in enumerate(pts):
        a=pts[max(0,i-1)];b=pts[min(len(pts)-1,i+1)];dy=b[0]-a[0];dz=b[1]-a[1];ll=math.hypot(dy,dz)
        ny=-dz/ll*th/2;nz=dy/ll*th/2
        left.append([p[0]+ny,p[1]+nz]);right.append([p[0]-ny,p[1]-nz])
    return op('x',x0,width,[poly(left+right[::-1])],label='Recorrido_textil')

# Independent shallow C stays. Internal radii add material to the conservative calculation.
for side,cx in [('I',-S/2),('D',S/2)]:
    sec=dict(kind='channel',cx=cx,B=B,D=D,t=t,r=G['radio_raiz'])
    ops=[op('y',0,H,[sec],label='Canal_abierto',depth_name='Altura_refuerzo'),
         op('x',cx-B/2-.1,B+.2,[circle(yy,G['eje_pernos_z'],G['taladro_union']/2) for yy in G['pernos_y']],True,'Alojamiento_pasador_hueco')]
    for j,yy in enumerate(G['ventanas_refuerzo_y']):
        ops.append(op('z',-.1,t+.2,[rect(cx-G['ancho_ventana_refuerzo']/2,yy,G['ancho_ventana_refuerzo'],G['alto_ventana_refuerzo'],G['ancho_ventana_refuerzo']/2)],True,'Ventana_superior_'+str(j+1)))
    part('Refuerzo_C_'+side,ops,description='6061-T6. Canal mecanizado/extruido, no chapa T6 doblada. Boca del canal hacia la bolsa. Sin recortes en zona inferior.',edge_radius=G['radio_redondeo_refuerzo'])
    for yy in G['pernos_y']:
        part(f'Casquillo_{side}_{yy}',[op('x',cx-B/2+t,B-2*t,[circle(yy,G['eje_pernos_z'],G['casquillo_od']/2),circle(yy,G['eje_pernos_z'],G['taladro_union']/2)],label='Separador_compresion')],group='uniones',description='6061-T6. Colocar por la boca del canal antes del pasador; longitud ajustada al interior real. Evita aplastar las alas durante el apriete.')
        part(f'Pasador_hueco_{side}_{yy}',[op('x',cx-B/2-3+.2,B+6-.4,[circle(yy,G['eje_pernos_z'],G['pasador_od']/2),circle(yy,G['eje_pernos_z'],G['pasador_id']/2)],label='Pasador_cortante')],group='uniones',description='6061-T6 mecanizado, pasante extraible. OD10 ID5.5, extremos retraidos 0.2 mm respecto a mejillas. Transmite cortante; el M5 interior aporta apriete y retencion. Ajustes por cerrar.')

# Lumbar bridge: only the centre is rigid. Textile wings articulate outside it.
# Rounded openings preserve the mounting bosses and continuous top/bottom load paths.
ops=[op('z',Z0,ECU,[rect(-160,12,320,112,16)],label='Placa_lumbar'),
     op('z',-3.7,G['espesor_anclaje']-ECU,[rect(-160,34,34,68,4),rect(126,34,34,68,4)],label='Refuerzos_locales_puentes'),
     op('z',-3.7,ECU,[rect(cx-32,88,64,36,4) for cx in [-S/2,S/2]],label='Refuerzos_locales_cuna'),
     op('z',-6.8,G['espesor_anclaje']+.2,[rect(-66,34,132,103,15),rect(-140,42,8,52,4),rect(132,42,8,52,4)]+[rect(cx-26,100,52,8,4) for cx in [-S/2,S/2]],True,'Ventanas_cinturon_y_cuna')]
for cx in [-S/2,S/2]:
    for xx in [cx-B/2-3,cx+B/2]:
        ops.append(op('x',xx,EM,[rect(18,-3.7,100,D+3.7,5)],label='Mejilla_apoyo'))
    ops.append(op('x',cx-B/2-3-.1,B+6+.2,[circle(yy,G['eje_pernos_z'],G['taladro_union']/2) for yy in G['pernos_y'][:2]]+[rect(50,4,30,11,4)],True,'Pasadores_y_ventana_mejillas'))
part('Interfaz_lumbar_aligerada',ops,group='anclajes',edge_radius=G['radio_redondeo_lumbar'],description='Centro lumbar resistente; alas del cinturon textiles. Recorte central de esquinas redondeadas. Sin apoyo de bandeja.')
for side,cx in [('I',-S/2),('D',S/2)]:
    for yy in G['pernos_y'][:2]:bolt('x',[cx-B/2-3,yy,G['eje_pernos_z']],B+6,'Lumbar_'+side)

# Compact upper yokes. Two slots separate the cargo sling and the shoulder harness.
for side,cx in [('I',-S/2),('D',S/2)]:
    ops=[op('z',-6.7,G['espesor_anclaje'],[rect(cx-36,375,72,100,10)],label='Placa_yugo'),
         op('z',-6.8,G['espesor_anclaje']+.2,[rect(cx-26,443,52,8,4),rect(cx-26,415,52,8,4),rect(cx-21,383,42,14,6)],True,'Cintas_y_aligeramiento')]
    for xx in [cx-B/2-3,cx+B/2]:
        ops.append(op('x',xx,EM,[rect(376,-2,98,D+2,5)],label='Mejilla_yugo'))
    ops.append(op('x',cx-B/2-3-.1,B+6+.2,[circle(yy,G['eje_pernos_z'],G['taladro_union']/2) for yy in G['pernos_y'][2:]]+[rect(405,4,30,11,4)],True,'Pasadores_yugo_y_ventana'))
    part('Yugo_superior_'+side,ops,group='anclajes',edge_radius=G['radio_redondeo_yugo'],description='Anclajes independientes: el textil permite movilidad relativa. Sin travesano metalico entre hombros.')
    for yy in G['pernos_y'][2:]:bolt('x',[cx-B/2-3,yy,G['eje_pernos_z']],B+6,'Yugo_'+side)

# Perforated contact panel; no structural credit. Open spine and ventilation.
loops=[rect(-AP/2,2,AP,ALP,25)]
ops=[op('z',-8,G['espesor_panel'],loops,label='Panel_contacto'),
     op('z',-8.1,G['espesor_panel']+.2,[rect(-45,145,90,265,20),rect(-122,150,25,80,12),rect(97,150,25,80,12),rect(-122,250,25,80,12),rect(97,250,25,80,12),rect(-60,34,120,68,14)]+[rect(cx-27,yy,54,10,4) for cx in [-S/2,S/2] for yy in [99,414,442]],True,'Ventilacion_y_paso_cintas')]
part('Espaldera_HDPE_aligerada',ops,'hdpe',False,'protecciones',description='Distribucion local del contacto y separacion de aristas. No se cuenta como elemento resistente; retenida dentro de funda textil.')
# Light covers over the two channels; not a closed structural tube.
for side,cx in [('I',-S/2),('D',S/2)]:
    part('REF_Funda_refuerzo_'+side,[op('y',128,235,[rect(-.5,cx-B/2-.7,D+1.5,B+1.4,2),rect(-.1,cx-B/2-.1,D+.7,B+.2,1.5)],label='Funda_textil')],'textil',True,'textiles')
    part('REF_Acolchado_dorsal_'+side,[op('z',-24,15,[rect(cx-29,150,58,215,18)],label='Apoyo_dorsal')],'espuma',True,'acolchados')
part('REF_Acolchado_lumbar',[op('z',-26,17,[rect(-125,10,250,118,25)],label='Apoyo_lumbar')],'espuma',True,'acolchados')

# The broad saddles carry the water bag from below. A free centre gap protects the hose.
# Separate continuous load webbing is represented; sewn shell pattern remains provisional.
for side,sg in [('I',-1),('D',1)]:
    cx=sg*(HM/2+ANC/2); xx=cx-ANC/2
    path=[(156,30),(105,40),(78,65),(75,135),(100,170),(158,174)]
    part('REF_Cuna_textil_'+side,[ribbon_path(xx,ANC,path,2.0)],'textil',True,'textiles',description=f'Superficie ancha de contacto; confeccion y resistencia del conjunto por definir. Ventana central de {HM:.0f} mm.')
    webpath=[(117,15),(128,7),(128,-8),(104,-8),(104,7),(130,28),(102,40),(76,65),(73,135),(98,173),(175,177),(300,172),(430,140),(465,60),(448,-7)]
    part('REF_Cinta_carga_'+side,[ribbon_path(cx-ACI/2,ACI,webpath,ECI)],'textil',True,'textiles',description='Cinta continua desde el anclaje lumbar a cuna y yugo superior. Seccion tejida esquematica. No presupone resistencia por area.')
    # Shoulder loop and adjustment leg.
    shoulder=[(418,-9),(472,-35),(493,-75),(476,-115),(418,-145),(340,-155),(282,-145)]
    part('REF_Hombrera_'+side,[ribbon_path(cx-28,56,shoulder,10)],'espuma',True,'acolchados')
    part('REF_Cinta_hombrera_'+side,[ribbon_path(cx-19,38,[(418,-12),(472,-39),(488,-75),(470,-110),(412,-139),(338,-149),(282,-139),(220,-104),(100,-18)],ECI)],'textil',True,'textiles')
    part('REF_Regulador_hombro_'+side,[op('z',-151,6,[rect(cx-24,267,48,34,5),rect(cx-17,275,34,18,3)],label='Envolvente_regulador')],'hebilla_ref',True,'herrajes_textiles',description='Envolvente de regulador comercial a seleccionar; no mecanismo validado.')

# Transverse restraint against lateral bag motion; reference envelope, not a sewn pattern.
for yy in [225,350]:
    part('REF_Cinta_estabilizadora_'+str(yy),[op('y',yy,25,[rect(26,-165,160,330,30),rect(27.5,-163.5,157,327,28.5)],label='Retencion_transversal')],'textil',True,'textiles',description='Correa transversal ajustable de 25 mm. Envolvente propuesta para controlar desplazamiento lateral; ajuste a bolsa llena/vacia pendiente. No estrangular costuras ni tapa.')
    part('REF_Hebilla_carga_'+str(yy),[op('z',185,7,[rect(-20,yy-4,40,33,5)],label='Envolvente_hebilla')],'hebilla_ref',True,'herrajes_textiles',description='Cierre comercial protegido contra apertura accidental, operable con guantes; seleccion y ubicacion definitiva pendientes.')

# Articulating belt wings, wrapping the body. The silhouette is provisional, not anthropometric evidence.
def belt_outline(sign,radial_width):
    aa=[math.radians(v) for v in range(48,163,6)]
    outer=[[(-145+(140+radial_width)*math.cos(a)),sign*(170+radial_width)*math.sin(a)] for a in aa]
    inner=[[(-145+140*math.cos(a)),sign*170*math.sin(a)] for a in aa]
    return outer+inner[::-1]
for side,sg in [('I',-1),('D',1)]:
    part('REF_Ala_cinturon_'+side,[op('y',15,88,[poly(belt_outline(sg,10))],label='Ala_flexible')],'espuma',True,'acolchados')
    # Connection textile from the plate slot to the belt: permits hip motion.
    pts=[[-8,sg*136],[-38,sg*142],[-55,sg*150],[-57,sg*151],[-39,sg*140],[-8,sg*134]]
    part('REF_Bisagra_textil_'+side,[op('y',44,50,[poly(pts)],label='Conexion_flexible_cinturon')],'textil',True,'textiles')
    part('REF_Cinta_cierre_cinturon_'+side,[op('z',-292,ECI,[rect(-70 if sg<0 else 18,42,52,40,3)],label='Cierre_frontal')],'textil',True,'textiles')
part('REF_Hebilla_cinturon',[op('z',-300,12,[rect(-25,37,50,50,8),rect(-18,46,9,31,3),rect(9,46,9,31,3)],label='Envolvente_cierre')],'hebilla_ref',True,'herrajes_textiles',description='Envolvente de hebilla frontal comercial accionable con guantes. Requiere seleccion por carga, apertura accidental y temperatura.')
part('REF_Correa_pectoral',[op('z',-146,ECI,[rect(-82,350,164,25,3)],label='Correa_pecho')],'textil',True,'textiles')
part('REF_Hebilla_pectoral',[op('z',-152,6,[rect(-18,346,36,33,5)],label='Envolvente_cierre')],'hebilla_ref',True,'herrajes_textiles')
handle=ribbon_path(0,25,[[-95,448],[-95,500],[-65,525],[65,525],[95,500],[95,448]],2)
handle.update(axis='z',start=-1,label='Asa_textil_continua')
part('REF_Asa_sistema',[handle],'textil',True,'textiles',description='Asa vinculada a las cintas de carga; requiere continuidad y costuras ensayadas. No utiliza el asa de la bolsa.')

# Hardware: short fasteners, washers, metallic locknuts; native cosmetic metric thread.
created=set()
def hexagon(af):return poly([[af/math.sqrt(3)*math.cos(a*math.pi/3),af/math.sqrt(3)*math.sin(a*math.pi/3)] for a in range(6)])
def hp(name,ops,thread=None,desc=''):
    if name in created:return
    created.add(name);part(name,ops,'herrajes',False,'fijaciones',no_instance=True,thread=thread,description=desc)
def inst(name,axis,pos,tag):instances.append(dict(part=name,name=tag,axis=axis,position=pos,reference=False,group='fijaciones'))
for j,bb in enumerate(bolts,1):
    gr=bb['grip']; wt=G['espesor_arandela']; need=gr+2*wt+5+1.6; ln=next(z for z in [16,20,25,30,35,40,45,50,55] if z>=need)
    bn=f'Tornillo_M5x{ln}_ISO4762_A2_80';wn='Arandela_M5_16x3_GN6341';nn='Tuerca_M5_autofreno_metalica'
    hp(bn,[op('z',0,ln,[circle(0,0,2.5)],label='Vastago'),op('z',-5,5,[circle(0,0,4.25)],label='Cabeza'),op('z',-5.1,3.1,[hexagon(4)],True,'Hexagono_interior')],dict(d=5,pitch=.8,internal=False,length=22),'ISO 4762 M5x0.8, A2-80. Rosca parcial b=22 mm nominal; confirmar proveedor.')
    hp(wn,[op('z',0,wt,[circle(0,0,8),circle(0,0,2.65)],label='Arandela_gruesa')],desc='Envolvente GN 6341-ST-5-16-A-ZB: 5.3x16x3 mm, acero protegido. Confirmar proveedor; minimo de calculo Sy=200 MPa y espesor=2.9 mm. No es el elemento de autofreno.')
    hp(nn,[op('z',0,5,[hexagon(8),circle(0,0,2.5)],label='Tuerca')],dict(d=5,pitch=.8,internal=True,length=5),'Envolvente derivada DIN 980 M5; seleccionar clase y par prevalente compatibles. No se modela deformacion de autofreno.')
    axis=bb['axis'];ii={'x':0,'y':1,'z':2}[axis];origin=bb['pos']
    def sh(delta):a=origin.copy();a[ii]+=delta;return a
    for name,delta,suf in [(bn,-wt,'Tornillo'),(wn,-wt,'Arandela_cabeza'),(wn,gr,'Arandela_tuerca'),(nn,gr+wt,'Tuerca')]:inst(name,axis,sh(delta),f'{bb["tag"]}_{j}_{suf}')
    bb.update(longitud=ln,paso=.8,protrusion=ln-gr-2*wt-5,tornillo=bn,tuerca=nn)

for p in parts:
    if p['material']=='6061':p['mechanical']=dict(E_MPa=69000,nu=.33,Sy_MPa=240,Su_MPa=260,nota='Minimos de prediseno 6061-T6; certificacion de suministro requerida')
    elif p['material']=='herrajes':
        if p['name'].startswith('Arandela'):p['mechanical']=dict(E_MPa=200000,nu=.3,Sy_MPa=200,Su_MPa=400,nota='Minimos exigidos de prediseno; confirmar acero/proveedor de arandela')
        else:p['mechanical']=dict(E_MPa=193000,nu=.3,Sy_MPa=600,Su_MPa=800,nota='Hipotesis A2-80; tuerca requiere prueba de carga y par prevalente compatibles')

manifest=dict(version='P2.05',units='mm',parameters=P,parts=parts,instances=instances,bolts=bolts)
(O/'MODELO_API.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
with (O/'BOM_FIJACIONES.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,['tag','diam','grip','longitud','paso','protrusion','tornillo','tuerca']);w.writeheader();w.writerows({k:q[k] for k in w.fieldnames} for q in bolts)
print(json.dumps(dict(piezas=len(parts),ocurrencias=len(instances),uniones=len(bolts))))
