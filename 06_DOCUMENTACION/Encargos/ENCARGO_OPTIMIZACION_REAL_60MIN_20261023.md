# Encargo para DeepSeek — optimización del producto real SEDAC, 60 minutos

Quiero que trabajes durante un máximo de 60 minutos en una nueva iteración del PRODUCTO REAL SEDAC, a escala maestra 1:1 en mm. Prioriza reducir masa mediante una arquitectura y unas uniones mejor resueltas, manteniendo el camino de cargas y los materiales ya considerados. Quiero un avance concreto, editable y comparable al anterior.

## Autorización y alcance

Te autorizo a preparar alternativas, corregir dependencias necesarias en copias, ejecutar comprobaciones de propagación y cálculos de prediseño, y generar CAD nativo nuevo en Inventor. Esta autorización permite desarrollar una propuesta sin disponer todavía de la bomba; no permite inventar mediciones ni declarar validación física. Las prohibiciones históricas de diseñar todavía no bloquean esta nueva iteración autorizada; las restricciones de integridad, trazabilidad y validación siguen vigentes.

La carpeta de trabajo es C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD. Lee sus AGENTS.md y documentos de contexto. Consulta el estado real de los archivos, no solo resúmenes antiguos. Ejecuta git status antes de escribir. Hay trabajo previo sin commit de Codex/OpenCode: consérvalo y registra su estado inicial. Trabaja como único escritor; si detectas otro proceso modificando las mismas fuentes, detén esas escrituras y explica el conflicto.

Crea todo tu trabajo en una carpeta nueva con fecha y hora bajo:
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Iteraciones\Optimizacion_Real_YYYYMMDD_HHmmss

Preserva fuentes, entregas y evidencias anteriores. Copia los generadores necesarios a tu iteración y adapta sus rutas para que tampoco escriban indirectamente en carpetas históricas. No hagas commit, push, borrados ni cambios en Notion. No sustituyas la entrega vigente ni cierres P2.05.

## Qué debes integrar

Lee primero estos documentos de la raíz:
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\CONTEXTO_SEDAC.md
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\ESTADO_ACTUAL.md
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\DECISIONES.md
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\CHANGELOG_SEDAC.md

Referencia geométrica del producto:
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_04_20261016\Entrega\Inventor\SEDAC_P2_04.iam

Revisa su manifiesto MODELO_API.json y datos nativos en la misma carpeta. El BOM y el resumen de masa están en:
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_04_20261016\BOM_Y_MASAS.csv
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_04_20261016\RESUMEN_ENTREGA.json

Avances de soporte, auditoría y corrección que debes aprovechar:
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\LEEME_P2_05.md
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635\AUDITORIA.md
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Iteraciones\Correccion_Dependencias_20261022_192327\INFORME.md
C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Pruebas\cierre\INFORME_CIERRE_20261022.md

P2.04 sigue siendo la referencia vigente del producto. P2.05 contiene mejoras de código y controles que debes contrastar; su existencia no significa que haya una entrega nativa completa más reciente. Revisa también los avances posteriores de OpenCode que estén realmente en disco y registra cuáles incorporas.

Las R1–R4 dentro de Maqueta_PLA_20261023_Codex son adaptaciones pequeñas para presentación. Sus paredes de PLA, sus sólidos fusionados y su ahorro geométrico del 35,2 % no se trasladan al producto real.

## Punto de partida y prioridades

El resumen P2.04 registra 1,442327847 kg de estructura/protectores y 2,212327847 kg de presupuesto total del sistema, sin bomba ni agua. El segundo valor utiliza 0,65 kg para textiles/arnés y 0,12 kg de reserva: no sumes otra vez las referencias visuales textiles.

Masa por grupos registrada: canales 0,568758 kg; anclajes 0,560488 kg; fijaciones 0,164802 kg; uniones 0,067520 kg; protecciones 0,080759 kg. Verifica la base antes de usarla. Son estimaciones del modelo, no pesajes.

Prioriza canales, lumbar, yugos y número/arquitectura de uniones. Busca simplificación, mejor reparto de material y refuerzos locales justificados. La espaldera del concepto es HDPE de 1 mm, y las cunas/cinturón contienen textiles. Conserva sus funciones de contacto, separación de aristas y movilidad relativa; no conviertas todo en una pieza rígida de aluminio ni elimines protecciones por su aspecto visual.

No adelgaces todas las piezas por igual. No reduzcas masa disminuyendo cargas, cambiando propiedades sin fuente o borrando el arnés del presupuesto. No apliques al canal el mínimo analítico de otra pieza. Los recortes próximos a pernos, ventanas y ligamentos necesitan revisión local propia.

## Cómo usar las auditorías

Antes de variar una dimensión, demuestra en tu copia qué parámetro controla el CAD y cuál controla el cálculo. Las correcciones H03 y parte de H13 están implementadas, pero la propagación e invariancia posteriores siguen pendientes. Revisa los H02/H04/H05 y las capas locales si afectan a tu variante.

Haz una regeneración nominal de control con salidas nuevas y compara contra la referencia. Después perturba por separado los parámetros que vayas a optimizar: demuestra qué cambia en mejillas, agarre, pasadores, casquillos, taladros y cortes. No repitas toda la auditoría histórica: concentra el trabajo en las dependencias necesarias para esta iteración. Si una dependencia no está resuelta, no presentes su variante como comprobada.

Mantén separados generación, coherencia y cribado analítico. Conserva los controles de cierre existentes. No fuerces la aceptación del redondeo lumbar parcial 236/472 ni inventes la clasificación A/B/C sin recorrido y tensión de cintas.

## Distribución orientativa de la hora

1. Minutos 0–10: reconciliar fuentes y masas; identificar cambios previos y el caso de cálculo gobernante. Escribir un resumen breve, sin rehacer toda la documentación.
2. Minutos 10–25: comprobar y resolver en copias las dependencias indispensables. Preparar hasta dos alternativas de aligeramiento con sus motivos, variables, masas estimadas y limitaciones. No impongas un porcentaje de ahorro previo.
3. Minutos 25–45: elegir la alternativa mejor respaldada; recalcular lo afectado y crear el CAD editable nuevo. Puedes empezar la generación antes si la integración nativa requiere más tiempo.
4. Minutos 45–60: revisar CAD, masas, uniones y vistas; exportar y documentar. Reserva tiempo para una entrega honesta aunque alguna fase quede incompleta. No emplees el último tramo en prometer comprobaciones que no ejecutaste.

Adapta el reparto al avance; mide el tiempo transcurrido y finaliza con un resultado revisable. No gastes toda la hora leyendo o enumerando habilidades. Aplica las habilidades locales pertinentes y comprueba qué herramientas están realmente disponibles.

## Cálculo y límites de diseño

Conserva la arquitectura de cargas hacia hombros/cinturón y la separación necesaria para manguera, bolsa y EPP, con interfaces provisionales editables. No tenemos medidas reales de bomba, centro de gravedad, arnés ni usuarios.

Los 25 kg, 3g verticales totales, 1g horizontal, reparto 70/30, excentricidad 107,5 mm y precarga 2000 N son hipótesis de prediseño. El umbral 2,2 es un criterio elegido; no certifica el producto. El mínimo nominal heredado cercano a 2,247 exige especial atención a la sensibilidad: no lo conviertas en permiso para recortar secciones.

Para cada cambio resistente, revisa los modos afectados: fluencia/flexión, rigidez y desplazamientos, estabilidad, sección neta, aplastamiento y desgarro, pasador/perno, agarre, arandelas, precarga/retención y zonas de contacto. Calcula lo que el modelo pueda justificar y lista expresamente lo que queda sin cubrir: fatiga, dinámica, temperatura, contacto textil, desgaste, liberación y ergonomía. No reutilices el resultado viejo para un contorno nuevo sin comprobar su aplicabilidad.

Compara alternativas bajo las mismas hipótesis y con escenarios de sensibilidad razonados, identificados como supuestos. Una comprobación no cubierta queda pendiente; no se sustituye por una cifra inventada. Las mediciones faltantes impiden cerrar el producto fabricable, pero permiten desarrollar una propuesta conceptual condicionada.

## Entrega obligatoria

- Informe breve con fuentes utilizadas, avance real por fase, cambios, decisiones, riesgos y pendientes, etiquetando hecho/cálculo/supuesto/hipótesis.
- Tabla antes/después con masa rígida, presupuesto total con textiles y reserva, parámetros modificados, modos calculados y resultados comparables. Separar resultados analíticos de masas nativas y de cualquier medición física.
- Si logras generar en Inventor: IAM con todas sus referencias IPT, STEP y vistas frontal/posterior/lateral/isométrica. Comprobar actualización, referencias, número de cuerpos, masas e interferencias nominales, indicando herramientas y resultados reales. Un STEP o un JSON no prueban que exista un editable nativo correcto.
- Si Inventor o la generación fallan: conservar código, registros, parámetros y cálculos; indicar el bloqueo exacto y qué falta. No sustituir el producto por un STL importado ni declarar nativos que no se crearon.
- Comparación de masa recalculada con materiales y cantidades coherentes; manifiesto de archivos y hashes; LEEME con cuál es la propuesta, cómo abrirla y qué está pendiente. Cualquier ZIP debe incluir todas las referencias necesarias.
- Mantener pendientes Mathcad y PDF hasta acordar geometría. Entregar ahora cálculos reproducibles y una explicación breve, sin inventar ensayos o FEA.

Al terminar, quiero saber cuánto material pudiste retirar realmente, qué consecuencias tiene y qué evidencia respalda cada conclusión. Si no puedes justificar una reducción resistente dentro de la hora, deja una alternativa conceptual identificada y el avance de coherencia conseguido. No declares seguridad, flexibilidad, comodidad ni fabricación validada por haber terminado el CAD.
