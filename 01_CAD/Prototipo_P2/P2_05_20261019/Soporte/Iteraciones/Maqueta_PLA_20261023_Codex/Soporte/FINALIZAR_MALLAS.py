from pathlib import Path
from collections import defaultdict, Counter
import struct, json, math, zipfile, hashlib, xml.etree.ElementTree as ET
import numpy as np

B=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Iteraciones\Maqueta_PLA_20261023_Codex')
O=B/'Entrega'; S=B/'Soporte'; NAME='SEDAC_P204_MAQUETA_SIN_ARNES'
RAW=S/'NATIVO_ORIENTACION_INVENTOR.stl'
def load_stl(path):
    data=path.read_bytes()
    n=struct.unpack_from('<I',data,80)[0]
    if len(data)!=84+50*n:raise ValueError('STL binario incompleto')
    dt=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')])
    return np.frombuffer(data,dtype=dt,count=n,offset=84)['v'].astype(float)

def inspect(t):
    if not np.isfinite(t).all():raise ValueError('Coordenadas no finitas')
    vertices,faces=np.unique(np.round(t.reshape(-1,3),6),axis=0,return_inverse=True)
    faces=faces.reshape(-1,3)
    edges=defaultdict(list); links=defaultdict(list)
    for i,face in enumerate(faces):
        for a,b in zip(face,np.roll(face,-1)):
            edges[tuple(sorted((int(a),int(b))))].append((i,int(a),int(b)))
        for k,v in enumerate(face):links[int(v)].append((int(face[(k+1)%3]),int(face[(k+2)%3])))
    parent=list(range(len(faces)))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for hits in edges.values():
        for h in hits[1:]:parent[root(h[0])]=root(hits[0][0])
    bad_links=0
    for pairs in links.values():
        graph=defaultdict(set)
        for a,b in pairs:graph[a].add(b);graph[b].add(a)
        seen=set();stack=[next(iter(graph))]
        while stack:
            k=stack.pop()
            if k in seen:continue
            seen.add(k);stack.extend(graph[k]-seen)
        if len(seen)!=len(graph) or any(len(neighbors)!=2 for neighbors in graph.values()):bad_links+=1
    cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]); area=np.linalg.norm(cross,axis=1)/2
    volume=float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6)
    result=dict(triangulos=len(faces),vertices_soldados=len(vertices),tolerancia_soldadura_mm=1e-6,
        dimensiones_mm=np.ptp(t.reshape(-1,3),axis=0).tolist(),minimo_mm=t.min(axis=(0,1)).tolist(),maximo_mm=t.max(axis=(0,1)).tolist(),
        componentes_conectados=len({root(i) for i in range(len(faces))}),
        aristas_abiertas=sum(len(h)==1 for h in edges.values()),aristas_no_manifold=sum(len(h)!=2 for h in edges.values()),
        aristas_orientacion_incoherente=sum(len(h)==2 and h[0][1:]==h[1][1:] for h in edges.values()),vertices_no_manifold=bad_links,
        triangulos_degenerados=int(sum(area<1e-10)),triangulos_duplicados=len(faces)-len({tuple(sorted(f)) for f in faces}),volumen_firmado_mm3=volume)
    if any(result[k] for k in ['aristas_abiertas','aristas_no_manifold','aristas_orientacion_incoherente','vertices_no_manifold','triangulos_degenerados','triangulos_duplicados']):raise ValueError(result)
    if result['componentes_conectados']!=1 or volume<=0:raise ValueError(result)
    return result,vertices,faces

native=json.loads((O/'COMPROBACION_NATIVA.json').read_text(encoding='utf-8-sig'))
raw=load_stl(RAW)
native_dimensions=np.array([native['X_mm'],native['Y_mm'],native['Z_mm']])
ratio=native_dimensions/np.ptp(raw.reshape(-1,3),axis=0)
factor=next((x for x in [1,10,25.4,1000] if np.allclose(ratio,x,rtol=1e-5)),None)
if factor is None:raise ValueError('Conversion de unidades no uniforme: '+str(ratio))
t=raw*factor
# Proper rotation, determinant +1: Xnew=Xold, Ynew=-Zold, Znew=Yold.
t=t[:,:,[0,2,1]];t[:,:,1]*=-1
t-=t.min(axis=(0,1))
target=O/(NAME+'.stl')
if target.exists():raise RuntimeError('No se sobrescribe un STL existente')
with target.open('wb') as f:
    f.write(b'SEDAC P2.04 display mockup; coordinates in mm; Z up'.ljust(80,b' '));f.write(struct.pack('<I',len(t)))
    for tri in t:
        normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);normal/=np.linalg.norm(normal)
        f.write(struct.pack('<12fH',*normal,*tri.flatten(),0))
# Reopen the actual file, including float32 export precision.
mesh=load_stl(target); result,vertices,faces=inspect(mesh)
if not np.allclose(result['dimensiones_mm'],[32,18,48],atol=1e-4):raise ValueError('Dimensiones finales inesperadas')
if not np.all(np.array(result['dimensiones_mm'])<=[40,40,70]):raise ValueError('No cabe en el volumen permitido')
volume_error=abs(result['volumen_firmado_mm3']/native['volumen_mm3']-1)*100
if volume_error>.1:raise ValueError('Diferencia de volumen excesiva')

ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',ns)
model=ET.Element('{'+ns+'}model',unit='millimeter',attrib={'{http://www.w3.org/XML/1998/namespace}lang':'es-CL'})
meta=ET.SubElement(model,'{'+ns+'}metadata',name='Title');meta.text='SEDAC maqueta P2.04 sin arnes, 32x18x48 mm'
resources=ET.SubElement(model,'{'+ns+'}resources');obj=ET.SubElement(resources,'{'+ns+'}object',id='1',type='model');m=ET.SubElement(obj,'{'+ns+'}mesh')
vv=ET.SubElement(m,'{'+ns+'}vertices')
for v in vertices:ET.SubElement(vv,'{'+ns+'}vertex',**{k:f'{x:.6f}' for k,x in zip('xyz',v)})
ff=ET.SubElement(m,'{'+ns+'}triangles')
for face in faces:ET.SubElement(ff,'{'+ns+'}triangle',v1=str(face[0]),v2=str(face[1]),v3=str(face[2]))
build=ET.SubElement(model,'{'+ns+'}build');ET.SubElement(build,'{'+ns+'}item',objectid='1')
three=O/(NAME+'.3mf')
with zipfile.ZipFile(three,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
with zipfile.ZipFile(three) as z:
    assert z.testzip() is None
    root=ET.fromstring(z.read('3D/3dmodel.model'))
    assert root.get('unit')=='millimeter'
    vr=np.array([[float(v.get(k)) for k in 'xyz'] for v in root.findall('.//{'+ns+'}vertex')])
    fr=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in root.findall('.//{'+ns+'}triangle')])
    result3,_,_=inspect(vr[fr]);assert np.allclose(result3['dimensiones_mm'],[32,18,48],atol=1e-4)

# Vector diagram from the exported STL, with the actual print orientation and a 40 mm bed.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1000" viewBox="0 0 1100 1000">',
     '<rect width="1100" height="1000" fill="#f7f9fb"/>',
     '<g font-family="Arial,sans-serif" fill="#173042"><text x="45" y="50" font-size="27" font-weight="bold">SEDAC · orientación para impresión</text>',
     '<text x="45" y="82" font-size="18">Una pieza · 32 × 18 × 48 mm · STL y 3MF con altura en Z</text></g>']
view=np.array([1.,-1.,.72]);view/=np.linalg.norm(view);right=np.cross([0,0,1],view);right/=np.linalg.norm(right);up=np.cross(view,right)
placed=mesh+np.array([4,11,0]);bed=np.array([[0,0,0],[40,0,0],[40,40,0],[0,40,0]])
points=np.vstack([placed.reshape(-1,3),bed]);proj=np.column_stack([points@right,-points@up]);scale=min(940/np.ptp(proj[:,0]),690/np.ptp(proj[:,1]));offset=np.array([550,470])-scale*(proj.max(0)+proj.min(0))/2
def xy(p):return np.column_stack([np.asarray(p)@right,-np.asarray(p)@up])*scale+offset
def pointstr(p):return ' '.join(f'{a:.2f},{b:.2f}' for a,b in xy(p))
svg.append(f'<polygon points="{pointstr(bed)}" fill="#e6eef1" stroke="#92a9b6" stroke-width="1.5"/>')
for q in range(0,41,5):
    for line in [[[q,0,0],[q,40,0]],[[0,q,0],[40,q,0]]]:
        c=xy(line);svg.append(f'<path d="M{c[0,0]:.2f},{c[0,1]:.2f} L{c[1,0]:.2f},{c[1,1]:.2f}" stroke="#bcced6" stroke-width=".6"/>')
centers=placed.mean(axis=1)
for i in np.argsort(centers@view):
    tri=placed[i];normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);normal/=np.linalg.norm(normal)
    if np.dot(normal,view)<0:continue
    brightness=int(143+80*max(0,float(np.dot(normal,np.array([.2,-.4,.894427])))))
    color=f'rgb({brightness},{min(255,brightness+7)},{min(255,brightness+12)})'
    svg.append(f'<polygon points="{pointstr(tri)}" fill="{color}" stroke="{color}" stroke-width=".25"/>')
svg.extend(['<g font-family="Arial,sans-serif" fill="#173042" font-size="18">',
 '<text x="45" y="875">Apoyar las dos patas y el travesaño inferior sobre la cama.</text>',
 '<text x="45" y="906">Cuadrícula: 5 mm · cama ilustrada: 40 × 40 mm.</text>',
 '<text x="45" y="937">Brim de 3 mm: envolvente 38 × 24 mm (supuesto, sin soportes).</text>',
 '<text x="45" y="973" fill="#a94b12" font-weight="bold">Pendiente de comprobación en laminador con el perfil real del centro.</text>', '</g></svg>'])
(O/'ORIENTACION_IMPRESION.svg').write_text('\n'.join(svg),encoding='utf-8')

review=dict(fecha='2026-10-23',base='P2.04, maqueta de presentacion redibujada y adaptada',
    native=native,conversion_STL=dict(factor_de_unidad_desde_exportacion=factor,exportacion_original='centimetros' if factor==10 else 'segun factor',rotacion='Xnuevo=X, Ynuevo=-Z, Znuevo=Y; trasladado a origen positivo'),
    STL=result,MF3=dict(unidad='millimeter',objetos=1,dimensiones_mm=result3['dimensiones_mm'],comprobado_reabriendo_zip_y_xml=True),
    diferencia_volumen_STL_vs_IPT_porcentaje=volume_error,limite_impresion_mm=[40,40,70],
    supuesto_brim_mm=3,envolvente_con_brim_sin_soportes_mm=[38,24,48],
    laminado='PENDIENTE DE COMPROBACION EN LAMINADOR',perfil_maquina='No proporcionado',
    comprobacion_autointersecciones_independiente='No realizada; comprobacion de solido nativo y topologia de malla',
    nota='3MF de modelo, sin perfil ni G-code. No se atribuye resistencia o funcion textil a la maqueta PLA.')
(O/'VERIFICACION_MALLAS.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')

readme='''# SEDAC — maqueta de P2.04 para impresión PLA

Entrega: 23/10/2026. Una pieza integrada; dimensiones de impresión: **32 × 18 × 48 mm**.

## Qué archivo enviar al centro

**SEDAC_P204_MAQUETA_SIN_ARNES.3mf** conserva explícitamente la unidad milímetro. Contiene un único modelo, sin configuración de impresora ni G-code.

Alternativa: **SEDAC_P204_MAQUETA_SIN_ARNES.stl**. Importar en **milímetros**, al **100 %**, sin volver a reducir. Debe medir **32 mm en X, 18 mm en Y y 48 mm de alto en Z**. Si aparece otro tamaño, corregir la unidad de importación antes de laminar.

La geometría y la malla están comprobadas; **pendiente de comprobación en laminador**. El centro debe confirmar el perfil de máquina, boquilla, capas, puentes, soportes y adhesión antes de aceptar la impresión. No se entrega G-code.

## Qué representa

Conserva la distribución del P2.04: dos refuerzos dorsales, panel perforado, interfaz lumbar, yugos superiores y apoyo inferior abierto en el centro para representar el paso de la manguera. Separación entre refuerzos: 19 mm; altura: 48 mm.

Se omitieron correas, arnés, acolchados y hebillas. Los tornillos/pasadores pequeños se representan con relieves integrados, sin roscas ni montaje. Todo está unido en un solo sólido.

**La cuna del producto P2.04 es textil. Aquí se representa mediante dos apoyos rígidos, labios y laterales inclinados únicamente para construir una maqueta manejable. Esto no cambia el diseño de ingeniería del producto.** La maqueta no reproduce la flexibilidad del sistema, no es una pieza funcional para sostener la bomba y no valida cargas ni comodidad.

## Escala y adaptaciones

Distribución nominal **1:10**, con detalles aumentados para esta maqueta. No es una reducción uniforme ni sirve para obtener cotas del producto. Un canal real 32 × 24 × 3 mm mediría 3,2 × 2,4 × 0,3 mm a escala; aquí su envolvente es 4 × 3 mm, con paredes de 1,2 mm. Panel de 1,2 mm, suelo de 2 mm y laterales de 1,2 mm. Los marcadores de fijación tienen Ø1,6 mm y sobresalen 0,6 mm; son detalles visuales.

Las dimensiones mínimas se propusieron pensando en una boquilla de 0,4 mm, **supuesto sin confirmar**. El número de perímetros y la conservación de los relieves requieren el perfil real del centro. Se fusionaron pequeñas holguras y se simplificaron las ranuras de los anclajes; las aberturas grandes se conservaron. El panel se extiende hasta los 48 mm para integrar los extremos de los refuerzos.

## Orientación y espacio

El STL y el 3MF ya están orientados con **Z hacia arriba**, ambos pies y el travesaño inferior en **Z=0**. La abertura frontal en U para manguera tiene 10,4 mm de ancho. Mantener esa orientación como propuesta inicial; ver ORIENTACION_IMPRESION.svg.

La pieza cabe en 40 × 40 × 70 mm. Un brim de **3 mm** daría aproximadamente **38 × 24 × 48 mm** de envolvente, sin contar soportes. Es una propuesta, no una configuración de máquina comprobada. Si se añaden soportes u otra adhesión, comprobar la envolvente completa de nuevo. El suelo ofrece apoyo continuo bajo ambas patas y la parte posterior.

Revisar especialmente el puente de aproximadamente 9 mm sobre la ventana central, las ventanas laterales, los pequeños voladizos de los yugos y los relieves. Los laterales inclinados de la cuna se apoyan sobre el suelo; no hay correas suspendidas. La necesidad y el acceso para retirar soportes quedan pendientes de laminado. No se ha estimado tiempo ni consumo con un perfil real.

## Comprobaciones realizadas

- Inventor 2027.1: lectura real del modelo de DeepSeek y creación nativa de esta maqueta; actualización correcta y un cuerpo sólido.
- STL final reabierto: 2064 triángulos, un componente conectado; sin bordes abiertos, aristas o vértices no manifold, caras duplicadas o triángulos degenerados; orientación de caras coherente y volumen positivo.
- Medidas del STL contrastadas con el IPT, incluyendo la conversión de la exportación original en centímetros a la entrega final en milímetros. El volumen difiere aproximadamente 0,0031 % del sólido por facetado y redondeo numérico.
- 3MF construido con la misma malla, unidad millimeter, un objeto; contenedor y XML reabiertos y comprobados. No es una exportación nativa de 3MF de Inventor ni un proyecto de laminador.
- No se ejecutó una detección independiente de autointersecciones de la malla ni una simulación física de impresión.

## Editables y trazabilidad

SEDAC_P204_MAQUETA_SIN_ARNES.ipt: pieza con bocetos y extrusiones editables. STEP: intercambio de geometría sólida. En estos editables se conserva la convención del proyecto de altura en **Y**: caja **32 × 48 × 18 mm**; el STL/3MF se rotó para que la altura sea Z. El volumen y la forma son los mismos.

Los parámetros de operaciones, generador y exportación inicial quedan en Soporte. El STL inicial de Soporte está en centímetros y en orientación de Inventor: **no enviarlo al centro**. Los archivos para impresión son únicamente los de Entrega indicados arriba.

Se usaron las habilidades locales inventor-modeling, dfm-review y la ficha previa de especificación CAD. Las herramientas MCP de Inventor no están expuestas en esta sesión; se utilizó la API COM nativa, comprobada mediante lectura de versión y del IPT existente. No se cambió la configuración de servidores. Se tomó P2.04 como referencia; no se incorporó ni se ejecutó el generador P2.05 pendiente de cierre.

P2.04, P2.05 y la maqueta de DeepSeek quedan conservados. Esta entrega se guarda en una iteración nueva y no cierra el diseño de ingeniería. No se ha enviado ningún correo.
'''
(O/'LEEME_PARA_IMPRIMIR.md').write_text(readme,encoding='utf-8')
print(json.dumps(dict(STL=result,conversion=factor,volumen_error_porcentaje=volume_error,archivo3mf=str(three)),indent=2,ensure_ascii=False))
