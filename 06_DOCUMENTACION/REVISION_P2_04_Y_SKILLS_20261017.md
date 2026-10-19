# Revisión local de P2.04 y skills de Inventor

Fecha: 17/10/2026. Revisión de archivos, código, imágenes CAD y registros existentes. No se modificaron modelos, parámetros, generadores ni skills. No se abrió ni revalidó el ensamblaje en una sesión nueva de Inventor. Los resultados nativos citados son evidencia registrada por la entrega, no una nueva inspección COM.

## 1. Versión vigente y alcance

La última propuesta local identificada es **P2.04**, iniciada el 16/10 y cerrada el 17/10. Referencia: `00_GUIA_PERSONAL_SEDAC.md` y `01_CAD/Prototipo_P2/P2_04_20261016/`.

Archivo principal: `01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/SEDAC_P2_04.iam`, para Inventor 2027.1.

Los IPT de la raíz y `CONTEXTO_SEDAC.md` corresponden a P0 y no describen el diseño actual. Las memorias Mathcad/PDF de P2.02/P2.03 tampoco validan P2.04. No se consultó Notion ni el historial privado de conversaciones de Codex.

Arquitectura actual: dos canales abiertos 6061-T6 de 32 × 24 × 3 mm, largo 480 mm, separados 190 mm; interfaz lumbar y yugos superiores independientes; cuna textil de dos apoyos y abertura central nominal de 104 mm; panel HDPE de contacto de 1 mm; cinturón con alas flexibles. Ocho uniones M5×55, con pasadores huecos y separadores independientes. La bolsa no está representada como geometría medida: no se puede verificar su ajuste con estas vistas.

## 2. Comprobaciones independientes sobre los archivos

- Coinciden las **79 huellas SHA-256** de `HUELLAS_ENTREGA.json`.
- ZIP: **80 entradas**, sin errores CRC y sin diferencias de contenido respecto de sus archivos locales correspondientes.
- Manifiesto: **54 diseños de piezas y 83 ocurrencias**.
- Masa recalculada desde `MASAS_CAD.json`: **1,442327847 kg**, excluyendo referencias textiles.
- Presupuesto: 1,442328 + 0,650 + 0,120 = **2,212328 kg**, sin bomba ni agua. Supera 2 kg en **212 g**, aproximadamente 10,6 % del objetivo.
- La auditoría guardada declara actualización correcta; registra **82 operaciones con estado `kUpToDateHealth`**. El registro de interferencias rígidas está vacío.
- Se ejecutó en memoria el tramo de cálculo de `Soporte/calcular_p2_04.py`, omitiendo escrituras. Reproduce exactamente el margen mínimo **2,247130919**, la flecha **0,866676880 mm**, el giro ideal **3,176152176°** y el cierre residual de junta **282,223280 N** publicados.

Reproducibilidad numérica no equivale a validación del modelo mecánico. Una pieza con una operación omitida puede estar totalmente actualizada: la salud de operaciones no comprueba por sí sola el cumplimiento de la intención de diseño.

## 3. Hallazgos prioritarios

### A. Redondeo lumbar ausente: discrepancia comprobada

`Entrega/Inventor/REDONDEOS.json` informa `aplicado: false` para `Interfaz_lumbar_aligerada`, radio 0,5 mm, con error COM E_FAIL. Los dos canales y los dos yugos sí figuran con redondeo aplicado.

El informe de diseño, sección 2, afirma que el CAD incluye radios de 0,5 mm en interfaces, sin esta excepción. El constructor captura el fallo, aborta solo la transacción de redondeo y continúa; por ello puede terminar con `ESTADO_OK.txt` aunque falte ese acabado.

**Acción recomendada:** corregir el informe y tratar los radios de contacto requeridos como criterio explícito de aceptación. En una nueva revisión, identificar las aristas pertinentes y verificar el redondeo y desbarbado, en especial donde pasan cintas. No asumir que aplicar un radio a todas las aristas sustituye una revisión de abrasión.

### B. El JSON no es un control geométrico global

`generar_p2_04.py` tiene muchas coordenadas y medidas literales. Entre los campos geométricos declarados que no lee para construir están `ancho_panel`, `alto_panel`, `ancho_cuna`, `profundidad_cuna`, `hueco_manguera`, `ancho_cinta`, `espesor_cinta`, `espesor_cuerpo_lumbar` y `espesor_mejilla`.

Otros campos no leídos por ese generador son deliberadamente de cálculo o presupuesto; su ausencia no implica por sí sola un defecto. El problema es que algunos nombres sugieren control geométrico, pero cambiar solo su valor no cambia la pieza correspondiente.

Los apoyos, separación de pernos y dimensiones de puentes usados por cálculo tampoco se derivan automáticamente del sólido. Hay riesgo de recalcular una hipótesis que ya no corresponda al CAD tras una edición. El LEEME advierte correctamente esta limitación, pero no la elimina.

**Acción recomendada:** separar entradas de geometría, hipótesis analíticas y reservas; eliminar constantes duplicadas; comprobar dimensiones críticas del CAD frente al JSON tras cada regeneración.

### C. Editable no significa completamente parametrizado

El constructor crea bocetos nativos y parámetros de posición/profundidad de extrusión. No añade cotas ni restricciones geométricas explícitas que aseguren la definición completa de todos los contornos, ni comprueba su estado de restricción. La auditoría almacenada no registra `ConstraintStatus` o equivalente.

No se afirma que todos los bocetos estén libres: se concluye que **no está acreditado que estén totalmente restringidos**, como exige `inventor-modeling`.

Las 246 restricciones de ensamblaje posicionan 82 ocurrencias con tres planos cada una, más la interfaz lumbar fijada. Mantienen la colocación; no crean uniones físicas adaptativas ni simulan articulación textil, contacto o apriete.

### D. Margen analítico cercano al umbral y condicionado por apoyos

El mínimo 2,247 supera el umbral elegido 2,20 en aproximadamente **2,14 %** respecto de ese umbral. No es una reserva frente a todas las incertidumbres del producto ni un factor global certificado.

El cálculo presupone apoyos efectivos de hombro y cinturón, luz 380 mm, reparto 70/30 y excentricidad 107,5 mm. El propio informe excluye el caso de canal en voladizo. Debe estudiarse sensibilidad a cambios de apoyo, excentricidad, masa, reparto y flexibilidad de las conexiones antes de reducir sección o masa.

La masa transportada supuesta de 25 kg incluye el sistema auxiliar. Quedarían aproximadamente 22,788 kg para el resto del equipo dentro de ese escenario; falta comprobar la combinación real bomba/agua/accesorios.

### E. Tolerancias y proceso todavía abiertos

Los 0,2 mm nominales entre pasador Ø10 y alojamiento Ø10,2, así como el retranqueo nominal de 0,2 mm por extremo, necesitan cadenas de tolerancias, alineación de taladros y revisión de montaje. Cero interferencias nominales no acredita montabilidad ni apriete correcto.

El generador representa las interfaces como sólidos unidos; no entrega un proceso probado para fabricarlas. Deben definirse mecanizado, disponibilidad del perfil y acceso de herramientas. No convertirlas en chapa doblada o soldada conservando sin revisión las propiedades 6061-T6 del cálculo.

Tuercas, arandelas y tornillos requieren proveedores, propiedades y compatibilidad verificadas. La precarga de 2000 N no es un par de montaje autorizado.

### F. Regeneración parcial, no entrega reproducida de extremo a extremo

`CONSTRUIR_P2_04.ps1` genera manifiesto, CAD, masas, restricciones, vistas y STEP. No invoca `calcular_p2_04.py` ni recompone automáticamente resumen, informe, auditoría nativa, huellas y ZIP. Sus rutas a Python y a la biblioteca de Inventor son específicas de este equipo.

**Acción recomendada:** una secuencia futura de entrega debe recalcular, construir, auditar, reconciliar masas y parámetros, generar documentos y empaquetar. Si se mantiene el flujo actual, documentar todos esos pasos por separado.

## 4. Skills de Inventor: presencia frente a uso demostrado

### `inventor-modeling`

Hay dos copias idénticas: `.agents/skills/inventor-modeling/SKILL.md` y `tools/inventor-mcp/skills/inventor-modeling/SKILL.md`.

Puntos útiles: conversión mm/cm, evitar índices topológicos obsoletos, nombres explícitos de operaciones, transacciones, verificación volumétrica, materiales y guardado versionado. El servidor local sí implementa `execute_python`, `reload_api`, `inspect` y `transaction`.

Desajustes y riesgos:

1. Está escrita para **Inventor 2026**; P2.04 y su constructor usan **2027.1**. Las notas empíricas necesitan pruebas versionadas, no extrapolación automática.
2. P2.04 se construye con **Python para el manifiesto y PowerShell/C# Interop para COM**, sin importar `InventorConnection` ni llamar al MCP. La configuración `.codex/config.toml` demuestra que existe configuración MCP, no que se usara para generar esta entrega.
3. La regla «extruir siempre positivo» describe una limitación del wrapper de taladros y no una prohibición general de Inventor. `hole()` usa XY y dirección negativa fija; debe decidirse plano/dirección y verificarse el corte, sin generalizar el comportamiento de un ensayo a toda geometría.
4. La skill recomienda `reload_api()` y más adelante afirma que los cambios del wrapper requieren reiniciar o usar Python directo. El servidor sí implementa recarga: distinguir métodos del wrapper de cambios en esquemas de herramientas.
5. Obliga a bocetos totalmente restringidos, pero ni el constructor P2.04 ni `inspect()` acreditan esa condición. `draw_circle()` intenta una cota de diámetro, pero eso no fija automáticamente el centro; `draw_rectangle()` no añade cotas explícitas.
6. Algunas recomendaciones de borrar archivos o cachés son demasiado amplias para un proyecto con trabajo abierto. Priorizar versiones nuevas y diagnóstico dirigido, sin borrar originales ni cachés compartidas sin autorización.

### `inventor-din-parts`

Está en `tools/inventor-mcp/skills/inventor-din-parts/SKILL.md`, pero no en `.agents/skills/`; no aparece como skill registrada en esta sesión. Se leyó como archivo de referencia.

Es útil para patrones geométricos y la conversión de ancho entre caras a circunradio. No hay registro que demuestre su invocación histórica en P2.04.

Sus plantillas no cubren directamente el conjunto actual ISO 4762 / envolvente DIN 980 / GN 6341. Sus tablas se presentan como «autoritativas» sin identificar edición o fuente suficiente: deben comprobarse con norma/fabricante. DIN e ISO no deben considerarse intercambiables en todas las medidas por defecto.

Contiene contradicciones con la skill principal: recomienda scripts en vez de MCP, utiliza extrusión negativa en una plantilla y dice que las roscas externas no están expuestas por MCP. El constructor actual demuestra que se pueden crear roscas cosméticas nativas mediante `ThreadFeatures`; no son hélices sólidas ni certifican el herraje.

### Otras nueve skills presentes

`dfm-review`, `dfmea-design`, `fatigue-analysis`, `fea-structural`, `material-selection`, `test-planning`, `thermal-analysis`, `tolerance-stackup` y `trade-study` son guías metodológicas. Enumerar ANSYS, Abaqus, bases de materiales o software de tolerancias en sus textos no instala ni conecta esas herramientas.

No se encontró en los archivos revisados un registro de invocaciones que permita atribuirles el trabajo histórico. Hay cálculo analítico y comparación de secciones; eso no prueba ejecución de FEA, fatiga, DFMEA, simulación térmica o tolerancias. La entrega declara expresamente que no hay FEA ni ensayos físicos.

Prioridad práctica: tolerancias y fabricación para cerrar las uniones; DFMEA y plan de ensayo para fallos de retención, costuras, liberación y roce; selección de textiles/materiales por temperatura y ambiente; después análisis local y fatiga con cargas y apoyos definidos. Las tablas genéricas de las skills no sustituyen datos de proveedor ni requisitos específicos del equipo.

## 5. Conclusión y orden recomendado

P2.04 es una propuesta CAD más ligera, con buena trazabilidad de archivos y cálculo analítico reproducible. **No es todavía un diseño validado ni listo para fabricar para uso con personas.**

1. Resolver/documentar el redondeo lumbar fallido.
2. Hacer coherentes parámetros, geometría y cálculo; auditar restricciones de bocetos.
3. Incorporar medidas reales de bolsa/arnés cuando estén disponibles y comprobar el recorrido completo de las cintas.
4. Cerrar procesos, tolerancias, proveedores y presupuesto real de masa; no ahorrar los 212 g eliminando reservas sin evidencia.
5. Definir riesgos, casos de carga y criterios de aceptación; completar análisis y ensayos de banco antes de considerar pruebas con personas.

No se cambiaron las skills durante esta revisión: las correcciones anteriores son recomendaciones, no modificaciones ya aplicadas.
