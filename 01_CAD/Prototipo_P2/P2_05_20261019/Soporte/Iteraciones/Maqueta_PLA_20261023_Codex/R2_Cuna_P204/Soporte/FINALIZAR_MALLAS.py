from pathlib import Path
from collections import defaultdict, Counter
import struct, json, math, zipfile, hashlib, xml.etree.ElementTree as ET
import numpy as np

B=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Iteraciones\Maqueta_PLA_20261023_Codex\R2_Cuna_P204')
O=B/'Entrega'; S=B/'Soporte'; NAME='SEDAC_P204_MAQUETA_CUNA_CURVA'
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
if not np.allclose(result['dimensiones_mm'],[32,18,48],atol=.01):raise ValueError('Dimensiones finales inesperadas')
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
    result3,_,_=inspect(vr[fr]);assert np.allclose(result3['dimensiones_mm'],[32,18,48],atol=.01)

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
 '<text x="45" y="875">Espalda vertical sobre el borde inferior. Soportes bajo las cunas.</text>',
 '<text x="45" y="906">Cuadrícula: 5 mm · cama ilustrada: 40 × 40 mm.</text>',
 '<text x="45" y="937">Brim de 3 mm: envolvente 38 × 24 mm (supuesto, sin soportes).</text>',
 '<text x="45" y="973" fill="#a94b12" font-weight="bold">Pendiente de comprobación en laminador con el perfil real del centro.</text>', '</g></svg>'])
(O/'ORIENTACION_IMPRESION.svg').write_text('\n'.join(svg),encoding='utf-8')

review=dict(fecha='2026-10-23',base='P2.04 señalado por usuario; cunas originales escaladas y engrosadas',
    native=native,conversion_STL=dict(factor_de_unidad_desde_exportacion=factor,exportacion_original='centimetros' if factor==10 else 'segun factor',rotacion='Xnuevo=X, Ynuevo=-Z, Znuevo=Y; trasladado a origen positivo'),
    STL=result,MF3=dict(unidad='millimeter',objetos=1,dimensiones_mm=result3['dimensiones_mm'],comprobado_reabriendo_zip_y_xml=True),
    diferencia_volumen_STL_vs_IPT_porcentaje=volume_error,limite_impresion_mm=[40,40,70],
    supuesto_brim_mm=3,envolvente_con_brim_sin_soportes_mm=[38,24,48],
    laminado='PENDIENTE DE COMPROBACION EN LAMINADOR',perfil_maquina='No proporcionado',
    comprobacion_autointersecciones_independiente='No realizada; comprobacion de solido nativo y topologia de malla',
    nota='3MF de modelo, sin perfil ni G-code. No se atribuye resistencia o funcion textil a la maqueta PLA.')
(O/'VERIFICACION_MALLAS.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')


readme='# SEDAC — maqueta P2.04 sin arnés, con cuna original\n\nEntrega: 23/10/2026. **Una pieza, aproximadamente 32 × 18 × 48 mm** en orientación de impresión (X ×Y × altura Z). Usar esta revisión **R2_Cuna_P204**; el primer borrador de bandeja plana queda como antecedente y no es el archivo propuesto para enviar.\n\n## Para el centro de impresión\n\nEnviar **SEDAC_P204_MAQUETA_CUNA_CURVA.3mf** (unidad milímetro incluida) o **SEDAC_P204_MAQUETA_CUNA_CURVA.stl** (importar en milímetros, al 100 %). No volver a reducir. Confirmar en el laminador unos **48 mm de alto**.\n\nEs una maqueta visual para PLA. **Pendiente de comprobación en laminador**: se necesita el perfil real de la máquina y revisar **soportes bajo las dos cunas curvas elevadas**. No se entregaG-code ni se garantiza impresión sin soportes. No es una pieza funcional para cargar una bomba.\n\nEl volumen máximo comunicado es 40 ×40 ×70 mm. La pieza cabe; un brim hipotético de 3 mm daría aproximadamente 38 × 24 mm de envolvente en planta. Los soportes y cualquier otra adhesión también deben quedar dentro de 40 ×40 mm: comprobarlo con el laminado real. Boquilla 0,4 mm es únicamente el supuesto utilizado al proponer los espesores.\n\n## Relación con el modelo que eligió el usuario\n\nReferencia: **SEDAC_P2_04.iam** de P2_04_20261016/Entrega/Inventor. Se preservan el panel dorsal perforado, los dos canales, el lumbar y los yugos. Se omiten el arnés, las correas largas, acolchados, hebillas y fundas. Las fijaciones pequeñas quedan como relieves, sin roscas reales.\n\nLas dos cunas toman **su posición, ancho y recorrido del contorno REF_Cuna_textil_I/D del manifiesto de ese P2.04**, a 1:10. No se desplazan hacia abajo ni se sustituyen por una bandeja plana. Se aumentó su espesor a 1,2 mm y se unieron a los canales engrosados de la maqueta. Se retiraron la bandeja y los laterales triangulares del primer borrador. El registroREFERENCIA_GEOMETRICA_P204.json contiene los recorridos y huellas de las fuentes.\n\n**La cuna del producto original sigue siendo textil. Su representación rígida aquí es exclusivamente una adaptación de maqueta.** La geometría de fabricación y los cálculos del producto no se modifican.\n\n## Escala y edición\n\nDistribución nominal 1:10 con espesores magnificados. No es una reducción uniforme ni permite obtener dimensiones reales del producto. Canales: envolvente 4 × 3 mm y pared 1,2 mm, frente a 3,2 × 2,4 × 0,3 mm que resultarían al reducir uniformemente la sección del producto. Panel nominal 1,2 mm y cuna 1,2 mm. Se integran holguras para formar un único sólido. Algunos pequeños relieves sobresalen 0,6 mm y requieren comprobar que el laminador los conserve.\n\nEl IPT contiene bocetos y extrusiones editables; STEP es la alternativa de intercambio. En IPT/STEP se conserva alturaY, con caja aproximada32 × 48 × 18 mm. En STL/3MF la altura esZ: aproximadamente 32 × 18 × 48 mm. El paquete para el centro contiene los archivos de malla y las instrucciones; los editables quedan en la carpetaEntrega y su paquete técnico.\n\n## Qué se comprobó\n\n- Creación nativa en Inventor 2027.1; actualización, un sólido y geometría editable.\n- STL reabierto: un componente cerrado, aristas y vértices manifold, sin caras duplicadas o degeneradas, orientación de caras coherente y volumen positivo. Dimensiones contrastadas con el IPT.\n- La exportación inicial de Inventor estaba en centímetros; el STL final está convertido a milímetros y girado aZ vertical. El archivo inicial deSoporte no debe enviarse.\n- 3MF de modelo creado con la misma malla; ZIP/XML reabiertos, unidad millimeter y un objeto. No es un proyecto laminado ni una exportación3MF del traductor de Inventor.\n- Detalles numéricos enVERIFICACION_MALLAS.json. No se realizó una detección independiente de autointersecciones ni un ensayo de impresión.\n\n## Cómo se preparó\n\nHabilidades de especificaciónCAD, inventor-modeling y dfm-review. La creación y exportación utilizaron la API COM nativa; no había herramientas MCP de Inventor expuestas en esta sesión. El manifiesto fuente esP2.04; no se ejecutó ni incorporó el generadorP2.05 pendiente de cierre.\n\nLas fuentes y la maqueta de DeepSeek se conservan. Esta maqueta no cierraP2.05 ni valida resistencia, flexibilidad o comodidad del sistema auxiliar.\n'
(O/'LEEME_PARA_IMPRIMIR.md').write_text(readme,encoding='utf-8')
print(json.dumps(dict(STL=result,conversion=factor,volumen_error_porcentaje=volume_error,archivo3mf=str(three)),indent=2,ensure_ascii=False))
