# Guion de implementación de la memoria de cálculo en Mathcad 15

> Documento de referencia para **rehacer, extender o auditar** la hoja `Memoria_SEDAC_P204_MC01_EDITABLE.xmcd`.
> La hoja ya está construida, abierta, recalculada y verificada en la instalación Mathcad 15 de este
> equipo. Este guion explica qué contiene, cómo se generó y cómo se modifica sin romper la
> coherencia con el control numérico.

## 1. Formato y verificación

| Elemento | Detalle |
|---|---|
| Formato | XMCD clásico (`worksheet30` / `math30`), no formato Mathcad Prime |
| Aplicación | Mathcad 15 instalado en `C:\Program Files (x86)\Mathcad\Mathcad 15`; por automatización se identifica como **14.1.4.587** |
| Apertura y recálculo | `Mathcad.Application` → `Worksheets.Open(...)` → `Recalculate()` |
| Guardado | `SaveAs(ruta, 20)` para XMCD; `SaveAs(ruta, 3)` para HTML |
| Lectura de resultados | `GetValue(nombre).Real` devuelve el valor en unidades SI |
| Verificación | 177 variables numéricas cotejadas contra el control numérico, 0 fuera de tolerancia (error relativo < 1e-9) |
| Cotejo del modelo | Peor error relativo frente a los resultados publicados del repositorio: **8,06·10⁻¹⁶** |

Archivos: `Memoria_SEDAC_P204_MC01_FUENTE.xmcd` (fuente), `Memoria_SEDAC_P204_MC01_EDITABLE.xmcd`
(final, con resultados guardados por la aplicación), `Memoria_SEDAC_P204_MC01.html` (exportación para
revisión visual).

## 2. Orden de declaración (obligatorio)

En Mathcad una función se evalúa en el momento de declararse. **Una función que use variables todavía
no declaradas no se resuelve**, y todo lo que dependa de ella queda marcado como error. Por eso la hoja
declara, en este orden:

1. **Entradas geométricas** y **entradas de carga y material**.
2. **Funciones de sección**: `A_sec`, `z_sec`, `I_sec`, `Ix_sec`, `Z_sec`, `J_sec`.
3. **Propiedades de la sección** del caso base: `A_min`, `z_min`, `I_min`, `Ix_min`, `Z_min`, `J_min`.
4. **Caso de carga**: `L_luz`, `Fv`, `Fh`, `N_lado`, `Q_lado`, `M0`.
5. **Función de la envolvente** `M_env`, declarada *después* de las cargas porque usa `M0`, `Q_lado` y `L_luz`.
6. **Máximo de la envolvente**: `step`, `x_cont`, `i_cont`, `x_a`, `x_b`, `Mmax`, `x_max`.
7. **Tensiones y estabilidad**, **uniones**, **puentes**, **resumen**, **masa**, **apilamiento**,
   **sensibilidad**, **bloques de mediciones pendientes**.

## 3. Cómo se evalúa el máximo de la envolvente sin vectores

El cribado vigente evalúa la envolvente sobre una malla de 801 puntos. En XMCD clásico no se ha
logrado codificar un rango o un vector (`ml:range` existe en el esquema pero no acepta los hijos que
se probaron), así que el máximo se reproduce con la misma malla por fórmula cerrada:

```
x_cont := (L_luz - M0/Q_lado)/2      ' punto critico continuo de la envolvente
step   := L_luz/800                   ' paso de la malla de 801 puntos
i_cont := floor(x_cont/step)          ' indice del tramo que contiene el critico
x_a    := i_cont*step                 ' punto de malla anterior
x_b    := (i_cont+1)*step             ' punto de malla posterior
Mmax   := max(M_env(x_a), M_env(x_b)) ' maximo exacto sobre esa malla
x_max  := x_a + (M_env(x_b) > M_env(x_a))*(x_b - x_a)
```

Como la envolvente es unimodal en cada tramo, el máximo discreto está en uno de esos dos puntos.
Resultado: **Mmax = 55 738,58598984375 N·mm**, idéntico al barrido numérico del repositorio
(55 738,58598984375), con diferencia cero.

## 4. Ecuaciones, con su expresión exacta

### 4.1 Sección (caso general, `b` ancho, `d` profundidad, `t` espesor)

```
A_sec(b,d,t) := b*t + 2*t*(d-t)
z_sec(b,d,t) := (b*t*t/2 + 2*t*(d-t)*(t+d)/2)/A_sec(b,d,t)
I_sec(b,d,t) := b*t^3/12 + b*t*(t/2 - z_sec(b,d,t))^2
                 + 2*(t*(d-t)^3/12 + t*(d-t)*((t+d)/2 - z_sec(b,d,t))^2)
Ix_sec(b,d,t) := t*b^3/12 + 2*((d-t)*t^3/12 + t*(d-t)*((b-t)/2)^2)
Z_sec(b,d,t) := I_sec(b,d,t)/max(z_sec(b,d,t), d-z_sec(b,d,t))
J_sec(b,d,t) := (b + 2*(d-t))*t^3/3
```

Son las mismas expresiones del generador y del cribado del repositorio. La notación es la de Mathcad: `^` es potencia, `*` es producto y `:=` es definición.
(`^` es potencia, `*` es producto, `:=` es definición).

### 4.2 Caso de carga

```
Fv := m_total*g*fv                     ' 735,75 N
Fh := m_total*g*fh                     ' 245,25 N
N_lado := Fv*frac                      ' 515,025 N
Q_lado := Fh*frac                      ' 171,675 N
L_luz := apoyo_hombro_y - apoyo_cinturon_y   ' 380 mm
M0 := N_lado*excentricidad             ' 55 365,19 N·mm
M_env(x) := M0*max(1-x/L_luz, x/L_luz) + Q_lado*x*(L_luz-x)/L_luz
```

### 4.3 Tensiones y estabilidad

```
mlat := Q_lado*L_luz/4
sig := N_lado/A_min + K_borde*Mmax/Z_min
sig_biax := sig + K_borde*mlat*(B/2)/Ix_min
T := Q_lado*brazo_torsion
tau := T*t_min/J_min + Q_lado/A_min
vm := sqrt(sig_biax^2 + 3*tau^2)
n_combinado := Sy_al/vm
n_euler := pi^2*E_al*min(I_min,Ix_min)/(L_luz^2*N_lado)
sig_placa := 0.43*pi^2*E_al/(12*(1-nu^2))*(t_min/(D-t_min))^2
n_local := min(Sy_al,sig_placa)/vm
Mcr := pi/L_luz*sqrt(E_al*Ix_min*GG*J_min)
n_ltb := Mcr/Mmax
```

### 4.4 Uniones

**SUPUESTOS heredados, no mediciones ni tolerancias de fabricación aprobadas:**
`pin_od_eff = pasador_od − 0,1 mm = 9,9 mm` y `pin_id_eff = 5,6 mm` proceden de
`SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:63,71`.
Se conservan para reproducir el cribado; deben revisarse con el proceso y las dimensiones reales.
El diámetro de taladro de 10,2 mm no sustituye al diámetro efectivo del pasador en esas ecuaciones.

En el caso base `Sy_al = 240 MPa < sig_placa = 477,699 MPa`. Por ello `n_local = n_combinado`:
el límite activo es la fluencia bajo tensión combinada, no el pandeo local elástico.
La igualdad de ambos márgenes no constituye dos comprobaciones físicas independientes.

```
reaction := Mmax/separacion_pernos + Q_lado/2
R := 1.5*reaction
V_union := sqrt((N_lado/2)^2 + reaction^2)
fb := 1.25*precarga + 0.2*R
bolt_vm := sqrt((fb/As_M5)^2 + 3*(V_union/As_M5)^2)
n_perno := Sy_perno/bolt_vm
n_aplast_ala := Sy_al/(V_union/(t_min*pin_od_eff))
n_arranc := 0.577*Sy_al/(V_union/(2*t_min*(dist_borde_perno - d_taladro/2)))
n_casquillo := Sy_al/((1.25*precarga)/(pi/4*((casquillo_od-0.1*mm)^2 - (d_taladro+0.1*mm)^2)))
pin_vm := sqrt((V_union*3.4*mm/pin_Z)^2 + 3*(2*V_union/pin_area)^2)
washer_sigma := 6*(fb/(2*pi*4*mm))*max(0, d_taladro/2 - 4*mm)/(arandela_esp_min^2)
washer_contact := sqrt(3)/2*(8*mm)^2 - pi/4*(5.5*mm)^2
```

**Ojo con las longitudes**: cualquier constante que sea una longitud debe llevar `*mm`. En el control
numérico el error de omitir una de ellas fue de un factor 1000 en la arandela y de un factor 500 en el
pasador, porque se mezclaba mm con SI. La hoja de Mathcad detecta esas mezclas por sí misma: por eso
todas las constantes de longitud están escritas con su unidad.

### 4.5 Puentes de anclaje y de cuna

```
Tstrap := N_lado/(2*cos(angulo_eslinga))
Tinterface := max(N_lado/cos(angulo_eslinga), sqrt(N_lado^2 + (Q_lado + M0/L_luz)^2))
bridge_M := Tinterface*luz_puente_cinta/4
Z_bridge := esp_anclaje_min*alto_puente_cinta^2/6
Z_bridge_out := alto_puente_cinta*esp_anclaje_min^2/6
sbri := 1.5*bridge_M*(cos(angulo_eslinga)/Z_bridge + sin(angulo_eslinga)/Z_bridge_out)
n_puente_anclaje := Sy_al/sbri
cuna_sigma := 1.5*(Tstrap*luz_puente_cinta/4)*(cos(angulo_eslinga)/cuna_Zin + sin(angulo_eslinga)/cuna_Zout)
n_puente_cuna := Sy_al/cuna_sigma
```

## 5. Verificaciones dimensionales

La hoja incluye cuatro comprobaciones explícitas que deben valer 1 o la unidad indicada:

```
u_fuerza := 1*kg*m/s**2            ' debe equivaler a 1 N
u_fuerza_ratio := u_fuerza/(1*N)   ' debe valer 1
u_presion_ratio := (1*MPa)/(1*N/mm**2)  ' debe valer 1: MPa equivale a N/mm2
u_area := 1*mm**2
u_momento := 1*N*1*mm
```

## 6. Cómo incorporar una medición nueva

1. Editar el archivo `Memoria_SEDAC_P204_MC01_EDITABLE.xmcd` en Mathcad y **añadir la definición del
   símbolo medido** en la página 13 (datos de laboratorio pendientes), con su unidad y su estado.
2. Mathcad activa los resultados dependientes de ese símbolo; si aparece un error, es que la
   expresión necesita el valor en la unidad esperada.
3. Recalcular con `Ctrl+F9` y guardar.
4. Registrar el dato en la planilla (`02_Variables`) con su estado `MEDIDO`, su incertidumbre y el
   identificador de ensayo.
5. Volver a ejecutar `verificar_mathcad.ps1` para confirmar que la hoja sigue calculando sin errores.
6. Actualizar el control numérico (`construir_memoria.py`) y volver a ejecutar `comparar_control.py`.

## 7. Reglas de mantenimiento

- **Una sola fuente de verdad por resultado**: la memoria calcula; la planilla registra. No recalcular
  resistencia en la planilla.
- **No cambiar la geometría sin regenerar**: si el CAD cambia, hay que regenerar, remedir la masa en
  Inventor y recalcular esta hoja. La coherencia entre CAD, memoria y documentos no es automática.
- **No usar ceros como sustituto**: un símbolo sin dato se deja sin definir o se marca como entrada no
  medida; nunca se pone 0.
- **Toda constante nueva debe llevar su unidad escrita**, o el verificador dimensional no avisará del
  error más adelante.

## 8. Regenerar la hoja desde cero

```
cd 03_Memoria_Calculo\Soporte
python construir_memoria.py          # genera FUENTE.xmcd + control numérico
powershell -File verificar_mathcad.ps1   # abre en Mathcad, verifica y guarda el EDITABLE
python comparar_control.py           # coteja el control contra el repositorio
```

Los scripts están en `03_Memoria_Calculo/Soporte/` y no modifican nada del repositorio SEDAC_CAD.
