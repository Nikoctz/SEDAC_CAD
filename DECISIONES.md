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
