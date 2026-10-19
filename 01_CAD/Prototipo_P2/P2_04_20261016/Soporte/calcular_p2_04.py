from pathlib import Path
import json, math, csv
import numpy as np

BASE=Path(__file__).resolve().parent.parent
P=json.loads((BASE/'PARAMETROS_P2_04.json').read_text(encoding='utf-8-sig'))
G=P['geometria']; C=P['cargas']; M=P['materiales']
O=BASE/'Calculos'; O.mkdir(exist_ok=True)

def section(B,D,t,slot=0):
    # Conservative sharp-corner section; no credit for the root radii.
    rects=[(B,t,0,t/2),(t,D-t,-(B-t)/2,(D+t)/2),(t,D-t,(B-t)/2,(D+t)/2)]
    if slot: rects.append((-slot,t,0,t/2))
    A=sum(w*h for w,h,x,z in rects)
    z=sum(w*h*z for w,h,x,z in rects)/A
    I=sum(w*h**3/12+w*h*(zz-z)**2 for w,h,x,zz in rects)
    Ix=sum(h*w**3/12+w*h*x*x for w,h,x,zz in rects)
    J=(B+2*(D-t))*t**3/3
    return dict(A=A,z=z,I=I,Ix=Ix,Z=I/max(z,D-z),J=J)

Fv=C['masa_total_kg']*C['g']*C['factor_vertical']
Fh=C['masa_total_kg']*C['g']*C['factor_horizontal']
N=Fv*C['fraccion_lado']; Q=Fh*C['fraccion_lado']
L=G['apoyo_hombro_y']-G['apoyo_cinturon_y']; e=C['excentricidad_mm']; M0=N*e
E=M['E_6061_MPa']; Sy=M['Sy_6061_MPa']; nu=.33; GG=E/(2*(1+nu))
S=section(G['ancho_refuerzo'],G['profundidad_refuerzo'],G['pared_minima'])
x=np.linspace(0,L,801)
# Simply supported stay: lower belt and upper shoulder restraint in service.
# Any horizontal point force position is enveloped by Q*x*(L-x)/L.
moment=M0*np.maximum(1-x/L,x/L)+Q*x*(L-x)/L
mmax=float(max(abs(moment))); xmax=float(x[np.argmax(abs(moment))])
sig=N/S['A']+C['K_borde']*mmax/S['Z']
# Additional lateral inertial case, with loads conservatively simultaneous.
mlat=Q*L/4
sig_biax=sig+C['K_borde']*mlat*(G['ancho_refuerzo']/2)/S['Ix']
T=Q*C['brazo_torsion_mm']; tau=T*G['pared_minima']/S['J']+Q/S['A']
vm=math.sqrt(sig_biax**2+3*tau*tau)

checks=[]
def check(name,n,detail):
    checks.append(dict(nombre=name,margen=float(n),umbral=C['margen_objetivo'],cumple=bool(n>=C['margen_objetivo']),modelo=detail))
check('Refuerzo combinado, pared minima',Sy/vm,'N/A + K M/Z + flexion lateral + torsion St Venant; apoyos hombro/cinturon activos')
check('Pandeo Euler, eje debil',math.pi**2*E*min(S['I'],S['Ix'])/(L*L*N),'Articulado-articulado ideal; no acredita pandeo distorsional')
plate_sigma=.43*math.pi**2*E/(12*(1-nu*nu))*(G['pared_minima']/(G['profundidad_refuerzo']-G['pared_minima']))**2
check('Pandeo local de alas',min(Sy,plate_sigma)/vm,'Placa sobresaliente k=0.43; aproximacion elastica conservadora limitada por fluencia')
Mcr=math.pi/L*math.sqrt(E*S['Ix']*GG*S['J'])
check('Pandeo lateral torsional ideal',Mcr/mmax,'Viga uniforme; sin credito de alabeo. Excentricidades y ranuras requieren FEA')
# Upper web relief. Ends are rounded; keep full flanges and the lower web.
for yy in G['ventanas_refuerzo_y']:
    uu=max(0,yy-G['apoyo_cinturon_y']); mm=M0*max(1-uu/L,uu/L)+Q*uu*(L-uu)/L
    ss=section(G['ancho_refuerzo'],G['profundidad_refuerzo'],G['pared_minima'],G['ancho_ventana_refuerzo'])
    sw=N/ss['A']+abs(mm)*ss['z']/ss['I']+mlat*G['ancho_ventana_refuerzo']/2/ss['Ix']
    check('Borde ventana y='+str(yy),Sy/(C['K_ventana']*sw),'Seccion neta; K=3 de cribado, no solucion local de la ranura')
# Bolt holes in flanges close to the section centroid, not through the back web.
hole_d=G['taladro_union']; local_z=G['eje_pernos_z']; netA=S['A']-2*G['pared_minima']*hole_d
local_stress=N/netA+mmax*abs(local_z-S['z'])/S['I']+mlat*(G['ancho_refuerzo']/2)/S['Ix']
check('Taladro en alas, tension local',Sy/(3*local_stress),'Cribado K=3 en plano del agujero; no acredita fatiga')
# Lower joint and strap interface; no credit for friction in the shear check.
sp=G['separacion_pernos']; reaction=mmax/sp+Q/2; R=1.5*reaction; V=math.hypot(N/2,reaction)
As=14.2; d=5; f0=C['precarga_estudio_N']; fb=1.25*f0+.2*R
sb=fb/As; tb=V/As; bolt_vm=math.sqrt(sb*sb+3*tb*tb)
check('M5 combinacion precarga y servicio',M['Sy_perno_MPa']/bolt_vm,'Precarga dispersa 25%, rigidez de junta Cj=.2 y palanca 1.5; verificar proveedor')
pin_od=G['pasador_od']-.1; pin_id=5.6
check('Aplastamiento ala por pasador',Sy/(V/(G['pared_minima']*pin_od)),'Se admite una sola ala efectiva en cortante')
check('Aplastamiento mejilla por pasador',Sy/(V/(G['pared_minima']*pin_od)),'Mejilla de 3 mm nominal / 2.8 minima; se admite una sola mejilla efectiva')
check('Arrancamiento ala',.577*Sy/(V/(2*G['pared_minima']*(G['distancia_borde_perno']-hole_d/2))),'Dos ligamentos, sin credito de reparto entre alas')
check('Casquillo compresion',Sy/((1.25*f0)/(math.pi/4*((G['casquillo_od']-.1)**2-(hole_d+.1)**2))),'Separador independiente OD12.5 ID10.2; tolerancias exploradas +/-0.1 mm; longitud a ajustar al interior real')
pin_area=math.pi/4*(pin_od**2-pin_id**2)
pin_Z=math.pi/32*(pin_od**4-pin_id**4)/pin_od
pin_vm=math.sqrt((V*3.4/pin_Z)**2+3*(2*V/pin_area)**2)
check('Pasador hueco flexion y cortante',Sy/pin_vm,'6061-T6 OD10 ID5.5, min OD9.9/max ID5.6; una sola interfaz toma V, brazo local3.4mm, tau=2V/A; holguras por verificar')
washer_sigma=6*(fb/(2*math.pi*4))*max(0,hole_d/2-4)/(G['espesor_arandela_minimo']**2)
check('Arandela gruesa flexion local',200/washer_sigma,'Cribado de tira anular en voladizo, carga distribuida en perimetro r4mm; acero Sy minimo exigido200MPa, confirmar contacto real')
washer_contact=math.sqrt(3)/2*8**2-math.pi/4*5.5**2
check('Arandela presion bajo tuerca',200/(fb/washer_contact),'Area de apoyo hexagonal AF8 menos agujero5.5; no verifica roscas o prueba de tuerca')
# Strap bar / slot bridge in the lower and upper anchors.
Tstrap=N/(2*math.cos(math.radians(C['angulo_eslinga_grados'])))
Tinterface=max(N/math.cos(math.radians(C['angulo_eslinga_grados'])),math.hypot(N,Q+M0/L))
bridge_M=Tinterface*G['luz_puente_cinta']/4
tt=G.get('espesor_minimo_anclaje',G['espesor_anclaje'])
Z_bridge=tt*G['alto_puente_cinta']**2/6
Z_bridge_out=G['alto_puente_cinta']*tt**2/6
angle=math.radians(C['angulo_eslinga_grados'])
sbri=1.5*bridge_M*(math.cos(angle)/Z_bridge+math.sin(angle)/Z_bridge_out)
check('Puente anclaje arnes/cinturon biaxial',Sy/sbri,'Se toma la carga completa del lado, no la mitad de la cuna; carga oblicua35grados, viga simplemente apoyada, espesor minimo y K=1.5; 6061')
cuna_Zin=tt*15**2/6;cuna_Zout=15*tt**2/6
cuna_sigma=1.5*(Tstrap*52/4)*(math.cos(angle)/cuna_Zin+math.sin(angle)/cuna_Zout)
check('Puente inferior de cuna',Sy/cuna_sigma,'Ranura horizontal52x8 con puente nominal16/min15 y espesor6/min5.8; carga de una rama de cuna, K1.5')
joint_residual=.75*f0-.8*R
delta_bound=M0*L*L/(9*math.sqrt(3)*E*S['I'])+Q*L**3/(48*E*S['I'])
twist=T*L/(GG*S['J'])*180/math.pi
result=dict(version='P2.04',alcance='Prediseno analitico condicionado; NO validacion del conjunto',
  entrada=P,seccion_minima=S,Fv_N=Fv,Fh_N=Fh,N_lado_N=N,Q_lado_N=Q,L_mm=L,M0_Nmm=M0,
  Mmax_Nmm=mmax,pos_Mmax_mm=xmax,sigma_VM_MPa=vm,flecha_envolvente_mm=delta_bound,
  giro_torsion_ideal_grados=twist,cierre_residual_junta_N=joint_residual,
  cortante_union_N=V,traccion_externa_union_N=R,fuerza_max_perno_N=fb,pasador_sigma_VM_MPa=pin_vm,
  T_por_rama_cuna_N=Tstrap,T_anclaje_arnes_cinturon_N=Tinterface,resistencia_minima_conjunto_cuna_N=5*Tstrap,resistencia_minima_conjunto_cinta_costura_hebilla_N=5*Tinterface,
  verificaciones=checks,minimo_margen=min(q['margen'] for q in checks),
  cumple_cribado=all(q['cumple'] for q in checks) and joint_residual>0 and delta_bound<=C['flecha_limite_mm'],
  pendiente=['Medidas de la Scotty llena/vacia y su centro de masa','Rigidez/contacto real del arnes y reparto de cargas','FEA local, pandeo distorsional y fatiga','Textiles, costuras, hebillas y exposicion termica','Impacto, vibracion, ergonomia y liberacion con guantes'])
(O/'RESULTADOS_PREDISENO.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
with (O/'COMPARACION_SECCIONES.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['ancho_mm','profundidad_mm','espesor_mm','masa_par_kg','margen_solo_flexion','nota'])
    for b,d,t in [(30,20,2.5),(30,22,3),(30,24,3),(30,26,3),(32,24,3),(35,25,3)]:
        ss=section(b,d,t);nn=Sy/(N/ss['A']+C['K_borde']*mmax/ss['Z'])
        w.writerow([b,d,t,2*ss['A']*G['alto_refuerzo']*2.7e-6,nn,'cribado, sin ranuras ni carga lateral'])
print(json.dumps({k:result[k] for k in ['minimo_margen','cumple_cribado','flecha_envolvente_mm','giro_torsion_ideal_grados','cierre_residual_junta_N']},indent=2))
for q in checks: print(q['nombre'],round(q['margen'],3),q['cumple'])
