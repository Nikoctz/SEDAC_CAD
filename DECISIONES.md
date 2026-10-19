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

---

**Propuestas recibidas del proyecto ChatGPT el 2026-10-19** (`07_ENLACE_CHATGPT/Entrada_20261019.md`).
Estado `revisar`: **ninguna está adoptada**. Se registran para no perderlas y para que su adopción o descarte quede trazable.

**D-12 — Tratamiento funcional de bordes en contacto textil**
Fecha: 2026-10-19 · Estado: revisar · Origen: propuesta externa (ChatGPT)
Sustituir el criterio de «redondear todas las aristas» por un criterio de exposición funcional: zona A (contacto textil bajo tensión o movimiento), zona B (contacto incidental) y zona C (interfaz funcional). Los bordes de zona A deben tener transición continua, sin rebabas ni aristas cortantes, con acabado definido por evidencia de fabricación y ensayos. El radio de 0,5 mm **no se considera validado** mientras no haya ensayos de compatibilidad y desgaste. El redondeo parcial de P2.05 (236/472) sigue abierto.
Verificado por el agente: el redondeo parcial y la parada del constructor son ciertos (corrida `Nueva_20261019_060807`).

**D-13 — Evidencia auditable de restricciones CAD**
Fecha: 2026-10-19 · Estado: revisar · Origen: propuesta externa (ChatGPT)
Verificar el estado de restricciones de los bocetos funcionales y estructurales de P2.05 en Inventor y conservar evidencia: pieza y versión, boceto, estado (Fully/Under/Over/Unknown), captura visual, versión del software y vínculo al commit y al SHA-256 del archivo. Las excepciones se justifican. No se declarará cerrado sin resultados verificables.
**Sin verificar**: la propiedad `PlanarSketch.ConstraintStatus` que propone usar (el MCP de Inventor responde «Not connected to Inventor»).

**D-14 — Sensibilidad del margen estructural**
Fecha: 2026-10-19 · Estado: revisar · Origen: propuesta externa (ChatGPT)
El margen mínimo 2,247 frente al umbral 2,20 equivale a una reserva del **2,14 %** de demanda *si* el modo de falla gobernante admite relación inversa lineal entre margen y demanda (supuesto, no medido). Identificar primero el caso gobernante y después estudiar masa y centro de gravedad reales, apoyos, reparto, excentricidad, tolerancias y modos de falla adicionales. El 70/30 y la excentricidad de 107,5 mm permanecen como hipótesis no medidas. No se declarará robustez a partir del margen nominal aislado.
Verificado por el agente: las tres cuentas se reproducen exactas (2,136 % · 0,71495 · 109,80 mm).

**D-15 — Validación escalonada y alcance de los ensayos con personas**
Fecha: 2026-10-19 · Estado: revisar · Origen: propuesta externa (ChatGPT)
Adoptar una secuencia de validación en cuatro fases: 0) preparación técnica y análisis de riesgos; 1) banco mecánico sin personas; 2) sistema completo con carga inerte; 3) evaluación con personas solo con autorización documentada. Cada fase necesita, **antes** de empezar, condiciones de ensayo, instrumentos, criterios cuantitativos de aceptación y parada, evidencia trazable y decisión formal de avance. Una fase no autoriza la siguiente.
Se distingue la **Etapa 3 de Despega (dic 2026 – ene 2027)**, que exige validación técnica y comercial, del **piloto de funcionalidad de la preincubación (abril–diciembre 2027)**. Queda pendiente confirmar con la organización qué evidencia admite cada etapa.
P2.04 y P2.05 no están liberados para ensayos con personas. Ningún avance se presumirá a partir de resultados solo analíticos o de CAD.
