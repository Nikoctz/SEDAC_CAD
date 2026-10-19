# PAQUETE DE CONTEXTO SEDAC

Generado: 2026-10-19 07:26  |  por: 07_ENLACE_CHATGPT/GENERAR_PAQUETE.ps1
Uso: pegar este archivo entero (o subirlo como documento del proyecto). No editar a mano.

Este documento lo ha escrito el repositorio SEDAC_CAD de este PC. Los numeros salen de
los archivos del proyecto, no de la memoria de nadie.

---

## 0. Como quiero que trabajes con este documento

1. Este documento es la version vigente. Si algo que recuerdes de conversaciones
   anteriores contradice lo que aqui dice, manda este documento.
2. Marca CADA afirmacion que hagas como **[hecho]**, **[calculo]**, **[supuesto]** o
   **[hipotesis]**:
   - **[hecho]** solo si lo respalda un archivo o comando citado aqui.
   - **[calculo]** si es reproducible con una formula o un numero que aparezca aqui.
   - **[supuesto]** si es un valor que se adopta sin medir.
   - **[hipotesis]** si es una condicion aun no comprobada.
3. Si falta un dato, escribe **pendiente**. No lo rellenes con un valor plausible.
4. No declares seguridad, comodidad, resistencia ni cumplimiento normativo que no este
   demostrado por un archivo, un ensayo o un calculo trazable.
5. No inventes resultados de ensayos, FEA, propiedades de materiales ni normas.
6. Distingue siempre lo comprobado de lo que falta por comprobar.
7. Fuentes de cada cosa: el estado tecnico (masas, piezas, pendientes, numeros) sale de
   este documento. Los requisitos y plazos del programa tambien los ves tu en mi espacio de
   Notion; la version citada esta en la seccion 5. Si algo se contradice, no decidas: dime
   el conflicto y que dice cada fuente.
8. Si una pagina de Notion no te aparece, dilo. No la supongas ni la resumas de memoria.
9. No reproduzcas datos personales de terceros (nombres, medidas corporales, salud, imagenes).

---

## 1. Estado vigente (ESTADO_ACTUAL.md, literal)

## ESTADO ACTUAL — SEDAC_CAD

Última actualización: 2026-10-19
Alcance: estado vigente. No repite `CONTEXTO_SEDAC.md`.

### Versión vigente

- **P2.04** — `01_CAD/Prototipo_P2/P2_04_20261016/`
- Base: doble canal abierto 6061-T6 de 32 × 24 × 3 mm, largo 480 mm, separados 190 mm; interfaz lumbar y yugos superiores; cuna textil; panel HDPE de 1 mm.
- Masa CAD rígida y protectores: **1,442 kg**. Presupuesto con textiles: **2,212 kg**. No incluye bomba ni agua.
- **P2.05 no está cerrado.** P2.04 sigue siendo prediseño, no liberado a fabricación ni uso con personas.

### Estado de Git

- Repositorio local, rama `main`.
- Baseline: **`20f1ef3`** — "Baseline inicial SEDAC antes de P2.05" (2026-10-18 22:30).
- Commit vigente (HEAD): **`0f7d03b`** — "Gobierno: corregir estado, registrar D-10/D-11, requisitos de las convocatorias y enlace con ChatGPT" (2026-10-19).
- Historial reciente: `e27cf4e` — "P2.05: copia de trabajo sobre P2.04, parametros coherentes con la geometria y calculo regenerado" (2026-10-19, 148 archivos) sobre `f26f010` — "Agregar contexto compartido para agentes SEDAC".
- Sin remoto configurado: el repositorio solo existe en este equipo, dentro de una carpeta sincronizada en la nube, que es la **única copia de seguridad** (advertencia en `MAPA_DEL_REPOSITORIO.md`).
- **Árbol limpio** a 2026-10-19: no quedan carpetas ni archivos sin rastrear.
- Excluidos de Git por decisión intencional: `.codex/config.toml` (contiene rutas locales de este equipo, verificado), `tools/inventor-mcp/` (repositorio externo clonado), `.venv-inventor-mcp/`, `OldVersions/` y `01_CAD/Automatizacion/python_libs/` (retirado a la Papelera el 2026-10-19). No deben agregarse al repositorio.
- Mapa de la carpeta —qué es actual, qué es historia, qué está superado y qué se limpió el 2026-10-19—: `MAPA_DEL_REPOSITORIO.md`.

### MCP de Inventor — estado

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
| Integración MCP dentro de OpenCode | **Configurada.** Existe sección `mcp` en `~/.config/opencode/opencode.json` (servidor `inventor`, declarado `enabled: false`) y `status()` responde desde OpenCode («Not connected to Inventor»). Lectura estructural del ensamblaje: **no reproducida en OpenCode** |

Nota: la verificación de lectura proviene de una sesión previa en Codex y no fue reproducida por mí en esta revisión.

Nota (2026-10-19): el servidor MCP `inventor` está declarado `enabled: false` y, aun así, la herramienta responde desde OpenCode. Queda por aclarar qué clave gobierna realmente ese interruptor y reproducir la lectura estructural en OpenCode.

### Skills instaladas

`10` skills versionadas en `.agents/skills/`:
`dfm-review`, `dfmea-design`, `fatigue-analysis`, `fea-structural`, `inventor-modeling`, `material-selection`, `test-planning`, `thermal-analysis`, `tolerance-stackup`, `trade-study`.

Son guías metodológicas. Enumerar herramientas (ANSYS, Abaqus, etc.) no significa que estén instaladas ni conectadas.

### Revisión de ingeniería P2.04

Realizada y versionada en `06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md`.

Verificado sobre archivos: 79 huellas SHA-256 coincidentes; ZIP de 80 entradas sin error CRC; masa recalculada 1,442328 kg; 54 piezas y 83 ocurrencias; 82 operaciones actualizadas; cero interferencias rígidas nominales; cálculo de prediseño reproducido.

Hallazgo principal: **el redondeo de 0,5 mm de `Interfaz_lumbar_aligerada` figura como `aplicado: false`** (error COM) en `REDONDEOS.json`, aunque el informe lo da por incluido.

### Programas de financiamiento (2026)

Ambos vigentes. Requisitos, plazos y citas: `REQUISITOS_SEDAC.md`.

- **Vector 2026** (Centro de Innovación, FING USACH): inscrito; al 2026-10-19 va por la **clase 8**. **Lions Cage el 9 de diciembre** (40 % de la selección y es un pitch **en inglés**); Demo Day el 16 de diciembre. Autodiagnóstico TRL/IRL/CRL: se repite periódicamente, **todavía básico y sin registro versionado**.
- **Despega USACH 2026** (DINEM / INNOVO USACH): inscrito; **sesión 1 el 2026-10-19** (Etapa 1, Ideación, octubre–noviembre 2026). **Etapa 3: Validación, diciembre 2026 – enero 2027**: exige validación técnica y comercial, y pesa **50 % de la nota de finalistas**. Final en marzo 2027.
- **Premio:** hasta **$2.000.000 CLP** para actividades críticas, incluyendo expresamente el **desarrollo de prototipos**; **+25 %** si el proyecto es liderado por mujer.
- **Uso de IA generativa: declarado** ante el organizador (lo exige Vector §8).
- **Regla derivada, en vigor:** no introducir datos personales de terceros ni información confidencial en herramientas de IA. Afecta directamente a los **datos antropométricos de usuarios** listados en «Datos físicos pendientes de medir».
- **Tensión declarada, sin resolver:** los programas piden piloto con **usuarios reales** (TRL 6–7) y este proyecto **no está liberado a uso con personas**. No se declarará ninguna validación que no exista.

### Pendientes principales para P2.05

1. Redondeo lumbar ausente y criterio de aceptación de bordes de contacto.
2. Separar parámetros de geometría, hipótesis analíticas y reservas de masa; hoy varios campos del JSON no gobiernan la geometría.
3. Acreditar bocetos totalmente restringidos.
4. Margen analítico mínimo 2,247 frente a umbral 2,20: revisar sensibilidad a apoyos, excentricidad y reparto.
5. Tolerancias de pasador/separador y proceso de fabricación real (mecanizado, no chapa doblada ni soldada).
6. Cerrar FEA local, fatiga y pandeo distorsional.
7. Definir liberación de emergencia y compatibilidad manguera/EPP.
8. Regeneración de extremo a extremo: hoy el cálculo y los documentos no se regeneran con el CAD.

### Datos físicos pendientes de medir

- Bomba: masa llena y vacía, centro de masa, envolvente, tapa, manguera y controles.
- Bolsa Scotty y arnés: costuras, anclajes, anchos y puntos de apoyo.
- Textiles, acolchados, hebillas y cierres: selección, masa y temperatura de servicio.
- Antropometría de usuarios y recorrido real de las cintas.
- Herrajes: proveedores, propiedades y par de montaje.

### Próximo paso recomendado

Medir la bomba y el arnés antes de decidir cotas; en paralelo, cerrar el redondeo lumbar y hacer coherentes geometría, parámetros y cálculo. No reducir masa comprometiendo seguridad.

**Con el calendario de los programas encima, el hito que manda todo es la Etapa 3: Validación de Despega (diciembre 2026 – enero 2027)**, que exige validación técnica y pesa el 50 % de la nota de finalistas; y el **9 de diciembre** (Lions Cage de Vector, pitch en inglés). Eso pone fecha a tres cosas que hasta hoy parecían técnicas y ahora son entregables:

- **Pendiente 5** (tolerancias y proceso de fabricación real): sin prototipo no hay validación que mostrar.
- **Pendiente 6** (FEA, fatiga, pandeo): es la evidencia del TRL que se declare. No se declarará un nivel que no esté respaldado.
- **Medición real de la bomba**: `02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md` sigue **en blanco**.

---

## 2. Decisiones ya adoptadas (DECISIONES.md, literal)

## DECISIONES TÉCNICAS — SEDAC_CAD

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

## 3. Cambios registrados (CHANGELOG_SEDAC.md, literal)

## CHANGELOG — SEDAC_CAD

Registra cambios **realizados** sobre el proyecto. No ideas, no planes, no propuestas.
Formato: fecha · versión/ámbito · descripción · evidencia.

---

### 2026-10-19

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

---

### 2026-10-18

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

### 2026-10-17

**Revisión de ingeniería de P2.04**
Se auditó la entrega P2.04 con verificación de archivos: 79 huellas SHA-256 coincidentes; ZIP de 80 entradas sin error CRC; masa CAD recalculada 1,442328 kg; cálculo de prediseño reproducido.
- Hallazgo: redondeo de 0,5 mm de `Interfaz_lumbar_aligerada` con `aplicado: false` en `REDONDEOS.json`.
- Entregable: `06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md`.
- Evidencia: informe versionado en el baseline `20f1ef3`.

---

### 2026-10-16 / 2026-10-17

**Entrega P2.04**
Prediseño de doble canal abierto con cuna textil y alas de cinturón flexibles. 54 piezas, 83 ocurrencias, 246 restricciones. Masa rígida 1,442 kg; presupuesto 2,212 kg.
- Evidencia: `01_CAD/Prototipo_P2/P2_04_20261016/` (`ESTADO_ENTREGA.md`, `RESUMEN_ENTREGA.json`, `HUELLAS_ENTREGA.json`).

---

## 4. Numeros de la ultima construccion CAD (generados desde el repositorio)

- Carpeta de la corrida: Nueva_20261019_060807  (2026-10-19 06:11)
- Version del resumen: P2.05   fecha declarada: 2026-10-19

| dato | valor |
|---|---|
| masa rigida + protectores | 1.4420687346427812 kg |
| masa de referencias visuales (textiles provisionales) | 0.48115405180950926 kg |
| reserva textil | 0.65 kg |
| reserva adicional | 0.12 kg |
| presupuesto del sistema | 2.2120687346427812 kg |
| masa del sistema realmente medida | pendiente |
| interferencias | 0 |
| redondeos pendientes declarados | 1 |

Masa por grupo:

| grupo | kg |
|---|---|
| estructura | 0.56875841944370775 |
| uniones | 0.067520127186974685 |
| anclajes | 0.5602290385369032 |
| protecciones | 0.080759083995325887 |
| fijaciones | 0.16480206547986972 |

Redondeos declarados por pieza (aristas con radio aplicado):

| pieza | radio_mm | estado | redondeadas/total | criterio | pruebas de sondeo |
|---|---|---|---|---|---|
| Refuerzo_C_I | 0.35 | total | 46/46 | todas | 1 |
| Refuerzo_C_D | 0.35 | total | 46/46 | todas | 1 |
| Interfaz_lumbar_aligerada | 0.5 | parcial | 236/472 | grupo_mayor | 14 |
| Yugo_superior_I | 0.5 | total | 248/248 | todas | 1 |
| Yugo_superior_D | 0.5 | total | 248/248 | todas | 1 |

Nota: estado "parcial" significa que el redondeo pedido NO se aplico completo. En esa
situacion el constructor se detiene a proposito y no escribe el sello ESTADO_OK.txt.

---

## 5. Requisitos y plazos de los programas (REQUISITOS_SEDAC.md, literal)

## REQUISITOS — Programas Despega USACH 2026 y Vector 2026

**Qué es este documento.** Los requisitos y plazos de las dos convocatorias en las que se mueve el
proyecto, extraídos y ordenados desde los dos PDF que están en la raíz del repositorio. No es una
interpretación: cada afirmación remite a la sección de las bases donde se puede comprobar.

**Fuentes** (incorporadas al repositorio el 2026-10-19):

| archivo | páginas | qué es |
|---|---|---|
| `BASES-DESPEGA-USACH-2026.pdf` | 27 | Bases del concurso Despega USACH 2026 (DINEM / INNOVO USACH) |
| `Terminos-y-condiciones-Vector-2026.pdf` | 7 | Términos y condiciones del Programa Vector 2026 (Centro de Innovación FING USACH) |

**Estado de participación** (declarado por el responsable el 2026-10-19):

| programa | situación declarada |
|---|---|
| Vector 2026 | **Inscrito.** Va por la **clase 8** de las sesiones. Autodiagnóstico TRL/IRL/CRL: se repite periódicamente; hasta ahora, **básico**. |
| Despega USACH 2026 | **Inscrito.** La **primera sesión es el 2026-10-19** (hoy): arranca la Etapa 1, Ideación. |
| Uso de IA generativa | **Declarado** ante el equipo organizador. |

Lo que sigue son los requisitos de las bases; la situación declarada es la de la tabla de arriba.

---

### 1. Vector 2026 — «Startup Fraternity» (Centro de Innovación, Facultad de Ingeniería USACH)

**1.1 Calendario** (hecho, §4.6)

| etapa | fechas |
|---|---|
| Postulación | 20 de julio al 23 de agosto |
| Sesiones | 24 de agosto al 20 de noviembre |
| Lions Cage | 9 de diciembre |
| Demo Day | 16 de diciembre |

Las propias bases advierten que las fechas pueden sufrir modificaciones.

**1.2 Qué se exige para el certificado** (hecho, §4.5): asistencia ≥ 75 % (máximo 5 ausencias
justificadas) · realizar todas las actividades y tareas de los módulos · participar en la jornada
Lions Cage · asistir al Demo Day.

**1.3 Selección** (hecho, §5): 60 % plataforma + 40 % Lions Cage, que es **un pitch en inglés**. Los 6
mejores pasan al Demo Day.

**1.4 Madurez** (hecho, §2.1 y §4.3): el programa se rige por **TRL, IRL y CRL**; cada equipo debe
hacer un **autodiagnóstico** al inicio.

**1.5 Prototipos** (hecho, §2.1): entre los objetivos está la «creación de prototipos físicos y/o
digitales o formatos mínimos de validación».

**1.6 Propiedad intelectual** (hecho, §7): sigue siendo de los proponentes. Sólo la desarrollada por
funcionarios de la Universidad sigue el reglamento de la USACH (Res. 4085/2015).

**1.7 Obligaciones que afectan a cómo trabajamos** (hecho, §8 y §6.1) — **esto nos toca directamente:**

- «Cuando en el desarrollo de la propuesta se empleen herramientas de inteligencia artificial
  generativa, dicho uso deberá ser **declarado** ante el equipo organizador». → **Cumplido.**
- «Será responsabilidad de cada equipo **no incorporar en ellas datos personales de terceros ni
  información confidencial de la Universidad**». → Regla activa: la antropometría de usuarios y
  cualquier dato personal **no entra** en herramientas de IA ni en el paquete de contexto.
- Los datos personales se rigen por la Ley N° 19.628, reformada por la Ley N° 21.719, **plenamente
  vigente desde el 1 de diciembre de 2026**.
- §9: imagen, voz y nombre son datos personales y requieren consentimiento previo y expreso.

### 2. Despega USACH 2026 (DINEM / INNOVO USACH)

**2.1 Categorías** (hecho, §4): A) Innovación Científica Tecnológica · B) Innovación en Industrias
Creativas y Culturales · C) Innovación Social y desarrollo territorial.

**2.2 Etapas y umbrales** (hecho, §8)

| etapa | qué es | umbral |
|---|---|---|
| Postulación | formulario + certificado de alumno regular | admisibilidad |
| Etapa 1: Ideación | ciclo de hasta 7 talleres | ≥ 70 % (5 de 7) |
| Semifinalistas | formulario que recoge lo trabajado | hasta 36 proyectos + 6 cupos |
| Etapa 2: Negocios | ciclo de entrenamiento en modelo de negocios | **100 % de asistencia** |
| Etapa 3: Validación | ciclo práctico-teórico de validación técnica y comercial, máx. 6 semanas, con **mesas técnicas** | **100 % de asistencia**; el director/a debe asistir |
| Finalistas | informe de avance y resultados + informe de propuesta emprendedora | hasta 20 proyectos |
| Final | pitch comercial + plan de trabajo | hasta 10 ganadores |

**2.3 Calendario** (hecho, §11)

| etapa | fechas |
|---|---|
| Inscripción | Agosto – Octubre 2026 |
| Etapa 1: Ideación | Octubre – Noviembre 2026 |
| Etapa 2: Negocios | Diciembre 2026 |
| Etapa 3: Validación | Diciembre 2026 – Enero 2027 |
| Final | Marzo 2027 |
| Financiamiento | Abril – Noviembre 2027 |
| Nivelación de inglés | Abril – Noviembre 2027 |
| Pasantía internacional | Marzo – Diciembre 2027 |
| Programa de preincubación | Abril – Diciembre 2027 |

**2.4 Premios** (hecho, §9): hasta **$2.000.000 CLP** para «actividades críticas» de validación,
incluyendo expresamente el **desarrollo de prototipos**; **+25 % ($500.000)** para proyectos liderados
por mujeres; pasantía internacional; programa de preincubación; espacios de cowork.

**2.5 Qué exige la preincubación** (hecho, §9.c): prototipo temprano (MVP) con **validación técnica de
la incubadora** · **piloto de validación con actores externos o usuarios reales** · pitch técnico en
español e inglés · formulación de un subsidio real · nivelación de inglés.

**2.6 Criterios de evaluación** (hecho, §10)

- Semifinalistas: ajuste problema–solución 20 % · novedad y diferenciación 25 % · mercado y segmento
  15 % · equipo 10 % · componente por categoría 15 % · proceso formativo 15 %.
- Finalistas: etapa de validación 50 % · potencial de mercado 30 % · criterios de categoría 20 %.
- Ganadores: pitch 50 % + plan de trabajo 50 %.

**2.7 Escala TRL** (hecho, Anexo 1): TRL 1 idea básica · TRL 3 prueba de concepto · **TRL 4 validación
de componentes en laboratorio** · **TRL 5 componentes en entorno relevante** · **TRL 6 sistema en
entorno relevante** · **TRL 7 sistema en entorno real** · TRL 9 pruebas con éxito en entorno real.

**2.8 Propiedad intelectual** (hecho, §14): de los proponentes, con la misma excepción de funcionarios
de la Universidad.

### 3. Qué le exige esto al proyecto SEDAC

| lo que pide el programa | estado hoy en el repositorio | hueco |
|---|---|---|
| Validación técnica (TRL 4–6) | P2.05 abierto; FEA, fatiga y pandeo sin cerrar (pendiente 6) | falta evidencia de validación de componentes |
| Prototipo físico / MVP | sólo CAD; sin tolerancias ni proceso de fabricación decidido (pendiente 5) | **no existe prototipo** |
| Piloto con usuarios reales (TRL 6–7) | `ESTADO_ACTUAL.md`: no liberado a uso con personas | **conflicto real**: no se puede probar con personas sin demostrar seguridad |
| Autodiagnóstico TRL / IRL / CRL | hecho en Vector, pero **no se guarda** ninguno | falta el registro histórico de madurez |
| Pitch técnico en inglés (Vector) y en dos idiomas (Despega) | no consta | falta material y ensayo |
| **Declaración de uso de IA generativa** | declarado al organizador | **cumplido** |
| No poner datos personales de terceros en herramientas de IA | el generador del paquete filtra rutas locales y nombres | extender la regla a datos de usuarios y antropometría |
| Presupuesto de prototipo y ensayos | no consta | el financiamiento (hasta $2M + 25 %) puede cubrir mecanizado, materiales y ensayos |

### 4. Fechas frente a hoy (2026-10-19)

- **Despega USACH**: inscrito, y **hoy es la sesión 1** de la Etapa 1 (Ideación, octubre–noviembre
  2026). Después: Negocios en diciembre, **Validación en diciembre 2026 – enero 2027** y Final en
  marzo 2027. El hito duro es la **Etapa 3: Validación**, que exige validación técnica y pesa el 50 %
  de la nota de finalistas.
- **Vector**: va por la **clase 8**; las sesiones van hasta el 20 de noviembre, **Lions Cage el 9 de
  diciembre** (40 % de la selección, y es un pitch **en inglés**) y Demo Day el 16 de diciembre.
- Las bases advierten que las fechas pueden cambiar. Esto es lo que dicen los documentos.

### 5. Cómo se verifica

Cada afirmación remite a la sección de las bases (los propios PDF las numeran). Los PDF están en la
raíz del repositorio, **sin rastrear en git** a 2026-10-19. El texto se extrajo con `pdfminer` desde
el intérprete del proyecto; los `.txt` resultantes quedaron fuera del repositorio (carpeta temporal),
porque la fuente es el PDF.

### 6. Pendiente (lo tiene que declarar o hacer el responsable)

1. **Categoría de postulación** en Despega (A científica-tecnológica, B creativas o C social): no consta.
2. **Registrar el autodiagnóstico TRL/IRL/CRL**: se repite periódicamente en Vector, pero no se guarda
   ninguna copia. Es la evidencia del avance de madurez y conviene versionarla aquí.
3. **Protocolo de validación con usuarios reales**: no existe, y la Etapa 3 lo pide.
4. **Convenio de preincubación**: qué compromisos exige en materia de validación con personas.

---

## 6. Mis preguntas

## Preguntas para ChatGPT — SEDAC

Escribe aquí lo que quieras preguntar. Este archivo se pega tal cual dentro de
`PAQUETE_CHATGPT.md` (sección 6). Borra las preguntas ya resueltas para que el paquete no
crezca sin control.

Reglas rápidas:

- Una pregunta por bloque, numeradas.
- Si la respuesta debe ser un número o una decisión, dilo: «quiero un número y su fórmula»,
  «quiero dos alternativas y sus contras».
- No pidas datos de este PC; pide criterio de ingeniería.

---

### Preguntas pendientes

1. **Redondeo del lumbar (472 aristas).** El redondeo pedido de 0,5 mm falla si se aplica a
   las 472 aristas de golpe, pero funciona en cada mitad (236) por separado. ¿Cuál es el
   criterio de diseño correcto para decidir qué bordes de una pieza de aluminio que queda en
   contacto con cintas textiles deben romperse, y cuáles no? Quiero un criterio aplicable
   (no una lista de aristas).

2. **Bocetos de Inventor.** Cómo acreditar que un boceto queda totalmente restringido y qué
   evidencia dejar en el repositorio para que sirva en una auditoría.

3. **Margen 2,247 frente a umbral 2,20.** Qué sensibilidades conviene estudiar y en qué orden,
   sabiendo que el reparto de carga (70/30) y la excentricidad (107,5 mm) son hipótesis sin
   medir.

4. **Protocolo de validación con usuarios reales (plazo: diciembre 2026 – enero 2027).** El
   programa de financiamiento exige un piloto de validación con usuarios reales, y el proyecto
   **no está liberado a uso con personas** ni tiene la seguridad demostrada. Propón un protocolo
   de validación **por fases** (banco de pruebas → ensayo con carga inerte → y sólo después
   personas, si procede) que sea honesto y defendible: qué se mide en cada fase, con qué
   instrumento, qué criterio de parada, qué evidencia deja cada fase y qué NO se puede afirmar
   al terminar cada una.

---

*(plantilla: qué es `[hecho]` / `[calculo]` / `[supuesto]` / `[hipotesis]` se explica dentro
del propio paquete, en su sección 0.)*

(Si arriba solo aparece la plantilla, significa que no he escrito preguntas nuevas:
responde entonces a lo que te pida en el mensaje.)

---

## 7. Contexto historico

- CONTEXTO_SEDAC.md describe P0 y esta desactualizado respecto a P2.04. No se incluye aqui.
  En caso de conflicto, manda ESTADO_ACTUAL.md (seccion 1).
- Unidades del proyecto: milimetros. Escala maestra 1:1.
- P2.04 es la base vigente; P2.05 no esta cerrado y es borrador de trabajo.

---

## 8. Formato en que quiero tu respuesta

1. Empieza con un resumen de 5 lineas como maximo.
2. Despues, desarrolla con las marcas [hecho] / [calculo] / [supuesto] / [hipotesis]
   en cada afirmacion.
3. Si detectas una contradiccion entre dos partes de este documento, dilo aparte y
   senala cual crees que es el dato bueno y por que.
4. Termina con una seccion titulada exactamente PROPUESTA DE CAMBIO, redactada para
   copiar y pegar en DECISIONES.md o ESTADO_ACTUAL.md, sin adornos.
