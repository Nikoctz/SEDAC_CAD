# ESTADO ACTUAL — SEDAC_CAD

Última actualización: 2026-10-19
Alcance: estado vigente. No repite `CONTEXTO_SEDAC.md`.

## Versión vigente

- **P2.04** — `01_CAD/Prototipo_P2/P2_04_20261016/`
- Base: doble canal abierto 6061-T6 de 32 × 24 × 3 mm, largo 480 mm, separados 190 mm; interfaz lumbar y yugos superiores; cuna textil; panel HDPE de 1 mm.
- Masa CAD rígida y protectores: **1,442 kg**. Presupuesto con textiles: **2,212 kg**. No incluye bomba ni agua.
- **P2.05 no está cerrado.** P2.04 sigue siendo prediseño, no liberado a fabricación ni uso con personas.

## Estado de Git

- Repositorio local, rama `main`.
- Baseline: **`20f1ef3`** — "Baseline inicial SEDAC antes de P2.05" (2026-10-18 22:30).
- Commit vigente (HEAD): **`0f7d03b`** — "Gobierno: corregir estado, registrar D-10/D-11, requisitos de las convocatorias y enlace con ChatGPT" (2026-10-19).
- Historial reciente: `e27cf4e` — "P2.05: copia de trabajo sobre P2.04, parametros coherentes con la geometria y calculo regenerado" (2026-10-19, 148 archivos) sobre `f26f010` — "Agregar contexto compartido para agentes SEDAC".
- Sin remoto configurado: el repositorio solo existe en este equipo, dentro de una carpeta sincronizada en la nube, que es la **única copia de seguridad** (advertencia en `MAPA_DEL_REPOSITORIO.md`).
- **Árbol limpio** a 2026-10-19: no quedan carpetas ni archivos sin rastrear.
- Excluidos de Git por decisión intencional: `.codex/config.toml` (contiene rutas locales de este equipo, verificado), `tools/inventor-mcp/` (repositorio externo clonado), `.venv-inventor-mcp/`, `OldVersions/` y `01_CAD/Automatizacion/python_libs/` (retirado a la Papelera el 2026-10-19). No deben agregarse al repositorio.
- Mapa de la carpeta —qué es actual, qué es historia, qué está superado y qué se limpió el 2026-10-19—: `MAPA_DEL_REPOSITORIO.md`.

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
| Integración MCP dentro de OpenCode | **Configurada.** Existe sección `mcp` en `~/.config/opencode/opencode.json` (servidor `inventor`, declarado `enabled: false`) y `status()` responde desde OpenCode («Not connected to Inventor»). Lectura estructural del ensamblaje: **no reproducida en OpenCode** |

Nota: la verificación de lectura proviene de una sesión previa en Codex y no fue reproducida por mí en esta revisión.

Nota (2026-10-19): el servidor MCP `inventor` está declarado `enabled: false` y, aun así, la herramienta responde desde OpenCode. Queda por aclarar qué clave gobierna realmente ese interruptor y reproducir la lectura estructural en OpenCode.

## Skills instaladas

`10` skills versionadas en `.agents/skills/`:
`dfm-review`, `dfmea-design`, `fatigue-analysis`, `fea-structural`, `inventor-modeling`, `material-selection`, `test-planning`, `thermal-analysis`, `tolerance-stackup`, `trade-study`.

Son guías metodológicas. Enumerar herramientas (ANSYS, Abaqus, etc.) no significa que estén instaladas ni conectadas.

## Revisión de ingeniería P2.04

Realizada y versionada en `06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md`.

Verificado sobre archivos: 79 huellas SHA-256 coincidentes; ZIP de 80 entradas sin error CRC; masa recalculada 1,442328 kg; 54 piezas y 83 ocurrencias; 82 operaciones actualizadas; cero interferencias rígidas nominales; cálculo de prediseño reproducido.

Hallazgo principal: **el redondeo de 0,5 mm de `Interfaz_lumbar_aligerada` figura como `aplicado: false`** (error COM) en `REDONDEOS.json`, aunque el informe lo da por incluido.

## Programas de financiamiento (2026)

Ambos vigentes. Requisitos, plazos y citas: `REQUISITOS_SEDAC.md`.

- **Vector 2026** (Centro de Innovación, FING USACH): inscrito; al 2026-10-19 va por la **clase 8**. **Lions Cage el 9 de diciembre** (40 % de la selección y es un pitch **en inglés**); Demo Day el 16 de diciembre. Autodiagnóstico TRL/IRL/CRL: se repite periódicamente, **todavía básico y sin registro versionado**.
- **Despega USACH 2026** (DINEM / INNOVO USACH): inscrito; **sesión 1 el 2026-10-19** (Etapa 1, Ideación, octubre–noviembre 2026). **Etapa 3: Validación, diciembre 2026 – enero 2027**: exige validación técnica y comercial, y pesa **50 % de la nota de finalistas**. Final en marzo 2027.
- **Premio:** hasta **$2.000.000 CLP** para actividades críticas, incluyendo expresamente el **desarrollo de prototipos**; **+25 %** si el proyecto es liderado por mujer.
- **Uso de IA generativa: declarado** ante el organizador (lo exige Vector §8).
- **Regla derivada, en vigor:** no introducir datos personales de terceros ni información confidencial en herramientas de IA. Afecta directamente a los **datos antropométricos de usuarios** listados en «Datos físicos pendientes de medir».
- **Tensión declarada, sin resolver:** los programas piden piloto con **usuarios reales** (TRL 6–7) y este proyecto **no está liberado a uso con personas**. No se declarará ninguna validación que no exista.

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

**Con el calendario de los programas encima, el hito que manda todo es la Etapa 3: Validación de Despega (diciembre 2026 – enero 2027)**, que exige validación técnica y pesa el 50 % de la nota de finalistas; y el **9 de diciembre** (Lions Cage de Vector, pitch en inglés). Eso pone fecha a tres cosas que hasta hoy parecían técnicas y ahora son entregables:

- **Pendiente 5** (tolerancias y proceso de fabricación real): sin prototipo no hay validación que mostrar.
- **Pendiente 6** (FEA, fatiga, pandeo): es la evidencia del TRL que se declare. No se declarará un nivel que no esté respaldado.
- **Medición real de la bomba**: `02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md` sigue **en blanco**.
