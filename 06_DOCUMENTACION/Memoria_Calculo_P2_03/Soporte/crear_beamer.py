from pathlib import Path
import json,re,collections
ROOT=Path(r'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD')
OUT=ROOT/'06_DOCUMENTACION/Memoria_Calculo_P2_03'
BASE=ROOT/'01_CAD/Prototipo_P2/P2_03_20261016'
V={x['name']:x['value'] for x in json.loads((OUT/'Soporte/VALORES_ESPERADOS_SI.json').read_text(encoding='utf-8-sig'))}
R=json.loads((OUT/'Soporte/REGIONES.json').read_text(encoding='utf-8-sig'))
sections={}
for i,t in enumerate(R['pages'],1):sections.setdefault(int(t.split('.')[0]),[]).append(i)
def num(x,n=2):return f'{x:.{n}f}'.replace('.',r'{,}')
def token(m):
 a=m.group(1).split('|');return num(V[a[0]]/(float(a[1]) if len(a)>1 else 1),int(a[2]) if len(a)>2 else 2)
def subst(s):return re.sub(r'<<([^<>]+)>>',token,s)
frames=[]
def F(title,body,sec=None):
 ref='Guía de diseño'
 if sec:
  pp=sections[sec];ref=f'Mathcad: sección {sec} / pág. {pp[0]}'+(f'-{pp[-1]}' if len(pp)>1 else '')
 frames.append('\\gdef\\mcref{'+ref+'}\n\\begin{frame}[t]{'+title+'}\n'+subst(body)+'\n\\end{frame}\n')
preamble=r'''% !TeX program = pdflatex
% Documento independiente, generado a partir de los valores de la revisión MC02.
\documentclass[10pt,aspectratio=169]{beamer}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage{lmodern,amsmath,amssymb,booktabs,array,tikz}
\usetikzlibrary{arrows.meta,positioning}
\usefonttheme{professionalfonts}
\usefonttheme[onlymath]{serif}
\definecolor{azul}{HTML}{173345}
\definecolor{verde}{HTML}{007D86}
\definecolor{gris}{HTML}{576B79}
\definecolor{rojo}{HTML}{9D302C}
\setbeamercolor{normal text}{fg=azul,bg=white}
\setbeamercolor{structure}{fg=verde}
\setbeamercolor{frametitle}{fg=azul}
\setbeamercolor{alerted text}{fg=rojo}
\setbeamerfont{frametitle}{size=\Large,series=\bfseries}
\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=9mm,text margin right=9mm}
\setlength{\parskip}{4pt}
\newcommand{\mc}[1]{\texttt{\detokenize{#1}}}
\newcommand{\mm}{\,\mathrm{mm}}
\newcommand{\MPa}{\,\mathrm{MPa}}
\newcommand{\kg}{\,\mathrm{kg}}
\newcommand{\N}{\,\mathrm{N}}
\newcommand{\cita}[1]{\par\smallskip{\scriptsize\color{gris}#1}}
\newcommand{\mcref}{Guía de diseño}
\setbeamertemplate{footline}{\leavevmode\hbox{%
\begin{beamercolorbox}[wd=.32\paperwidth,ht=2.8ex,dp=1.25ex,leftskip=9mm]{normal text}\scriptsize\color{gris}SEDAC P2.03 / MC02\end{beamercolorbox}%
\begin{beamercolorbox}[wd=.51\paperwidth,ht=2.8ex,dp=1.25ex,center]{normal text}\scriptsize\color{verde}\mcref\end{beamercolorbox}%
\begin{beamercolorbox}[wd=.17\paperwidth,ht=2.8ex,dp=1.25ex,rightskip=9mm]{normal text}\hfill\scriptsize\color{gris}\insertframenumber/\inserttotalframenumber\end{beamercolorbox}}}
\title{Aligeramiento y uniones mecánicas}
\subtitle{SEDAC P2.03\\Memoria de cálculo explicada}
\author{Guía para leer junto a Mathcad MC02}
\date{16 de octubre de 2026}
\begin{document}
\spanishplainpercent
\begin{frame}
\titlepage
\vspace{-6mm}\begin{center}\small Prediseño a escala 1:1. Medidas de bomba y arnés pendientes.\end{center}
\end{frame}
'''
F('Qué cambia en esta revisión',r'''
\begin{itemize}
\item Rieles de aluminio: de $50\times25\times2{,}5$ a $50\times40\times1{,}5\mm$. Mayor profundidad para conservar rigidez con menos masa.
\item Anclajes de hombro y cintura con alma de $2\mm$ y retornos hasta $18\mm$; se aprovecha la forma de la sección.
\item Tres refuerzos bajo la cuna, cartelas con ala de $5\mm$ y protector HDPE hueco.
\item Se mantienen las diagonales. Se eliminan paneles rígidos posteriores y fijaciones secundarias.
\item Tornillos M5/M6 A2-80, arandelas, tuercas autofrenantes y apoyos interiores individualizados.
\end{itemize}
No se ha demostrado un óptimo global ni un diseño listo para uso sobre una persona.
''')
F('El peso incluye una reserva para la mochila',r'''
\begin{center}\begin{tabular}{lrr}\toprule
Concepto & P2.02 & P2.03\\\midrule
CAD sin espuma de referencia & $3{,}153\kg$ & $<<mCAD|1|3>>\kg$\\
Reserva de arnés, cintas, hebillas y acolchado & $0{,}500\kg$ & $0{,}500\kg$\\
Otros elementos aún no representados & $0{,}080\kg$ & $0{,}080\kg$\\\midrule
Comparación con iguales reservas & $3{,}733\kg$ & $<<mTotal|1|3>>\kg$\\\bottomrule
\end{tabular}\end{center}
\textbf{El objetivo de $2\kg$ todavía no se cumple.} Las reservas son estimaciones, no el peso de un arnés seleccionado.

La espuma visible en Inventor pertenece a los $0{,}50\kg$ de textiles. Se evita contarla dos veces. La masa CAD procede de volúmenes y densidades asignadas.
''',25)
F('Cómo seguir Mathcad y esta guía',r'''
\small
\begin{columns}[T,onlytextwidth]
\column{.49\textwidth}
\begin{tabular}{ll}\toprule Sección MC02 & Tema\\\midrule
1--3 & Cargas, geometría y material\\
4--8 & Sección y rieles\\
9--10 & Cartelas\\
11--12 & Piso y refuerzos\\
13--16 & Hombro y cinturón\\\bottomrule\end{tabular}
\column{.49\textwidth}
\begin{tabular}{ll}\toprule Sección MC02 & Tema\\\midrule
17 & Diagonales\\
18--23 & Uniones y tornillería\\
24 & Resumen de márgenes\\
25 & Masa completa\\
26--27 & Pendientes y uso\\\bottomrule\end{tabular}
\end{columns}
\medskip
El pie de cada diapositiva indica la sección y página lógica de la hoja. Algunas secciones ocupan varias páginas.

Abrir el archivo terminado en \mc{EDITABLE.xmcd}. Las entradas con fondo azul son hipótesis editables. Modificar Mathcad no modifica automáticamente el CAD.
''')
F('Operadores y unidades de Mathcad',r'''
\begin{tabular}{p{.23\textwidth}p{.68\textwidth}}\toprule
Símbolo & Qué hace\\\midrule
$\texttt{:=}$ & Define una variable o función. Debe aparecer antes de usarla.\\
$=$ & Evalúa y muestra el resultado de una expresión.\\
$\sqrt{x}$ y $|x|$ & Raíz positiva y valor absoluto. El valor absoluto es un operador nativo, no una variable llamada \mc{abs}.\\
$\min,\max$ & Eligen el menor o mayor argumento. Los argumentos deben tener las mismas dimensiones.\\
$\mathrm{mm,MPa,N}$ & Unidades; $1\,\mathrm{MPa}=1\,\mathrm{N/mm^2}$.\\\bottomrule
\end{tabular}
\medskip
Mathcad distingue mayúsculas y minúsculas. Se recalcula con \textbf{Ctrl+F9}. Un resultado con unidades incompatibles requiere revisar la fórmula, no eliminar sus unidades.
''',27)
F('Las funciones tienen argumentos locales',r'''
\[
A_r(B,D,R):=BD-(4-\pi)R^2
\]
$B,D,R$ representan los datos que recibe cada llamada. No necesitan valores globales. En la hoja, el argumento de profundidad se llama \mc{DD}.
\[
A=A_r(b,d,2t)-A_r(b-2t,d-2t,t)
\]
La primera llamada calcula el contorno exterior; la segunda, el hueco. Se obtienen resultados numéricos cuando se introducen $b,d,t$.

\mc{Jc} calcula una contribución al segundo momento de área. \textbf{No es una constante de torsión}. \mc{Ir} calcula el momento de área de un rectángulo redondeado.
''',4)
F('Qué significa un margen frente a falla',r'''
Para material dúctil bajo tensión normal $\sigma$ y cortante $\tau$:
\[
\sigma_{\mathrm{VM}}=\sqrt{\sigma^2+3\tau^2},\qquad
n_y=\frac{S_y}{\sigma_{\mathrm{VM}}}
\]
Se adopta Von Mises para aluminio y tornillos. Tresca usaría la máxima diferencia de tensiones principales; en cortante puro resulta más conservador.

Un margen de fluencia no comprueba por sí solo pandeo, rigidez, fatiga, rotura frágil, contacto ni aflojamiento.

\textbf{Criterio del prediseño:} márgenes modelados $n\ge2{,}2$, flecha del riel $\delta\le5\mm$ y compresión residual positiva en las uniones.
\cita{Base: MIT OCW, mecánica estructural; NASA RP-1228 para uniones.}
''',26)
F('Los 25 kg son el sistema completo',r'''
\[
F_v=mga_v=25(9{,}81)(3)=735{,}75\N
\]
\[
F_h=mga_h=25(9{,}81)(1)=245{,}25\N
\]
$m=25\kg$ incluye bomba, líquido, soporte, arnés y accesorios. No son $25\kg$ de bomba más una estructura adicional.

$a_v=3$ representa \textbf{3 g verticales totales}, incluida gravedad. Se asigna $\eta=0{,}70$ al lado más cargado; no se divide siempre la carga por dos.

Con el presupuesto de masa actual quedarían $<<mRestante|1|2>>\kg$ para la bomba, el líquido y los componentes no incluidos. Es una hipótesis de cálculo, no una carga autorizada de uso.
''',1)
F('Geometría que controla el momento',r'''
\begin{center}\begin{tabular}{ll}\toprule
Altura / separación de rieles & $500/200\mm$\\
Cuna: ancho / profundidad & $300/125\mm$\\
Riel: ancho / profundidad / pared & $50/40/1{,}5\mm$\\
Pared mínima propuesta de recepción & $1{,}4\mm$\\
Excentricidad $e$ & $107{,}5\mm$\\
Longitud equivalente $L$ & $423\mm$\\\bottomrule\end{tabular}\end{center}
El riel más profundo desplaza la carga: se aumenta $e$ desde $100\mm$. La cuna y el protector elevan la superficie de apoyo: se aumenta $L$ desde $400\mm$.

Los dos brazos siguen siendo supuestos. La forma de la bolsa llena y los puntos reales del arnés deben reemplazarlos.
''',2)
F('Materiales y factores utilizados',r'''
\begin{center}\begin{tabular}{lll}\toprule
Material & Valor adoptado & Uso\\\midrule
6061-T6 sin soldar & $S_y=240\MPa$ & Rieles, cartelas y anclajes\\
5052-H32 & $S_y=130\MPa$ & Piso y diagonales\\
Inoxidable A2-80 & $R_{p0,2}=600\MPa$ & Tornillos M5/M6\\
Aluminio & $E=69\,000\MPa,\ \nu=0{,}33$ & Rigidez / estabilidad\\\bottomrule\end{tabular}\end{center}
$K_t=2$, $K_b=1{,}2$ y $K_{\mathrm{ranura}}=1{,}5$ son factores provisionales de concentración o reparto, no resultados de FEA.

No sustituir A2-80 por A2-70 conservando estos resultados. El temple, espesor y grado de cada producto deben confirmarse con el proveedor.
\cita{Fuentes: Hydro 6061, Atlas 5052/TN14 y Bossard ISO 3506.}
''',3)
F('Ruta de carga del concepto',r'''
\begin{center}\begin{tikzpicture}[every node/.style={font=\small,align=center},box/.style={draw=verde,rounded corners,minimum width=26mm,minimum height=13mm}]
\node[box] (a) at (0,0) {Bomba\\y protector};
\node[box] (b) at (3.1,0) {Piso y\\3 refuerzos};
\node[box] (c) at (6.2,0) {Cartelas\\y rieles};
\node[box] (d) at (9.3,0) {Anclajes\\y arnés};
\draw[-{Stealth},thick] (a)--(b);\draw[-{Stealth},thick] (b)--(c);\draw[-{Stealth},thick] (c)--(d);
\node[draw=gris,rounded corners] at (6.2,-1.7) {Travesaños y X: estabilidad lateral};
\draw[-{Stealth},gris] (6.2,-1.35)--(c);
\end{tikzpicture}\end{center}
El reparto entre hombros y cintura depende de un arnés flexible aún no definido. El modelo de viga equivalente representa una envolvente de prediseño; no reproduce toda la interacción con el cuerpo.
''')
F('Sección redondeada: de dónde sale Jc',r'''
Se resta de cada esquina el área entre el cuadrado y el cuarto de círculo:
\[
c_0=1-\frac\pi4,\qquad c_1=\frac13-\frac\pi{16}
\]
\[
J_c(c,r)=c_0c^2r^2+\frac{cr^3}{3}+c_1r^4
\]
\[
A_r(B,D,R)=BD-(4-\pi)R^2
\]
\[
I_r(B,D,R)=\frac{BD^3}{12}-4J_c\left(\frac D2-R,R\right)
\]
$c=D/2-R$ localiza el centro del redondeo respecto del eje neutro. Todas las contribuciones de $I_r$ tienen dimensión de longitud a la cuarta.
''',4)
F('Propiedades del riel aligerado',r'''
\[
A=A_r(b,d,2t)-A_r(b-2t,d-2t,t)
\]
\[
I_x=I_r(b,d,2t)-I_r(b-2t,d-2t,t)
\]
$I_z$ se obtiene intercambiando $b$ y $d$; $Z_x=2I_x/d$ y $Z_z=2I_z/b$.
\begin{center}\begin{tabular}{rrrr}\toprule
$A\ (\mathrm{mm^2})$ & $I_x\ (\mathrm{mm^4})$ & $I_z\ (\mathrm{mm^4})$ & Masa de tubos sin taladrar\\\midrule
$<<Area|0.000001|2>>$ & $<<Ix|1e-12|0>>$ & $<<Iz|1e-12|0>>$ & $<<mRails|1|3>>\kg$\\\bottomrule\end{tabular}\end{center}
Se incluyen radios nominales exteriores $2t$ e interiores $t$. La masa final procede del CAD con taladros; el perfil comercial debe corresponder a esta geometría.
''',5)
F('Riel: axial y flexión biaxial',r'''
\[
N_r=\eta F_v,\qquad M_e=\eta F_ve
\]
\[
\sigma_a=\frac{N_r}{A},\qquad \sigma_e=\frac{M_e}{Z_x}
\]
\[
\sigma_h=\eta F_hL\sqrt{\frac1{Z_x^2}+\frac1{Z_z^2}}
\]
La expresión de $\sigma_h$ maximiza la combinación de flexión para una fuerza horizontal de dirección variable y módulo fijo.

Se suman magnitudes en la fibra desfavorable: $\sigma=\sigma_a+\sigma_e+\sigma_h$. Es una envolvente, no una solución completa de las reacciones del arnés.
''',6)
F('Riel: torsión de pared delgada',r'''
\[
A_m=(b-t)(d-t)-(4-\pi)(1{,}5t)^2
\]
\[
T_r=\frac{\eta F_hS}{2},\qquad
\tau_T=\frac{T_r}{2A_mt},\qquad
\tau_V=\frac{\eta\sqrt{F_v^2+F_h^2}}{A}
\]
La relación $T/(2A_mt)$ corresponde a un tubo cerrado de pared delgada. $A_m$ es el área encerrada por la línea media.

$V/A$ es un cortante \textbf{medio}. No describe máximos locales alrededor de taladros ni contacto. Su suma con la torsión se conserva como modelo de comparación y debe contrastarse con FEA del detalle.
''',6)
F('Riel: combinación, flecha y pared mínima',r'''
\[
\sigma_{VM}=K_t\sqrt{(\sigma_a+\sigma_e+\sigma_h)^2+3(\tau_T+\tau_V)^2}
\]
\[
\delta=\frac{\eta F_hL^3}{3E\min(I_x,I_z)}+\frac{M_eL^2}{2EI_x}
\]
\begin{center}\begin{tabular}{lll}\toprule
Riel nominal & $n_y=<<nRail>>$ & $\delta=<<deltaR|0.001|2>>\mm$\\
Pared mínima $1{,}4\mm$ & $n_y=<<nMinWall>>$ & Se recalcula toda la sección\\\bottomrule\end{tabular}\end{center}
$1{,}4\mm$ es un límite propuesto, no una tolerancia de proveedor ya asegurada. La condición de voladizo para la flecha es una idealización de apoyo.
''',8)
F('Pandeo: criterios diferentes de la fluencia',r'''
\[
P_{cr}=\frac{\pi^2E I_{\min}}{(2L)^2},\qquad n_E=\frac{P_{cr}}{N_r}
\]
Euler usa $K=2$ para un voladizo ideal. Debe comprobarse la condición real de apoyo.
\[
\sigma_{cr}=\frac{k\pi^2E}{12(1-\nu^2)}\left(\frac{t}{b_f}\right)^2,
\qquad b_f=\max(b,d)-4t
\]
Para pared apoyada en ambos bordes se utiliza $k=4$. Se limita la capacidad a $\min(S_y,\sigma_{cr})$.

Estas fórmulas no incorporan imperfecciones, abolladuras ni perforaciones. No se acredita una resistencia superior a la fluencia por obtener un valor elástico de pandeo elevado.
''',7)
F('Cartela: fuerza en el grupo de dos M6',r'''
\[
V_y=\eta F_v,\quad V_z=\eta F_h,\quad
M_C=\eta(F_ve+F_h\,75\mm)
\]
\[
R_p=K_b\sqrt{\left(\frac{V_y}{2}\right)^2+
\left(\frac{V_z}{2}+\frac{M_C}{80\mm}\right)^2}
=<<Rpin|1|1>>\N
\]
Los dos ejes están a $y=20$ y $100\mm$. Se combinan las componentes de cortante directo y las producidas por el momento.

Cada M6 atraviesa un pasador hueco de aluminio: exterior $10\mm$, interior $6{,}6\mm$, longitud $53\mm$. El diámetro exterior aumenta el área de apoyo en la pared del riel. No se acredita fricción.
''',9)
F('Cartela: aplastamiento y arrancamiento',r'''
\[
p_b=\frac{R_p}{d_p t},\qquad n_b=\frac{S_y}{p_b}
\]
\[
A_{arr}=2\left(e_b-\frac{d_h}{2}\right)t_g,
\qquad n_{arr}=\frac{S_y}{\sqrt3\,R_p/A_{arr}}
\]
\begin{center}\begin{tabular}{lll}\toprule
Pared del riel & $d_p=10,\ t=1{,}4\mm$ & $n=<<nBearR>>$\\
Alma de cartela & $d_p=10,\ t_g=3\mm$ & $n=<<nBearG>>$\\
Arrancamiento cartela & $e_b=15,\ d_h=10{,}2\mm$ & $n=<<nTearG>>$\\\bottomrule\end{tabular}\end{center}
Son tensiones nominales. Holguras, reparto entre paredes, ovalización y radios requieren análisis del contacto real.
''',9)
F('La raíz y el ala no se adelgazan por igual',r'''
Para raíz de altura $h_r=115\mm$:
\[
\sigma_r=\frac{6M_C}{t_gh_r^2},\quad
\tau_r=\frac{\sqrt{V_y^2+V_z^2}}{t_gh_r},\quad
n_r=\frac{S_y}{2\sqrt{\sigma_r^2+3\tau_r^2}}=<<nRoot>>
\]
Para el ala local de ancho $w_f=10\mm$, brazo $a_f=8\mm$ y espesor $t_f=5\mm$:
\[
\sigma_f=\frac{6\eta F_v a_f}{w_ft_f^2},\qquad n_f=<<nFlange>>
\]
Se asigna el $70\%$ de toda $F_v$ a un apoyo. El ala gobierna antes que la raíz: reducirla a $3\mm$ no conserva este margen.

Cartela 6061 mecanizada, con alma y ala de distinto espesor; no se supone una unión soldada ni un doblez que conserve automáticamente el temple T6.
''',10)
F('Cuna: tres apoyos y dos modelos locales',r'''
\begin{center}\begin{tikzpicture}[x=.071cm,y=.5cm]
\draw[thick] (0,0)--(125,0);
\foreach \x in {15,60,105}{\draw[verde,thick] (\x,-.2)--(\x-.9,-.7)--(\x+.9,-.7)--cycle;}
\draw[<->] (15,1)--node[above,font=\small]{$45\mm$}(60,1);
\draw[<->] (105,1)--node[above,font=\small]{$20\mm$}(125,1);
\node[font=\small,anchor=east] at (0,0){Atrás};\node[font=\small,anchor=west] at (125,0){Frente};
\end{tikzpicture}\end{center}
\[
q=\frac{2F_v}{WD},\qquad P=100\N,\quad b_p=50\mm
\]
Se analiza una franja del piso bajo presión doble y un parche concentrado. Los apoyos quedan a $15$, $60$ y $105\mm$ del borde posterior.

La suma de presión doble y parche es una envolvente local exigente; no representa por sí sola un caso global en equilibrio.
''',11)
F('Cuna: momento por unidad de ancho',r'''
\[
M_{luz}=\frac{qs^2}{8}+\frac{Ps}{4b_p},\qquad
M_{borde}=\frac{qa^2}{2}+\frac{Pa}{b_p}
\]
\[
\sigma=\frac{6\max(M_{luz},M_{borde})}{t_p^2},\qquad
n=\frac{S_{y,5052}}{\sigma}=<<nFloor>>
\]
Aquí $M$ tiene unidad \textbf{N}, porque es momento por unidad de ancho; al dividir por $t_p^2$ se obtienen $\mathrm{N/mm^2}$.

Con $s=45\mm$, $a=20\mm$ y $t_p=2{,}5\mm$, el espesor requerido para $n=2{,}2$ resulta $<<tNeed|0.001|2>>\mm$.

Se retiene $2{,}5\mm$. La escotadura frontal cambió para alojar el tercer refuerzo; debe contrastarse con la manguera real.
''',11)
F('Los refuerzos conservan altura con poca pared',r'''
Tres tubos cerrados $20\times10\times1{,}5\mm$ bajo la cuna.
\[
I_b=I_r(10,20,3)-I_r(7,17,1{,}5),\qquad Z_b=\frac{I_b}{10\mm}
\]
\[
\sigma_b=\frac{\eta F_v L_b}{4Z_b},\qquad L_b=250\mm,
\qquad n_b=<<nRib>>
\]
Se aplica el $70\%$ de toda la fuerza a un único tubo. La luz equivalente supera los $234\mm$ entre ejes de fijación.

Los M5 retienen la cuna. Los apoyos interiores siguen el hueco redondeado del tubo y permiten aplicar precarga sin aplastar sus paredes. El análisis local de los taladros queda sujeto a FEA y ensayo.
''',12)
F('Anclajes: la forma sustituye espesor macizo',r'''
\begin{columns}[T,onlytextwidth]
\column{.58\textwidth}
Alma nominal $2\mm$, retornos hasta $18\mm$. Para cálculo se utiliza $u=1{,}8\mm$ mínimo.

El puente junto a la ranura tiene una sección L, con $a=24\mm$ en hombro y $26\mm$ en cinturón. La ranura conserva $52\mm$ de luz.

La sección es asimétrica: $I_{yz}\ne0$. No basta usar $I/c$ respecto de un solo eje geométrico.
\column{.37\textwidth}
\begin{tikzpicture}[scale=.12]
\fill[verde!35] (0,0)--(24,0)--(24,18)--(22.2,18)--(22.2,1.8)--(0,1.8)--cycle;
\draw[thick,verde] (0,0)--(24,0)--(24,18)--(22.2,18)--(22.2,1.8)--(0,1.8)--cycle;
\draw[->] (-2,-2)--(28,-2) node[right]{$y$};\draw[->] (-2,-2)--(-2,21) node[above]{$z$};
\node at (11,-7){$a$};\node at (29,9){$d_p$};
\end{tikzpicture}
\end{columns}
''',13)
F('Puente L: área, centroide e inercias',r'''
\small
Se descompone en $A_1=au$ y $A_2=(d_p-u)u$, sin contar dos veces la esquina:
\[
A=A_1+A_2,\quad
\bar y=\frac{A_1a/2+A_2(a-u/2)}A,\quad
\bar z=\frac{A_1u/2+A_2(d_p+u)/2}A
\]
\[
I_y=\frac{au^3+u(d_p^3-u^3)}3-A\bar z^2
\]
\[
I_z=\frac{ua^3+(d_p-u)[a^3-(a-u)^3]}3-A\bar y^2
\]
\[
I_{yz}=\frac{a^2u^2+[a^2-(a-u)^2](d_p^2-u^2)}4-A\bar y\bar z
\]
Las expresiones son integrales de área trasladadas al centroide. En Mathcad los prefijos \mc{Ls} y \mc{Lb} corresponden a hombro y cinturón.
''',14)
F('Puente L: flexión asimétrica en seis vértices',r'''
\[
\Delta=I_yI_z-I_{yz}^2,\qquad
\phi(y,z)=\frac{I_z(z-\bar z)-I_{yz}(y-\bar y)}{\Delta}
\]
Para el momento en el eje $y$, $\sigma=M_y\phi$. Se evalúan los vértices
\[
(0,0),(a,0),(a,d_p),(a-u,d_p),(a-u,u),(0,u).
\]
\[
Z_{ef}=\frac1{\max_i|\phi_i|},\qquad
n=\frac{S_y}{K_{ranura}\,\eta F_v\,52\mm/(4Z_{ef})}
\]
\textbf{Hombro:} $n=<<nSlot>>$. \qquad \textbf{Cinturón:} $n=<<nBelt>>$.

El modelo no acredita resistencia de cintas, costuras ni hebillas, ni reproduce el radio de contacto de la cinta.
''',15)
F('Raíz del anclaje: sección C',r'''
Para altura $h$, pared $u$ y profundidad $d_p$:
\[
A=hu+2u(d_p-u),\quad
\bar z=\frac{hu^2/2+u(d_p^2-u^2)}A
\]
\[
I=\frac{hu^3+2u(d_p^3-u^3)}3-A\bar z^2,\qquad
Z=\frac I{\max(\bar z,d_p-\bar z)}
\]
\[
\sigma=\frac{2\eta F_v a_r}{Z}
\]
\begin{center}\begin{tabular}{lrrr}\toprule
 & $h\ (\mathrm{mm})$ & $a_r\ (\mathrm{mm})$ & $n_y$\\\midrule
Hombro & 72 & 17 & $<<nShoulderRoot>>$\\
Cinturón & 100 & 25 & $<<nHipRoot>>$\\\bottomrule\end{tabular}\end{center}
''',16)
F('Pandeo local de anclajes nervados',r'''
\[
\sigma_{cr}=\frac{k\pi^2E}{12(1-\nu^2)}\left(\frac{u}{b_l}\right)^2
\]
Alma: $k=4$, $b_l=h-2u$. Retorno saliente: $k=0{,}43$, $b_l=d_p-u$.
\[
\sigma_{alma}=\frac{2\eta F_v a_r}{I}\max(\bar z,|u-\bar z|)
\]
La tensión del alma difiere de la máxima de toda la sección. Se compara cada zona con su tensión correspondiente y se limita la capacidad a la fluencia.

\textbf{Resultados:} alma hombro $<<CsnWeb>>$; alma cinturón $<<CbnWeb>>$; retorno/puente $<<nPanLocal>>$.

El pandeo de piezas perforadas, sus radios y su contacto requieren un modelo de detalle; los coeficientes corresponden a placas ideales.
''',16)
F('Diagonales: solo se acredita la traccionada',r'''
\[
\ell_X=\sqrt{S^2+h_X^2},\qquad F_X=F_h\frac{\ell_X}{S}
\]
\[
A_{net}=2\mm(20\mm-6{,}6\mm),\qquad
n_{net}=\frac{130\MPa}{F_X/A_{net}}=<<nX>>
\]
Las dos cintas de aluminio 5052 son de $20\times2\mm$. La comprimida puede pandear y no se acredita para resistir el esfuerzo lateral.

La segunda diagonal ocupa otro plano y usa calces en sus extremos. Los encuentros no se modelan pegados ni como uniones soldadas.
''',17)
F('Fijación de travesaño y diagonal',r'''
\[
n_{apl,X}=\frac{S_{y,5052}}{K_bF_X/(6\mm\,2\mm)}=<<nXBearing>>
\]
\[
n_{arr,X}=\frac{S_{y,5052}}{\sqrt3K_bF_X/[2(12-3{,}3)\mm\,2\mm]}=<<nXTear>>
\]
\[
R_F=K_b(F_h+F_X)=<<Rframe|1|1>>\N
\]
La suma de magnitudes es una envolvente local del perno compartido. Para el travesaño se obtiene $n=<<nFrameBear>>$ y para la pared mínima del riel $n=<<nRailFrame>>$.

Se conserva la contribución de flexión local del perno, especialmente por el desplazamiento entre planos de las diagonales.
''',17)
F('Tornillos: qué está representado en Inventor',r'''
\begin{itemize}
\item Cabeza cilíndrica con hexágono interior, vástago, arandelas individuales y tuerca con agujero pasante.
\item Roscas nativas métricas derechas: M6$\times$1 y M5$\times$0,8; clases geométricas 6g/6H.
\item Rosca parcial nominal: $b=2d+12\mm$ para estas longitudes. El vástago liso cubre el plano de carga crítico de los M6.
\item Tuerca autofrenante metálica derivada DIN 980. Su deformación de bloqueo y su par prevalente no se simulan.
\end{itemize}
La rosca nativa es \textbf{cosmética}: Inventor conoce su designación, pero no se ha tallado una hélice sólida. El STEP conserva el sólido nominal y puede no mostrar la textura de rosca.
\cita{Autodesk: ThreadFeatures y documentación sobre exportación de roscas.}
''',19)
F('Paquetes de montaje y longitudes',r'''
\begin{center}\begin{tabular}{lrrrr}\toprule
Unión & Cant. & Tornillo & Paquete & Saliente\\\midrule
Cartela & 4 & M6$\times$65 & $53\mm$ & $2{,}8\mm$\\
Marco/X & 4 & M6$\times$60 & $44/46\mm$ & $6{,}8/4{,}8\mm$\\
Hombro y cintura & 8 & M6$\times$55 & $42\mm$ & $3{,}8\mm$\\
Cuna & 6 & M5$\times$40 & $27{,}5\mm$ & $5{,}5\mm$\\\bottomrule\end{tabular}\end{center}
Cada unión lleva dos arandelas planas y una tuerca. Total: 22 tornillos, 44 arandelas y 22 tuercas.
\[
L\ge g+2t_w+h_n+2p
\]
El saliente deja al menos dos pasos de rosca. En la cuna, el protector hueco tiene $12\mm$ libres bajo su cara superior y separa la bolsa de las puntas.

Confirmar longitud de rosca, chaflanes, acceso de herramienta y tolerancias con el producto real.
''',19)
F('Precarga: cerrar la unión sin aplastar el tubo',r'''
\begin{center}\begin{tabular}{lrr}\toprule
Grupo & $F_0$ nominal & Dispersión adoptada\\\midrule
Cartela & $1500\N$ & $\pm25\%$\\
Marco/X & $1400\N$ & $\pm25\%$\\
Hombro/cintura & $1800\N$ & $\pm25\%$\\
Cuna M5 & $1000\N$ & $\pm25\%$\\\bottomrule\end{tabular}\end{center}
Son objetivos de estudio. La precarga máxima aumenta la tensión del tornillo y la presión de asiento; la mínima reduce la reserva contra apertura.

Se emplean dos extremos conservadores por separado: toda la carga de apertura $P$ se suma al tornillo, y toda $P$ se resta a la compresión del paquete. No se ha medido el reparto elástico real tornillo/unión.
''',18)
F('Apertura y efecto de palanca',r'''
\small
Con factor provisional de palanca $q_p=1{,}5$:
\[
P_C=P_F=q_p\frac{\eta F_h}{2}
\]
\[
P_{HS}=q_p\eta F_v\left(\frac12+\frac{17}{30}\right),\qquad
P_{HB}=q_p\frac{\eta F_v}{2}\left(1+\frac{25}{20}\right)
\]
\[
P_H=\max(P_{HS},P_{HB})=<<PH|1|1>>\N,\qquad
P_5=q_p\frac{\eta F_v}{3}=<<P5|1|1>>\N
\]
Los cocientes son relaciones de brazos, expresados todos en milímetros. El M5 se reparte entre los tres puntos de un lado de la cuna.

Las hipótesis de contacto y palanca deben ajustarse con FEA y ensayo de la unión; no se trata de una predicción de precarga medida.
''',18)
F('Áreas de rosca y sección del vástago',r'''
\[
A_{s,6}=20{,}1\,\mathrm{mm^2},\quad A_{s,5}=14{,}2\,\mathrm{mm^2}
\]
\[
A_{v,6}=\frac{\pi d^2}{4},\qquad Z_6=\frac{\pi d^3}{32},\quad d=6\mm
\]
\[
d_{r,5}=5\mm-1{,}22687(0{,}8\mm),\qquad
Z_{r,5}=\frac{\pi d_{r,5}^3}{32}
\]
La tracción se calcula con área resistente de rosca. El M6 usa sección lisa para cortante/flexión en el plano crítico; su posición se comprueba en el CAD. Para M5 se conserva la raíz de rosca en la flexión.

La cabeza se orienta hacia el anclaje de hombro y hacia la cartela exterior correspondiente para asegurar esa condición del vástago.
''',19)
F('Flexión local del tornillo',r'''
\small
Además del cortante, se incluye un momento por separación entre planos:
\[
M_{b,C}=R_p\frac{t_g+t_{min}}2
\]
\[
M_{b,F}=K_b\left[F_X\left(5\mm+\frac{t_{min}}2\right)+F_h\left(1\mm+\frac{t_{min}}2\right)\right]
\]
\[
R_H=K_b\frac{\eta F_v}{2},\quad M_{b,H}=R_H\frac{t_a+t_{min}}2
\]
\[
R_5=K_b\frac{\eta F_h}{3},\quad M_{b,5}=R_5\frac{t_f+t_b}{2}
\]
$t_a=2\mm$, $t_f=5\mm$ y $t_b=1{,}5\mm$. Los $5\mm$ del marco representan el caso de la diagonal exterior, calce y travesaño.

Es una envolvente de viga corta del perno; la interacción exacta con los agujeros sigue pendiente.
''',19)
F('Tornillos: tracción, flexión y cortante',r'''
\[
\sigma_{VM}=\sqrt{\left(\frac{1{,}25F_0+P}{A_s}+\frac{M_b}{Z}\right)^2
+3\left(\frac{R}{A_v}\right)^2},\qquad n=\frac{600\MPa}{\sigma_{VM}}
\]
\begin{center}\begin{tabular}{lrr}\toprule
Grupo & $\sigma_{VM}\ (\mathrm{MPa})$ & Margen\\\midrule
Cartela M6 & $<<VMC|1000000|1>>$ & $<<nBoltC>>$\\
Marco/X M6 & $<<VMF|1000000|1>>$ & $<<nBoltF>>$\\
Hombro/cintura M6 & $<<VMH|1000000|1>>$ & $<<nBoltH>>$\\
Cuna M5 & $<<VM5|1000000|1>>$ & $<<nBolt5>>$\\\bottomrule\end{tabular}\end{center}
La fijación del marco es el menor margen del conjunto de modelos revisados. No es un factor de seguridad global del equipo.
''',20)
F('Pasador hueco: compresión, flexión y cortante',r'''
\[
A_p=\frac\pi4(10^2-6{,}6^2)\,\mathrm{mm^2},\qquad
Z_p=\frac{\pi(10^4-6{,}6^4)}{32(10)}\,\mathrm{mm^3}
\]
\[
\sigma_{VM,p}=\sqrt{\left(\frac{1{,}25F_{0C}+P_C}{A_p}+\frac{M_{b,C}}{Z_p}\right)^2
+3\left(\frac{R_p}{A_p}\right)^2}
\]
\[
n_p=<<nPin>>,\qquad n_{apoyo\ interior}=<<nPinBore>>
\]
Se asigna la reacción completa tanto al pasador como al perno en comprobaciones separadas.

La longitud nominal de $53\mm$ debe ajustarse a la suma real de cartela y riel: un pasador largo impide sujetar; uno corto permite deformar la pared. Falta cerrar la tolerancia con el taller.
''',21)
F('Apoyos interiores: la forma debe caber en el tubo',r'''
M6: casquillo interior de exterior $10\mm$, interior $6{,}6\mm$ y longitud $37\mm$.
\[
n_{c,6}=\frac{240\MPa}{(1{,}25F_{0H}+P_H)/A_{c,6}}=<<nSleeve6>>
\]
M5: bloque interior de ancho $10\mm$, contorno redondeado $17\times7\mm$ y taladro $5{,}5\mm$. Sigue el hueco del refuerzo $20\times10\times1{,}5\mm$.
\[
A_{c,5}=10(10-4\cdot1{,}5)-\frac\pi4(5{,}5)^2
=<<Asp5|0.000001|2>>\,\mathrm{mm^2}
\]
\[
n_{c,5}=\frac{240\MPa}{(1{,}25F_{05}+P_5)/A_{c,5}}=<<nSleeve5>>
\]
Se cuenta solo el asiento plano de $4\mm$ y se resta conservadoramente el agujero completo.
''',22)
F('Arandelas: asiento y punzonamiento nominal',r'''
\[
A_w=\frac\pi4(D_w^2-d_w^2),\qquad p=\frac{1{,}25F_0+P}{A_w}
\]
M6: $D_w/d_w/t_w=12/6{,}4/1{,}6\mm$; M5: $10/5{,}3/1\mm$.
\[
\tau_{punz}=\frac{1{,}25F_{0H}+P_H}{\pi(12\mm)(1{,}8\mm)}
\]
\begin{center}\begin{tabular}{lll}\toprule
Asiento M6 & Asiento M5 & Punzonamiento de anclaje\\\midrule
$n=<<nSeat6>>$ & $n=<<nSeat5>>$ & $n=<<nPanPunch>>$\\\bottomrule\end{tabular}\end{center}
Son presiones medias y un perímetro nominal. Falta comprobar flexión de arandela, contacto no uniforme, dureza, asentamiento y el producto comprado.

El HDPE queda fuera del paquete de apriete de las uniones primarias.
''',22)
F('Cierre residual y resistencia de la tuerca',r'''
\[
F_{c,min}=0{,}75F_0-P>0
\]
\begin{center}\begin{tabular}{lrrrr}\toprule
 & Cartela & Marco & Arnés & Cuna\\\midrule
$F_{c,min}\ (\mathrm{N})$ & $<<ClampC|1|1>>$ & $<<ClampF|1|1>>$ & $<<ClampH|1|1>>$ & $<<Clamp5|1|1>>$\\\bottomrule\end{tabular}\end{center}
Para una tuerca comercial de clase 80 con tensión de prueba especificada:
\[
n_{prueba}=\frac{800\MPa\,A_s}{1{,}25F_0+P}
\]
M6: $<<nProof6>>$; M5: $<<nProof5>>$. Es un criterio de carga de prueba de la tuerca, distinto del margen frente a fluencia del perno.

La clase de la tuerca autofrenante y su carga de prueba deben estar certificadas. La forma hexagonal dibujada no acredita ese requisito.
''',23)
F('Aflojamiento y par: qué queda por definir',r'''
\[
T\approx K F_0d
\]
Con $K=0{,}20$ se obtienen, solo como ilustración, $<<TorqueC>>$, $<<TorqueF>>$, $<<TorqueH>>$ y $<<Torque5>>\,\mathrm{N\,m}$ para cartela, marco, arnés y cuna.

\textbf{No son pares de montaje.} La tuerca autofrenante añade par prevalente; fricción, recubrimiento y lubricación cambian la precarga alcanzada.
\begin{itemize}
\item Confirmar grado, par prevalente y límites de reutilización del proveedor.
\item Acceso para sujetar cabeza y tuerca; no fiarse de la arandela plana como bloqueo.
\item Calibrar apriete y comprobar pérdida de precarga, vibración y asentamiento.
\end{itemize}
\cita{NASA RP-1228: precarga, bloqueo y comportamiento de uniones.}
''',23)
F('Qué comprobó el ensamblaje digital',r'''
\begin{itemize}
\item 51 diseños de piezas sólidas y 131 ocurrencias, incluida la tornillería individual y dos referencias de acolchado.
\item Un riel fijado y tres restricciones de posición para cada una de las otras 130 ocurrencias: 390 restricciones.
\item Transformaciones y grados de libertad comprobados en Inventor.
\item Cero interferencias volumétricas nominales detectadas en la revisión final.
\end{itemize}
Las restricciones usan planos de referencia para conservar la posición. No simulan contacto, apriete ni fricción, y no son una prueba física del montaje.

Cero interferencias no comprueba tolerancias, acceso de herramientas, roscado real, deformación de la bolsa ni facilidad de insertar los apoyos interiores.
''')
labels={'nRail':'Riel nominal','nMinWall':'Riel con pared mínima','nBearR':'Apoyo pasador en riel','nBearG':'Apoyo cartela','nTearG':'Arrancamiento cartela','nRoot':'Raíz cartela','nFlange':'Ala cartela','nFloor':'Piso de cuna','nRib':'Refuerzo bajo cuna','nRibBear':'Apoyo nominal refuerzo','nSlot':'Puente hombro','nBelt':'Puente cinturón','nHipRoot':'Raíz cinturón','nShoulderRoot':'Raíz hombro','CsnWeb':'Pandeo alma hombro','CbnWeb':'Pandeo alma cinturón','nPanLocal':'Pandeo retorno/puente','nX':'Diagonal: sección neta','nXBearing':'Diagonal: aplastamiento','nXTear':'Diagonal: arrancamiento','nFrameBear':'Travesaño: apoyo','nRailFrame':'Riel: apoyo marco','nBoltC':'M6 de cartela','nBoltF':'M6 de marco/X','nBoltH':'M6 de arnés','nBolt5':'M5 de cuna','nPin':'Pasador hueco','nPinBore':'Interior del pasador','nSleeve6':'Casquillo M6','nSleeve5':'Apoyo interior M5','nSeat6':'Asiento M6','nSeat5':'Asiento M5','nPanPunch':'Punzonamiento anclaje'}
items=list(labels.items())
for j in range(0,len(items),11):
 rows='\n'.join(label+' & $'+num(V[k])+r'$\\' for k,label in items[j:j+11])
 F(f'Márgenes analíticos ({j//11+1}/3)',r'\small\begin{center}\begin{tabular}{lr}\toprule Comprobación & Margen\\\midrule '+rows+r'\bottomrule\end{tabular}\end{center} Todos los valores listados superan $2{,}2$ bajo las hipótesis de esta hoja. Las comprobaciones pendientes no se consideran aprobadas.',24)
F('Qué limita el resultado actual',r'''
\[
\min(n_i)=<<MinModel>>\quad\text{en el M6 del marco/X}
\]
\[
\delta_{riel}=<<deltaR|0.001|2>>\mm<5\mm
\]
Estos valores corresponden al conjunto de modelos parciales documentados. No incluyen toda posible falla del sistema.

El margen $2{,}25$ de esta revisión corresponde al perno del marco. El valor parecido citado en P2.02 correspondía al riel: \textbf{son comprobaciones distintas}.

Seguir quitando material sin medir cambia los brazos, los contactos o las condiciones de carga y puede hacer que una comprobación deje de cumplir.
''',24)
F('Fatiga y fractura: no se inventa una vida útil',r'''
\begin{columns}[T,onlytextwidth]
\column{.49\textwidth}
\textbf{Fatiga}
\[
\sigma_a=\frac{\sigma_{max}-\sigma_{min}}2,\quad
\sigma_m=\frac{\sigma_{max}+\sigma_{min}}2
\]
Se necesitan ciclos, amplitudes, acabado, entallas y curvas S--N del material y detalle. En aluminio no se adopta automáticamente un límite de resistencia a vida infinita.
\column{.49\textwidth}
\textbf{Fractura}
\[
K_I=Y\sigma\sqrt{\pi a}
\]
Se requieren tamaño de defecto $a$, factor geométrico $Y$ y tenacidad aplicable. Un margen de fluencia no sustituye esta comprobación.
\end{columns}
\medskip
La memoria no asigna número de ciclos ni tamaño de fisura admisible. Se deberán definir cuando exista el uso real y el proceso de fabricación.
''',26)
F('Otros modos de falla aún abiertos',r'''
\begin{itemize}
\item FEA de uniones, ranuras, pandeo con taladros, radios y contacto de la bolsa.
\item Impacto y caída, vibración, desgaste de cintas y pérdida de precarga.
\item Temperatura de uso: propiedades de aluminio, HDPE y textiles; las propiedades actuales son de temperatura ambiente.
\item Corrosión y contacto aluminio/inoxidable; protección compatible con el apriete, drenaje y limpieza.
\item Costuras, hebillas, liberación, reparto de presión y compatibilidad con distintos torsos.
\end{itemize}
No se ha calculado ni acreditado la seguridad del contacto con una persona. Primero deben definirse interfaces y ensayos de banco con una carga simulada.
''',26)
F('Medir la bomba antes de la siguiente reducción',r'''
\begin{columns}[T,onlytextwidth]
\column{.49\textwidth}
\textbf{Bomba y carga}
\begin{enumerate}
\item Marca y modelo exactos.
\item Masa vacía con manguera.
\item Masa con llenado de trabajo.
\item Volumen de agua utilizado.
\item Ancho, altura y profundidad llena.
\item Huella y forma de apoyo inferior.
\item Desplazamiento del centro de masa.
\item Deformación al vaciarse.
\end{enumerate}
\column{.49\textwidth}
\textbf{Interfaces}
\begin{enumerate}\setcounter{enumi}{8}
\item Posición y tamaño de salida.
\item Radio de giro de manguera.
\item Tapa y zona necesaria para abrir.
\item Costuras y zonas que no deben rozar.
\item Separación de anclajes existentes.
\item Ancho y espesor de las cintas.
\item Geometría de arnés/cinturón.
\item Masa completa de esos textiles.
\end{enumerate}
\end{columns}
''',26)
F('Cómo documentar las mediciones',r'''
\begin{itemize}
\item Fotografías frontal, posterior, laterales, superior e inferior, con regla en el mismo plano de la medida.
\item Registrar bolsa llena y vacía; nivel de llenado, instrumento, unidad e incertidumbre aproximada.
\item Medir acceso a herramientas, espacio para dedos y recorrido de cinta/hebilla.
\item Anotar tolerancias y radios reales de perfiles, espesores y certificados de material.
\end{itemize}
Con esos datos se podrán reducir brazos, altura, envolvente de carga o elementos duplicados de forma justificada. La reserva de textiles se sustituye por la masa pesada del arnés elegido.

La reducción adicional debe medirse frente al equipo completo, no frente a una maqueta que omita herrajes o mochila.
''',26)
F('Ruta de actualización del proyecto',r'''
\begin{enumerate}
\item Conservar P2.02 y esta entrega como revisiones trazables.
\item Introducir medidas reales en los parámetros; registrar origen y fecha.
\item Regenerar geometría y comprobar ajuste, interferencias y masa.
\item Actualizar cargas/brazos y recalcular la hoja Mathcad completa.
\item Comparar los resultados y actualizar esta guía.
\item Cerrar tolerancias, productos comerciales y plan de ensayo antes de fabricar para uso.
\end{enumerate}
El archivo Mathcad tiene resultados guardados por la aplicación. La fuente LaTeX permite editar la explicación manteniendo ecuaciones legibles.
''',27)
F('Fuentes: materiales y propiedades',r'''
\small
\begin{itemize}
\item \href{https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf}{Hydro: Alloy 6061, ficha de extrusión}. Referencia de temple y propiedades; no equivale a certificado de la pieza comprada.
\item \href{https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf}{Atlas Steels: Aluminium Alloy 5052} y \href{https://www.atlassteels.com.au/documents/TN14-5052\%20and\%205251\%20rev\%20June\%202013.pdf}{Technical Note 14}. Propiedades y diferencias de especificación.
\item \href{https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf}{Bossard: Stainless steel fasteners, ISO 3506}. Clases de tornillos y tuercas a temperatura ambiente.
\end{itemize}
Los valores seleccionados son hipótesis conservadas en la hoja, condicionadas al material real y al proceso. No se acredita la resistencia de una zona soldada con valores de T6 intacto.
''')
F('Fuentes: uniones y geometría comercial',r'''
\small
\begin{itemize}
\item \href{https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf}{NASA RP-1228, Barrett: Fastener Design Manual (1990)}. Precarga, cargas combinadas, bloqueo y fatiga.
\item \href{https://www.bossard.com/nl-en/-/media/bossard-group/website/documents/technical-resources/en/f-040-en.pdf}{Bossard: Arrangement, design, assembly}. Áreas resistentes y apoyo bajo cabeza.
\item \href{https://www.bossard.com/th-en/-/media/bossard-group/website/documents/technical-resources/en/f-077-en.pdf}{Bossard: herramientas de accionamiento}. Tamaños de hexágono.
\item \href{https://www.accu.co.uk/metal-locking-nuts/154970-HLN-M6-A2-BL}{Accu: tuerca autofrenante metálica M6, derivada DIN 980}. Referencia de geometría; la clase 80 del producto final queda por confirmar.
\item \href{https://www.mcmaster.com/products/washers/specifications-met~iso-7089/}{McMaster-Carr: arandelas ISO 7089}. Dimensiones nominales M5/M6.
\end{itemize}
No se ha confirmado una lista de compra local ni la disponibilidad de todas las longitudes/grados.
''')
F('Fuentes: teoría y representación CAD',r'''
\small
\begin{itemize}
\item \href{https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/}{MIT OCW 2.080J: Structural Mechanics}. Vigas, torsión e inestabilidad.
\item \href{https://ocw.mit.edu/courses/16-001-unified-engineering-materials-and-structures-fall-2021/}{MIT OCW 16.001: Materials and Structures}. Resistencia y criterios de falla.
\item \href{https://web.mit.edu/course/3/3.11/www/modules/frac.pdf}{MIT: Fracture}. Relación entre tensión, defecto y tenacidad.
\item \href{https://help.autodesk.com/cloudhelp/2024/ENU/Inventor-API/files/ThreadFeatures.htm}{Autodesk Inventor: ThreadFeatures} y \href{https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Threads-are-not-visible-in-STL-exported-from-Inventor.html}{exportación de roscas}. Diferencia entre información de rosca y hélice sólida.
\item \href{https://scottyfire.com/wp-content/uploads/2017/04/2017ScottyFireCatalogue_LR.pdf}{Scotty Fire: catálogo}. Referencia del concepto de bomba; no sustituye mediciones de la unidad real.
\end{itemize}
Fórmulas particulares, factores y envolventes de SEDAC: desarrollos de este prediseño, con el alcance indicado en cada sección.
''')
tex=preamble+'\n'.join(frames)+'\n\\end{document}\n'
assert '<<' not in tex
(OUT/'Guia_SEDAC_P2_03_MC02_Beamer.tex').write_text(tex,encoding='utf-8')
print(json.dumps({'frames':len(frames)+1,'tex':str(OUT/'Guia_SEDAC_P2_03_MC02_Beamer.tex')},ensure_ascii=False))
