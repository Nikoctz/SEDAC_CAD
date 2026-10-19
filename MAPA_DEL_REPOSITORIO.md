# MAPA DEL REPOSITORIO — SEDAC_CAD

Para quien abra esta carpeta y necesite saber **qué es cada cosa y por dónde empezar**, sin leer
9.288 archivos. Este documento **no borra ni decide**: declara.

Última actualización: 2026-10-19

> Si algo de aquí contradice a `ESTADO_ACTUAL.md`, **manda `ESTADO_ACTUAL.md`**.

## Por dónde empezar (agente que llega nuevo)

| orden | archivo | qué te da |
|---|---|---|
| 1 | `AGENTS.md` | las reglas y las prohibiciones |
| 2 | `ESTADO_ACTUAL.md` | qué versión es la vigente y qué está pendiente |
| 3 | `REQUISITOS_SEDAC.md` | qué piden los programas Despega y Vector, y con qué plazos |
| 4 | `DECISIONES.md` | lo ya decidido, para no volver a decidirlo |
| 5 | `01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md` | el trabajo en curso |
| 6 | `CHANGELOG_SEDAC.md` | qué se cambió y cuándo |

## Qué es actual, qué es historia y qué está superado

| ámbito | estado | dónde |
|---|---|---|
| Trabajo en curso | **actual, sin cerrar** | `01_CAD/Prototipo_P2/P2_05_20261019/` |
| Entrega de referencia | **actual y congelada** | `01_CAD/Prototipo_P2/P2_04_20261016/Entrega/` |
| Etapas anteriores | historia congelada, no se edita | `P2_01_20261015`, `P2_02_20261015`, `P2_03_20261016` |
| Generación «maqueta» (5–9 oct) | **superada** en geometría, **vigente** como justificación | raíz + `01_CAD/Automatizacion/`, `Ensamblajes/`, `Exportaciones/`, `02_PROTOTIPO/` |
| Memorias de cálculo | superadas las de P2_02 y P2_03 | `06_DOCUMENTACION/Memoria_Calculo_P2_02|P2_03` |
| Memoria vigente del diseño | `REVISION_P2_04_Y_SKILLS_20261017.md` | `06_DOCUMENTACION/` |
| Enlace con ChatGPT | activo | `07_ENLACE_CHATGPT/` |
| Notion (lectura de solo lectura) | activo | `08_NOTION/` |

## La generación «maqueta» NO es basura

Los cinco CAD de la raíz (`SEDAC_Anclaje`, `SEDAC_Cuna_Base_V0.1`, `SEDAC_Kit_Montaje_V01`,
`SEDAC_Maqueta_Editable_V01`, `SEDAC_Separador`) son de la etapa anterior a la serie P2: otra
arquitectura. **No son desechables** aunque lo parezcan:

- `02_PROTOTIPO/BOM/KIT_MONTAJE_V01.md` — sección **«Por qué estas dimensiones»**: justifica el
  separador de 6 mm, la arandela de 15 mm y el tornillo M5×30 (`1,2 + 8 + 6 + 3 + 1,2 + 5 = 24,4 mm`).
  Incluye el límite de impresión confirmado por el responsable (40 × 40 × 70 mm) y por qué el
  anclaje y la base **no** son imprimibles.
- `02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md` — la **hoja de medición de la bomba**: 13 puntos
  (A–M) y las referencias P0. Está **en blanco**: esa medición sigue sin hacerse.
- `01_CAD/Automatizacion/` — las reglas iLogic y los generadores que produjeron la maqueta.
- `01_CAD/Exportaciones/Maqueta_Kit_1a12/` — STL, 3MF y `.ipt` de la maqueta, más `VISTA_MAQUETA.png`.

**Regla:** quien limpie esto se lleva el *por qué* de las cotas que hoy siguen en pie.

## Fuera de Git a propósito (no versionar)

| qué | por qué |
|---|---|
| `.codex/config.toml` | contiene rutas de este PC (verificado) |
| `tools/inventor-mcp/` | repositorio externo clonado |
| `.venv-inventor-mcp/` | entorno del MCP de Inventor, 79 MB, reproducible |
| `OldVersions/` | autoguardados de Inventor |
| `01_CAD/Automatizacion/python_libs/` | dependencias vendorizadas — retiradas el 2026-10-19 |

## Limpieza del 2026-10-19

Retirado **a la Papelera de Windows** (recuperable, no destruido):

| qué | peso | por qué se fue |
|---|---:|---|
| `01_CAD/Automatizacion/python_libs/` | 54,4 MB, 1.366 arch. | numpy 2.5.3 + manifold3d 3.5.4 vendorizados; fuera de Git |
| `OldVersions/Part1.0003.ipt` | 0,2 MB | autoguardado huérfano de Inventor; era el único `Part1*` del proyecto |

**Para volver a ejecutar los generadores de la maqueta** (que hacían
`sys.path.insert(.../python_libs)` + `import manifold3d`):

```powershell
pip install numpy==2.5.3 manifold3d==3.5.4
```

Resultado medido: de **486,2 MB / 10.655 archivos** a **431,6 MB / 9.288 archivos**.
`git status` quedó limpio: nada de lo retirado estaba versionado.

**No se borró nada más.** En particular, siguen intactos: la generación «maqueta», las memorias
de cálculo P2_02 y P2_03 (las citan 19 líneas desde otros documentos), las instantáneas de
iteración y **todas las entregas**.

## Los PNG de las memorias

Casi todos son imágenes de fórmulas que Mathcad exporta junto a cada memoria, en carpetas
`*_imágenes`: 2.014 archivos que **juntos pesan 1,4 MB**. Se conservan, porque son el material para
rehacer el HTML/PDF de esas memorias y porque no estorban a un agente (los buscadores ignoran los
binarios). Las carpetas `Revision_visual` / `Revision_PDF` (~16 MB) son capturas de revisión.

Dato comprobado: las carpetas `memoria_final_imágenes` y `memoria_MC02_final_imágenes` de P2_03
(659 PNG cada una) **no son iguales** — distinta lista de archivos y distinto tamaño.

## Aviso — el repositorio vive en OneDrive

`.git` pesa 158 MB y está dentro de `OneDrive\Documentos`. **No hay remoto: OneDrive es la única
copia de seguridad**, y OneDrive sincroniza mientras Git escribe. [hipótesis] Ese solapamiento es
una causa conocida de bloqueos y de objetos dañados si se trabaja desde dos equipos a la vez.
No se ha cambiado nada; queda dicho.
