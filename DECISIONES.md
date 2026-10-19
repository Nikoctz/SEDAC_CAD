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
**Aclaración (2026-10-19, hecho verificado por el agente):** este agente **no tiene acceso a Notion** — ni conector ni integración MCP (la lista de servidores MCP expuesta está vacía) — y la única vía disponible, un navegador, pide iniciar sesión (`notion.so/login`). Por tanto D-11 se refiere al conector de la cuenta de ChatGPT del responsable, **no** al acceso de los agentes. Lo que sí depende de este repositorio ya está resuelto: **ninguna afirmación sobre Notion puede entrar como `hecho`** en la documentación si no la aporta el responsable.

---

**Decisiones adoptadas el 2026-10-19 con autorización expresa del responsable**

El responsable delegó el 2026-10-19 la toma de decisiones técnicas («toma tú las decisiones importantes»). Las cuatro siguientes se adoptan **con argumento breve, fecha y reversibilidad**, y con una regla de límite declarada:

> **La delegación alcanza a criterios, orden de trabajo y gobernanza. No alcanza a mediciones.** Cuando una decisión exige un dato que no existe, deja de ser decisión y pasa a ser ensayo: esos puntos quedan `pendiente` y **no** se rellenan por decreto, ni por el agente ni por una IA externa.

Origen de las propuestas: `07_ENLACE_CHATGPT/Entrada_20261019.md`. Verificación previa de sus afirmaciones: ese mismo archivo, §2.

**D-12 — Tratamiento funcional de bordes en contacto textil**
Fecha: 2026-10-19 · Estado: **adoptada** · Propuesta: proyecto ChatGPT · Adopción: agente, con autorización del responsable
Sustituir el criterio de «redondear todas las aristas» por un criterio de exposición funcional: zona A (contacto textil bajo tensión o movimiento), zona B (contacto incidental) y zona C (interfaz funcional). Los bordes de zona A deben tener transición continua, sin rebabas ni aristas cortantes, con acabado definido por evidencia de fabricación y ensayos. El radio de 0,5 mm **no se considera validado** mientras no haya ensayos de compatibilidad y desgaste. El redondeo parcial de P2.05 (236/472) sigue abierto.
*Argumento:* el criterio vigente —«todas las aristas» y, si falla, «el grupo mayor»— es un criterio **de la herramienta**, no del diseño: `LEEME_P2_05.md` §3 ya midió que las 236 aristas son «un subconjunto arbitrario por orden de enumeración… no es el criterio correcto». Adoptar el criterio funcional **no exige ningún dato nuevo** (solo clasificar las superficies alcanzables por las cintas) y prohíbe presentar 0,5 mm como validado.
*Regla añadida por el agente:* **el aviso del constructor no se silencia.** Mientras no exista la clasificación, la corrida debe seguir terminando en `ERROR.txt` y sin `ESTADO_OK.txt`. Silenciarlo para obtener una corrida en verde reproduciría exactamente el fallo de P2.04 —un sello de «correcto» junto a un pendiente declarado—. Por ese motivo se **descarta** la opción «dejar el lumbar sin redondeo declarado para que la corrida cierre sin avisos» (`LEEME_P2_05.md` §7, opción 4).
*Consecuencia:* el «redondeo parcial 236/472» queda declarado como **lo que la herramienta pudo hacer**, no como decisión de diseño. La clasificación A/B/C queda `pendiente`: necesita el recorrido y la tensión reales de las cintas.

**D-13 — Evidencia auditable de restricciones CAD**
Fecha: 2026-10-19 · Estado: **adoptada** · Propuesta: proyecto ChatGPT · Adopción: agente
Verificar el estado de restricciones de los bocetos funcionales y estructurales de P2.05 en Inventor y conservar evidencia: pieza y versión, boceto, estado (Fully/Under/Over/Unknown), captura visual, versión del software y vínculo al commit y al SHA-256 del archivo.
*Argumento:* el control solo **añade** evidencia; no cambia geometría y su coste es una lectura. Con dos matices: (a) **plan B** — si `PlanarSketch.ConstraintStatus` no existe o falla en Inventor 2027.1, vale la evidencia visual, que muestre nombre de pieza, boceto, cotas y estado; (b) el objetivo es que **ninguna libertad sea desconocida**, no que todos los bocetos estén fijados: una subrestricción intencional y justificada es aceptable.
*Estado de ejecución:* **no ejecutada.** Inventor no está conectado desde OpenCode y la propiedad de la API no está comprobada. No se declarará cerrado sin evidencia guardada en el repositorio.

**D-14 — Sensibilidad del margen estructural**
Fecha: 2026-10-19 · Estado: **adoptada** · Propuesta: proyecto ChatGPT · Adopción: agente
El margen mínimo 2,247 frente al umbral 2,20 equivale a una reserva del **2,14 %** de demanda *si* el modo de falla gobernante admite relación inversa lineal entre margen y demanda (supuesto, no medido). Identificar primero el caso gobernante y después estudiar masa y centro de gravedad reales, apoyos, reparto, excentricidad, tolerancias y modos de falla adicionales. El reparto 70/30 y la excentricidad de 107,5 mm permanecen como hipótesis no medidas. No se declarará robustez a partir del margen nominal aislado.
*Argumento:* adoptarla solo **restringe** lo que se puede afirmar, que es la dirección segura, y ordena el gasto (medir antes de simular). Añade una urgencia concreta: con una reserva de 2,14 %, pasar de un reparto 70/30 a 71,5/28,5 agota el margen. Es decir, **el margen no es robusto frente a nuestras propias hipótesis no medidas**, así que medir masa y centro de gravedad reales pesa más que cualquier FEA.
*Verificado:* las tres cuentas se reproducen exactas (2,136 % · 0,71495 · 109,80 mm).

**D-15 — Validación escalonada y alcance de los ensayos con personas**
Fecha: 2026-10-19 · Estado: **adoptada** · Propuesta: proyecto ChatGPT · Adopción: agente
Secuencia de validación en cuatro fases: 0) preparación técnica y análisis de riesgos; 1) banco mecánico sin personas; 2) sistema completo con carga inerte; 3) evaluación con personas solo con autorización documentada. Cada fase necesita, **antes** de empezar, condiciones de ensayo, instrumentos, criterios de aceptación y parada, evidencia trazable y decisión formal de avance. Una fase no autoriza la siguiente.
*Argumento:* solo restringe (no permite declarar más de lo ensayado) y ordena el gasto hacia lo barato y productivo —banco y carga inerte—, que es justo la «validación técnica» que pide la Etapa 3. Encaja con el calendario: dic 2026 – ene 2027 es validación **técnica**, no pilotaje humano.
*Distinción de etapas:* la **Etapa 3 de Despega (dic 2026 – ene 2027)** exige validación técnica y comercial; el **piloto de funcionalidad con actores externos o usuarios reales** es un hito del **Programa de Preincubación (abril–diciembre 2027)** — bases, apartado 9.c. Queda `pendiente` confirmar con la organización qué evidencia admite cada etapa.
P2.04 y P2.05 no están liberados para ensayos con personas. Ningún avance de fase se presumirá a partir de resultados solo analíticos o de CAD.
