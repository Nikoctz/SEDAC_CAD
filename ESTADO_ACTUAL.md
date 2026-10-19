# ESTADO ACTUAL — SEDAC_CAD

Última actualización: 2026-10-18
Alcance: estado vigente. No repite `CONTEXTO_SEDAC.md`.

## Versión vigente

- **P2.04** — `01_CAD/Prototipo_P2/P2_04_20261016/`
- Base: doble canal abierto 6061-T6 de 32 × 24 × 3 mm, largo 480 mm, separados 190 mm; interfaz lumbar y yugos superiores; cuna textil; panel HDPE de 1 mm.
- Masa CAD rígida y protectores: **1,442 kg**. Presupuesto con textiles: **2,212 kg**. No incluye bomba ni agua.
- **P2.05 no está cerrado.** P2.04 sigue siendo prediseño, no liberado a fabricación ni uso con personas.

## Estado de Git

- Repositorio local, rama `main`.
- Baseline: **`20f1ef3`** — "Baseline inicial SEDAC antes de P2.05" (2026-10-18).
- Árbol limpio al momento de esta revisión.
- Excluidos de Git por decisión intencional: `.codex/config.toml` (contiene rutas locales de este equipo) y `tools/inventor-mcp/` (repositorio externo clonado). También se ignoran `.venv*/` y `OldVersions/`. No deben agregarse al repositorio.

## MCP de Inventor — estado

**Configurado y verificado en modo lectura desde Codex**, en este equipo con Autodesk Inventor 2027.1.

Evidencia de la verificación previa (reportada por el responsable, sesión en Codex):
- Conexión COM exitosa: `"Connected to running Inventor 2027.1"`.
- Con `SEDAC_P2_03.iam` abierto, `get_document_info()` leyó correctamente el documento.
- Lecturas estructurales correctas del ensamblaje: 131 ocurrencias activas, 51 archivos de pieza únicos, 390 restricciones, 1 componente grounded.
- Configuración declarada en `.codex/config.toml` (no versionado, exclusión intencional). El intérprete `.venv-inventor-mcp/Scripts/python.exe` y `tools/inventor-mcp/src/server.py` existen en disco.

Separación de estados:

| Ámbito | Estado |
|---|---|
| Lectura estructural desde Codex | **Verificada y funcional** |
| Compatibilidad de lectura | Funcional, con **al menos una incompatibilidad menor** detectada en una consulta geométrica (`Coordinate`), atribuida a compatibilidad parcial Inventor 2027.1 / MCP |
| Escritura / modificación CAD mediante MCP | **Todavía no validada** |
| Integración MCP dentro de OpenCode | **Todavía no configurada ni verificada** (no hay sección `mcp` en `~/.config/opencode/opencode.json`) |

Nota: la verificación de lectura proviene de una sesión previa en Codex y no fue reproducida por mí en esta revisión.

## Skills instaladas

`10` skills versionadas en `.agents/skills/`:
`dfm-review`, `dfmea-design`, `fatigue-analysis`, `fea-structural`, `inventor-modeling`, `material-selection`, `test-planning`, `thermal-analysis`, `tolerance-stackup`, `trade-study`.

Son guías metodológicas. Enumerar herramientas (ANSYS, Abaqus, etc.) no significa que estén instaladas ni conectadas.

## Revisión de ingeniería P2.04

Realizada y versionada en `06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md`.

Verificado sobre archivos: 79 huellas SHA-256 coincidentes; ZIP de 80 entradas sin error CRC; masa recalculada 1,442328 kg; 54 piezas y 83 ocurrencias; 82 operaciones actualizadas; cero interferencias rígidas nominales; cálculo de prediseño reproducido.

Hallazgo principal: **el redondeo de 0,5 mm de `Interfaz_lumbar_aligerada` figura como `aplicado: false`** (error COM) en `REDONDEOS.json`, aunque el informe lo da por incluido.

## Pendientes principales para P2.05

1. Redondeo lumbar ausente y criterio de aceptación de bordes de contacto.
2. Separar parámetros de geometría, hipótesis analíticas y reservas de masa; hoy varios campos del JSON no gobiernan la geometría.
3. Acreditar bocetos totalmente restringidos.
4. Margen analítico mínimo 2,247 frente a umbral 2,20: revisar sensibilidad a apoyos, excentricidad y reparto.
5. Tolerancias de pasador/separador y proceso de fabricación real (mecanizado, no chapa doblada ni soldada).
6. Cerrar FEA local, fatiga y pandeo distorsional.
7. Definir liberación de emergencia y compatibilidad manguera/EPP.
8. Regeneración de extremo a extremo: hoy el cálculo y los documentos no se regeneran con el CAD.

## Datos físicos pendientes de medir

- Bomba: masa llena y vacía, centro de masa, envolvente, tapa, manguera y controles.
- Bolsa Scotty y arnés: costuras, anclajes, anchos y puntos de apoyo.
- Textiles, acolchados, hebillas y cierres: selección, masa y temperatura de servicio.
- Antropometría de usuarios y recorrido real de las cintas.
- Herrajes: proveedores, propiedades y par de montaje.

## Próximo paso recomendado

Medir la bomba y el arnés antes de decidir cotas; en paralelo, cerrar el redondeo lumbar y hacer coherentes geometría, parámetros y cálculo. No reducir masa comprometiendo seguridad.
