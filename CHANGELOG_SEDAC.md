# CHANGELOG — SEDAC_CAD

Registra cambios **realizados** sobre el proyecto. No ideas, no planes, no propuestas.
Formato: fecha · versión/ámbito · descripción · evidencia.

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
