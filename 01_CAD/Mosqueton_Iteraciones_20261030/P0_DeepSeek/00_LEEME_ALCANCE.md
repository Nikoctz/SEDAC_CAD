# Mosquetón giratorio P0 — alcance y contenido

Fecha: 2026-10-29. Autor del paquete: agente (Buffy) a pedido del responsable.

## Qué es esto

Propuesta **P0** de un mosquetón giratorio para conectar un arnés recuperado de
mochila a una bomba de espalda de depósito flexible, pensada para **fabricar
prototipos por FDM y ensayar en banco de laboratorio**.

## Qué NO es esto

- **No** es una pieza validada para combate de incendios.
- **No** es una pieza validada para uso con personas.
- **No** hay ensayo físico, ni FEA, ni validación de resistencia.
- **No** se ha comprobado el ajuste con la bomba real ni con el arnés real.
- **No** existe archivo nativo de Inventor (`.ipt`/`.iam`) en este paquete. Ver
  §Bloqueo.

Cualquier uso distinto de "probeta de laboratorio en banco, sin personas en la
zona de carga" queda fuera del alcance de lo construido.

## Bloqueo declarado: escritura CAD nativa

**hecho:** en esta sesión no hay herramientas MCP de Inventor conectadas y no se
ejecutó escritura CAD nativa. Por eso **no se entregan** `.ipt` ni `.iam`.

Lo que sí se entrega, y sí se verificó:

| Elemento | Estado |
|---|---|
| Modelo paramétrico (fuente de verdad) | `SCRIPTS/modelo_p0.py`, ejecutado sin error |
| STEP de cada pieza | generados y reimportados (volumen coincidente) |
| STEP del conjunto en posición de montaje | 2 sólidos, sin interferencia |
| STL de impresión | generados, binario consistente |
| Verificación de montaje y giro | numérica, ver §Informe |
| Ficha de cotas | `01_FICHA_COTAS_P0.md` |
| Informe con cálculos, fallas y ensayos | `02_INFORME_P0.md` |

Para obtener el `.iam` nativo hace falta: abrir Inventor 2027.1 y reconstruir
según la ficha de cotas, o ejecutar una rutina COM validada (la del repositorio
SEDAC no está validada para escritura). **No se declara construido nada que no
exista.**

## Archivos

```
00_LEEME_ALCANCE.md          este documento
01_FICHA_COTAS_P0.md         cotas exactas, clasificadas medida/cálculo/supuesto
02_INFORME_P0.md             cálculos, modos de falla, materiales, ensayos, pendientes
CAD/P0_Cuerpo_Gancho.step    cuerpo del gancho + horquilla
CAD/P0_Argolla.step          cubo + cuello + anilla
CAD/P0_Conjunto_Montaje.step conjunto en posición de montaje (2 sólidos)
CAD/*.stl                    mallas de las piezas (misma geometría)
IMPRESION/*.stl              archivos para imprimir
SCRIPTS/modelo_p0.py         modelo paramétrico y verificación geométrica
SCRIPTS/calculos_p0.py       cálculos reproducibles de prediseño
SCRIPTS/verificar_salidas.py verificación de STEP/STL
EVIDENCIAS/verificacion_modelo.json
EVIDENCIAS/calculos_p0.json
EVIDENCIAS/verificacion_salidas.json
EVIDENCIAS/log_modelo.txt, log_giro.txt
```

## Cómo regenerar

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install cadquery
./.venv/Scripts/python.exe SCRIPTS/modelo_p0.py
./.venv/Scripts/python.exe SCRIPTS/calculos_p0.py
./.venv/Scripts/python.exe SCRIPTS/verificar_salidas.py
```

Todas las cotas están en el diccionario `P` al inicio de `modelo_p0.py`. Cambiar
un valor y volver a ejecutar regenera STEP, STL y la verificación.

## Relación con el trabajo previo

- Se leyeron `ANALISIS_PRELIMINAR.md`, `Cuerpo_1.ipt`, `Cuerpo_2.ipt`,
  `Mosqueton_Giro_Borrador.iam` y `Mosqueton_Giro_Revision.step` **solo como
  referencia**. No se modificó ni se sobrescribió ningún archivo de
  `Mosqueton_Revision_20261029`.
- El modelo previo tenía un eje Ø7 dentro de un alojamiento Ø8 con cabezales
  Ø15 que no pasan por el Ø8: **el montaje físico no estaba resuelto**.
  P0 sustituye esos cabezales integrales por un **tornillo de hombro comercial
  ISO 7379 M6×16** con tuerca autoblocante, que es montable y desmontable.
- El modelo previo verificó 30° de giro y un barrido cada 30° sin
  interferencias. P0 **no reproduce esos números**: su cinemática es distinta
  (ver §Informe, "Giro").

## Estado del repositorio SEDAC_CAD

**hecho:** se ejecutó `git status` antes de cualquier trabajo. El árbol tiene
cambios **ajenos** (modificaciones en `AGENTS.md`, `ESTADO_ACTUAL.md`,
`CHANGELOG_SEDAC.md`, `08_NOTION/…`, borrado de `landing-sedac/**` y carpetas
sin rastrear). **No se tocaron.** Todo el trabajo de este paquete se hizo en la
carpeta externa
`C:\Users\nicol\.codex\visualizations\2026\10\29\01a1893e-07a5-7f30-b54a-9e63b9ceb0a0\Mosqueton_Giratorio_P0_20261029`.
**No se hizo commit ni push.**

## Seguridad de los ensayos

Los ensayos previstos son **de banco, con la pieza sola o con carga inerte, sin
personas en la zona de carga** y con contención. Ningún resultado de este
paquete autoriza a cargar el conjunto puesto sobre una persona.
