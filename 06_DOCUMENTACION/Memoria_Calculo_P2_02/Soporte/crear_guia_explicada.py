# -*- coding: utf-8 -*-
"""Guia de lectura independiente para la memoria clasica MC01."""
from pathlib import Path
import json, math, re, sys
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Memoria_Calculo_P2_02')
SUP = BASE / 'Soporte'
OUT = BASE / 'Guia_Explicada_Memoria_SEDAC_P2_02_MC01.pdf'
V = {x['name']:x['value'] for x in json.loads((SUP/'VALORES_ESPERADOS_SI.json').read_text(encoding='utf-8-sig'))}
W,H = 595.276,841.89
M=48
CW=W-2*M
NAVY=colors.HexColor('#173345')
TEAL=colors.HexColor('#007D86')
INK=colors.HexColor('#243746')
MUTED=colors.HexColor('#576B79')
PALE=colors.HexColor('#F0F5F7')
LINE=colors.HexColor('#D6E1E6')
AMBER=colors.HexColor('#8F4D13')
RED=colors.HexColor('#9D302C')
for name,fn in [('Body','arial.ttf'),('BodyBold','arialbd.ttf'),('BodyItalic','ariali.ttf'),('Code','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path(r'C:\Windows\Fonts')/fn)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
ST={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=14.4,textColor=INK,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.7,leading=12,textColor=MUTED,spaceAfter=6),
 'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=11.7,leading=15.4,textColor=TEAL,spaceBefore=5,spaceAfter=6),
 'title':ParagraphStyle('title',fontName='BodyBold',fontSize=21,leading=25.4,textColor=NAVY,spaceAfter=12),
 'formula':ParagraphStyle('formula',fontName='Code',fontSize=9.5,leading=14.2,textColor=NAVY,spaceAfter=0),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=9.3,leading=12.5,textColor=INK),
 'cellhead':ParagraphStyle('cellhead',fontName='BodyBold',fontSize=9.3,leading=12.5,textColor=colors.white),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=10.2,leading=14.4,textColor=INK,leftIndent=11,firstLineIndent=-9,spaceAfter=5),
}
def fmt(x,n=2):
    return f'{x:,.{n}f}'.replace(',','@').replace('.',',').replace('@','.')
def val(n,scale=1,d=2): return fmt(V[n]*scale,d)
def p(s,style='body'): return Paragraph(s,ST[style])
def bullet(s): return p('• '+s,'bullet')
def h(s): return p(s,'h2')
def eq(*lines):
    cells=[[p(escape(s),'formula')] for s in lines]
    t=Table(cells,colWidths=[CW],hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),0.5,LINE),
      ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
      ('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,-1),(-1,-1),7)]))
    return [t,Spacer(1,9)]
def box(title,text,kind='note'):
    col=RED if kind=='risk' else TEAL
    textp=Paragraph(f'<b>{title}</b><br/>{text}',ParagraphStyle('box',parent=ST['body'],fontSize=10,leading=14,textColor=col,spaceAfter=0))
    t=Table([[textp]],colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FBEFEB') if kind=='risk' else colors.HexColor('#EAF5F5')),('LINEBEFORE',(0,0),(0,0),3,col),('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    return [t,Spacer(1,9)]
def table(rows,widths,header=True):
    data=[[p(str(s),'cellhead' if i==0 and header else 'cell') for s in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    rules=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.35,LINE)]
    if header: rules += [('BACKGROUND',(0,0),(-1,0),NAVY)]
    for i in range(1 if header else 0,len(rows)):
        if i%2:rules.append(('BACKGROUND',(0,i),(-1,i),PALE))
    t.setStyle(TableStyle(rules))
    return [t,Spacer(1,9)]

def arrow(c,x1,y1,x2,y2,col=TEAL,head=6):
    c.setStrokeColor(col);c.setFillColor(col);c.setLineWidth(1.4);c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1)
    path=c.beginPath();path.moveTo(x2,y2)
    path.lineTo(x2-head*math.cos(a-.45),y2-head*math.sin(a-.45))
    path.lineTo(x2-head*math.cos(a+.45),y2-head*math.sin(a+.45));path.close()
    c.drawPath(path,stroke=0,fill=1)
def label(c,x,y,s,size=9,col=INK):
    c.setFillColor(col);c.setFont('Body',size);c.drawString(x,y,s)

class Sketch(Flowable):
    def __init__(self,kind,height=142):super().__init__();self.kind=kind;self.width=CW;self.height=height
    def draw(self):
        c=self.canv;w=self.width
        c.setFillColor(PALE);c.roundRect(0,0,w,self.height,7,fill=1,stroke=0)
        if self.kind=='path':
            xs=[12,139,266,393];labels=[('Bomba + agua','Fv, Fh y excentricidad'),('Cuna y cartelas','Apoyo y unión M8'),('Rieles y anclajes','Flexión + torsión'),('Arnés y persona','Reacciones reales')]
            for x,(a,b) in zip(xs,labels):
                c.setStrokeColor(LINE);c.setFillColor(colors.white);c.roundRect(x,53,105,58,5,fill=1,stroke=1)
                label(c,x+8,88,a,9);label(c,x+8,70,b,7.2,MUTED)
                if x<390:arrow(c,x+107,82,x+125,82)
            label(c,14,26,'Esquema de transmisión de carga. No representa la geometría ni el reparto medidos.',8,MUTED)
        elif self.kind=='section':
            x,y,sc=34,23,3.2
            c.setStrokeColor(TEAL);c.setFillColor(colors.HexColor('#CEEAEC'));c.setLineWidth(1.4)
            c.roundRect(x,y,50*sc,25*sc,5*sc,fill=1,stroke=1)
            c.setFillColor(colors.white);c.roundRect(x+2.5*sc,y+2.5*sc,45*sc,20*sc,2.5*sc,fill=1,stroke=1)
            c.setStrokeColor(MUTED);c.setDash(3,3);c.line(x-12,y+40,x+175,y+40);c.line(x+80,y-6,x+80,y+94);c.setDash()
            label(c,63,115,'b = 50 mm',9);label(c,215,99,'d = 25 mm; t = 2,5 mm',9)
            label(c,215,78,'ro = 5 mm; ri = 2,5 mm',9)
            label(c,215,57,'Área: material de la pared',9)
            label(c,215,36,'Ix / Iz: distribución del área',9)
        elif self.kind=='bolts':
            c.setStrokeColor(MUTED);c.setFillColor(colors.white);c.roundRect(48,19,110,112,5,stroke=1,fill=1)
            for yy in (45,105):
                c.setFillColor(TEAL);c.circle(103,yy,5,fill=1,stroke=0)
            arrow(c,103,105,162,105)
            arrow(c,103,105,103,72)
            arrow(c,103,45,75,45)
            label(c,19,71,'pitch',8)
            label(c,190,111,'Tornillo crítico:',10,TEAL)
            label(c,190,91,'componente vertical = Vy/2',9)
            label(c,190,71,'componente horizontal = Vz/2 + MomC/pitch',9)
            label(c,190,49,'La fuerza del par se suma con signo.',9)
            label(c,190,27,'Magnitud final multiplicada por Kb = 1,2.',9)
        elif self.kind=='floor':
            c.setStrokeColor(INK);c.setLineWidth(2);c.line(28,76,w-28,76)
            for x in (137,317):
                c.setFillColor(TEAL);path=c.beginPath();path.moveTo(x,73);path.lineTo(x-7,60);path.lineTo(x+7,60);path.close();c.drawPath(path,fill=1,stroke=0)
            for x in range(35,int(w-25),24):arrow(c,x,117,x,81,TEAL,4)
            arrow(c,w-30,135,w-30,81,RED,6)
            label(c,26,129,'Presión qfloor',8)
            label(c,315,130,'Ppatch en borde',8,RED)
            label(c,173,42,'spanF = 65 mm',9)
            label(c,342,42,'over = 40 mm',9)
            label(c,29,16,'Apoyos sobre ejes de tubos. Esquema sin escala; franja de ancho unitario.',8,MUTED)
        elif self.kind=='diagonal':
            x,y=35,18;ww,hh=80,110
            c.setStrokeColor(LINE);c.setLineWidth(2);c.rect(x,y,ww,hh,stroke=1,fill=0)
            c.setStrokeColor(TEAL);c.line(x,y,x+ww,y+hh)
            c.setDash(3,3);c.setStrokeColor(MUTED);c.line(x+ww,y,x,y+hh);c.setDash()
            arrow(c,x+ww,y+hh,x+ww+48,y+hh)
            label(c,195,112,'Se acredita una diagonal a tracción.',10,TEAL)
            label(c,195,88,'sin(ángulo desde vertical) = Sep/LenX',9)
            label(c,195,64,'ForceX · Sep/LenX = Fh',9)
            label(c,195,40,'La opuesta puede quedar floja o pandear.',9)
        else:raise ValueError(self.kind)
PAGES=[]
def page(key,title,items,section=None):
    flat=[]
    for item in items:
        if isinstance(item,list): flat.extend(item)
        else:flat.append(item)
    PAGES.append(dict(key=key,title=title,items=flat,section=section))

page('portada','Guía explicada de la memoria de cálculo',[
 p('SEDAC  /  P2.02  /  MC01', 'h2'),
 p('Desarrollos, teoría de fallas y lectura en Mathcad 15', 'h2'),
 Spacer(1,12),
 p('Esta guía acompaña la hoja editable y permite seguir sus ecuaciones en el mismo orden. Cada capítulo indica la sección de Mathcad, explica qué se está calculando y desarrolla un ejemplo con las entradas iniciales.'),
 Sketch('path',145),Spacer(1,14),
 box('Archivo de referencia','Memoria_SEDAC_P2_02_MC01_EDITABLE.xmcd<br/>Los 17 encabezados numerados de esa hoja se conservan en esta guía.'),
 p('<b>Cómo leerla:</b> consulta primero las dos páginas de ayuda de Mathcad y la base teórica. Luego abre el capítulo que tenga el mismo número que la sección de la hoja.'),
 p('<b>Estado:</b> prediseño paramétrico; falta medir la bomba real. Los valores ilustran las hipótesis actuales y todavía no establecen una capacidad de uso.'),
 p('<b>Edición de esta guía:</b> 15 de octubre de 2026. Las cifras del PDF son estáticas; si cambias entradas en Mathcad, sus resultados pueden dejar de coincidir con estos ejemplos.','small'),
 p('Las ecuaciones de la memoria se explican tal como están implementadas. Cuando una aproximación necesita revisión, se identifica expresamente dentro del capítulo correspondiente.','small'),
])
maprows=[['En Mathcad','Tema','En esta guía']]
titles=[
'Cargas y alcance','Geometría y brazos','Materiales y factores','Funciones de sección redondeada',
'Riel: tensión normal','Riel: torsión, fluencia y flecha','Pandeo global y local',
'Grupo de tornillos M8','Cortante, aplastamiento y arrancamiento','Raíz de cartela',
'Cargas sobre el piso','Piso: resultado y espesor','Refuerzos y anclaje de hombro',
'Cinturón y diagonales','M6 y alcance de los criterios','Lectura de resultados','Uso y actualización del modelo']
for i,tit in enumerate(titles,1):maprows.append([str(i),tit,f'Página {i+5}'])
page('mapa','Mapa para leer ambos archivos',[
 p('La página indicada abajo corresponde al número impreso en el pie de esta guía. El encabezado de cada capítulo remite a la sección numerada de la hoja MC01.'),
 table(maprows,[66,CW-150,84]),
 p('<b>Antes de los capítulos:</b> pág. 3, operadores y recálculo; pág. 4, unidades y funciones; pág. 5, criterio de fluencia.'),
 p('<b>Después:</b> pág. 23, fatiga y fractura; pág. 24, sensibilidad y próximos cálculos; pág. 25, diccionario; págs. 26-27, fuentes y trazabilidad.','small')
])
page('mathcad1','Mathcad: definir, evaluar y recalcular',[
 h('1. Los dos signos que más se usan'),
 eq('Mass := 25*kg','Fv := Mass*grav*av','Fv = 735.75 N'),
 p('<b>:= define</b> una variable o una función. <b>= evalúa</b> una expresión y muestra su valor. Una definición no necesita terminar mostrando un número para estar bien construida. En la hoja, las entradas editables están resaltadas en azul claro.'),
 h('2. Leer en el orden de cálculo'),
 p('Mathcad clásico procesa las regiones de arriba hacia abajo y, cuando están a la misma altura, de izquierda a derecha. Define una variable antes de utilizarla. Una región puede aparecer cerca de su definición y aun así quedar antes en el orden de lectura. [1]'),
 h('3. Una función es una regla reutilizable'),
 eq('Ar(B,D,R) := B*D - (4-pi)*R^2','Ar(50*mm,25*mm,5*mm) = 1228.54 mm^2'),
 p('B, D y R son argumentos locales: indican dónde se insertan los datos al llamar a la función. El ejemplo calcula un rectángulo macizo con esquinas redondeadas; para un tubo se resta el hueco interior. Las funciones Ar, Ir y Jc se desarrollan en el capítulo 4.'),
 h('4. Actualizar la hoja completa'),
 p('La ayuda instalada de Mathcad clásico indica <b>Ctrl + F9</b> para recalcular toda la hoja. En modo manual puede verse “Calc” en la barra de estado; en modo automático se muestra “AUTO”. Antes de imprimir, recalcula la hoja completa. [1]'),
 box('Si alguna vez falta un resultado','Comprueba el orden de las regiones, la escritura exacta del nombre, las unidades y el modo de cálculo. Un nombre marcado en rojo indica un error; una definición de función sin evaluación numérica es normal.'),
 p('La ayuda local utilizada pertenece a la instalación clásica. No se extrapolan menús o atajos de Mathcad Prime.','small')
])
page('mathcad2','Mathcad: unidades y funciones utilizadas',[
 table([
 ['Expresión','Qué significa en esta memoria'],
 ['sqrt(x) o raíz cuadrada','Raíz principal. sqrt(9 mm²) = 3 mm. En la hoja puede verse el radical, aunque aquí se escriba sqrt.'],
 ['min(a,b,...)','Devuelve el menor valor. min(Ix,Iz) escoge el eje menos rígido; min(SyR,SigCr) limita la tensión por el fenómeno que ocurre primero.'],
 ['max(a,b,...)','Devuelve el mayor valor. max(Mspan,Medge) selecciona el momento por ancho más exigente.'],
 ['pi / π; x^2; x^3','Constante π y potencias. t^2 multiplica t por sí mismo; una potencia también eleva la unidad.'],
 ['Paréntesis y multiplicación','* expresa multiplicación en esta guía. Conserva los paréntesis: eta*(Fv*ecc+Fh*armH) multiplica la suma completa.'],
 ['Nr y nR','Son nombres distintos. Nr es una fuerza axial en N; nR es un margen adimensional. Mayúsculas y minúsculas importan.'],
 ],[117,CW-117]),
 h('Unidades que conviene reconocer'),
 eq('1 N = 1 kg*m/s^2','1 MPa = 1 N/mm^2 = 10^6 Pa','1 mm^4 = 10^(-12) m^4'),
 p('Un dato dimensional se introduce multiplicando por su unidad: <b>t := 2.5*mm</b>. No reemplaces 2,5 mm por el número 2,5 sin unidad. Cambiar la unidad de presentación del resultado no cambia el valor físico. [1]'),
 p('<b>Notación científica:</b> Ix = 3,2784 × 10<super>-8</super> m<super>4</super> equivale a 32.784,01 mm<super>4</super>. El exponente cambia al cambiar la unidad; no es un error.'),
 p('<b>Momento por ancho:</b> Mfloor se muestra en N porque (N·mm)/mm = N. Sigue siendo momento flector por unidad de ancho, no una fuerza externa aplicada.'),
 p('En las ecuaciones escritas con nombres de funciones se usa punto decimal para separar visualmente los argumentos. En el texto y las tablas se usa coma decimal. Respeta la configuración regional de tu Mathcad.','small')
])
page('teoria','Base teórica: fluencia y margen calculado',[
 h('Qué se compara'),
 p('En un metal dúctil, la fluencia marca el inicio de deformación plástica. Sy es la tensión de referencia de fluencia o la resistencia convencional al 0,2 %. La rigidez E relaciona tensión y deformación elástica; no sustituye a Sy.'),
 eq('n = Sy / tensión_equivalente','Criterio adoptado: n >= nReq = 2.2'),
 p('n es un cociente adimensional. Un resultado n = 1,22 sigue por debajo del umbral de fluencia ideal bajo esa carga, pero no alcanza el margen objetivo 2,2. No significa que la pieza vaya a romperse inmediatamente ni que tenga una vida útil conocida.'),
 h('Por qué aparece Von Mises'),
 p('Se adopta como criterio de fluencia para el aluminio y los tornillos dúctiles del prediseño. Combina tensiones normales y cortantes en una tensión equivalente. En un estado con una tensión normal σ y una cortante τ: [2]'),
 eq('sigmaVM = sqrt(sigma^2 + 3*tau^2)','Cortante puro: sigmaVM = sqrt(3)*tau'),
 p('Por eso el M8 se compara con SyB usando sqrt(3)*R8/As8. En el riel se combina SigN con TauT + TauV y se aplica el multiplicador provisional Kt. Esta operación usa una envolvente de solicitaciones, no un campo local completo.'),
 h('Qué cambiaría con Tresca'),
 p('Tresca usa la máxima diferencia entre tensiones principales: max(|σ1-σ2|,|σ2-σ3|,|σ3-σ1|). En cortante puro conduce a 2|τ|, frente a sqrt(3)|τ| de Von Mises. No se ha implementado una verificación separada con Tresca. [2]'),
 box('Los factores tienen funciones distintas','av y ah representan cargas elegidas; Kt, Kslot y Kb amplifican demandas; nReq fija el margen buscado. Que sean números mayores que uno no los vuelve intercambiables.'),
 p('Fluencia, fractura, fatiga, pandeo y deformación excesiva son fenómenos distintos. La memoria calcula algunos de ellos con modelos simplificados; los otros requieren información adicional.','small')
])

page('s1','Alcance y escenario de carga',[
 h('De la masa a las fuerzas de cálculo'),
 p('Se adopta <b>Mass = 25 kg</b> como masa total soportada por el sistema auxiliar. Es una entrada provisional: debe incluir lo que realmente atraviese esa trayectoria de carga. No se deduce directamente de la capacidad en litros de la bolsa.'),
 eq('Fv = Mass*grav*av = 25*9.81*3 = 735.75 N','Fh = Mass*grav*ah = 25*9.81*1 = 245.25 N'),
 p('grav convierte masa en peso. av = 3 representa una resultante vertical de tres veces el peso estático, incluyendo la gravedad. No significa agregar otros 3g al peso. ah = 1 fija una resultante horizontal igual al peso estático.'),
 h('Cómo se reparte entre lados'),
 eq('eta = 0.7','Carga vertical en el lado más exigido = eta*Fv','eta*Fv = 515.025 N'),
 p('eta representa un reparto supuesto 70/30 entre los dos lados. El lado opuesto recibe el 30 % cuando se plantea ese mismo caso asimétrico. No se debe asignar 70 % a cada lado y luego sumar ambos como si fuese el equilibrio del mismo caso.'),
 h('Qué carga se está simulando'),
 p('Los factores sirven para explorar una condición de prediseño; todavía no provienen de aceleraciones medidas, de una norma de uso seleccionada ni de ensayos del equipo. El movimiento del agua y la bolsa flexible pueden modificar fuerzas, direcciones y contacto.'),
 box('Interpretación','Estas fuerzas permiten comparar geometrías. No convierten 25 kg en una capacidad nominal aprobada. El piso incorpora además una envolvente local adicional, que se explica en el capítulo 11.'),
 p('Ruta de carga a revisar con el equipo real: bolsa y cuna → cartelas → rieles → anclajes → arnés y persona. Las reacciones del arnés son parte del problema mecánico.'),
],section=1)

page('s2','Geometría y brazos de palanca',[
 Sketch('section',140),Spacer(1,9),
 p('El riel principal se idealiza como un tubo cerrado de 6061-T6 de 50 × 25 × 2,5 mm. Los radios se incluyen en área e inercias. H = 500 mm es su longitud y Sep = 200 mm es la distancia entre centros de rieles.'),
 h('Excentricidad y longitud de trabajo'),
 eq('ecc = 100 mm','Le = max(Linput,H-100*mm)','Le = max(400 mm,400 mm) = 400 mm'),
 p('<b>ecc</b> es la distancia desde el eje del riel a la línea de acción de la carga vertical. Multiplicar fuerza por esa distancia da el momento de flexión. No debe medirse desde la cara del tubo si la fórmula supone su eje.'),
 p('<b>Le</b> es la longitud del voladizo idealizado. max evita que quede demasiado corta si aumenta H, pero la expresión H - 100 mm no reemplaza la medición de los apoyos y la posición del anclaje.'),
 h('Objetivos de comparación'),
 eq('nReq = 2.2','deltaLim = 5 mm'),
 p('nReq es el margen provisional frente a fluencia. deltaLim es un límite de flecha elegido para comparar rigidez. Son decisiones de prediseño, pendientes de relacionar con funcionamiento, comodidad y exigencias aplicables.'),
 box('Modelo a escala real','Los cálculos corresponden a la geometría 1:1. Una maqueta reducida para imprimir muestra la arquitectura; no reproduce automáticamente las cargas, deformaciones ni resistencia del equipo real.'),
],section=2)

page('s3','Materiales y factores provisionales',[
 table([
 ['Entrada','Valor','Uso'],
 ['SyR','240 MPa','6061-T6: rieles y anclajes.'],
 ['SyS','130 MPa','5052-H32: piezas de chapa.'],
 ['SyB','450 MPa','Tornillos A2-70: referencia de fluencia al 0,2 %.'],
 ['Emod / nu','69.000 MPa / 0,33','Módulo elástico y coeficiente de Poisson del aluminio.'],
 ['rho','2.700 kg/m³','Estimación de masa de rieles.'],
 ['Kt / Kslot / Kb','2 / 1,5 / 1,2','Amplificaciones provisionales del cálculo.'],
 ],[92,104,CW-196]),
 h('Resistencia, rigidez y masa son propiedades diferentes'),
 p('Sy controla la comparación frente a fluencia; Emod controla la deformación elástica; nu describe la contracción transversal; rho transforma volumen en masa. Al elegir un material más resistente no se obtiene necesariamente un aumento proporcional de rigidez.'),
 h('Por qué 130 MPa para la chapa'),
 p('Las fichas de Atlas distinguen propiedades por especificación y espesor: para 5052-H32 aparecen mínimos diferentes en ASTM B209M y EN 485-2. La memoria usa 130 MPa como referencia conservadora de prediseño; debe sustituirse por el valor del producto certificado que se compre. [4,5]'),
 p('El valor de 6061-T6 depende también del producto, temple y condición. Si se suelda una zona, no debe mantenerse sin revisión la resistencia del material base T6. [3]'),
 h('Qué representan los multiplicadores'),
 p('Kt se aplica a la combinación del riel; Kslot al puente de la cinta; Kb a la resultante del tornillo. No se han obtenido de tablas específicas de entalla, ensayos o un modelo local. El Kt de esta hoja no es un Kf de fatiga.'),
 p('Las áreas resistentes de rosca y propiedades A2-70 deben coincidir con tornillos reales e identificados. “A2-70” no significa Sy = 700 MPa: ese 700 corresponde a resistencia mínima a tracción, mientras aquí se usa SyB = 450 MPa. [6]'),
],section=3)

page('s4','Sección redondeada: Ar, Ir y Jc',[
 h('1. Área del rectángulo redondeado'),
 p('A un rectángulo B × D se le quitan cuatro cuadrados de lado R y se restituyen cuatro cuartos de círculo. Por eso:'),
 eq('Ar(B,D,R) = B*D - (4-pi)*R^2','Area = Ar(b,d,ro) - Ar(b-2*t,d-2*t,ri)'),
 p(f'La resta del hueco da <b>Area = {val("Area",1e6)} mm²</b>. Ar calcula una figura maciza; Area corresponde al metal del tubo. Los argumentos deben describir una figura posible: radios positivos y menores o iguales a la mitad del lado menor.'),
 h('2. Momento de área de una esquina que se retira'),
 p('Para el eje paralelo a B, el cuadrado de esquina parte a una distancia c = D/2 - R del centro. En esa esquina, v mide desde el inicio del cuadrado hacia el borde. Se integra (c + v)² sobre el material que se elimina.'),
 eq('c0 = 1-pi/4;  c1 = 1/3-pi/16','Jc(c,r) = c0*c^2*r^2 + c*r^3/3 + c1*r^4'),
 p('El desarrollo usa: área retirada = c0·r²; integral de v = r³/6; integral de v² = c1·r⁴. Al expandir (c + v)² aparece el término 2c·r³/6 = c·r³/3.'),
 h('3. Rectángulo menos cuatro esquinas y menos el hueco'),
 eq('Ir(B,D,R) = B*D^3/12 - 4*Jc(D/2-R,R)','Ix = Ir(b,d,ro) - Ir(b-2*t,d-2*t,ri)','Iz = Ir(d,b,ro) - Ir(d-2*t,b-2*t,ri)'),
 p(f'Ix = <b>{val("Ix",1e12)} mm<super>4</super></b>; Iz = <b>{val("Iz",1e12)} mm<super>4</super></b>. Cambiar B y D intercambia el eje de flexión.'),
 box('Nombre y unidades','Jc es una función auxiliar de segundo momento de área: tiene unidades de longitud⁴. No es la constante torsional de Saint-Venant. B, D, R, c y r son argumentos locales, no datos que falte medir.'),
],section=4)

page('s5','Riel: esfuerzo axial y flexión',[
 h('De segundo momento a módulo resistente'),
 eq('Zx = Ix/(d/2);  Zz = Iz/(b/2)','Nr = eta*Fv;  Me = eta*Fv*ecc','SigAx = Nr/Area;  SigEc = Me/Zx'),
 p('La tensión axial media se obtiene de N/A. En flexión elástica, σ = M·y/I; en la fibra más alejada y = c, de modo que σ = M/(I/c) = M/Z. Z tiene unidades de mm³ y M/Z queda en N/mm².'),
 p(f'Con los datos iniciales: Nr = {val("Nr",1,3)} N; Me = {val("Me",1000)} N·mm; SigAx = {val("SigAx",1e-6)} MPa; SigEc = {val("SigEc",1e-6)} MPa.'),
 h('Por qué la carga horizontal usa una raíz'),
 eq('SigH = eta*Fh*Le*sqrt(1/Zx^2 + 1/Zz^2)','SigN = SigAx + SigEc + SigH'),
 p('Se permite que la fuerza horizontal de módulo Fh tenga componentes sobre dos direcciones perpendiculares. La tensión de flexión se expresa como a·Fx + b·Fz, con a = eta·Le/Zx y b = eta·Le/Zz.'),
 p('Al imponer Fx² + Fz² = Fh², el máximo de esa suma es Fh·sqrt(a² + b²), por la desigualdad de Cauchy-Schwarz. Así se obtiene la expresión usada, sin aplicar Fh completa en ambas direcciones a la vez.'),
 p(f'SigH = {val("SigH",1e-6)} MPa y SigN = <b>{val("SigN",1e-6)} MPa</b>. La suma toma signos que agravan la fibra crítica dentro del modelo de voladizo.'),
 h('Masa de los dos rieles'),
 eq('MassR = 2*H*Area*rho'),
 p(f'Resulta {val("MassR",1,3)} kg. Es una estimación de los tubos sin descontar perforaciones; no es la masa total del conjunto.'),
 p('Cambiar apoyos, orientación del tubo, uniones o dirección de la carga exige revisar la idealización. Esta combinación no resuelve la distribución completa de esfuerzos dentro del ensamblaje.','small')
],section=5)

page('s6','Riel: torsión, Von Mises y flecha',[
 h('Torsión en un tubo cerrado'),
 eq('Am = (b-t)*(d-t) - (4-pi)*(1.5*t)^2','Tr = eta*Fh*Sep/2;  TauT = Tr/(2*Am*t)'),
 p('Am encierra la línea media de la pared; no es Area. Para una celda delgada cerrada, el equilibrio de torsión da un flujo cortante aproximadamente constante T/(2Am); al dividir por t se obtiene TauT. La aproximación requiere pared continua y espesor uniforme.'),
 h('Envolvente de cortante y fluencia'),
 eq('TauV = eta*sqrt(Fv^2+Fh^2)/Area','SigVM = Kt*sqrt(SigN^2+3*(TauT+TauV)^2)','nR = SyR/SigVM'),
 p('TauV conserva la envolvente del prediseño: incluye Fv aunque el riel ya la recibe axialmente. V/A es cortante medio; no localiza sus máximos. Sumarlo a TauT y a la tensión normal no reconstruye un estado tensional real en un punto. Se necesita revisar el flujo cortante y las zonas perforadas.'),
 p(f'TauT = {val("TauT",1e-6)} MPa; TauV = {val("TauV",1e-6)} MPa; SigVM = <b>{val("SigVM",1e-6)} MPa</b>; nR = <b>{val("nR")}</b>. El resultado supera 2,2 por aproximadamente 2,4 %; es un margen cercano al objetivo.'),
 h('De curvatura a desplazamiento'),
 eq('deltaH = eta*Fh*Le^3/(3*Emod*min(Ix,Iz))','deltaE = Me*Le^2/(2*Emod*Ix)','deltaR = deltaH + deltaE'),
 p('Al integrar E·I·v″ = M(x) con desplazamiento y giro nulos en el empotramiento, una fuerza en el extremo da F·L³/(3EI) y un momento extremo da M·L²/(2EI). La hoja suma ambas contribuciones como aproximación. [7]'),
 p(f'deltaH = {val("deltaH",1000,3)} mm; deltaE = {val("deltaE",1000,3)} mm; deltaR = <b>{val("deltaR",1000,3)} mm</b> frente a 5 mm. La flexibilidad del arnés y de las uniones todavía no está incluida.'),
],section=6)

page('s7','Estabilidad: pandeo global y local',[
 h('Pandeo global del riel idealizado'),
 eq('Pcr = pi^2*Emod*min(Ix,Iz)/(Kcol*Le)^2','Kcol = 2;  nEuler = Pcr/Nr'),
 p('Euler describe la pérdida de estabilidad de una columna elástica ideal comprimida. Se usa el eje más débil y Kcol = 2, correspondiente a un extremo empotrado y otro libre. Esa condición es una hipótesis del modelo, no una propiedad del tubo. [8]'),
 p(f'Pcr = {val("Pcr",1)} N y nEuler = {val("nEuler")}. El cociente grande no representa seguridad global: una unión, una entalla, la fluencia o un modo no estudiado pueden limitar antes.'),
 h('Pandeo de una pared del tubo'),
 eq('bp = max(b,d)-4*t = 40 mm','SigCr = kplate*pi^2*Emod/(12*(1-nu^2))*(t/bp)^2','kplate = 4;  SigCap = min(SyR,SigCr)'),
 p('La pared se aproxima como una placa larga apoyada en sus bordes y comprimida. El coeficiente 4 corresponde a ese caso ideal; cambia con los apoyos, la proporción de lados y la distribución de tensión. bp es una anchura plana aproximada. [9]'),
 p(f'El valor elástico calculado SigCr = {val("SigCr",1e-6)} MPa supera SyR = 240 MPa. Por eso SigCap = 240 MPa: el cálculo elástico de placa no permite atribuir resistencia superior a la fluencia adoptada.'),
 h('Qué revisar antes de aceptar este cálculo'),
 bullet('Esbeltez, imperfecciones iniciales, longitud y rigidez real de los apoyos.'),
 bullet('Agujeros, casquillos, discontinuidades y compresión con flexión.'),
 bullet('Pandeo flexotorsional, deformación local de la unión y comportamiento inelástico.'),
 box('Cómo leer min y max','max elige la cara más ancha para estimar bp; min selecciona el menor momento de área y la menor tensión límite. Cada elección responde a un mecanismo físico distinto.'),
],section=7)

page('s8','M8: equilibrio del grupo de tornillos',[
 Sketch('bolts',145),Spacer(1,9),
 h('Carga directa y carga producida por el momento'),
 eq('Vy = eta*Fv;  Vz = eta*Fh','MomC = eta*(Fv*ecc + Fh*armH)','R8 = Kb*sqrt((Vy/2)^2+(Vz/2+MomC/pitch)^2)'),
 p('Dos tornillos separados pitch = 45 mm comparten las fuerzas directas. El momento se equilibra mediante un par: si cada fuerza del par vale Q, entonces Q·pitch = MomC y Q = MomC/pitch.'),
 p('En el tornillo crítico, la componente horizontal directa y la del par actúan en el mismo sentido. Se suman antes de aplicar Pitágoras con la componente vertical. En el tornillo opuesto cambia el signo del par.'),
 p(f'Vy/2 = {fmt(V["Vy"]/2)} N; Vz/2 = {fmt(V["Vz"]/2)} N; MomC/pitch = {fmt(V["MomC"]/V["pitch"])} N. Con Kb = 1,2, <b>R8 = {val("R8")} N</b>.'),
 h('Por qué R8old aparece en la hoja'),
 p(f'R8old = {val("R8old")} N conservaba la resultante directa y el par como si fueran ortogonales entre sí. Se muestra para documentar la corrección, pero la revisión de resistencia utiliza R8.'),
 p('Esta es una idealización en el plano YZ con tornillos de igual rigidez. El diseño completo de una unión también exige estudiar cargas fuera del plano, apertura y fuerzas combinadas; el manual NASA se usa como referencia general. [10]'),
],section=8)

page('s9','M8 y chapa: tres modos diferentes',[
 h('1. Cortante del tornillo'),
 eq('tau8 = R8/As8;  VM8 = sqrt(3)*R8/As8','nBolt8 = SyB/VM8'),
 p(f'As8 = 36,6 mm² representa la sección resistente de rosca usada en la idealización. Es menor que el círculo nominal de diámetro 8 mm. Resultan VM8 = {val("VM8",1e-6)} MPa y nBolt8 = <b>{val("nBolt8")}</b>. Se supone un plano de corte.'),
 h('2. Aplastamiento de la pared y la cartela'),
 eq('BearR = R8/(dia8*t);  nBearR = SyR/BearR','BearG = R8/(dia8*tg); nBearG = SyS/BearG'),
 p('Se divide la fuerza por el área proyectada diámetro × espesor. Es una tensión media de contacto; comparar con Sy es una comprobación de prediseño, no un valor normalizado de resistencia última al aplastamiento. Se acredita una sola pared del tubo.'),
 p(f'En el tubo: {val("BearR",1e-6)} MPa y nBearR = <b>{val("nBearR")}</b>. En la cartela de 4 mm: {val("BearG",1e-6)} MPa y nBearG = <b>{val("nBearG")}</b>.'),
 h('3. Arrancamiento hacia un borde'),
 eq('edge = min(15*mm,d/2) = 12.5 mm','Aarr = 2*(edge-hole8/2)*tg','TearG = sqrt(3)*R8/Aarr;  nTearG = SyS/TearG'),
 p(f'Con hole8 = 8,6 mm queda un ligamento de {fmt((V["edge"]-V["hole8"]/2)*1000)} mm por plano. Se suponen dos planos de corte. La tensión equivalente es {val("TearG",1e-6)} MPa y nTearG = <b>{val("nTearG")}</b>.'),
 box('La geometría debe corresponder al modo','edge debe ser la distancia real desde el centro del agujero al borde que puede arrancarse, en la dirección de la fuerza. Si hay recortes, fuerzas oblicuas o cambia la cartela, esta expresión debe revisarse.'),
],section=9)

page('s10','Cartela: flexión de la raíz y unión real',[
 h('De una sección rectangular al esfuerzo de raíz'),
 eq('Vcart = sqrt(Vy^2 + Vz^2)','Zraiz = tg*hRoot^2/6','SigRoot = MomC/Zraiz = 6*MomC/(tg*hRoot^2)','TauRoot = Vcart/(tg*hRoot)'),
 p('Se representa la raíz mediante una sección rectangular de espesor tg = 4 mm y altura hRoot = 80 mm. Su módulo resistente es espesor × altura²/6. La orientación del momento debe corresponder a ese eje de flexión.'),
 eq('VMroot = 2*sqrt(SigRoot^2+3*TauRoot^2)','nRoot = SyS/VMroot'),
 p(f'SigRoot = {val("SigRoot",1e-6)} MPa; TauRoot = {val("TauRoot",1e-6)} MPa. Con el multiplicador local 2 se obtiene VMroot = {val("VMroot",1e-6)} MPa y <b>nRoot = {val("nRoot")}</b>.'),
 h('Lo que todavía no describe esta sección'),
 p('El pliegue, el recorte de aligeramiento y la conexión tridimensional con el riel pueden concentrar deformación y cambiar el ancho efectivo. El multiplicador 2 no sustituye un modelo de esas zonas ni una medición.'),
 h('Por qué la unión necesita más cálculos'),
 p('Además del cortante externo, faltan precarga, tracción por palanca, separación, aflojamiento y presión bajo cabeza o arandela. El casquillo debe limitar la compresión del tubo y mantener un contacto adecuado; su longitud y tolerancia forman parte del diseño. [10]'),
 box('Diferencia entre piezas de CAD y piezas fabricables','Los tornillos y herrajes representados son referencias geométricas. La cartela necesita definición de radios, pliegues, tolerancias y procedimiento antes de convertirse en un plano de fabricación.'),
 p('No se atribuye resistencia a fricción por apriete en los cálculos mostrados. Sin una precarga especificada y controlada, ese aporte no puede suponerse disponible.','small')
],section=10)

page('s11','Piso de cuna: cargas y franjas de cálculo',[
 Sketch('floor',145),Spacer(1,9),
 p('El piso mide Width = 300 mm, Depth = 125 mm y tf = 2,5 mm. Las líneas de apoyo se toman sobre los ejes de los refuerzos: spanF = 65 mm; el voladizo delantero tiene over = 40 mm.'),
 h('Presión y carga localizada adoptadas'),
 eq('qfloor = 2*Fv/(Width*Depth) = 0.03924 N/mm^2','Ppatch = 100 N;  strip = 50 mm'),
 p('El factor 2 duplica la presión media basada en Fv para explorar una concentración local. Sumado al parche, no describe el equilibrio global del mismo caso: qfloor·Width·Depth + Ppatch = 1.571,5 N, mientras Fv = 735,75 N. Es una envolvente local elegida y pendiente de justificar con el contacto real.'),
 h('Dos posiciones alternativas del parche'),
 eq('Mspan = qfloor*spanF^2/8 + Ppatch*spanF/(4*strip)','Medge = qfloor*over^2/2 + Ppatch*over/strip'),
 p('Entre apoyos, una viga simple tiene M = w·L²/8 para carga uniforme y P·L/4 para un punto central. En el voladizo, el momento en el apoyo es w·a²/2 + P·a. Se aplica cada expresión por unidad de ancho y el parche se reparte sobre 50 mm.'),
 p('Las dos posiciones son casos alternativos; no son dos parches simultáneos. Los resultados son momentos por ancho: Mspan = 53,22 N y Medge = 111,39 N. La placa real distribuye carga en dos direcciones y el contacto con los tubos tiene ancho finito.'),
],section=11)

page('s12','Piso: desarrollo de tensión y espesor',[
 h('De momento por ancho a tensión de flexión'),
 p('Para una franja de ancho u, I = u·tf³/12 y c = tf/2. El módulo resistente resulta Z = u·tf²/6. Si Mfloor es el momento por ancho, el momento de esa franja es Mfloor·u. Al dividir ambos, u se cancela:'),
 eq('sigma = (Mfloor*u)/(u*tf^2/6) = 6*Mfloor/tf^2','Mfloor = max(Mspan,Medge) = 111.392 N','SigFloor = 6*111.392/2.5^2 = 106.93632 MPa','nFloor = 130/106.93632 = 1.21568'),
 box('Resultado actual','El margen calculado de 1,22 es inferior al objetivo nReq = 2,2. Este caso exige revisar el piso o sus apoyos. No predice por sí solo una rotura inmediata.','risk'),
 h('Despeje del espesor orientativo'),
 p('Se exige SyS / (6Mfloor/tf²) ≥ nReq. Como las cantidades son positivas, se despeja tf² ≥ 6Mfloor·nReq/SyS.'),
 eq('tNeed = sqrt(6*Mfloor*nReq/SyS) = 3.36312 mm','tfProp = 3.5 mm','SigProp = 54.55935 MPa;  nProp = 2.38273'),
 p('El resultado orienta una comparación. No incluye tolerancia negativa del espesor, flexión bidireccional, agujeros, contacto local, fatiga ni todos los efectos del pliegue. También puede reducirse over o acercarse un apoyo al borde.'),
 h('Por qué cambió frente al cálculo preliminar'),
 p('La revisión usa ejes de refuerzos como apoyos y coloca el parche en el extremo del voladizo al revisar el borde. El valor anterior de aproximadamente 38,55 MPa no cubría este escenario.'),
 p('<b>Estado del CAD:</b> conserva el piso de 2,5 mm. tfProp = 3,5 mm solo cambia la comparación de la hoja; no actualiza automáticamente Inventor.'),
],section=12)

page('s13','Refuerzo inferior y anclaje de hombro',[
 h('Refuerzo inferior: viga de tubo cuadrado'),
 eq('Irib = Ir(br,br,2*tr)-Ir(br-2*tr,br-2*tr,tr)','Zrib = Irib/(br/2);  Lrib = Sep+b','SigRib = eta*Fv*Lrib/(4*Zrib)','nRib = SyR/SigRib'),
 p('br = 20 mm y tr = 1,5 mm describen el refuerzo tubular con esquinas redondeadas. Lrib = 250 mm es la luz idealizada. Se asigna a un refuerzo una fuerza puntual equivalente eta·Fv y se aplica Mmax = P·L/4 de una viga simplemente apoyada.'),
 p(f'Irib = {val("Irib",1e12)} mm<super>4</super>; Zrib = {val("Zrib",1e9)} mm³. SigRib = {val("SigRib",1e-6)} MPa y <b>nRib = {val("nRib")}</b>. Esta revisión no resuelve la unión en sus extremos.'),
 h('Puente que sostiene la cinta del hombro'),
 eq('Mpuente = eta*Fv*slot/4','Zpuente = bridgeS*ta^2/6','SigSlot = Kslot*Mpuente/Zpuente','nSlot = SyR/SigSlot'),
 p('El material que queda junto a la ranura se idealiza como una viga apoyada. slot = 52 mm es su luz; bridgeS = 24 mm es el ancho del ligamento; ta = 5 mm es el espesor. La carga se toma fuera del plano de la chapa, por eso el espesor aparece al cuadrado en Z.'),
 p(f'Con Kslot = 1,5, SigSlot = {val("SigSlot",1e-6)} MPa y <b>nSlot = {val("nSlot")}</b>.'),
 box('El metal no es todo el anclaje','El cálculo no verifica cinta, costuras, hebilla, desgaste ni corte de fibras en el borde. El radio y acabado de la ranura, la orientación de la cinta y su trayectoria de carga necesitan revisión propia.'),
],section=13)

page('s14','Yugo de cinturón y diagonales',[
 h('Puente de ranura y flexión del yugo'),
 eq('SigBelt = Kslot*6*(eta*Fv*slot/4)/(bridgeB*tb^2)','Zbelt = 100*mm*tb^2/6','SigYoke = 2*eta*Fv*40*mm/Zbelt'),
 p(f'El puente usa bridgeB = 26 mm y tb = 5 mm: nBelt = {val("nBelt")}. La raíz del yugo se aproxima como una sección de 100 × 5 mm con brazo local de 40 mm y multiplicador 2: nYoke = {val("nYoke")}. Ese brazo no representa el equilibrio completo de la cadera o del arnés.'),
 Sketch('diagonal',145),Spacer(1,9),
 h('Fuerza axial en la diagonal activa'),
 eq('riseX = H-30*mm-(120*mm+30*mm) = 320 mm','LenX = sqrt(Sep^2+riseX^2)','ForceX = Fh*LenX/Sep','NetX = 2*mm*(24*mm-6.6*mm); nX = SyS/(ForceX/NetX)'),
 p('La proyección horizontal de la tracción debe equilibrar Fh: ForceX·Sep/LenX = Fh. El área neta descuenta un agujero de 6,6 mm de una pletina de 24 × 2 mm.'),
 p(f'LenX = {val("LenX",1000)} mm; ForceX = {val("ForceX")} N; NetX = 34,8 mm²; <b>nX = {val("nX")}</b>. Se acredita una diagonal a tracción; la opuesta puede pandear.'),
 p('Los 120 mm y los 40 mm están escritos como constantes en la hoja. Si cambia la altura de la cuna o el yugo, deben revisarse explícitamente: no se ajustan todos los brazos solo cambiando H.','small')
],section=14)

page('s15','M6 y alcance de los criterios de falla',[
 h('Comprobación simple de cortante M6'),
 eq('R6 = Kb*eta*Fv/2 = 309.015 N','VM6 = sqrt(3)*R6/As6','nM6 = SyB/VM6'),
 p(f'Con As6 = 20,1 mm² y SyB = 450 MPa, VM6 = {val("VM6",1e-6)} MPa y nM6 = <b>{val("nM6")}</b>. Es una revisión del tornillo frente a la fuerza externa adoptada; no verifica por sí sola las piezas que conecta.'),
 h('Qué reúne MinYield'),
 p('La función min selecciona el menor de los márgenes de fluencia, aplastamiento, arrancamiento y flexión listados. Con las entradas iniciales, coincide con nFloor = 1,22.'),
 eq('MinYield = min(nR,nBolt8,nBearR,nBearG,...,nM6)'),
 box('Interpretación de ese mínimo','MinYield identifica el resultado más bajo entre los modelos incluidos. No es un factor de seguridad global: deja fuera mecanismos, estados de carga y componentes todavía no calculados.'),
 table([
 ['Fenómeno','Estado de esta memoria'],
 ['Fluencia y deformación','Calculadas para escenarios simplificados.'],
 ['Pandeo','Estimaciones ideales del riel; faltan modos y uniones.'],
 ['Fatiga y fractura','Sin vida calculada ni evaluación de grietas. Ver pág. 23.'],
 ['Unión completa','Faltan precarga, tracción, apertura y aflojamiento.'],
 ['Textiles y entorno','Sin verificación de costuras, ergonomía, temperatura o compatibilidad con uso cerca del fuego.'],
 ],[128,CW-128]),
 p('Un equipo puede fallar por exceso de deformación o pérdida de fijación aunque el metal no llegue a fluencia. Por eso el criterio de resistencia debe acompañarse de una revisión funcional de todo el sistema.'),
],section=15)

summaryrows=[['Modo / variable','Resultado','Frente a objetivo 2,2']]
for name,labeltext in [
('nR','Riel: nR'),('nBolt8','M8: nBolt8'),('nBearR','Pared de tubo: nBearR'),('nBearG','Cartela: nBearG'),('nTearG','Arrancamiento: nTearG'),('nRoot','Raíz de cartela: nRoot'),('nFloor','Piso actual: nFloor'),('nRib','Refuerzo: nRib'),('nSlot','Hombro: nSlot'),('nBelt','Puente cinturón: nBelt'),('nYoke','Raíz yugo: nYoke'),('nX','Diagonal: nX'),('nM6','M6: nM6')]:
    summaryrows.append([labeltext,val(name),'Inferior' if V[name]<V['nReq'] else 'Superior en este modelo'])
page('s16','Resumen: cómo interpretar los resultados',[
 table(summaryrows,[221,71,CW-292]),
 p(f'<b>Flecha del riel:</b> deltaR = {val("deltaR",1000,3)} mm frente a deltaLim = 5 mm. La comparación de rigidez se mantiene separada de los márgenes de fluencia.'),
 h('Prioridad que resulta de los cálculos'),
 p('1. Revisar el piso y el apoyo delantero. 2. Confirmar la geometría local de cartelas y anclajes. 3. Contrastar el riel, cuyo margen está cerca del objetivo. 4. Completar unión, arnés y cargas reales antes de aceptar el conjunto.'),
 p('La alternativa de piso de 3,5 mm da nProp = 2,38 para el mismo caso. Si se aplica, MinYield no pasa automáticamente a ese valor: la hoja conserva nFloor del piso actual dentro de su lista y los demás modos deben compararse otra vez.'),
 p('“Superior” significa que supera el objetivo en el cálculo parcial indicado. No incorpora verificación de los fenómenos pendientes ni aceptación para uso.','small')
],section=16)

page('s17','Estado del modelo y cómo actualizarlo',[
 h('Qué datos provienen del CAD'),
 p('La referencia geométrica P2.02 registra 54 diseños de piezas y 70 ocurrencias en el ensamblaje. La masa representada es aproximadamente 3,206 kg, sin arnés completo. Estos números son registros de una generación del CAD, no variables enlazadas al cálculo.'),
 p('La ausencia de interferencias volumétricas en esa revisión comprueba compatibilidad geométrica de los sólidos representados. No demuestra resistencia, accesibilidad para montar, comodidad ni tolerancias correctas.'),
 h('Qué falta medir de la bomba real'),
 table([
 ['Dato por obtener','Efecto en la memoria'],
 ['Masa llena y componentes soportados','Mass y fuerzas de cálculo.'],
 ['Bolsa llena: forma y centro de carga','ecc, ancho, profundidad y contacto del piso.'],
 ['Alturas y puntos del arnés','Le, reacciones y transmisión de momentos.'],
 ['Conexión inferior y manguera','Recortes, espacio y protección de contacto.'],
 ['Tubos, chapas y tornillos comprados','t, radios, Sy, áreas y holguras reales.'],
 ],[220,CW-220]),
 h('Secuencia práctica de actualización'),
 bullet('Guardar una copia de trabajo de la hoja y registrar qué entrada cambió y por qué.'),
 bullet('Ajustar datos medidos y revisar también los brazos escritos como constantes.'),
 bullet('Recalcular toda la hoja; comprobar unidades, márgenes y deformaciones.'),
 bullet('Aplicar los cambios correspondientes al CAD y comparar las dimensiones entre ambos.'),
 bullet('Preparar después la revisión local de uniones y las pruebas de banco del prototipo.'),
 box('Enlace manual entre documentos','Editar Mathcad no regenera Inventor, los STL ni los archivos de parámetros del CAD. El PDF de esta guía tampoco se actualiza por sí solo.'),
],section=17)

page('fatiga','Ampliación: fatiga y fractura',[
 h('Fatiga: por qué Sy no basta'),
 p('Las cargas al caminar pueden fluctuar. La fatiga depende de la historia de tensiones y del detalle local; alcanzar un margen estático no determina la vida en ciclos. Para describir un ciclo se distinguen tensión media y amplitud alternante. [11]'),
 eq('sigma_m = (sigma_max + sigma_min)/2','sigma_a = (sigma_max - sigma_min)/2'),
 p('Aún faltan el espectro de carga, los ciclos esperados y datos del detalle fabricado. Una curva S-N relacionaría amplitud con ciclos a falla para condiciones específicas. No se ha asignado vida útil ni un límite de fatiga genérico al aluminio.'),
 h('Entallas y fabricación'),
 p('Agujeros, ranuras, acabado, radios, corrosión y uniones cambian la respuesta local. El Kt = 2 de la hoja es provisional y no puede reutilizarse como un factor de fatiga validado. Antes de añadir Goodman u otro diagrama, deben elegirse propiedades cíclicas y un método adecuados.'),
 h('Fractura: otra pregunta de diseño'),
 p('Si se considera una grieta, el análisis deja de depender solo de σ/Sy. Una aproximación lineal elástica de modo I utiliza un factor de intensidad de tensiones:'),
 eq('KI = Y*sigma*sqrt(pi*a)'),
 p('a describe el tamaño de grieta y Y depende de su forma y de la pieza. Se necesitarían tenacidad del producto, tamaño de defecto, geometría, espesor y límites de validez. KI se compara con el valor crítico apropiado bajo esas condiciones; no se han introducido esos datos en MC01. [12]'),
 box('Alcance de esta ampliación','Estas expresiones explican qué cálculos faltan y qué información requieren. No son resultados adicionales de la hoja ni una predicción de vida o de resistencia a grietas.'),
 p('Para uniones y textiles, la falla también puede ocurrir por desgaste, deslizamiento, apertura o pérdida de retención, sin una grieta metálica como mecanismo inicial.'),
])
sensrows=[['Espesor hipotético','Tensión del mismo caso','Margen frente a 130 MPa']]
for thick in (2.5,3.0,3.5,4.0):
    sigma=6*V['Mfloor']/thick**2
    sensrows.append([fmt(thick,1)+' mm',fmt(sigma)+' MPa',fmt(130/sigma)])
page('sensibilidad','Ampliación: sensibilidad y siguientes decisiones',[
 h('Qué cambios tienen mayor efecto en el piso'),
 eq('SigFloor = 6*(qfloor*over^2/2 + Ppatch*over/strip)/tf^2'),
 p('Con cargas y apoyos fijos, la tensión varía con 1/tf². La parte de presión crece con over² y la del parche con over. Reducir el voladizo puede ser una alternativa eficiente frente a aumentar el espesor de toda la chapa.'),
 table(sensrows,[132,166,CW-298]),
 p('Esta tabla cambia solo tf y mantiene el resto del escenario. No representa cuatro diseños ya modelados o verificados.'),
 h('Espesor y masa añadida'),
 eq('Delta_m_piso = Width*Depth*(3.5-2.5)*mm*rho','Delta_m_piso = 0.10125 kg'),
 p('Aumentar una placa plana de 300 × 125 mm de 2,5 a 3,5 mm agregaría aproximadamente 101 g sin contar pliegues, recortes o cambios en otras piezas. La masa real debe obtenerse del CAD actualizado.'),
 h('Datos que se deben resolver primero'),
 bullet('Definir el apoyo efectivo y la huella de la bolsa llena para justificar qfloor, Ppatch y strip.'),
 bullet('Comparar acercar el refuerzo al borde con cambiar espesor; revisar espacio para manguera y montaje.'),
 bullet('Revisar tornillos, cartelas y arnés después de fijar la trayectoria de carga.'),
 bullet('Actualizar la estimación de masa: el modelo actual de aproximadamente 3,206 kg supera la meta preliminar de 1,5 a 2 kg.'),
 p('Ninguno de estos cambios se ha aplicado al CAD durante la preparación de esta guía.'),
])
page('diccionario','Diccionario rápido de símbolos y nombres',[
 table([
 ['En la hoja','Interpretación y unidad habitual'],
 ['Mass / grav / av / ah / eta','Masa [kg], gravedad [m/s²] y factores adimensionales.'],
 ['Fv / Fh; Nr','Fuerzas vertical y horizontal; axial de un riel [N].'],
 ['H / Le / Sep / ecc','Altura, longitud de trabajo, separación y excentricidad [mm].'],
 ['b / d / t; ro / ri','Ancho, profundidad, pared y radios del riel [mm].'],
 ['Ar / Ir / Jc','Funciones de área [mm²] y de segundo momento [mm⁴].'],
 ['Area / Am','Área metálica del tubo / área encerrada por su línea media [mm²].'],
 ['Ix / Iz; Zx / Zz','Segundos momentos [mm⁴]; módulos resistentes [mm³].'],
 ['SyR / SyS / SyB','Fluencia de perfil, chapa y tornillo [MPa].'],
 ['Emod / nu / rho','Módulo [MPa], Poisson [sin unidad] y densidad [kg/m³].'],
 ['Me / Tr / MomC','Momentos de flexión y torsión [N·mm].'],
 ['Sig... / Tau... / VM...','Tensiones normales, cortantes o equivalentes [MPa].'],
 ['nR / nFloor / n...','Márgenes de comprobaciones parciales [sin unidad].'],
 ['delta... / Pcr','Desplazamiento [mm] / carga crítica ideal [N].'],
 ['pitch / armH / edge','Separación M8, brazo horizontal y distancia a borde [mm].'],
 ['As8 / As6 / NetX','Áreas resistentes de rosca y de sección neta [mm²].'],
 ['qfloor / Ppatch / strip','Presión [N/mm²], carga localizada [N], ancho de reparto [mm].'],
 ['Mspan / Medge / Mfloor','Momento por unidad de ancho [N·mm/mm = N].'],
 ['tf / tNeed / tfProp','Espesor actual, espesor despejado y comparación [mm].'],
 ['slot / bridgeS / bridgeB','Luz de ranura y anchos de ligamentos [mm].'],
 ],[167,CW-167]),
 p('Mayúsculas, minúsculas y nombre completo identifican variables distintas. Las abreviaturas Sig y Tau ayudan a distinguir tensión normal y cortante; no son funciones especiales de Mathcad.','small'),
])
def link(title,url): return f'<link href="{escape(url)}" color="#007D86">{escape(title)}</link>'
page('fuentes1','Fuentes y trazabilidad / 1',[
 p('Los desarrollos numéricos se explican a partir de las ecuaciones y entradas de MC01. Las referencias siguientes permiten revisar conceptos, propiedades y limitaciones. Consulta de enlaces: 15/10/2026.','small'),
 h('[1] Ayuda de Mathcad clásico instalada'),
 p('Carpeta: Mathcad 15/doc/HELP_ES/Help. Temas: Defining_a_Function.html; Equal_sign_for_evaluation.html; Calculation_order.html; Automatic_Calculation_Mode.html; Units_and_Dimensions.html; Unit_Conversions.html. La ayuda local confirma operadores, orden de evaluación, unidades y recálculo.','small'),
 p(link('PTC: centro oficial de ayuda de Mathcad','https://www.ptc.com/en/support/help/mathcad'),'small'),
 h('[2] Fluencia de materiales dúctiles'),
 p(link('MIT OCW, 2.080J, Lecture 12: Fundamental Concepts in Structural Plasticity','https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/30dc1a0f74debf21fb92a1df56616929_MIT2_080JF13_Lecture12.pdf'),'small'),
 p('Apartados de Von Mises y Tresca. Se usan para explicar el criterio, sin atribuir a esa referencia los factores provisionales ni las geometrías de SEDAC.','small'),
 h('[3] Aluminio de perfil 6061'),
 p(link('Hydro: Alloy 6061, ficha de extrusión','https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf'),'small'),
 p('Referencia para el temple T6 y la resistencia adoptada. Confirmar el producto y el certificado; revisar zonas afectadas por soldadura.','small'),
 h('[4-5] Aluminio de chapa 5052'),
 p(link('Atlas Steels: Aluminium Alloy 5052 Data Sheet','https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf'),'small'),
 p(link('Atlas Steels: Technical Note 14, 5052 and 5251','https://www.atlassteels.com.au/documents/TN14-5052%20and%205251%20rev%20June%202013.pdf'),'small'),
 p('Se distinguen producto, espesor y especificación. El valor 130 MPa es una entrada elegida para este prediseño.','small'),
 h('[6] Tornillos inoxidables'),
 p(link('Bossard: Stainless steel fasteners, propiedades según ISO 3506','https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf'),'small'),
 p('Referencia para A2-70. La representación de tornillos en CAD no identifica por sí misma las piezas comerciales que se utilizarán.','small'),
])
page('fuentes2','Fuentes y trazabilidad / 2',[
 h('[7] Flexión y flecha de vigas'),
 p(link('MIT OCW, 2.080J, Lecture 5: Solution Method for Beam Deflections','https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/3533c046dafcc488f1432e92d05ec210_MIT2_080JF13_Lecture5.pdf'),'small'),
 h('[8] Estabilidad global'),
 p(link('MIT OCW, 16.001: Buckling of Beams','https://ocw.mit.edu/courses/16-001-unified-engineering-materials-and-structures-fall-2021/mit16_001_f21_lec33lec34lec35.pdf'),'small'),
 h('[9] Estabilidad local'),
 p(link('MIT OCW, 2.080J, Lecture 11: Buckling of Plates and Sections','https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/345c462fe40421ea0f795bd35d2e4af1_MIT2_080JF13_Lecture11.pdf'),'small'),
 h('[10] Diseño de uniones atornilladas'),
 p(link('NASA RP-1228, Richard T. Barrett: Fastener Design Manual, 1990','https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf'),'small'),
 p('Referencia de criterios de unión, grupos de tornillos y cargas combinadas. No implica conformidad de SEDAC con requisitos aeroespaciales.','small'),
 h('[11] Fatiga'),
 p(link('MIT OCW, 2.002, Anand y Parks: Defect-Free Fatigue','https://ocw.mit.edu/courses/2-002-mechanics-and-materials-ii-spring-2004/db45866e2fc0cf164d96828936748e8f_lec21_notes.pdf'),'small'),
 h('[12] Fractura'),
 p(link('MIT, David Roylance: Introduction to Fracture Mechanics','https://web.mit.edu/course/3/3.11/www/modules/frac.pdf'),'small'),
 h('Documentos internos de referencia'),
 p('Hoja: Memoria_SEDAC_P2_02_MC01_EDITABLE.xmcd. Correcciones de método: REVISION_CALCULOS.md. Entradas y resultados iniciales: Soporte/REGIONES.json y VALORES_ESPERADOS_SI.json. Modelo CAD de referencia: Inventor_20261015_152625.','small'),
 p('Esta guía explica las aproximaciones existentes y los cálculos que faltan. Prepararla no cambia los parámetros de Mathcad, el CAD ni la selección final de material. Las mediciones, la revisión de detalles y las pruebas de banco deben alimentar una siguiente revisión documental.','small'),
])

assert len(PAGES)==27,len(PAGES)
# Medir todos los bloques antes de dibujar: cada capitulo ocupa una pagina.
audit=[]
for i,pg in enumerate(PAGES,1):
    title=p(pg['title'],'title')
    tw,th=title.wrap(CW,1000)
    used=th+8
    for item in pg['items']:
        _,hh=item.wrap(CW,1000)
        used+=hh+getattr(item,'spaceBefore',0)+getattr(item,'spaceAfter',0)
    available=H-102-55
    audit.append(dict(page=i,key=pg['key'],section=pg['section'],used=round(used,2),available=round(available,2)))
    if used>available:
        raise ValueError(f'Pagina {i} ({pg["key"]}): requiere {used:.1f} pt, disponibles {available:.1f}')
    if pg['section']:
        assert i==pg['section']+5
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('SEDAC P2.02 MC01 - Guía explicada de la memoria de cálculo')
c.setAuthor('Proyecto SEDAC')
c.setSubject('Desarrollos de cálculo, criterios de falla y uso de Mathcad clásico')
for i,pg in enumerate(PAGES,1):
    c.bookmarkPage(pg['key']);c.addOutlineEntry((f'{pg["section"]}. ' if pg['section'] else '')+pg['title'],pg['key'],0,False)
    c.setStrokeColor(LINE);c.setLineWidth(.6);c.line(M,H-54,W-M,H-54)
    c.setFont('BodyBold',8.8);c.setFillColor(NAVY);c.drawString(M,H-40,'SEDAC  /  P2.02  /  GUÍA MC01')
    c.setFont('Body',8.5);c.setFillColor(TEAL)
    tag=f'MATHCAD · SECCIÓN {pg["section"]:02}' if pg['section'] else 'GUÍA DE LECTURA'
    c.drawRightString(W-M,H-40,tag)
    y=H-83
    title=p(pg['title'],'title');_,th=title.wrap(CW,1000);title.drawOn(c,M,y-th);y-=th+8
    for item in pg['items']:
        y-=getattr(item,'spaceBefore',0)
        _,hh=item.wrap(CW,1000);item.drawOn(c,M,y-hh)
        y-=hh+getattr(item,'spaceAfter',0)
    c.setStrokeColor(LINE);c.line(M,42,W-M,42)
    c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(M,28,'15/10/2026  ·  Prediseño sujeto a mediciones y revisión')
    c.drawRightString(W-M,28,f'{i} / {len(PAGES)}')
    c.showPage()
c.save()
reader=PdfReader(str(OUT))
assert len(reader.pages)==len(PAGES)
texts=[page.extract_text() or '' for page in reader.pages]
for i,pg in enumerate(PAGES):
    if pg['section']:
        assert f'SECCIÓN {pg["section"]:02}' in texts[i],(i,texts[i][:100])
assert all('\ufffd' not in s for s in texts)
assert sum(len(pg.get('/Annots',[])) for pg in reader.pages)>=12
(SUP/'AUDITORIA_GUIA_PDF.json').write_text(json.dumps(dict(output=str(OUT),pages=audit,characters=sum(map(len,texts)),cad_modified=False,worksheet_modified=False),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(file=str(OUT),pages=len(PAGES),bytes=OUT.stat().st_size,max_used_points=max(x['used'] for x in audit)),ensure_ascii=False))
