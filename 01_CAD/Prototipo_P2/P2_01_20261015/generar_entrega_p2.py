from pathlib import Path
import json,struct,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
O=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_01_20261015')
O.mkdir(parents=True,exist_ok=True)
P=[]
def add(n,b,c=(),color=(163,184,200)):P.append(dict(name=n,boxes=b,cuts=list(c),color=color))
for side,x in [('I',-90),('D',90)]:
 add('Riel_'+side,[[x-15,0,0,30,420,1.5],[x-15,0,1.5,1.5,420,13.5],[x+13.5,0,1.5,1.5,420,13.5]])
for i,y in enumerate([50,210,360]):add('Travesano_'+str(i+1),[[-105,y,-2,210,30,2]],color=(111,140,158))
add('Cuna',[[-140,0,1.5,280,2,140],[-140,2,1.5,280,58,2],[-140,2,3.5,2,15,138],[138,2,3.5,2,15,138]],[[-30,-.1,81.5,60,2.2,61]])
for side,x in [('I',-90),('D',90)]:
 add('Anclaje_'+side,[[x-35,320,15,70,60,3]],[[x-26,365,14.9,52,5,3.2],[x-15.1,330,14.9,6.2,20,3.2],[x+8.9,330,14.9,6.2,20,3.2]],(236,151,63))
add('REF_Interfaz_HDPE',[[-130,15,-4.5,260,390,2.5]],color=(47,106,115))
for side,x in [('I',-110),('D',20)]:add('REF_Pad_'+side,[[x,90,-14.5,90,240,10]],color=(49,62,75))
add('REF_Pad_Lumbar',[[-100,20,-14.5,200,50,10]],color=(49,62,75))
M=[]
for p in P[:8]:
 bs=[]
 for i,b in enumerate(p['boxes']):
  a=[v/12 for v in b];a[3:]=[max(v,1.2) for v in a[3:]]
  if p['name']=='Cuna' and i==0:a[4]=1.4
  bs.append(a)
 M.append(dict(name=p['name'],boxes=bs,cuts=[],color=p['color']))
M[5]['cuts']=[[-2.5,-.1,81.5/12,5,1.6,6]]
(O/'GEOMETRIA_P2.json').write_text(json.dumps(dict(version='P2.01',units='mm',status='COTAS PROVISIONALES',axes='X ancho; Y altura; Z hacia bomba',parts=P,mini_parts=M),indent=2),encoding='utf-8')
def surface(boxes,cuts=()):
 axes=[np.unique(np.round([v for b in boxes+list(cuts) for v in (b[k],b[k]+b[k+3])],8)) for k in range(3)]
 x,y,z=np.meshgrid(*[(a[:-1]+a[1:])/2 for a in axes],indexing='ij');occ=np.zeros(x.shape,bool)
 def mask(b):return (x>b[0])&(x<b[0]+b[3])&(y>b[1])&(y<b[1]+b[4])&(z>b[2])&(z<b[2]+b[5])
 for b in boxes:occ|=mask(b)
 for b in cuts:occ&=~mask(b)
 faces=[]
 for i,j,k in np.argwhere(occ):
  a,A=axes[0][i:i+2];b,B=axes[1][j:j+2];c,C=axes[2][k:k+2]
  for (di,dj,dk),face in [
   ((-1,0,0),[(a,b,c),(a,b,C),(a,B,C),(a,B,c)]),((1,0,0),[(A,b,c),(A,B,c),(A,B,C),(A,b,C)]),
   ((0,-1,0),[(a,b,c),(A,b,c),(A,b,C),(a,b,C)]),((0,1,0),[(a,B,c),(a,B,C),(A,B,C),(A,B,c)]),
   ((0,0,-1),[(a,b,c),(a,B,c),(A,B,c),(A,b,c)]),((0,0,1),[(a,b,C),(A,b,C),(A,B,C),(a,B,C)])]:
   ii,jj,kk=i+di,j+dj,k+dk
   if not(0<=ii<occ.shape[0] and 0<=jj<occ.shape[1] and 0<=kk<occ.shape[2]) or not occ[ii,jj,kk]:faces.append(face)
 return np.array(faces,float)
fs=surface([b for p in M for b in p['boxes']],[b for p in M for b in p['cuts']])
ts=np.concatenate([fs[:,[0,1,2]],fs[:,[0,2,3]]])
with (O/'SEDAC_P2_Maqueta_1a12_ADAPTADA_mm.stl').open('wb') as f:
 f.write(b'SEDAC P2.01 mm geometric mockup'.ljust(80,b' '));f.write(struct.pack('<I',len(ts)))
 for t in ts:
  n=np.cross(t[1]-t[0],t[2]-t[0]);n/=np.linalg.norm(n)
  f.write(struct.pack('<12fH',*n,*t.flatten(),0))
vs,idx=np.unique(np.round(ts.reshape(-1,3),8),axis=0,return_inverse=True)
edges={};parents=list(range(len(ts)))
def find(i):
 while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
 return i
for i,t in enumerate(idx.reshape(-1,3)):
 for a,b in zip(t,np.roll(t,-1)):edges.setdefault(tuple(sorted((int(a),int(b)))),[]).append((i,int(a),int(b)))
for es in edges.values():
 for e in es[1:]:parents[find(e[0])]=find(es[0][0])
report=dict(triangles=len(ts),closed_oriented=all(len(es)==2 and es[0][1:]==es[1][1:][::-1] for es in edges.values()),components=len({find(i) for i in range(len(ts))}),bounds_mm=np.ptp(vs,axis=0).tolist(),volume_mm3=float(np.einsum('ij,ij->i',ts[:,0],np.cross(ts[:,1],ts[:,2])).sum()/6),slicer_review='Pendiente')
assert report['closed_oriented'] and report['components']==1 and report['volume_mm3']>0,report
assert np.all(np.array(report['bounds_mm'])<=[40,40,70])
(O/'VERIFICACION_MALLA.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
im=Image.new('RGB',(1800,1200),(241,245,248));d=ImageDraw.Draw(im)
def txt(x,y,s,sz=24,b=False,c=(32,49,64)):
 d.text((x,y),s,font=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf' if b else r'C:\Windows\Fonts\segoeui.ttf',sz),fill=c)
txt(65,40,'SEDAC / P2.01',46,True);txt(65,100,'Doble riel · maqueta geométrica preliminar',29)
txt(65,148,'Cotas provisionales. No representa resistencia, ajuste ni ergonomía validados.',23,c=(94,111,126))
def render(ps,rect,az=35,el=18):
 az,el=map(math.radians,(az,el));right=np.array([math.cos(az),0,-math.sin(az)]);up=np.array([-math.sin(az)*math.sin(el),math.cos(el),-math.cos(az)*math.sin(el)]);view=np.cross(right,up)
 records=[];pts=[]
 for p in ps:
  for f in surface(p['boxes'],p['cuts']):
   n=np.cross(f[1]-f[0],f[2]-f[0]);n/=np.linalg.norm(n)
   if n@view<=.0001:continue
   uv=np.column_stack([f@right,-f@up]);pts.extend(uv)
   shade=.63+.37*max(0,float(n@np.array([.35,.7,.62])))
   records.append((f@view,uv,tuple(int(c*shade) for c in p['color'])))
 pts=np.array(pts);lo=pts.min(0);hi=pts.max(0);x,y,w,h=rect;s=min(w/(hi[0]-lo[0]),h/(hi[1]-lo[1]));off=np.array([x+(w-(hi[0]-lo[0])*s)/2,y+(h-(hi[1]-lo[1])*s)/2])
 pix=np.array(im);depthbuf=np.full((1200,1800),-np.inf)
 for depths,uv,col in records:
  q=(uv-lo)*s+off
  for ids in [[0,1,2],[0,2,3]]:
   t=q[ids];zv=depths[ids];mn=np.floor(t.min(0)).astype(int);mx=np.ceil(t.max(0)).astype(int)
   x0,y0=max(0,mn[0]),max(0,mn[1]);x1,y1=min(1799,mx[0]),min(1199,mx[1])
   xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
   den=(t[1,1]-t[2,1])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,1]-t[2,1])
   if abs(den)<1e-9:continue
   a=((t[1,1]-t[2,1])*(xx-t[2,0])+(t[2,0]-t[1,0])*(yy-t[2,1]))/den
   b=((t[2,1]-t[0,1])*(xx-t[2,0])+(t[0,0]-t[2,0])*(yy-t[2,1]))/den
   c=1-a-b;zz=a*zv[0]+b*zv[1]+c*zv[2]
   dep=depthbuf[y0:y1+1,x0:x1+1];keep=(a>=-1e-7)&(b>=-1e-7)&(c>=-1e-7)&(zz>dep)
   dep[keep]=zz[keep];pix[y0:y1+1,x0:x1+1][keep]=col
 im.paste(Image.fromarray(pix))
for x in [50,630,1210]:d.rounded_rectangle((x,210,x+540,1000),20,fill='white')
txt(78,235,'01  Estructura y cuna',27,True);render(P[:8],(85,300,470,570))
txt(78,910,'Rieles y travesaños: gris',21);txt(78,944,'Anclajes de correas: naranja',21)
txt(658,235,'02  Cara hacia la espalda',27,True);render(P,(665,300,470,570),205,15)
txt(658,910,'HDPE: verde · acolchados: oscuro',21);txt(658,944,'Arnés y bomba no representados',21)
txt(1238,235,'03  Maqueta para impresión',27,True);render(M,(1245,300,470,570))
txt(1238,910,'Disposición 1:12 · espesores adaptados',20);txt(1238,944,' × '.join(f'{v:.2f}' for v in report['bounds_mm'])+' mm',23,True)
txt(65,1040,'Referencia: altura 420 mm · cuna 280 × 140 mm · separación de rieles 180 mm',25)
txt(65,1090,'Vista calculada de la geometría entregada; no es captura de Inventor. Ranuras omitidas en miniatura.',21,c=(94,111,126))
im.save(O/'VISTA_PREVIA_P2.png')
# iLogic con llamadas explicitas editables y misma geometria.
s=[r''' ' SEDAC P2.01 - Maqueta geometrica, cotas provisionales.
' Cada ejecucion genera una carpeta nueva. No cambia fuentes P0.
' Bocetos editables sin acotacion completa. Ensamblaje Grounded.
' Cambiar cotas de las llamadas Block y regenerar; no es asociativo.
Sub Main()
 Dim root As String = "C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_01_20261015"
 Dim output As String = System.IO.Path.Combine(root,"Inventor_" & DateTime.Now.ToString("yyyyMMdd_HHmmss") & "_" & Guid.NewGuid().ToString("N").Substring(0,6))
 System.IO.Directory.CreateDirectory(output)
 Dim stage As String = "Inicio"
 Try
  Dim paths As New System.Collections.Generic.List(Of String)
  Dim p As Inventor.PartDocument = Nothing
''']
def vb(b):return ','.join(format(v,'.12g') for v in b)
for p in P:
 s+=['  stage = "'+p['name']+'"','  p = NewPart()']
 for i,b in enumerate(p['boxes']):s+=['  Block(p,"Vol_'+str(i+1)+'",'+vb(b)+',False)']
 for i,b in enumerate(p['cuts']):s+=['  Block(p,"Abertura_'+str(i+1)+'",'+vb(b)+',True)']
 s+=['  Finish(p,System.IO.Path.Combine(output,"'+p['name']+'.ipt"),'+','.join(map(str,p['color']))+')',
     '  paths.Add(System.IO.Path.Combine(output,"'+p['name']+'.ipt"))','  p.Close(True)']
s+=[r'''
  stage = "Ensamblaje"
  Dim assy As Inventor.AssemblyDocument = CType(ThisApplication.Documents.Add(Inventor.DocumentTypeEnum.kAssemblyDocumentObject,ThisApplication.FileManager.GetTemplateFile(Inventor.DocumentTypeEnum.kAssemblyDocumentObject),True),Inventor.AssemblyDocument)
  assy.UnitsOfMeasure.LengthUnits = Inventor.UnitsTypeEnum.kMillimeterLengthUnits
  For Each path As String In paths
   Dim occ As Inventor.ComponentOccurrence = assy.ComponentDefinition.Occurrences.Add(path,ThisApplication.TransientGeometry.CreateMatrix())
   occ.Name = System.IO.Path.GetFileNameWithoutExtension(path)
   occ.Grounded = True
  Next
  If Not assy.Update2(False) Then Throw New Exception("Fallo al actualizar ensamblaje")
  If assy.ComponentDefinition.Occurrences.Count <> 12 Then Throw New Exception("Se esperaban 12 piezas")
  assy.SaveAs(System.IO.Path.Combine(output,"SEDAC_P2_01.iam"),False)
  stage = "Maqueta reducida"
  p = NewPart()
''']
for pp in [M[i] for i in [2,0,1,3,4,5,6,7]]:
 for i,b in enumerate(pp['boxes']):s+=['  Block(p,"M_'+pp['name']+'_'+str(i+1)+'",'+vb(b)+',False)']
 for i,b in enumerate(pp['cuts']):s+=['  Block(p,"M_Corte_'+pp['name']+'_'+str(i+1)+'",'+vb(b)+',True)']
s+=[r'''
  Finish(p,System.IO.Path.Combine(output,"SEDAC_P2_Maqueta_1a12_ADAPTADA.ipt"),163,184,200)
  Dim box As Inventor.Box = p.ComponentDefinition.SurfaceBodies.Item(1).RangeBox
  Dim dims As String = ((box.MaxPoint.X-box.MinPoint.X)*10).ToString() & " x " & ((box.MaxPoint.Y-box.MinPoint.Y)*10).ToString() & " x " & ((box.MaxPoint.Z-box.MinPoint.Z)*10).ToString()
  If (box.MaxPoint.X-box.MinPoint.X)*10>40.001 OrElse (box.MaxPoint.Y-box.MinPoint.Y)*10>40.001 OrElse (box.MaxPoint.Z-box.MinPoint.Z)*10>70.001 Then Throw New Exception("Maqueta fuera de limite")
  p.Close(True)
  assy.Activate()
  Dim cam As Inventor.Camera = ThisApplication.ActiveView.Camera
  cam.ViewOrientationType = Inventor.ViewOrientationTypeEnum.kIsoTopRightViewOrientation
  cam.Fit()
  cam.Apply()
  Try
   ThisApplication.ActiveView.SaveAsBitmap(System.IO.Path.Combine(output,"CAPTURA_INVENTOR_P2.png"),1600,1200)
  Catch
  End Try
  System.IO.File.WriteAllText(System.IO.Path.Combine(output,"ESTADO_OK.txt"),"P2.01 generado y actualizado en Inventor. 12 piezas fijadas y maqueta de un cuerpo." & vbCrLf & "Maqueta mm: " & dims & vbCrLf & "Sin validacion estructural ni medidas reales de bomba.")
  System.IO.File.WriteAllText(System.IO.Path.Combine(root,"ULTIMA_EJECUCION.txt"),output)
 Catch ex As Exception
  System.IO.File.WriteAllText(System.IO.Path.Combine(output,"ERROR.txt"),stage & vbCrLf & ex.ToString())
  Throw
 End Try
End Sub
Function NewPart() As Inventor.PartDocument
 Dim p As Inventor.PartDocument = CType(ThisApplication.Documents.Add(Inventor.DocumentTypeEnum.kPartDocumentObject,ThisApplication.FileManager.GetTemplateFile(Inventor.DocumentTypeEnum.kPartDocumentObject),False),Inventor.PartDocument)
 p.UnitsOfMeasure.LengthUnits = Inventor.UnitsTypeEnum.kMillimeterLengthUnits
 Return p
End Function
Sub Block(p As Inventor.PartDocument,label As String,x As Double,y As Double,z As Double,w As Double,h As Double,d As Double,cut As Boolean)
 Dim cd As Inventor.PartComponentDefinition = p.ComponentDefinition
 Dim tg As Inventor.TransientGeometry = ThisApplication.TransientGeometry
 Dim plane As Inventor.WorkPlane = cd.WorkPlanes.Item(3)
 If Math.Abs(z) > 0.00000001 Then
  plane = cd.WorkPlanes.AddByPlaneAndOffset(plane,z/10)
  plane.Visible = False
 End If
 Dim sk As Inventor.PlanarSketch = cd.Sketches.Add(plane)
 sk.Name = "B_" & label
 sk.SketchLines.AddAsTwoPointRectangle(tg.CreatePoint2d(x/10,y/10),tg.CreatePoint2d((x+w)/10,(y+h)/10))
 Dim op As Inventor.PartFeatureOperationEnum = Inventor.PartFeatureOperationEnum.kJoinOperation
 If cut Then op = Inventor.PartFeatureOperationEnum.kCutOperation
 Dim ed As Inventor.ExtrudeDefinition = cd.Features.ExtrudeFeatures.CreateExtrudeDefinition(sk.Profiles.AddForSolid(),op)
 ed.SetDistanceExtent(d/10,Inventor.PartFeatureExtentDirectionEnum.kPositiveExtentDirection)
 cd.Features.ExtrudeFeatures.Add(ed).Name = label
 sk.Visible = False
End Sub
Sub Finish(p As Inventor.PartDocument,path As String,r As Integer,g As Integer,b As Integer)
 If Not p.Update2(False) Then Throw New Exception("Fallo al actualizar " & path)
 If p.ComponentDefinition.SurfaceBodies.Count <> 1 Then Throw New Exception("Pieza no tiene un cuerpo: " & path)
 If Not p.ComponentDefinition.SurfaceBodies.Item(1).IsSolid Then Throw New Exception("Pieza no solida")
 p.PropertySets.Item("Inventor User Defined Properties").Add("P2.01 - COTAS PROVISIONALES","SEDAC_Estado")
 Try
  Dim appearance As Inventor.Asset = p.Assets.Add(Inventor.AssetTypeEnum.kAssetTypeAppearance,"Generic","SEDAC_Color","SEDAC_Color")
  CType(appearance.Item("generic_diffuse"),Inventor.ColorAssetValue).Value = ThisApplication.TransientObjects.CreateColor(r,g,b)
  p.ActiveAppearance = appearance
 Catch
 End Try
 p.SaveAs(path,False)
End Sub
''']
(O/'SEDAC_P2_GENERAR.iLogicVb').write_text('\n'.join(s),encoding='utf-8-sig')
print(json.dumps(report))

