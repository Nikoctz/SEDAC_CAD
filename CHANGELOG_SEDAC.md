# CHANGELOG — SEDAC_CAD

Registra cambios **realizados** sobre el proyecto. No ideas, no planes, no propuestas.
Formato: fecha · versión/ámbito · descripción · evidencia.

---

## 2026-10-19

**Notion: corrección aplicada por el responsable y verificada por el agente**

El responsable corrigió las cuatro páginas desfasadas mediante su cuenta de ChatGPT (que sí puede escribir en Notion) y el agente **releyó y comprobó** el resultado, en lugar de dar por bueno el informe recibido.
- Verificado: solo esas cuatro páginas se editaron ese día (12:52–12:53); ninguna otra.
- Verificado: en **03.2** los datos propios de P2.03 quedaron **intactos** (51 diseños, 131 ocurrencias, 390 restricciones, rieles 50 × 40 × 1,5 mm, 2,333 kg, margen 2,254) y **el 2,247 no aparece**: no se trasvasaron cifras de P2.04 a P2.03.
- Verificado: en **04.1** las secciones 2 a 5, la ficha por prueba y la declaración de ausencia de ensayos físicos siguen intactas.
- **Defecto detectado, pendiente:** Notion autovinculó cuatro nombres de archivo `.md` (`.md` es dominio de Moldavia) a enlaces rotos como `http://04.md`; se corrige escribiéndolos entre acentos graves.
- Registrada una **falsa alarma propia**: una comprobación automática informó 0 apariciones de `pendiente` en 03.4; era un error del agente (búsqueda sensible a mayúsculas). Los pendientes estaban.
- Evidencia: llamadas `API-retrieve-page-markdown` y `API-post-search` del 2026-10-19; `08_NOTION/ESTADO_NOTION_20261019.md` §8.

**Notion: acceso de solo lectura en funcionamiento, y desfase verificado frente al repositorio**

Se cerró el diagnóstico que quedaba abierto: la conexión `SEDAC lectura` creada por el responsable quedó operativa y el agente **lee Notion**. El bloqueo era de entorno —el proceso de OpenCode no heredaba la variable `NOTION_TOKEN`; se reinició el servicio y quedó resuelto—.
- Verificado: `API-get-self` responde bot `SEDAC lectura` (id `3fef5e4b-db90-810b-b59b-0027dfdd45e0`); la búsqueda devuelve **90 páginas** compartidas; el servidor MCP `notion` aparece `connected`.
- **Hallazgo principal (hecho):** las páginas **03.1, 03.2, 03.4 y 04.1** de Notion siguen declarando **P2.03** como diseño y CAD vigentes, con enlaces de Drive al paquete P2.03 — **dos revisiones por detrás** del repositorio (P2.04 base, P2.05 abierto). Se verificó que ChatGPT acertó al señalarlo y se encontró un cuarto punto que no había mencionado: **03.4 (CAD vigente)**.
- Resuelto sin inventar: por `AGENTS.md` §1, en caso de conflicto manda `ESTADO_ACTUAL.md`; por tanto **lo que se corrige es Notion**, y esa corrección es del responsable (el agente no escribe en Notion).
- Registrado además que «margen 2,254 (Notion) vs 2,247 (repositorio)» **no es contradicción**: son dos revisiones distintas del diseño.
- Evidencia: llamadas `API-get-self`, `API-post-search` y `API-retrieve-page-markdown` del 2026-10-19.

**Corrección de desfases en `ESTADO_ACTUAL.md` y enlace de contexto con ChatGPT**

Se corrigieron afirmaciones desactualizadas de `ESTADO_ACTUAL.md`, detectadas al preparar el enlace con ChatGPT:
- **Git:** declaraba baseline `20f1ef3` y árbol limpio. El commit vigente es `f26f010` (2026-10-18 22:52), **no hay remoto configurado** y hay dos carpetas sin rastrear.
- **MCP en OpenCode:** declaraba «no hay sección `mcp`». La sección existe (servidor `inventor`, declarado `enabled: false`) y `status()` **responde** desde OpenCode. La lectura estructural del ensamblaje sigue sin reproducirse en OpenCode.
- **Evidencia:** `git log`, `git status`, `~/.config/opencode/opencode.json` y llamada `status()` del servidor MCP, todas del 2026-10-19.

Además se creó `07_ENLACE_CHATGPT/`: un generador que produce `PAQUETE_CHATGPT.md` leyendo los documentos y los números del repositorio, con revisión de privacidad, más el protocolo de ida y vuelta y la plantilla de entrada. **Sin commit todavía.**
- Evidencia: `07_ENLACE_CHATGPT/` (carpeta sin rastrear).

Se creó `REQUISITOS_SEDAC.md`: requisitos y plazos de las dos convocatorias en que participa el proyecto, extraídos de los PDF incorporados ese día a la raíz, ordenados y **citados por sección**, con el estado de participación declarado por el responsable y la tabla de huecos frente al proyecto.
- Fuentes: `BASES-DESPEGA-USACH-2026.pdf` (27 pág.), `Terminos-y-condiciones-Vector-2026.pdf` (7 pág.). Texto extraído con `pdfminer` desde el intérprete del proyecto; los `.txt` quedaron fuera del repositorio.
- Añadida la sección «Programas de financiamiento (2026)» a `ESTADO_ACTUAL.md`.
- El paquete de contexto ahora incluye `REQUISITOS_SEDAC.md` (sección 5) y una cuarta pregunta, sobre el protocolo de validación con usuarios.
- Evidencia: `REQUISITOS_SEDAC.md`, `07_ENLACE_CHATGPT/PAQUETE_CHATGPT.md` regenerado.

Se creó `07_ENLACE_CHATGPT/INSTRUCCIONES_PROYECTO.md` (reglas permanentes que se pegan en el campo «Instrucciones» del proyecto ChatGPT) y se **rectificó un supuesto propio**: en conversación se había afirmado que esa instancia de ChatGPT «no ve Notion». El responsable confirmó lo contrario: **sí lo ve**. Se separó el papel de cada fuente — **Notion** manda en requisitos y plazos; **el paquete** manda en estado técnico — y quedó recogido en las instrucciones, en `README_ENLACE.md` y en la sección 0 del paquete (reglas 7 a 9).
- Evidencia: `07_ENLACE_CHATGPT/INSTRUCCIONES_PROYECTO.md`; `PAQUETE_CHATGPT.md` regenerado.

El responsable **eliminó el ZIP del repositorio completo** que estaba subido en el proyecto ChatGPT y **pegó las instrucciones del proyecto** (ambas cosas declaradas por él el 2026-10-19). Se registraron las decisiones `D-10` (el repositorio no sale del PC) y `D-11` (alcance del conector de Notion, por acotar) en `DECISIONES.md`, y se añadió a las instrucciones que en ese proyecto **no hay ningún archivo del repositorio subido**.
- Motivo: el ZIP competía con la versión vigente dentro del mismo proyecto y llevaba rutas locales, historia de Git y archivos excluidos a propósito.
- Evidencia: `DECISIONES.md` (D-10, D-11); `INSTRUCCIONES_PROYECTO.md`; paquete regenerado.

**Commit, limpieza de la carpeta y mapa del repositorio**

Con autorización del responsable se hizo lo siguiente, **en este orden** (proteger primero, limpiar después):

- **Dos commits:** `e27cf4e` — P2.05 (148 archivos) y `0f7d03b` — gobierno, requisitos y enlace. `git status` queda limpio.
- **Retirado a la Papelera de Windows** (recuperable): `01_CAD/Automatizacion/python_libs/` (54,4 MB, 1.366 archivos; numpy 2.5.3 + manifold3d 3.5.4 vendorizados, fuera de Git, usados por `generar_maqueta_kit.py`) y `OldVersions/Part1.0003.ipt` (autoguardado huérfano; único `Part1*` del proyecto).
- **Medido:** de 486,2 MB / 10.655 archivos a **431,6 MB / 9.288 archivos**. `git status` limpio antes y después: nada de lo retirado estaba versionado.
- **No se borró nada más.** Se conservan, a propósito: la generación «maqueta» (contiene el porqué de las cotas del kit en `KIT_MONTAJE_V01.md` y la hoja de medición de la bomba en `REGISTRO_MEDICION_BOMBA_LOCAL.md`), las memorias P2_02/P2_03 (citadas por 19 líneas de otros documentos), las instantáneas de iteración y todas las entregas.
- **Nuevo `MAPA_DEL_REPOSITORIO.md`:** declara el estado de cada cosa, el orden de lectura para un agente, lo que está fuera de Git y la limpieza de hoy.
- Evidencia: `git log`, `git status`, y las mediciones de tamaño antes y después.
- Cierre: el aviso de privacidad del generador se había colado en el control de versiones; se retiró del índice y del disco y se añadió a `.gitignore`. La línea que señaló era **real** (el estado decía dónde vive el repositorio) y se reescribió sin la ruta. Además, el campo «commit vigente» del estado se sustituyó por la lista de commits del día, porque un documento no puede nombrar al commit que lo contiene. Commits del 2026-10-19: `e27cf4e`, `0f7d03b`, `d2ae769`, `acd7bd7` y los posteriores que registre `git log`.

**Entrada de ChatGPT archivada, y una corrección de interpretación propia**

- Guardada la respuesta del proyecto ChatGPT como `07_ENLACE_CHATGPT/Entrada_20261019.md` (plantilla rellenada + respuesta literal), marcada como **borrador externo**.
- **Corrección de un error de este repositorio:** `ESTADO_ACTUAL.md` afirmaba que «los programas piden piloto con usuarios reales» como exigencia de enero de 2027. Verificado en las bases Despega: el «Piloto de validación… actores externos o usuarios reales» es un hito del **Programa de Preincubación (abril–diciembre 2027)**; la **Etapa 3** (dic 2026 – ene 2027) pide validación **técnica y comercial**. Corregido en `ESTADO_ACTUAL.md` y en `REQUISITOS_SEDAC.md`. La advertencia sobre seguridad no cambia: P2.04/P2.05 siguen sin liberar para personas.
- Registradas `D-12` a `D-15` en `DECISIONES.md`, **en estado `revisar`**: son propuestas del proyecto ChatGPT, **no adoptadas**.
- **Verificado de lo propuesto:** las tres cuentas se reproducen exactas (2,136 % · 0,71495 · 109,80 mm); el seguro del constructor y la ausencia de `ESTADO_OK.txt` en la corrida parcial son ciertos; la atribución del piloto a preincubación es correcta.
- **Sin verificar:** las referencias a las páginas de Notion 03.1 y 04.1 (el repositorio no las menciona) y la propiedad `PlanarSketch.ConstraintStatus` (el MCP responde «Not connected to Inventor»).
- Evidencia: `Entrada_20261019.md`; `ERROR.txt` y `REDONDEOS.json` de la corrida `Nueva_20261019_060807`; texto extraído de las bases Despega.

**Decisiones delegadas: D-12 a D-15 adoptadas, y dos premisas corregidas**

- El responsable delegó la toma de decisiones técnicas (2026-10-19). Se adoptan **D-12, D-13, D-14 y D-15** en `DECISIONES.md`, cada una con argumento breve, fecha y reversibilidad, bajo una regla de límite escrita: **la delegación alcanza a criterios, orden de trabajo y gobernanza, no a mediciones.**
- **D-12** (criterio funcional de bordes): adoptada. Regla añadida por el agente: **el aviso del constructor no se silencia** mientras no exista la clasificación; se **descarta** la opción de dejar el lumbar sin redondeo declarado, por ser el atajo que reproduce el fallo de P2.04 (sello de «correcto» junto a un pendiente). **Sin cambios de código ni de CAD: no se ejecutó ninguna corrida nueva.**
- **D-13** (evidencia de bocetos): adoptada y **no ejecutada** — Inventor no está conectado desde OpenCode. Añadidos un plan B (evidencia visual) y el criterio de que una subrestricción justificada es aceptable.
- **D-14** (sensibilidad del margen): adoptada, con la urgencia añadida — con una reserva de 2,14 %, un reparto 71,5/28,5 en lugar de 70/30 agota el margen; medir masa y centro de gravedad pesa más que el FEA.
- **D-15** (validación escalonada): adoptada. Los criterios numéricos de parada quedan `pendiente`: no se inventan.
- **Premisa corregida 1:** «ya sabes todo sobre el proyecto» — no. El agente conoce el repositorio; **no** conoce la bomba, los textiles, la antropometría ni las cotizaciones.
- **Premisa corregida 2:** «tienes acceso a Notion» — **no lo tiene** (hecho, verificado): sin conector ni MCP, y la sesión de navegador pide login (`notion.so/login`). Registrado en `ESTADO_ACTUAL.md`, sección nueva «Acceso a fuentes externas desde el agente».
- Evidencia: `DECISIONES.md` (D-12 a D-15) y `ESTADO_ACTUAL.md`. **Sin cambios en `01_CAD/`.**

**Notion: vías de acceso estudiadas (documentación de Notion y de OpenCode, 2026-10-19)**

- Registrado en `DECISIONES.md` D-11. Hallazgo principal: **el MCP oficial de Notion (`https://mcp.notion.com/mcp`, OAuth) no acota** — alcanza todo el contenido al que acceda el usuario y además puede **crear y modificar páginas**; es decir, por sí solo contradice D-11. El servidor con token de integración **sí acota** (solo las páginas compartidas, y admite «solo lectura»), pero **ya no tiene mantenimiento**. La exportación de páginas al repositorio es la vía recomendada por este proyecto.
- Nada de esto se ha activado: **no se añadió ningún servidor MCP ni ninguna credencial**. Requiere decisión del responsable.

---

## 2026-10-18

**Baseline de control de versiones**
Se inicializó el repositorio Git del proyecto en la rama `main`.
- Commit: `20f1ef3` — "Baseline inicial SEDAC antes de P2.05"
- Contenido: 3254 archivos versionados, incluidos `01_CAD`, `02_PROTOTIPO`, `06_DOCUMENTACION`, los documentos de raíz y las skills de `.agents/skills/`.
- Ignorados: `.codex/config.toml`, `tools/inventor-mcp/`, `.venv*/`, `OldVersions/`.
- Evidencia: `git log --oneline` en la raíz del proyecto.

**Configuración del entorno de agentes AI / MCP**
- OmniRoute activo para OpenCode: plugin local `~/.config/opencode/omniroute-plugin-v2`, con enrutamiento a `http://127.0.0.1:20128`.
- MCP de Inventor configurado en `.codex/config.toml` (no versionado, exclusión intencional) y **verificado en modo lectura desde Codex con Inventor 2027.1**: conexión COM correcta, `get_document_info()` sobre `SEDAC_P2_03.iam` y lectura estructural (131 ocurrencias, 51 piezas únicas, 390 restricciones, 1 grounded).
- Detectada una incompatibilidad menor de lectura en una consulta geométrica (`Coordinate`).
- **Escritura CAD mediante MCP: no validada.** **Integración en OpenCode: no configurada.**
- `.codex/config.toml` y `tools/inventor-mcp/` permanecen fuera del repositorio por decisión intencional.

**Documentos de gobierno del proyecto**
Se crearon cuatro documentos en la raíz para trabajo alternado Codex / OpenCode:
- `AGENTS.md` — instrucciones para cualquier agente AI.
- `ESTADO_ACTUAL.md` — estado vigente, Git, MCP, pendientes.
- `DECISIONES.md` — registro de decisiones técnicas.
- `CHANGELOG_SEDAC.md` — este archivo.
- Evidencia: `git status` posterior a su creación.

---

## 2026-10-17

**Revisión de ingeniería de P2.04**
Se auditó la entrega P2.04 con verificación de archivos: 79 huellas SHA-256 coincidentes; ZIP de 80 entradas sin error CRC; masa CAD recalculada 1,442328 kg; cálculo de prediseño reproducido.
- Hallazgo: redondeo de 0,5 mm de `Interfaz_lumbar_aligerada` con `aplicado: false` en `REDONDEOS.json`.
- Entregable: `06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md`.
- Evidencia: informe versionado en el baseline `20f1ef3`.

---

## 2026-10-16 / 2026-10-17

**Entrega P2.04**
Prediseño de doble canal abierto con cuna textil y alas de cinturón flexibles. 54 piezas, 83 ocurrencias, 246 restricciones. Masa rígida 1,442 kg; presupuesto 2,212 kg.
- Evidencia: `01_CAD/Prototipo_P2/P2_04_20261016/` (`ESTADO_ENTREGA.md`, `RESUMEN_ENTREGA.json`, `HUELLAS_ENTREGA.json`).
