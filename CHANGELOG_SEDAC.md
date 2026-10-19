# CHANGELOG — SEDAC_CAD

Registra cambios **realizados** sobre el proyecto. No ideas, no planes, no propuestas.
Formato: fecha · versión/ámbito · descripción · evidencia.

---

## 2026-10-19

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
