# DECISIONES TÉCNICAS — SEDAC_CAD

Registro de decisiones adoptadas. Cada entrada indica fecha, decisión, motivo y estado.
Formato de estado: `adoptada` | `revisar` | `descartada`.

---

**D-01 — P2.04 pasa a ser baseline de diseño anterior a P2.05**
Fecha: 2026-10-18 · Estado: adoptada
P2.04 queda congelado como punto de partida verificable. P2.05 se construye sobre él, sin reescribir su historia.

**D-02 — No adelgazar piezas estructurales solo para reducir masa**
Fecha: 2026-10-18 · Estado: adoptada
La masa no justifica por sí sola reducir secciones resistentes. Cualquier aligeramiento debe venir de simplificación o de evidencia, no de recortar margen.

**D-03 — Simplificación arquitectónica antes que optimización ciega**
Fecha: 2026-10-18 · Estado: adoptada
Menos piezas y uniones desmontables antes que optimizar con cálculo sobre una arquitectura aún no decidida. Recomendable antes de invertir en FEA o fatiga.

**D-04 — Liberación de emergencia como requisito crítico**
Fecha: 2026-10-18 · Estado: adoptada
El sistema debe poder separarse del usuario de forma rápida, accesible y con guantes. No es un extra opcional.

**D-05 — Compatibilidad manguera/EPP/antropometría pendiente**
Fecha: 2026-10-18 · Estado: adoptada (pendiente de datos)
El recorrido de la manguera, la interferencia con equipo de protección personal y las tallas de usuario no están verificados. Bloquea cerrar el diseño fabricable.

**D-06 — 2 kg es un objetivo de masa, no un criterio que justifique comprometer seguridad**
Fecha: 2026-10-18 · Estado: adoptada
El presupuesto actual es 2,212 kg. Superar el objetivo es aceptable mientras no se degrade resistencia, retención ni liberación.

**D-07 — El IMU no se utilizará como sustituto de la medición de fuerzas**
Fecha: 2026-10-18 · Estado: adoptada
Un IMU mide movimiento y orientación; no mide fuerza ni presión. No se declararán cargas a partir de él.

**D-08 — Git será el control de versiones del proyecto**
Fecha: 2026-10-18 · Estado: adoptada
El historial se gestiona con Git desde el baseline `20f1ef3`. Un commit por cambio significativo, con mensaje descriptivo.

**D-09 — Codex y OpenCode trabajan sobre la misma carpeta local**
Fecha: 2026-10-18 · Estado: adoptada
Ambos agentes operan en `SEDAC_CAD` y comparten `AGENTS.md`, skills y estado. Regla de un solo escritor: ver `AGENTS.md`. Para evitar fragmentación, toda decisión durable se registra aquí y en `CHANGELOG_SEDAC.md`, no solo en la conversación.

**D-10 — El repositorio no sale del PC; el enlace con ChatGPT es un único paquete regenerado**
Fecha: 2026-10-19 · Estado: adoptada
El enlace con el proyecto ChatGPT se hace con `PAQUETE_CHATGPT.md`, generado por `GENERAR_PAQUETE.ps1` (con revisión de privacidad automática) y pegado en el chat. **No se sube el repositorio completo ni un ZIP de la carpeta**: llevan rutas locales (`.codex/config.toml` las contiene, verificado), 158 MB de historia de Git, `.venv-inventor-mcp`, `OldVersions/` y la guía personal; y sobre todo **compiten con la versión vigente** dentro del mismo proyecto, que es el fallo de «un documento que contradice a su propio dato».
El ZIP que estaba subido fue eliminado por el responsable el 2026-10-19, y desde esa fecha el proyecto ChatGPT no tiene ningún archivo del repositorio subido.
Papel de cada fuente: **Notion** manda en requisitos y plazos; **el paquete** manda en estado técnico; lo que vuelva de ChatGPT entra como `supuesto` o `hipótesis` hasta que lo respalde un archivo o un cálculo de este repositorio.

**D-11 — Alcance del conector de Notion, por acotar**
Fecha: 2026-10-19 · Estado: revisar
El conector de ChatGPT alcanza **todo** el espacio de Notion, no solo las páginas del proyecto. Como Vector §8 y la Ley 21.719 (vigencia plena desde el 2026-12-01) exigen no exponer datos personales de terceros ni información confidencial a herramientas de IA, conviene limitar el conector a las páginas del proyecto. **No adoptada**: es decisión del responsable y no se ha verificado si el conector permite acotarlo.
