# Auditoría de antecedentes: memoria de cálculo anterior y materiales reutilizables

**Fecha: 2026-10-25 · Alcance: revisión documental, en modo de solo lectura del repositorio SEDAC_CAD.**

Este documento respalda el §8 del informe. No reejecuta el constructor de la memoria anterior ni
recalcula sus resultados: la verificación numérica se hizo sobre la memoria **nueva**, que es la que
se entrega.

## 1. Qué se inspeccionó

| Archivo | Tamaño | Qué contiene | Verificación realizada |
|---|---|---|---|
| `06_DOCUMENTACION/Memoria_Calculo_P2_03/Memoria_SEDAC_P2_03_MC02_FINAL_EDITABLE.xmcd` | 1,30 MB | Hoja XMCD de Mathcad 14.1: 247 variables, 45 páginas lógicas, 659 regiones | Lectura del XML: estructura, unidades, orden de definición |
| `06_DOCUMENTACION/Memoria_Calculo_P2_03/LEEME_MEMORIA.md` | 2,2 kB | Ficha de la entrega anterior: 33 márgenes, n mínimo 2,254, advertencia de no sumar la bomba a la estructura | Lectura completa |
| `06_DOCUMENTACION/Memoria_Calculo_P2_03/Soporte/ENTRADAS.json` | 1,4 kB | Las 69 entradas de la memoria anterior con su unidad | Lectura completa; cotejo con el modelo vigente |
| `06_DOCUMENTACION/Memoria_Calculo_P2_03/Soporte/VALORES_ESPERADOS_SI.json` | 15 kB | Valores de control con los que se verificó la memoria anterior | Lectura: procedimiento de verificación reutilizado |
| `06_DOCUMENTACION/Memoria_Calculo_P2_03/Soporte/comprobar_mathcad.ps1` | 2,0 kB | Script de verificación por automatización: abrir, recalcular, comparar variable por variable y guardar | **Reutilizado** en este paquete como `verificar_mathcad.ps1` |
| `06_DOCUMENTACION/Memoria_Calculo_P2_02/` | — | Primera memoria de prediseño, mismo formato | Revisada como antecedente histórico |
| `01_CAD/Prototipo_P2/P2_03_20261016/Soporte/mathcad_base.py` | 6,9 kB | Generador programático de la hoja XMCD anterior | **Reutilizado**: portado a la biblioteca estándar y mejorado (soporta `and`/`or`, `floor`, funciones y verificación de unidades) |
| `01_CAD/Prototipo_P2/P2_03_20261016/HOJA_MEDICION_P2_03.md` | — | 22 ítems de medición de bomba, arnés y correas | Revisada: estructura reutilizada, cotas no aplicables |
| `02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md` | 3,3 kB | Formulario en blanco de medición de bomba | **Adoptado** como anexo A.1, ampliado con masas, centro de masa y correas |
| `02_PROTOTIPO/BOM/KIT_MONTAJE_V01.md` | 6,2 kB | Kit geométrico de anclaje, base y separadores; lista de fijaciones; apilamientos | Revisada: lista de componentes reutilizada, arquitectura descartada |

## 2. Verificación del formato y de la instalación

| Comprobación | Resultado |
|---|---|
| ¿Hay Mathcad instalado en este equipo? | Sí: `C:\Program Files (x86)\Mathcad\Mathcad 15\mathcad.exe` |
| ¿Cómo se identifica por automatización? | **14.1.4.587** (la carpeta dice 15; el motor es 14.1) |
| ¿El formato XMCD clásico se abre y recalcula? | Sí: `Worksheets.Open` + `Recalculate` + `GetValue` funcionan |
| ¿Se puede generar un XMCD de forma programática? | Sí, y verificado: la memoria nueva se generó con un script y se verificó variable por variable |
| ¿Se pueden codificar rangos o vectores en XMCD? | **No.** `ml:range` existe en el esquema pero rechaza los hijos probados (`ml:id`, `ml:real`). Se resolvió con la fórmula cerrada del máximo de la envolvente |
| ¿Cómo se verificaba la memoria anterior? | Con un control numérico en JSON y comparación por automatización, con tolerancia 1e-8. **Mismo procedimiento aquí** |

## 3. Dictamen por elemento de la memoria anterior

| Elemento | Dictamen | Justificación |
|---|---|---|
| Estructura de la hoja: entradas editables, salidas con unidades, verificaciones dimensionales | **REUTILIZABLE** | Es la estructura que el proyecto exige; se reprodujo íntegra |
| Convención de unidades (mm, N, MPa) y verificaciones de dimensionalidad | **REUTILIZABLE** | La memoria nueva trabaja igual y añade cuatro comprobaciones explícitas |
| Método de envolvente de momento | **REUTILIZABLE CON ADAPTACIÓN** | El método es válido; los brazos y la excentricidad son de P2.03 y hay que sustituirlos |
| Las 15 verificaciones del cribado, con su fórmula y su texto de modelo | **REUTILIZABLE CON ADAPTACIÓN** | Las fórmulas son las mismas; cambian los coeficientes de sección y la geometría |
| Formato XMCD y apertura con la instalación Mathcad de este equipo | **REUTILIZABLE** | Comprobado en esta sesión |
| Geometría de rieles 50 × 40 × 1,5, travesaños, diagonales y marco X M6 | **DESCARTADO** | Corresponde a P2.03, superada por P2.04 |
| Cargas, brazos y excentricidades de P2.03 | **DESCARTADO** | Son hipótesis de otro prototipo; se conservan como hipótesis, no como resultados |
| Resultados numéricos y márgenes de P2.03 (n mínimo 2,254) | **DESCARTADO** | No son comparables con el prototipo vigente |
| Masa de 2,333 kg y presupuesto de 2,913 kg de P2.03 | **DESCARTADO** | Historia; el valor vigente es 1,442328 kg medido en P2.04 |
| Guía en PDF con teoría y referencias a páginas de la hoja | **REUTILIZABLE COMO REFERENCIA** | Buena práctica de presentación; el contenido se rehizo para el prototipo vigente |
| M5×55, arandela GN 6341, tuerca autofrenante y apilamientos de 38 mm | **REUTILIZABLE** | Son las fijaciones del prototipo vigente; se verificaron las longitudes contra el modelo |

## 4. Comprobación de coherencia detectada al contrastar con el modelo vigente

Al cotejar la memoria anterior con el modelo actual aparecieron tres diferencias que conviene tener
presentes, porque las tres son la clase de error que una memoria arrastra al cambiar de prototipo:

1. **Longitud del tornillo.** La cadena de apilamiento del prototipo vigente es
   `38 (paquete) + 3 (arandela) + 5 (cabeza ISO 4762 M5) + 3 (arandela) + 5 (tuerca) = 49 mm` bajo cabeza,
   con una saliente de 6 mm en el M5×55. La altura de la cabeza del tornillo **no** se descuenta del largo
   nominal, porque la longitud nominal de un tornillo de cabeza cilíndrica se mide desde debajo de la
   cabeza. La memoria nueva deja esta cadena explícita en la página 11.
2. **Altura de la tuerca.** El generador del repositorio modela la tuerca autofrenante con 5 mm de alto
   (`op('z',0,5,…)` en `generar_p2_05.py`), no con 6 mm. La memoria nueva usa 5 mm.
3. **Longitud del casquillo.** El generador la define como `B − 2t`, es decir, exactamente igual al ancho
   interior del canal. La consecuencia —holgura axial nominal de 0,000 mm— está calculada en la memoria
   nueva y es el punto que exige cerrar la cadena de tolerancias con mediciones reales.

## 5. Cómo se verificó la memoria nueva (procedimiento reutilizado del repositorio)

1. Se genera la fuente XMCD con el script `construir_memoria.py`.
2. El mismo script evalúa las mismas expresiones en Python y guarda el **control numérico**.
3. `verificar_mathcad.ps1` abre la fuente en Mathcad, recalcula, lee las 177 variables por
   automatización y compara con el control; guarda la memoria final con resultados y exporta HTML.
4. `comparar_control.py` coteja el control contra los resultados publicados del repositorio.

| Comprobación | Resultado |
|---|---|
| Variables verificadas contra el control | 177, con 0 fuera de tolerancia (error relativo < 1e-9) |
| Cotejo contra el cribado publicado | Peor error relativo 8,06·10⁻¹⁶, en 15 verificaciones y 11 magnitudes |
| `Mmax` | 55 738,58598984375 N·mm, idéntico al barrido numérico del repositorio |
| `n_min` | 2,24713091866015, idéntico al publicado |
| Flecha | 0,8666768799116917 mm, idéntico |
