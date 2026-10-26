# A.4 · Diccionario de datos

Define los estados, los identificadores y las magnitudes que usa el paquete. Es la referencia común
del informe, la planilla y la memoria de cálculo.

## 1. Estados de un dato

| Estado | Significado | Qué exige |
|---|---|---|
| `ANTECEDENTE` | Valor tomado de un archivo del repositorio SEDAC_CAD o de un antecedente verificable | Ruta del archivo |
| `MEDIDO` | Valor obtenido con instrumento identificado | Instrumento, método, incertidumbre y fecha |
| `DATO DE FABRICANTE` | Valor declarado por el proveedor | Referencia de la ficha y fecha |
| `SUPUESTO` | Valor adoptado por decisión de ingeniería sin medición | Motivo declarado |
| `HIPÓTESIS` | Condición de carga o de uso no comprobada | Condición y cómo se va a comprobar |
| `CALCULADO` | Resultado de la memoria de cálculo | Memoria y expresión que lo produce |
| `PENDIENTE` | Sin dato | Qué medición lo resuelve y quién la hace |

Regla dura: **`PENDIENTE` nunca se sustituye por 0**. Si una magnitud es realmente nula, se escribe 0
en el resultado procesado y se deja constancia del método que lo demuestra.

## 2. Identificadores

| Prefijo | Objeto | Dónde vive |
|---|---|---|
| `R-xx` | Requisito | Informe §3; planilla `10_Trazabilidad` |
| `A-xx` | Actividad | Informe §4.1; planilla `01_Planificacion` |
| `V-xx` | Variable de entrada | Planilla `02_Variables`; informe §6 |
| `E-xx` | Ensayo | Planilla `03_Registro_Ensayos`; informe §5 |
| `I-xx` | Instrumento | Planilla `04_Instrumentos_Calibracion` |
| `M-xx` | Material | Planilla `05_Materiales`; informe §9 |
| `S-xx` | Sensor o instrumentación adicional | Planilla `06_Sensores`; informe §10 |
| `C-xx` | Cotización | Planilla `07_Cotizaciones`; informe §11 |
| `T-xx` | Resultado procesado | Planilla `08_Resultados`; informe §12 |
| `D-xx` | Decisión | Planilla `09_Decisiones`; informe §12 |

## 3. Magnitudes de la memoria de cálculo

Símbolo, unidad y estado. Todas las entradas viven en la hoja Mathcad; aquí solo la referencia.

| Símbolo | Descripción | Unidad | Estado actual | Origen |
|---|---|---|---|---|
| `L_canal` | Largo del canal | mm | ANTECEDENTE | P2.04 CAD |
| `B` | Ancho exterior del canal | mm | ANTECEDENTE | P2.04 CAD |
| `D` | Profundidad del canal | mm | ANTECEDENTE | P2.04 CAD |
| `t_nom` | Espesor nominal de pared | mm | ANTECEDENTE | P2.04 CAD |
| `t_min` | Espesor mínimo de cálculo | mm | ANTECEDENTE | P2.05 (no gobierna geometría) |
| `r_raiz` | Radio de raíz del perfil | mm | ANTECEDENTE | P2.04 CAD |
| `z_eje` | Altura del eje de las uniones | mm | ANTECEDENTE | P2.05 |
| `d_taladro` | Diámetro del taladro de unión | mm | ANTECEDENTE | P2.05 |
| `esp_mejilla` | Espesor de la mejilla | mm | ANTECEDENTE | P2.05 |
| `L_casq` | Longitud del casquillo | mm | CALCULADO (`B − 2t`) | Generador vigente |
| `holgura_axial` | Holgura axial casquillo-alas | mm | CALCULADO (0,000) | Generador vigente |
| `L_pasador` | Longitud del pasador hueco | mm | ANTECEDENTE | Modelo P2.04 |
| `m_total` | Masa total considerada en el caso de carga | kg | HIPÓTESIS | P2.05 |
| `g` | Aceleración de la gravedad | m/s² | SUPUESTO | Constante física |
| `fv`, `fh` | Factores de carga vertical y horizontal | — | HIPÓTESIS | P2.05 |
| `frac` | Reparto de carga entre lados | — | HIPÓTESIS | P2.05 |
| `excentricidad` | Excentricidad de la carga | mm | HIPÓTESIS | P2.05 |
| `precarga` | Precarga de estudio de las uniones | N | HIPÓTESIS | P2.05 |
| `margen_objetivo` | Umbral del cribado | — | HIPÓTESIS | P2.05 |
| `E_al`, `Sy_al` | Módulo y límite elástico del aluminio | MPa | SUPUESTO | P2.05 |
| `Sy_perno` | Límite elástico del perno | MPa | SUPUESTO | P2.05 |
| `masa_CAD` | Masa rígida y protectores | kg | MEDIDO en CAD | 01_CAD/Prototipo_P2/P2_04_20261016/BOM_Y_MASAS.csv |
| `m_bomba_vacia`, `m_bomba_llena` | Masas de la bomba | kg | PENDIENTE | Anexo A.1 |
| `z_cg_bomba` | Centro de masa de la bomba llena | mm | PENDIENTE | Anexo A.1 |
| `m_arnes` | Masa del arnés | kg | PENDIENTE | Anexo A.1 |
| `ancho_cinta`, `esp_cinta` | Geometría de la correa | mm | SUPUESTO | P2.05 |
| `rigidez_correa` | Rigidez axial de la correa | N/mm | PENDIENTE | Anexo A.1 |
| `par_apriete` | Par de apriete de las uniones | N·m | PENDIENTE | A02 |

Símbolos **no definidos** en la memoria a propósito, porque dependen de mediciones de laboratorio:
`m_bomba_vacia`, `m_bomba_llena`, `z_cg_bomba`, `x_cg_bomba`, `y_cg_bomba`, `m_arnes`, `z_cg_arnes`,
`B_med`, `t_med`, `L_casq_med`, `rigidez_correa`, `ancho_apoyo_hombro`,
`ancho_apoyo_cinturon`, `recorrido_cinta`, `IMU_1…n`. Definirlos activa los bloques de verificación.

## 4. Magnitudes derivadas de la memoria

| Símbolo | Descripción | Valor actual | Unidad |
|---|---|---:|---|
| `A_min`, `I_min`, `Ix_min`, `Z_min`, `J_min` | Propiedades de la sección con pared mínima | 208,32 · 11 858 · 33 030 · 752,35 · 544,41 | mm², mm⁴, mm⁴, mm³, mm⁴ |
| `M0` | Momento por excentricidad | 55 365,2 | N·mm |
| `Mmax` | Máximo de la envolvente | 55 738,6 | N·mm |
| `vm` | Tensión equivalente de von Mises | 106,80 | MPa |
| `flecha` | Flecha de la envolvente | 0,8667 | mm |
| `n_min` | Mínimo de los 15 factores de seguridad | 2,2471 | — |
| `V_union` | Cortante en la unión | 1046,98 | N |
| `R` | Tracción externa en la unión | 1522,22 | N |
| `fb` | Fuerza máxima en el perno | 2804,44 | N |
| `cierre_residual` | Reserva de cierre de junta | 282,22 | N |
| `holgura_axial` | Holgura axial del casquillo | 0,000 | mm |
| `bajo_cabeza` | Apilado bajo cabeza hasta la tuerca | 49,000 | mm |
| `saliente` | Saliente del tornillo | 6,000 | mm |
| `masa_presupuesto` | Presupuesto sin bomba ni agua | 2,212328 | kg |
| `masa_brecha_2kg` | Brecha hasta el objetivo de 2 kg | 0,212328 | kg |

## 5. Reglas de unidades

- La memoria trabaja en **mm, N, MPa y kg**; el verificador dimensional de Mathcad rechaza las
  combinaciones incompatibles y la hoja incluye cuatro comprobaciones explícitas.
- Las constantes de entrada llevan su unidad escrita en la expresión (`480*mm`, `240*MPa`, `2000*N`).
- La planilla registra en unidades SI y convierte solo al presentar resultados.
- Los ángulos se expresan en radianes dentro del cálculo (`35*pi/180`) y en grados al presentar.

## 6. Reglas de procesamiento de datos de ensayo

| Regla | Detalle |
|---|---|
| Separación | El dato bruto no se modifica. El procesado guarda el método, la versión del software y el sesgo aplicado |
| Corrección de sesgos | La corrección de gravedad, la deriva del giroscopio y la magnetometría se documentan una a una; no se aplican en bloque |
| Integración | El error de doble integración crece con el tiempo: no se integran señales largas sin declarar el modelo |
| Comparación | La diferencia entre predicción y ensayo se calcula solo cuando existen ambos valores; mientras tanto queda `PENDIENTE` |
| Trazabilidad | Cada resultado conserva el identificador del ensayo y de la variable que lo origina |
