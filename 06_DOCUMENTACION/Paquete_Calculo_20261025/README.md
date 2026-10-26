# SEDAC · Paquete documental para la memoria de cálculo y los ensayos

**Versión 0.1 · 2026-10-25 · Estado: borrador de trabajo, sujeto a revisión del profesor de biomecánica.**

Paquete documental para planificar la memoria de cálculo y los ensayos del prototipo SEDAC (transporte de
agua a la espalda con bomba), de modo que las mediciones reales del laboratorio puedan incorporarse sin
reconstruir la documentación y pueda fundamentar decisiones de geometría, material, unión, correa y
montaje.

> **Este paquete no valida el prototipo.** No hay ensayos, no hay mediciones, no hay FEA, no hay
> certificación de materiales. Las cifras de carga que aparecen son hipótesis de prediseño declaradas
> como tales. El prototipo sigue sin liberarse para uso con personas.

## 1. Qué hay en el paquete

| Ruta | Contenido | Estado |
|---|---|---|
| `01_Informe/Informe_SEDAC_Memoria_y_Ensayos_v0.1.docx` | Informe editable: objetivo, alcance, sistema, requisitos, planificación, protocolo, variables, memoria de cálculo, auditoría de la memoria anterior, materiales, sensores, cotizaciones, matriz de decisión, riesgos y anexos. Empieza por el §0, escrito para quien no conoce el proyecto | **Creado y verificado**: abre en Word (1849 párrafos, 26 tablas) |
| `01_Informe/Informe_SEDAC_Memoria_y_Ensayos_v0.1.pdf` | PDF de revisión, 27 páginas | **Creado y verificado**: exportado desde Word, texto legible y sin caracteres corruptos |
| `02_Planilla/Planilla_SEDAC_Captura_y_Seguimiento_v0.1.xlsx` | Planilla de captura y seguimiento, 12 hojas con trazabilidad requisito → ensayo → dato → cálculo → decisión | **Creado y verificado**: abre en Excel, fórmulas calculadas, comportamiento con entradas faltantes comprobado |
| `03_Memoria_Calculo/Soporte/Memoria_SEDAC_P204_MC01_EDITABLE.xmcd` | Memoria de cálculo en Mathcad 15 (formato XMCD clásico) con resultados guardados por la aplicación. Las páginas 0 a 0.2 explican cómo usarla e incluyen glosario de símbolos y de conceptos | **Creado y verificado**: 177 variables cotejadas, 0 fuera de tolerancia |
| `03_Memoria_Calculo/Guion_Implementacion_Mathcad15.md` | Guion de implementación: orden de declaración, ecuaciones, verificación dimensional, cómo incorporar una medición | **Creado** |
| `03_Memoria_Calculo/Soporte/` | Generador de la hoja, control numérico, scripts de verificación y sus salidas | **Creado y ejecutado** |
| `04_Anexos_Formularios/` | Formulario de bomba y correas, protocolo de laboratorio, ficha de ensayo, diccionario de datos | **Creado** |
| `05_Auditoria_Antecedentes/` | Auditoría documental de la memoria de cálculo anterior (P2.03) y de los antecedentes reutilizables | **Creado** |
| `06_Registro_Ensayos/` | Carpeta vacía para alojar los datos brutos de los ensayos cuando existan | **Preparada** |

## 2. Fuentes utilizadas (solo lectura)

Las rutas de esta sección son relativas a la raíz de SEDAC_CAD, no a la carpeta del paquete. El PARAMETROS del caso base usa D=24 mm, t=3 mm y mínimo 2,8 mm; no confundir con el PARAMETROS de OPT1 (28/2,5/2,3 mm).

Todo el contenido numérico proviene de estos archivos del repositorio `SEDAC_CAD`, que **no se
modificó**:

| Fuente | Uso en este paquete |
|---|---|
| `01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json` | Entradas geométricas, cargas, materiales y reservas |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py` | Ecuaciones del cribado de prediseño |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Optimizacion_Real_20261023_014225/Analisis/V0_base_P2_05/RESULTADOS_PREDISENO.json` | Valores de referencia para el cotejo |
| `01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py` | Definición del casquillo (`L_casq = B − 2t`) y de la tuerca (5 mm) |
| `01_CAD/Prototipo_P2/P2_04_20261016/BOM_Y_MASAS.csv` | Masa medida en CAD (1,442328 kg) |
| `01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/MODELO_API.json` | Función documentada del casquillo y del pasador |
| `01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/BOM_FIJACIONES.csv` | Fijaciones, empuje, longitud del tornillo y saliente |
| `06_DOCUMENTACION/Memoria_Calculo_P2_03/` | Memoria anterior auditada (formato XMCD) |
| `02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md` | Formulario de bomba adoptado como anexo A.1 |
| `ESTADO_ACTUAL.md`, `DECISIONES.md`, `CHANGELOG_SEDAC.md` | Estado vigente del proyecto y decisiones adoptadas |

## 3. Cómo completar el paquete con datos de laboratorio

1. **Medir** (formularios del anexo A.1 y A.2). No usar 0 como sustituto de un dato desconocido.
2. **Registrar el dato bruto** en la planilla, hoja `03_Registro_Ensayos`, con identificador de ensayo,
   versión del prototipo y configuración.
3. **Cargar el dato en la planilla**, hoja `02_Variables`, columna "Valor registrado", y cambiar su
   estado a `MEDIDO` con la incertidumbre y el método.
4. **Incorporar el valor a la memoria**: abrir `03_Memoria_Calculo/Soporte/Memoria_SEDAC_P204_MC01_EDITABLE.xmcd` en Mathcad, actualizar la entrada que alimenta el cálculo con su unidad y recalcular con `Ctrl+F9`. Definir un símbolo nuevo al final no sustituye automáticamente las entradas anteriores: verificar las dependencias.
5. **Reprocesar y comparar**: datos procesados en `08_Resultados`; las diferencias se calculan solas
   cuando existen medición y predicción.
6. **Recalcular y decidir**: actualizar la memoria (versión 2), registrar las decisiones en
   `09_Decisiones` y cerrar la trazabilidad de `10_Trazabilidad`.
7. **Revisar el diseño** con la matriz del informe §12: conservar, revisar geometría, cambiar sección,
   material, unión, correa o montaje, siempre condicionado a la evidencia.

## 4. Verificación realizada

Las comprobaciones originales se conservan como registro del autor. La reejecución de Mathcad de esta corrección cotejó 177 resultados, con cero discrepancias y cero no numéricos; Word abrió el informe corregido y exportó 27 páginas; Excel abrió 12 hojas y conservó entradas y fórmulas salvo la cita corregida en G26. No se repitió en esta corrección el banco completo de entradas incompletas de Excel. Véase `CORRECCIONES_VERIFICADAS_20261025.md`.

| Comprobación | Resultado |
|---|---|
| La memoria abre en Mathcad 15 y se recalcula | Sí, con 177 variables numéricas leídas por automatización |
| La memoria coincide con el control numérico | Sí, 0 variables fuera de tolerancia (error relativo < 1e-9) |
| La memoria reproduce el cribado publicado del repositorio | Sí, peor error relativo 8,06·10⁻¹⁶ en 15 verificaciones y 11 magnitudes |
| El .docx abre en Word | Sí, 1849 párrafos, 26 tablas |
| El PDF de revisión es legible | Sí, 27 páginas exportadas desde Word; el recuento de texto de la revisión original no se reutiliza como medición de esta versión |
| El .xlsx abre en Excel sin reparación | Sí, 12 hojas, fórmulas operativas |
| Las fórmulas detectan entradas faltantes | Sí: con las celdas vacías devuelven `PENDIENTE`; con valores simulados y luego borrados vuelven a `PENDIENTE` |
| Coherencia de unidades | Comprobada por el verificador dimensional de Mathcad (4 comprobaciones explícitas) |
| Referencias cruzadas | Requisito → ensayo → dato → cálculo → decisión en la hoja `10_Trazabilidad` |
| Datos ficticios de prueba | Los dos valores simulados en la prueba de fórmulas se borraron y se comprobó que no quedan en el archivo |
| Auditoría de texto de informe, planilla y memoria | La revisión anterior lo declaró; esta corrección comprobó los textos afectados, no acredita una auditoría lingüística exhaustiva |

### Revisión de redacción (2026-10-25, segunda vuelta)

La primera versión del generador del informe había quedado **doblemente codificada** (UTF-8 leído como
ANSI por una edición con PowerShell 5.1), de modo que los acentos y los símbolos salían corruptos tanto
en el `.docx` como en el `.pdf`. Se reparó el origen, no el resultado: se deshizo la doble codificación
en el generador, en la memoria y en los anexos, y se regeneraron los tres documentos. La auditoría
posterior se conserva como declaración histórica del autor, no como garantía exhaustiva de esta revisión.

### Orientación para quien no conoce el proyecto

- **Informe §0** — «Cómo leer este documento»: qué es SEDAC en dos párrafos, para qué sirve cada pieza
  del prototipo, en qué estado está el proyecto, las cuatro categorías de dato y un **glosario de 30
  términos técnicos** explicados en lenguaje sencillo. Además, cada sección empieza con un párrafo
  «En pocas palabras».
- **Memoria, páginas 0 a 0.2** — «Cómo usar esta memoria», glosario de los símbolos con su unidad y
  glosario de los conceptos (cribado, margen, modo que gobierna, pandeo, precarga, apilamiento axial,
  holgura axial, resistencia frente a rigidez).
- **Anexo A.4** — diccionario de datos con estados, identificadores, magnitudes y reglas de unidades.

### Pendiente

- **Anexo de la memoria dentro del informe**: la memoria está verificada y guardada por la aplicación,
  pero no se generó un PDF de su hoja de trabajo para incrustarlo como anexo. La exportación a HTML con
  imágenes queda en `03_Memoria_Calculo/Soporte/` para revisión visual.
- **Cotizaciones**: la tabla está preparada y vacía; no se consultaron proveedores.
- **Inventario del laboratorio**: la selección de sensores tiene los criterios completos y las
  candidatas sin datos, a la espera de la visita al laboratorio.

## 5. Reglas que gobiernan este paquete

- Cada afirmación lleva su estado: `ANTECEDENTE`, `MEDIDO`, `DATO DE FABRICANTE`, `SUPUESTO`,
  `HIPÓTESIS`, `CALCULADO` o `PENDIENTE`.
- No se inventa ninguna medición, propiedad, precio, disponibilidad ni resultado.
- El motor de cálculo es la memoria Mathcad; la planilla registra y sigue. No hay dos fuentes de
  verdad para el mismo resultado.
- Cambiar la geometría obliga a regenerar el CAD, remedir la masa y recalcular la memoria.
- Nada de este paquete autoriza ensayos con personas ni declara validación ergonómica, clínica o
  normativa.

## 6. Reproducir la memoria de cálculo

```
cd 03_Memoria_Calculo\Soporte
python construir_memoria.py            # genera la fuente y el control numérico
powershell -File verificar_mathcad.ps1 # abre en Mathcad, verifica y guarda el archivo final
python comparar_control.py             # coteja contra los resultados del repositorio
```

## 7. Donde sigue

- **Inmediato**: reunión de alcance y criterios con el profesor (A02) y medición de B, t y longitud de
  casquillo en las piezas disponibles (A03). Es la medición más barata y cierra el hallazgo de la
  holgura axial de 0,000 mm.
- **Después**: caracterización de bomba, correas y arnés (A05 a A08), inventario del laboratorio
  (A10) y selección de sensor e instrumentación de fuerza (A11).
- **Con esas entradas**: actualización de la memoria (A21), recálculo del cribado y de la sensibilidad
  (A22) y matriz de decisión de diseño (A23).

## 8. Corrección verificada del 2026-10-25

Se corrigieron citas, unidades y explicaciones sin cambiar las ecuaciones ni los valores del control. En el caso base, Sy=240 MPa < sigma crítica local=477,699 MPa: el empate de n_local con n_combinado procede del límite de fluencia, no de pandeo local elástico gobernante. Los diámetros efectivos de estudio 9,9/5,6 mm son supuestos heredados de calcular_p2_05.py:63,71; no son medidas ni tolerancias aprobadas. mlat es un momento en N·mm y J corresponde a sección abierta.

La etiqueta Mathcad 14.1 por automatización no contradice por sí sola la instalación Mathcad 15 del equipo. El control Python usa las mismas expresiones y comprueba implementación, no validez física independiente. Incorporar símbolos al final de la hoja no sustituye automáticamente entradas anteriores: revisar dependencias. El máximo de momento solo se cotejó para los casos nominales indicados, no para toda carga arbitraria.

Los pendientes de laboratorio, cotizaciones y PDF de la hoja Mathcad permanecen. La memoria no valida el producto. El respaldo previo queda en la carpeta externa original; la entrega versionada seleccionada excluye respaldos históricos, cachés y lockfiles.
