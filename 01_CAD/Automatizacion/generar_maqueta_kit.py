"""Maqueta SEDAC adaptada a 1:12. Reconstruccion desde cotas del generador,
no conversion ni lectura del IAM. Dependencias locales: manifold3d, numpy.
"""
from pathlib import Path
import sys, math, struct, json, zipfile
import xml.etree.ElementTree as ET
sys.path.insert(0, str(Path(__file__).parent / 'python_libs'))
import manifold3d as m
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '01_CAD' / 'Exportaciones' / 'Maqueta_Kit_1a12'
OUT.mkdir(parents=True, exist_ok=True)
NAME = 'SEDAC_Kit_Maqueta_1a12_ADAPTADA_mm'
def box(x,y,z,w,d,h):
    return m.Manifold.cube((w,d,h)).translate((x,y,z))
def cyl(x,y,z,r,h,n=64):
    return m.Manifold.cylinder(h,r,circular_segments=n).translate((x,y,z))
def slot(x,y,z,length,width,h,vertical=False):
    a=(length-width)/2
    if vertical:
        return box(x-width/2,y-a,z,width,2*a,h)+cyl(x,y-a,z,width/2,h)+cyl(x,y+a,z,width/2,h)
    return box(x-a,y-width/2,z,2*a,width,h)+cyl(x-a,y,z,width/2,h)+cyl(x+a,y,z,width/2,h)
def hexagon(x,y,z,af,h):
    return cyl(x,y,z,af/math.sqrt(3),h,6)

# XY es la cara posterior, Z el relieve. Cara posterior plana en Z=0.
kit=box(0,0,0,30,35,1.6)
# Base a 1:12; espesor del piso aumentado a 1.4 y labios a 1.2 mm.
left=40/12
front=1.6+140/12
floor=box(left,40/12,1.5,280/12,1.4,front-1.5)
# Escotadura U: anchura 5 y profundidad 7.5 mm desde borde delantero.
notch=(box(12.5,3.2,front-5,5,1.8,5.2)
       +m.Manifold.cylinder(1.8,2.5,circular_segments=96).rotate((-90,0,0)).translate((15,3.2,front-5)))
floor=floor-notch
kit=kit+floor
kit=kit+box(left,40/12,1.5,280/12,5.5,1.3)
for x in [left,left+280/12-1.2]:
    kit=kit+box(x,40/12+1.3,1.5,1.2,1.2,front-1.5)

# Placas de anclaje: dimensiones generales a 1:12 + 0.5 mm de borde.
anchor_axes=[]
for ax in [50/12,220/12]:
    ay=295/12
    plate=box(ax-.5,ay-.5,2.8,8.5,7.25,1.4)
    plate=plate-slot(ax+45/12,ay+57.5/12,2.7,52/12,1.2,1.6)
    for xx in [ax+12/12,ax+78/12]:
        yy=320/12
        plate=plate-slot(xx,yy,2.7,2.5,1.0,1.6,True)
        # Separadores macizos y vastagos fundidos: conservan union continua.
        kit=kit+cyl(xx,yy,1.5,1.1,1.4)
        kit=kit+cyl(xx,yy,2.75,.6,2.0)
        anchor_axes.append((xx,yy))
    kit=kit+plate

base_axes=[(x/12,y/12) for x in [90,270] for y in [70,90]]
for axes,face in [(anchor_axes,4.2),(base_axes,2.8)]:
    for x,y in axes:
        # Arandela y cabeza hexagonal exageradas para ser visibles.
        kit=kit+cyl(x,y,face-.1,1.3,.6)
        kit=kit+hexagon(x,y,face+.4,1.6,.8)
        # Herrajes posteriores integrados al panel: contorno grabado, sin salientes.
        # Arandela exterior y hexagono de tuerca representados por dos rebajes.
        groove=cyl(x,y,-.05,1.25,.3)-cyl(x,y,-.1,.95,.4)
        hexgroove=hexagon(x,y,-.05,1.45,.3)-hexagon(x,y,-.1,.95,.4)
        kit=kit-groove-hexgroove

# Comprobaciones de exportacion: dimensiones solicitadas y un solo volumen.
bounds=list(kit.bounding_box())
size=[bounds[i+3]-bounds[i] for i in range(3)]
if any(s>lim for s,lim in zip(size,[40,40,70])):
    raise RuntimeError(f'Fuera del limite: {size}')
if len(kit.decompose())!=1 or kit.volume()<=0:
    raise RuntimeError('La maqueta debe formar un unico volumen conectado.')
mesh=kit.to_mesh()
verts=np.asarray(mesh.vert_properties)[:,:3]
faces=np.asarray(mesh.tri_verts)

with (OUT/(NAME+'.stl')).open('wb') as f:
    f.write(b'SEDAC miniature; coordinates in mm; adapted 1:12'.ljust(80,b' '))
    f.write(struct.pack('<I',len(faces)))
    for face in faces:
        tri=verts[face]
        normal=np.cross(tri[1]-tri[0],tri[2]-tri[0])
        normal=normal/np.linalg.norm(normal)
        f.write(struct.pack('<12fH',*normal,*tri.reshape(-1),0))

# 3MF con unidades explicitas; geometria, sin perfiles de impresora ni soportes.
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',ns)
def tag(name): return '{'+ns+'}'+name
model=ET.Element(tag('model'),unit='millimeter',attrib={'{http://www.w3.org/XML/1998/namespace}lang':'es-ES'})
ET.SubElement(model,tag('metadata'),name='Title').text='SEDAC - maqueta adaptada 1:12'
res=ET.SubElement(model,tag('resources'))
obj=ET.SubElement(res,tag('object'),id='1',type='model')
meshxml=ET.SubElement(obj,tag('mesh'))
vx=ET.SubElement(meshxml,tag('vertices'))
for p in verts:
    ET.SubElement(vx,tag('vertex'),**dict(zip(['x','y','z'],[format(float(a),'.8g') for a in p])))
tx=ET.SubElement(meshxml,tag('triangles'))
for t in faces:
    ET.SubElement(tx,tag('triangle'),**dict(zip(['v1','v2','v3'],[str(int(a)) for a in t])))
build=ET.SubElement(model,tag('build'))
ET.SubElement(build,tag('item'),objectid='1')
with zipfile.ZipFile(OUT/(NAME+'.3mf'),'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

info={'units':'mm','scale':'1:12 adaptada, no uniforme en espesores ni herrajes',
      'source':'Reconstruccion desde SEDAC_Kit_Montaje_V01.iLogicVb; no lectura del IAM',
      'dimensions_xyz_mm':size,'bounding_box_mm':bounds,'connected_volumes':len(kit.decompose()),
      'triangles':len(faces),'volume_mm3':kit.volume(),
      'fits_40_40_70_geometry':True,'sliced':False,'printed':False,
      'note':'No incluye separador a escala real. Revisar soportes para hueco bajo anclajes. Sin validacion estructural.'}
(OUT/'DIMENSIONES_Y_ALCANCE.json').write_text(json.dumps(info,indent=2,ensure_ascii=False),encoding='utf-8')

# Vista geometrica del propio archivo: proyeccion isometrica por triangulos.
# No es una imagen generada por IA ni un render de Inventor.
from PIL import Image, ImageDraw, ImageFont
img=Image.new('RGB',(1100,1000),'#f4f6fa'); draw=ImageDraw.Draw(img)
screenx=np.array([.866,0.,.5]); screeny=np.array([.25,-.866,-.433]); depth=-np.cross(screenx,screeny)
pts=np.column_stack([verts@screenx,verts@screeny]); lo=pts.min(0); hi=pts.max(0)
scale=min(860/(hi[0]-lo[0]),760/(hi[1]-lo[1]))
pts=(pts-(lo+hi)/2)*scale+np.array([550,510])
light=np.array([-.4,-.6,1.]); light=light/np.linalg.norm(light)
pixels=np.asarray(img).copy()
zbuffer=np.full((1000,1100),-np.inf)
for f in faces:
    tri=verts[f]; normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]); normal/=np.linalg.norm(normal)
    if normal@depth<=0: continue
    p=pts[f]; zs=verts[f]@depth
    xmin=max(0,int(np.floor(p[:,0].min()))); xmax=min(1099,int(np.ceil(p[:,0].max())))
    ymin=max(0,int(np.floor(p[:,1].min()))); ymax=min(999,int(np.ceil(p[:,1].max())))
    if xmin>xmax or ymin>ymax: continue
    xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
    a,b,c=p
    den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(den)<1e-10: continue
    u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
    v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
    w=1-u-v; zz=u*zs[0]+v*zs[1]+w*zs[2]
    zb=zbuffer[ymin:ymax+1,xmin:xmax+1]
    mask=(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)&(zz>zb)
    lum=.5+.5*max(0,float(normal@light)); color=tuple(int(c*lum) for c in [225,151,55])
    pixels[ymin:ymax+1,xmin:xmax+1][mask]=color; zb[mask]=zz[mask]
img=Image.fromarray(pixels); draw=ImageDraw.Draw(img)
fontpath=Path('C:/Windows/Fonts/arial.ttf')
font=ImageFont.truetype(str(fontpath),30) if fontpath.exists() else ImageFont.load_default()
small=ImageFont.truetype(str(fontpath),22) if fontpath.exists() else font
draw.text((40,30),'SEDAC | Maqueta integrada 1:12 adaptada',fill='#22334b',font=font)
draw.text((40,920),'30 x 35 x 13.27 mm | Limite disponible: 40 x 40 x 70 mm',fill='#22334b',font=small)
img.save(OUT/'VISTA_MAQUETA.png')
print(json.dumps(info,ensure_ascii=False))
