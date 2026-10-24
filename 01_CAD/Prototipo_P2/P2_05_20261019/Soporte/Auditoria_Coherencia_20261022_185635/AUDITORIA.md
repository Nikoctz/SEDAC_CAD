# Auditoría de coherencia de P2.05 — 22/10/2026

**hecho — alcance:** lectura de fuentes, análisis AST y regeneración de descripciones JSON/CSV. No se ejecutó Inventor ni el cálculo; no se repitieron el banco de cierre ni la invariancia numérica del encargo anterior. No se adoptan decisiones técnicas ni correcciones.

## Respuesta a la pregunta del encargo

**hecho:** no toda dimensión o hipótesis sale de PARAMETROS_P2_05.json. Tampoco todo campo geométrico declarado controla directamente una cota del modelo. Hay campos exclusivos del cálculo, datos de presupuesto, literales declarados como fijos y conexiones parciales. Leer un campo y copiar el JSON completo dentro del manifiesto no demuestra que controle toda la geometría relacionada.

**hecho:** la regeneración actual coincide byte por byte con MODELO_API.json y BOM_FIJACIONES.csv de Nueva_20261019_060807. Esa coincidencia comprueba reproducibilidad de la descripción actual; no comprueba que cambiar un parámetro propague correctamente todas las dependencias, ni valida un sólido nativo.

**hecho:** se registran 13 hallazgos: 10 [I] informativos y 3 [C] a conservar, con severidad propuesta. No apareció una diferencia de regeneración que motive un nuevo [B] en este alcance. La aceptación nativa y física sigue pendiente; este resultado no autoriza una corrida de Inventor ni el cierre de P2.05.

## Método, fuentes y etiquetas

**hecho:** se leyó el contexto obligatorio del repositorio en el orden de AGENTS.md: CONTEXTO_SEDAC.md, ESTADO_ACTUAL.md, DECISIONES.md y CHANGELOG_SEDAC.md. Se usaron como fuentes de esta auditoría los archivos de la tabla; sus huellas de esta ejecución quedan en RESULTADOS.json → fuentes_sha256.

| Fuente leída | SHA-256 durante la auditoría |
| --- | --- |
| [01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json>) | 40f2491d01bdef73170a46fc3fabc2e019dde088515ff91dffc7c2e835293771 |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py>) | bd401a055d1bf8a1310681d40748f040b42a6e119723e586bb2e29367c59af96 |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py>) | b664720ea12b94c7ee59da310abc032ccd092898f5bbf2676c6bc54b7ad6b85d |
| [01_CAD/Prototipo_P2/P2_04_20261016/Soporte/generar_p2_04.py](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_04_20261016/Soporte/generar_p2_04.py>) | deb3f090419938c474c33e60617e1cbe5d6ed7cb077ff16efe414812c476bf9f |
| [01_CAD/Prototipo_P2/P2_04_20261016/PARAMETROS_P2_04.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_04_20261016/PARAMETROS_P2_04.json>) | 660de89e3c2201f2612e6f8d87564d6b39bf24c65ddcd77d73ec6faf46407f12 |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/MODELO_API.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/MODELO_API.json>) | d1e6949c670e4c4e5a5d8af71dccf9c9d5a14b6cf832c13f7f9113a9059c0f24 |
| [01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/BOM_FIJACIONES.csv](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Iteraciones/Nueva_20261019_060807/BOM_FIJACIONES.csv>) | 0ea272db2368885c3641e1d94bf8e2508eb860b140f1ea26fc800296481d997a |
| [01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md>) | 07e14c28ad4a1c78651b9c99fe8043c09ec7cc7ce0b1e1519bf1beee0742d6ae |
| [06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md>) | 87f416373aa32f32357f4bdeeb10e586db70a7f0eae5652f61a5381c0c3f953b |

**hecho — método A:** recorrido recursivo del JSON, incluidos contenedores y elementos de listas; resolución de alias P/G/C/M y accesos por subíndice/get en AST. Además se trazaron lecturas en memoria con los mismos valores y sin ejecutar escrituras en ese tramo. Su manifiesto resultante coincide con el del generador original ejecutado después. No se hicieron perturbaciones de parámetros.

**hecho — método B:** inventario de todos los literales numéricos, comentarios y textos con cifras; clasificación automática por contexto, con revisión semántica de los grupos de interés en la tabla B. Las coincidencias numéricas del CSV son candidatos; la igualdad numérica por sí sola no prueba duplicación semántica. Los coeficientes de fórmula, índices, colores, alternativas de comparación, salidas y funciones no invocadas se separan de dimensiones e hipótesis efectivas.

**cálculo — método C:** extracción de contornos y profundidades de operaciones del JSON histórico y regenerado; diferencias geométricas simples identificadas en la tabla C. Se comparan descripciones y nominales, no mediciones de sólidos. Los mínimos de estudio no se presentan como tolerancias medidas.

**hecho — método D:** ejecución del generador original, en Python disponible y bajo PowerShell 5.1.26100.9711, con salida nueva dentro de esta auditoría. Se compararon árboles completos, filas CSV y bytes. Registro: [REGISTRO_GENERACION.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/REGISTRO_GENERACION.json>). La ejecución final mediante ejecutar_auditoria.ps1 conserva también el proceso real y versión en REGISTRO_ENTORNO_POWERSHELL.json; las exploraciones anteriores registran 7.6.5 y no se presentan como ejecuciones de Windows PowerShell 5.1.

**hecho — etiquetas:** hecho = archivo/lectura/comando; cálculo = derivación identificada; supuesto = valor adoptado sin medir; hipótesis = condición física no comprobada. Las propuestas son pendientes, no decisiones adoptadas. Se normaliza el estado escrito como «no_leido Dale mas» en el encargo a no_leido_declarado. Se conserva sin_procultad como la etiqueta pedida para ausencia de origen geométrico verificable; no significa que el literal no tenga ubicación en el código.

## A. Parámetros → generador

**hecho:** 88 nodos declarados, de los cuales 78 son hojas (se cuenta una lista vacía como hoja). Estados de todos los nodos: {"no_leido": 49, "leido": 34, "no_leido_declarado": 5}. Ninguno se declara obsoleto solo por no leerse. La tabla completa con valores, notas, expresiones y referencias del cálculo está en [CAMPOS_PARAMETROS.csv](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/CAMPOS_PARAMETROS.csv>).

| Campo (contenedores incluidos) | Tipo | Estado AST del generador | Leído en control actual | Evidencia generador |
| --- | --- | --- | --- | --- |
| version | hoja | no_leido | no | sin referencia directa |
| fecha | hoja | no_leido | no | sin referencia directa |
| unidades | hoja | no_leido | no | sin referencia directa |
| estado | hoja | no_leido | no | sin referencia directa |
| origen | contenedor | no_leido | no | sin referencia directa |
| origen.version_base | hoja | no_leido | no | sin referencia directa |
| origen.carpeta_base | hoja | no_leido | no | sin referencia directa |
| origen.regla | hoja | no_leido | no | sin referencia directa |
| geometria | contenedor | leido | sí | [6:6](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:6>) |
| geometria.alto_refuerzo | hoja | leido | sí | [6:6](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:6>) |
| geometria.separacion_refuerzos | hoja | leido | sí | [6:6](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:6>) |
| geometria.ancho_refuerzo | hoja | leido | sí | [6:6](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:6>) |
| geometria.profundidad_refuerzo | hoja | leido | sí | [6:6](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:6>) |
| geometria.pared_refuerzo | hoja | leido | sí | [6:6](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:6>) |
| geometria.pared_minima | hoja | no_leido | no | sin referencia directa |
| geometria.radio_raiz | hoja | leido | sí | [35:35](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:35>) |
| geometria.ventanas_refuerzo_y | hoja | leido | sí | [38:38](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:38>) |
| geometria.ancho_ventana_refuerzo | hoja | leido | no | [39:39](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:39>) |
| geometria.alto_ventana_refuerzo | hoja | leido | no | [39:39](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:39>) |
| geometria.radio_redondeo_refuerzo | hoja | leido | sí | [40:40](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:40>) |
| geometria.apoyo_hombro_y | hoja | no_leido | no | sin referencia directa |
| geometria.apoyo_cinturon_y | hoja | no_leido | no | sin referencia directa |
| geometria.eje_pernos_z | hoja | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [42:42](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:42>), [43:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [57:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>), [67:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:67>) |
| geometria.pernos_y | contenedor | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [41:41](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:41>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [57:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>), [67:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:67>) |
| geometria.pernos_y[0] | hoja | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [41:41](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:41>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [57:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>), [67:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:67>) |
| geometria.pernos_y[1] | hoja | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [41:41](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:41>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [57:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>), [67:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:67>) |
| geometria.pernos_y[2] | hoja | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [41:41](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:41>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [57:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>), [67:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:67>) |
| geometria.pernos_y[3] | hoja | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [41:41](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:41>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [57:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>), [67:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:67>) |
| geometria.separacion_pernos | hoja | no_leido | no | sin referencia directa |
| geometria.distancia_borde_perno | hoja | no_leido | no | sin referencia directa |
| geometria.casquillo_od | hoja | leido | sí | [42:42](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:42>) |
| geometria.pasador_od | hoja | leido | sí | [43:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>) |
| geometria.pasador_id | hoja | leido | sí | [43:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>) |
| geometria.taladro_union | hoja | leido | sí | [37:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>), [42:42](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:42>), [54:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>), [65:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:65>) |
| geometria.espesor_anclaje | hoja | leido | sí | [8:8](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:8>), [48:48](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:48>), [50:50](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:50>), [61:61](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:61>), [62:62](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:62>) |
| geometria.espesor_minimo_anclaje | hoja | no_leido | no | sin referencia directa |
| geometria.espesor_cuerpo_lumbar | hoja | leido | sí | [7:7](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:7>) |
| geometria.espesor_mejilla | hoja | leido | sí | [7:7](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:7>) |
| geometria.radio_redondeo_lumbar | hoja | leido | sí | [55:55](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:55>) |
| geometria.radio_redondeo_yugo | hoja | leido | sí | [66:66](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:66>) |
| geometria.alto_puente_cinta | hoja | no_leido | no | sin referencia directa |
| geometria.luz_puente_cinta | hoja | no_leido | no | sin referencia directa |
| geometria.espesor_panel | hoja | leido | sí | [71:71](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:71>), [72:72](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:72>) |
| geometria.ancho_panel | hoja | leido | sí | [8:8](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:8>) |
| geometria.alto_panel | hoja | leido | sí | [8:8](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:8>) |
| geometria.ancho_cuna | hoja | leido | sí | [8:8](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:8>) |
| geometria.hueco_manguera | hoja | leido | sí | [8:8](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:8>) |
| geometria.espesor_cinta | hoja | leido | sí | [7:7](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:7>) |
| geometria.ancho_cinta | hoja | leido | sí | [7:7](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:7>) |
| geometria.espesor_arandela | hoja | leido | sí | [126:126](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:126>) |
| geometria.espesor_arandela_minimo | hoja | no_leido | no | sin referencia directa |
| reservas_masa | contenedor | no_leido | no | sin referencia directa |
| reservas_masa.masa_presupuesto_textil_kg | hoja | no_leido | no | sin referencia directa |
| reservas_masa.masa_reserva_kg | hoja | no_leido | no | sin referencia directa |
| reservas_masa.nota | hoja | no_leido | no | sin referencia directa |
| referencias_historicas | contenedor | no_leido | no | sin referencia directa |
| referencias_historicas.p2_03_rigida_kg | hoja | no_leido | no | sin referencia directa |
| referencias_historicas.p2_03_presupuesto_kg | hoja | no_leido | no | sin referencia directa |
| referencias_historicas.nota | hoja | no_leido | no | sin referencia directa |
| cargas | contenedor | no_leido | no | sin referencia directa |
| cargas.masa_total_kg | hoja | no_leido | no | sin referencia directa |
| cargas.g | hoja | no_leido | no | sin referencia directa |
| cargas.factor_vertical | hoja | no_leido | no | sin referencia directa |
| cargas.factor_horizontal | hoja | no_leido | no | sin referencia directa |
| cargas.fraccion_lado | hoja | no_leido | no | sin referencia directa |
| cargas.excentricidad_mm | hoja | no_leido | no | sin referencia directa |
| cargas.brazo_torsion_mm | hoja | no_leido | no | sin referencia directa |
| cargas.K_borde | hoja | no_leido | no | sin referencia directa |
| cargas.K_ventana | hoja | no_leido | no | sin referencia directa |
| cargas.margen_objetivo | hoja | no_leido | no | sin referencia directa |
| cargas.flecha_limite_mm | hoja | no_leido | no | sin referencia directa |
| cargas.precarga_estudio_N | hoja | no_leido | no | sin referencia directa |
| cargas.angulo_eslinga_grados | hoja | no_leido | no | sin referencia directa |
| cargas.nota | hoja | no_leido | no | sin referencia directa |
| materiales | contenedor | no_leido | no | sin referencia directa |
| materiales.E_6061_MPa | hoja | no_leido | no | sin referencia directa |
| materiales.Sy_6061_MPa | hoja | no_leido | no | sin referencia directa |
| materiales.Sy_perno_MPa | hoja | no_leido | no | sin referencia directa |
| materiales.aluminio | hoja | no_leido | no | sin referencia directa |
| materiales.panel | hoja | no_leido | no | sin referencia directa |
| materiales.textiles | hoja | no_leido | no | sin referencia directa |
| parametrizacion | contenedor | no_leido | no | sin referencia directa |
| parametrizacion.pendiente | contenedor | no_leido_declarado | no | sin referencia directa |
| parametrizacion.pendiente[0] | contenedor | no_leido_declarado | no | sin referencia directa |
| parametrizacion.pendiente[0].campo | hoja | no_leido_declarado | no | sin referencia directa |
| parametrizacion.pendiente[0].valor_nominal_mm | hoja | no_leido_declarado | no | sin referencia directa |
| parametrizacion.pendiente[0].motivo | hoja | no_leido_declarado | no | sin referencia directa |
| parametrizacion.fijo_en_generador | hoja | no_leido | no | sin referencia directa |

### Cruce con la revisión histórica y la declaración 10+4

**hecho:** [REVISION_P2_04_Y_SKILLS_20261017.md:39](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md:39>) enumera nueve campos geométricos antes no leídos. Los ocho siguientes tienen referencias nuevas en el generador P2.05. Profundidad_cuna queda pendiente, explícitamente no conectada. La presencia de una lectura no acredita propagación completa; H03/H13 precisan las limitaciones.

| Campo de la revisión del 17/10 | Situación P2.05 | Etiqueta |
| --- | --- | --- |
| alto_panel | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| ancho_cinta | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| ancho_cuna | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| ancho_panel | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| espesor_cinta | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| espesor_cuerpo_lumbar | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| espesor_mejilla | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| hueco_manguera | lectura geométrica incorporada; ver fila A y límites H03/H13 | hecho |
| profundidad_cuna | fuera de geometria, conservado en parametrizacion.pendiente[0]; no conectado | hecho |

**hecho:** los cuatro campos nuevos leídos son pasador_id, radio_redondeo_lumbar, radio_redondeo_refuerzo, radio_redondeo_yugo. El contraste AST entre ambos generadores respalda 8+4, no la frase 10+4 de [LEEME_P2_05.md:20](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md:20>). Espesor_anclaje y espesor_arandela ya tenían lecturas en P2.04; no son nuevas conexiones. Las reservas de masa 0,65/0,12 kg están fuera de geometría y no deben contarse como dimensiones conectadas. No se altera la frase histórica en este encargo; se documenta H01.

**hecho:** ancho_ventana_refuerzo y alto_ventana_refuerzo tienen referencia AST, pero no lectura efectiva con ventanas_refuerzo_y=[]. Los campos de cargas y materiales no generan geometría por sí mismos; los mínimos son de estudio. En cambio, luz_puente_cinta, alto_puente_cinta y separacion_pernos se usan en el cálculo sin gobernar los contornos/agujeros correspondientes (H02).

**hecho:** parametrizacion.fijo_en_generador reconoce textiles, radios de recortes y elementos M5 fijos. Su frase final sobre campos de geometria no se debe interpretar como garantía de control global: hay entradas exclusivamente analíticas y dependencias parciales. Evidencia: [PARAMETROS_P2_05.json:98](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json:98>).

## B. Constantes y duplicaciones

**hecho:** 879 registros entre literales, textos, comentarios y accesos a parámetros; inventario en [LITERALES.csv](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/LITERALES.csv>). Clases automáticas por contexto: {"coeficiente_o_control": 25, "origen_o_control": 47, "texto_no_operativo": 55, "literal_duplicado": 157, "control_o_visual": 21, "hipotesis_material_no_parametrizada": 7, "funcion_no_invocada": 15, "literal_sin_parametro_cota": 316, "coeficiente_de_formula": 65, "hipotesis_sin_etiqueta": 13, "literal_ya_etiquetado": 3, "variable_sin_uso": 1, "comentario_no_ejecutable": 1, "solo_trazabilidad": 4, "alternativa_de_comparacion_o_salida": 22, "es_parametro": 127}. Cada fila guarda ruta, línea y expresión. Las clases de contexto son propuestas de inventario; los hallazgos siguientes se fundamentan en relaciones revisadas, no en coincidencias numéricas accidentales.

| Grupo revisado | Clase semántica propuesta | Evidencia | Interpretación (hecho sobre el código; hipótesis físicas indicadas) |
| --- | --- | --- | --- |
| Canal, taladros y diámetros nominales | es_parametro | [generar_p2_05.py:35](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:35>); [generar_p2_05.py:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>) | B/D/t, raíz, pernos y nominales casquillo/pasador salen de G. Tolerancias de corte ±0,1/0,2 son literales auxiliares, no tolerancias de fabricación demostradas. |
| Mejillas: 3, 6; pasador: +0,2/−0,4 | literal_duplicado / literal_sin_parametro_cota | [generar_p2_05.py:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>); [generar_p2_05.py:52](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:52>) | El 3 de posicionamiento coincide semánticamente con EM actual y 6 con dos mejillas; no se derivan de EM. |
| Inicio z −3,7 / −6,7 / −6,8, corte y capas | literal_sin_parametro_cota / literal_duplicado | [generar_p2_05.py:49](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:49>); [generar_p2_05.py:61](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:61>) | ECU y espesor_anclaje se leen, con coordenadas todavía fijas. Refuerzo local de cuna = 2×ECU actual, no un vínculo general con espesor_anclaje. |
| Ranuras 52×8 y puentes locales | literal_duplicado / literal_sin_parametro_cota | [generar_p2_05.py:50](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:50>); [calcular_p2_05.py:87](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:87>) | 52 tiene contraparte luz_puente_cinta; alto de ranura 8 no es un término independiente de la fórmula de cuna. 15 mínimo y 16 nominal se explican en C. |
| Contornos, ventanas, radios de recorte, M5 | literal_sin_parametro_cota | [generar_p2_05.py:62](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:62>); [generar_p2_05.py:128](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:128>) | Existen numerosos contornos fijos, incluidos estructurales y de referencia. Su declaración como fijos no los convierte en comprobados. |
| Densidades y propiedades del modelo | literal_duplicado / hipotesis_sin_etiqueta | [generar_p2_05.py:11](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:11>); [generar_p2_05.py:137](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:137>) | E/Sy actuales coinciden con materiales; nu, Su y densidades están en código. No son certificados ni mediciones. El CSV distingue el contexto material. |
| 1,25 de borde y tres factores 1,5 | es_parametro / literal ya etiquetado | [calcular_p2_05.py:32](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:32>); [calcular_p2_05.py:126](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:126>) | K_borde proviene del JSON y tiene etiqueta; los tres 1,5 ya están en las 26 magnitudes. No se registran otra vez como ausentes. |
| Precarga 1,25 / 0,75; Cj=0,2 / 0,8 | hipotesis_sin_etiqueta | [calcular_p2_05.py:60](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:60>); [calcular_p2_05.py:89](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:89>) | Constantes explicadas en parte en textos, pero no incluidas individualmente en situacion_de_carga. El 1,25 de precarga es distinto de K_borde. |
| M5 As=14,2; nu=0,33; k placa=0,43; K taladro=3 | hipotesis_sin_etiqueta | [calcular_p2_05.py:60](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:60>); [calcular_p2_05.py:44](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:44>); [calcular_p2_05.py:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:57>) | As y modelo de placa tienen interpretación física; 0,43 es el coeficiente adoptado para placa sobresaliente. El 3 del taladro no lee K_ventana. d=5 se asigna pero no interviene después. |
| OD mínimo/ID máximo: ±0,1 y pin_id=5,6 | literal_sin_parametro_cota | [calcular_p2_05.py:63](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:63>); [calcular_p2_05.py:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:67>) | Nominales vienen del JSON; las tolerancias de estudio y el ID máximo están en código. No hay campo de tolerancias. |
| Brazo 3,4; radio 4; AF8; hueco 5,5; mínimo cuna15 | literal_duplicado / literal_sin_parametro_cota | [calcular_p2_05.py:70](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:70>); [calcular_p2_05.py:74](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:74>); [calcular_p2_05.py:86](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:86>) | 3,4 no tiene origen geométrico unívoco; 4 coincide con AF/2 sin demostrar contacto; AF8 está fijo en ambos scripts; 5,5 de área difiere del agujero de arandela 5,3. |
| Sy arandela 200; factor textil5 | hipotesis_sin_etiqueta | [calcular_p2_05.py:73](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:73>); [calcular_p2_05.py:139](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:139>) | Mínimos/requisitos adoptados para prediseño. No se atribuye resistencia al textil representado ni al material real sin proveedor/ensayo. |
| Ejemplos 0,35 / 3,4 / 2,3 del encargo | comprobación de contexto | [generar_p2_05.py:40](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:40>); [calcular_p2_05.py:70](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:70>) | 0,35 es radio pedido desde JSON; 3,4 es brazo local literal distinto. No se encontró un mínimo tunnel=2,3 en estos dos scripts. No se inventa una relación entre esas cifras. |

**hecho:** los textos OD10/ID5,5, 35 grados, 52×8, espesor6/min5,8 y arandela16×3 pueden quedar desactualizados al cambiar los campos relacionados. Son textos descriptivos; no gobiernan el cálculo. Los factores geométricos de sección, π, raíces, exponentes y conversión de unidades no se convierten automáticamente en hipótesis pendientes solo por ser números.

### Cruce con las 26 magnitudes ya trazadas

| Magnitud existente | Unidad | Etiqueta actual | Fuente |
| --- | --- | --- | --- |
| masa_total | kg | hipótesis | [calcular_p2_05.py:105](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:105>) |
| gravedad | m/s² | supuesto | [calcular_p2_05.py:106](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:106>) |
| factor_vertical | g totales | hipótesis | [calcular_p2_05.py:107](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:107>) |
| factor_horizontal | g | hipótesis | [calcular_p2_05.py:108](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:108>) |
| fuerza_vertical_total | N | cálculo | [calcular_p2_05.py:109](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:109>) |
| fuerza_horizontal_total | N | cálculo | [calcular_p2_05.py:110](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:110>) |
| fraccion_lado_mas_cargado | fracción | hipótesis | [calcular_p2_05.py:111](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:111>) |
| fraccion_otro_lado | fracción | cálculo | [calcular_p2_05.py:112](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:112>) |
| N_lado | N | cálculo | [calcular_p2_05.py:113](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:113>) |
| Q_lado | N | cálculo | [calcular_p2_05.py:114](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:114>) |
| apoyo_hombro_y | mm | hipótesis | [calcular_p2_05.py:115](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:115>) |
| apoyo_cinturon_y | mm | hipótesis | [calcular_p2_05.py:116](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:116>) |
| L | mm | cálculo | [calcular_p2_05.py:117](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:117>) |
| excentricidad | mm | hipótesis | [calcular_p2_05.py:118](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:118>) |
| M0 | N·mm | cálculo | [calcular_p2_05.py:119](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:119>) |
| Mmax | N·mm | cálculo | [calcular_p2_05.py:120](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:120>) |
| precarga | N | hipótesis | [calcular_p2_05.py:121](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:121>) |
| angulo_eslinga | grados | hipótesis | [calcular_p2_05.py:122](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:122>) |
| margen_objetivo | adimensional | hipótesis | [calcular_p2_05.py:123](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:123>) |
| flecha_limite | mm | supuesto | [calcular_p2_05.py:124](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:124>) |
| K_borde | adimensional | supuesto | [calcular_p2_05.py:125](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:125>) |
| factor_palanca_union | adimensional | supuesto | [calcular_p2_05.py:126](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:126>) |
| factor_puente_anclaje | adimensional | supuesto | [calcular_p2_05.py:127](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:127>) |
| factor_puente_cuna | adimensional | supuesto | [calcular_p2_05.py:128](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:128>) |
| E_aluminio | MPa | supuesto | [calcular_p2_05.py:129](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:129>) |
| Sy_aluminio | MPa | supuesto | [calcular_p2_05.py:130](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:130>) |

**hecho:** el brazo local 3,4, las tolerancias ±0,1 y pin_id máximo5,6, el mínimo cuna15, radio/área bajo arandela, Sy arandela200, As M5, coeficientes de junta y factor textil5 no están etiquetados individualmente en esa lista. También brazo_torsion_mm, K_ventana y Sy_perno_MPa provienen del JSON pero no tienen su propia entrada entre las 26. Se conserva lo trazado y se propone completar el resto; no se afirma que todos esos datos carezcan de explicación en otros textos.

## C. Cálculo ↔ descripción del modelo

**cálculo:** 29 comparaciones. Las dos columnas de modelo se obtienen por separado con geometria() de auditar_coherencia.py. MODELO_API.parameters se excluye como prueba de conexión geométrica: es copia de entrada. Evidencias y notas completas en [COMPARACION_GEOMETRICA.csv](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/COMPARACION_GEOMETRICA.csv>).

| Magnitud | Valor usado en cálculo | Modelo histórico | Modelo regenerado | Unidad | Relación | Etiqueta |
| --- | --- | --- | --- | --- | --- | --- |
| ancho_refuerzo | 32 | 32 | 32 | mm | coincide_nominal | cálculo |
| profundidad_refuerzo | 24 | 24 | 24 | mm | coincide_nominal | cálculo |
| Pared mínima canal | 2.8 | 3 | 3 | mm | minimo_frente_a_nominal | cálculo |
| Altura total (masa de comparación) | 480 | 480 | 480 | mm | coincide_nominal | cálculo |
| L entre apoyos | 380 | sin correspondencia geométrica demostrada | sin correspondencia geométrica demostrada | mm | hipotesis_sin_anclaje_CAD | cálculo |
| Separación de pernos | 60 | [60, 60] | [60, 60] | mm | coincidencia_derivada_independiente | cálculo |
| Eje de taladro | 12 | 12 | 12 | mm | coincide_nominal | cálculo |
| Distancia de borde | 12 | 12 | 12 | mm | coincidencia_derivada_independiente | cálculo |
| Anclaje mínimo | 5.8 | 6 | 6 | mm | minimo_frente_a_nominal | cálculo |
| Anclaje de cuna mínimo | 5.8 | 6 | 6 | mm | minimo_frente_a_nominal | cálculo |
| Mejilla efectiva mínima | 2.8 | 3 | 3 | mm | acoplamiento_analitico | cálculo |
| Luz de puente anclaje | 52 | 52 | 52 | mm | coincide_pero_literal | cálculo |
| Alto de puente anclaje | 18 | [20, 20, 24] | [20, 20, 24] | mm | sin_vinculo_univoco | cálculo |
| Luz de puente cuna | 52 | [[52, 8], [52, 8]] | [[52, 8], [52, 8]] | mm | coincide_pero_literal | cálculo |
| Alto mínimo de puente cuna | 15 | 16 | 16 | mm | minimo_literal_sin_parametro | cálculo |
| OD casquillo mínimo | 12.4 | 12.5 | 12.5 | mm | minimo_literal_sin_parametro | cálculo |
| ID casquillo máximo | 10.299999999999999 | 10.2 | 10.2 | mm | maximo_literal_sin_parametro | cálculo |
| OD pasador mínimo | 9.9 | 10.0 | 10.0 | mm | minimo_literal_sin_parametro | cálculo |
| ID pasador máximo | 5.6 | 5.5 | 5.5 | mm | literal_no_derivado_del_parametro | cálculo |
| Brazo local de pasador | 3.4 | sin correspondencia geométrica demostrada | sin correspondencia geométrica demostrada | mm | sin_procultad | hipótesis |
| Espesor mínimo arandela | 2.9 | 3 | 3 | mm | minimo_frente_a_nominal | cálculo |
| AF de apoyo bajo tuerca | 8 | 8.0 | 8.0 | mm | coincide_pero_literal | cálculo |
| Radio de carga arandela | 4 | 4.0 | 4.0 | mm | hipotesis_relacion_geometrica | cálculo |
| Agujero usado en área bajo tuerca | 5.5 | 5.3 | 5.3 | mm | idealizacion_distinta_de_nominal | cálculo |
| Radios de contacto y raíz | sin crédito resistente | [0.35, 0.5, 0.5] | [0.35, 0.5, 0.5] | mm | acabado_sin_credito | cálculo |
| E aluminio | 69000 | 69000 | 69000 | MPa | coincide_pero_literal | cálculo |
| Sy aluminio | 240 | 240 | 240 | MPa | coincide_pero_literal | cálculo |
| Brazo de torsión | 12 | sin correspondencia geométrica demostrada | sin correspondencia geométrica demostrada | mm | hipotesis_parametrizada_sin_linea_de_carga_CAD | cálculo |
| Ancho de ventana opcional | 10 | sin correspondencia geométrica demostrada | sin correspondencia geométrica demostrada | mm | rama_inactiva_actual | cálculo |

**cálculo — ancho_refuerzo:** Coincide con el perfil nominal de la descripción; no lectura del sólido nativo. Fuente: [calcular_p2_05.py:26](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:26>).

**cálculo — profundidad_refuerzo:** Coincide con el perfil nominal de la descripción; no lectura del sólido nativo. Fuente: [calcular_p2_05.py:26](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:26>).

**cálculo — Pared mínima canal:** 2,8 frente a 3 nominal; mínimo de estudio explícito, no error de identidad ni tolerancia medida. Fuente: [calcular_p2_05.py:26](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:26>).

**cálculo — Altura total (masa de comparación):** Solo aparece en la comparación de masas de secciones, no sustituye la luz L. Fuente: [calcular_p2_05.py:148](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:148>).

**cálculo — L entre apoyos:** Los parámetros 55/435 están copiados en parameters; no crean apoyos geométricos efectivos. Fuente: [calcular_p2_05.py:24](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:24>).

**cálculo — Separación de pernos:** El modelo usa pernos_y: las diferencias 95−35 y 450−390 son 60. El campo separacion_pernos no gobierna esos agujeros. Fuente: [calcular_p2_05.py:59](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:59>).

**cálculo — Eje de taladro:** Coordenada z de los centros en el perfil y en el cribado de agujeros. Fuente: [calcular_p2_05.py:55](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:55>).

**cálculo — Distancia de borde:** D−eje_pernos_z=24−12=12 hasta la boca del canal; el campo distancia_borde_perno no gobierna la geometría. La dirección del arrancamiento sigue siendo una hipótesis del cribado. Fuente: [calcular_p2_05.py:66](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:66>).

**cálculo — Anclaje mínimo:** 5,8 mínimo frente a placa yugo nominal de 6; mínimo de estudio. Fuente: [calcular_p2_05.py:80](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:80>).

**cálculo — Anclaje de cuna mínimo:** Dos capas nominales de 3 forman 6 en el refuerzo local; el cálculo usa 5,8. No se prueba contacto físico. Fuente: [calcular_p2_05.py:86](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:86>).

**cálculo — Mejilla efectiva mínima:** Usa pared_minima del canal, no espesor_mejilla ni un mínimo independiente. Nominal actual 3; relación mínima 2,8 no controlada por ese campo. Fuente: [calcular_p2_05.py:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:65>).

**cálculo — Luz de puente anclaje:** 52 coincide con la ranura de yugo; también con la altura de ranura de cinturón. El generador escribe 52 literal. Fuente: [calcular_p2_05.py:79](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:79>).

**cálculo — Alto de puente anclaje:** 18 no identifica un puente único: candidatos nominales de contorno 20, 20 y 24. Su elección conservadora o reducción mínima queda pendiente de justificación local. Fuente: [calcular_p2_05.py:81](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:81>).

**cálculo — Luz de puente cuna:** 52 usado en la fórmula; 8 es alto nominal de ranura descrito en el texto, no un término independiente de esa fórmula. Fuente: [calcular_p2_05.py:87](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:87>).

**cálculo — Alto mínimo de puente cuna:** Nominal geométrico 16; el mínimo 15 está en código/texto, sin campo de tolerancia o mínimo propio. Fuente: [calcular_p2_05.py:86](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:86>).

**cálculo — OD casquillo mínimo:** OD nominal 12,5; resta 0,1 embebida para estudiar 12,4, sin tolerancia en parámetros. Fuente: [calcular_p2_05.py:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:67>).

**cálculo — ID casquillo máximo:** ID nominal 10,2; suma 0,1 embebida para estudiar 10,3. Fuente: [calcular_p2_05.py:67](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:67>).

**cálculo — OD pasador mínimo:** OD nominal 10; mínimo 9,9 por tolerancia literal. Fuente: [calcular_p2_05.py:63](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:63>).

**cálculo — ID pasador máximo:** El nominal sí sale de pasador_id=5,5 en el generador; el cálculo mantiene 5,6 literal y no lee pasador_id. Fuente: [calcular_p2_05.py:63](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:63>).

**hipótesis — Brazo local de pasador:** Constante de brazo local sin campo ni correspondencia geométrica demostrada. No basta encontrar un número parecido en el modelo. Fuente: [calcular_p2_05.py:70](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:70>).

**cálculo — Espesor mínimo arandela:** 2,9 de estudio frente a 3 nominal; mínimo explícito en parámetros. Fuente: [calcular_p2_05.py:72](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:72>).

**cálculo — AF de apoyo bajo tuerca:** AF medido analíticamente del polígono nominal: 8; valor embebido en ambos scripts. Fuente: [calcular_p2_05.py:74](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:74>).

**cálculo — Radio de carga arandela:** Coincide con AF/2=4 como radio inscrito posible; el contacto y la distribución de presión no se derivan del modelo ni están validados. Fuente: [calcular_p2_05.py:72](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:72>).

**cálculo — Agujero usado en área bajo tuerca:** El nominal de arandela es 5,3. El cálculo resta un agujero de 5,5: idealización conservadora de área, pero sin campo ni trazabilidad del apoyo real. Fuente: [calcular_p2_05.py:74](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:74>).

**cálculo — Radios de contacto y raíz:** Radios pedidos 0,35/0,5/0,5 y raíz 2; se calcula esquina ideal sin crédito de esos radios. MODELO_API no prueba su aplicación nativa. Fuente: [calcular_p2_05.py:11](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:11>).

**cálculo — E aluminio:** 69 000 coincide hoy; el material del modelo se escribe como literal, sin leer materiales.E_6061_MPa. Fuente: [calcular_p2_05.py:25](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:25>).

**cálculo — Sy aluminio:** 240 coincide hoy; el material del modelo se escribe como literal, sin leer materiales.Sy_6061_MPa. Fuente: [calcular_p2_05.py:25](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:25>).

**cálculo — Brazo de torsión:** Existe en parámetros, pero no una línea de acción de carga en el JSON que demuestre este brazo. No deducirlo solo por coincidir con D/2. Fuente: [calcular_p2_05.py:36](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:36>).

**cálculo — Ancho de ventana opcional:** Las dos ramas generador/cálculo leen este campo solo al recorrer ventanas_refuerzo_y; lista vacía actual, sin ranuras de refuerzo activas. Fuente: [calcular_p2_05.py:51](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:51>).

**hipótesis — apoyos:** 55 y 435 mm son posiciones analíticas, L=380 mm. No existen entidades que demuestren contacto activo. Los pernos y=35/450 fuera del intervalo no prueban por sí solos omisión de carga: falta justificar resultantes y camino de transmisión. No se redefine el esquema ni se modifica la flecha.

**cálculo — nominales locales:** puente exterior de cinturón = 20 mm; entre ranuras superiores = 20 mm; superior de yugo = 24 mm; puente de cuna = 124−108=16 mm. El alto18 analítico no tiene identidad única con esos contornos. No se deduce su validez resistente por ser menor ni se propone reemplazarlo automáticamente.

### Recíproco: geometría sin comprobación individual correspondiente

**hecho:** [COTAS_MODELO.csv](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/COTAS_MODELO.csv>) inventaría 1189 valores numéricos de operaciones y radios de piezas. No es una lista de 1189 fallos: incluye cotas cubiertas parcialmente por C, coordenadas y detalles. Las dimensiones de interés sin comprobación individual están agrupadas aquí; la clasificación se basa en uso y crédito resistente explícito, no en que una pieza parezca cosmética.

| Detalle del modelo | Cobertura de cálculo / clasificación | Evidencia | Etiqueta |
| --- | --- | --- | --- |
| Ventanas lumbar/yugo y ligamentos de contornos | Estructural; solo se criban puentes idealizados. No se comprueban todos los ligamentos, esquinas, trayectorias ni apoyos de placa. | [generar_p2_05.py:50](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:50>); [generar_p2_05.py:62](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:62>) | hecho |
| Ventanas de mejillas 30×11, longitudes100/98 y posiciones | Estructural; bearing usa pared mínima del canal. No hay comprobación local individual de cada contorno. | [generar_p2_05.py:54](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:54>); [calcular_p2_05.py:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:65>) | hecho |
| Pasador largo37,6, retranqueos0,2 y casquillo largo26 | Fijación estructural; áreas/diámetros y brazo3,4 no verifican contacto, reparto, holgura ni todo el apoyo longitudinal. | [generar_p2_05.py:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>); [generar_p2_05.py:42](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:42>) | hecho |
| Roscas, cabeza, tuerca, penetración y montaje M5 | Geometría fija de unión; no hay verificación individual de rosca, prueba de tuerca ni acceso de herramienta. | [generar_p2_05.py:128](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:128>); [generar_p2_05.py:130](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:130>) | hecho |
| Radio raíz2 y redondeos0,35/0,5/0,5 | Acabado y contacto sin crédito de resistencia de radios en sección; aplicación nativa/desgaste pendiente. | [generar_p2_05.py:35](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:35>); [calcular_p2_05.py:11](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:11>) | hecho |
| Panel HDPE, espumas, textiles y hebillas de referencia | Protección/representación sin crédito resistente de su geometría. Textiles y costuras requieren selección y ensayo, no se validan con el área dibujada. | [generar_p2_05.py:73](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:73>); [generar_p2_05.py:87](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:87>) | hecho |
| Recorridos de cuna y profundidad130 no conectada | Referencia no equivalente a dimensión validada. No se deduce contacto A/B/C ni dimensiones de la bomba desde esas curvas. | [PARAMETROS_P2_05.json:93](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json:93>); [generar_p2_05.py:84](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:84>) | hecho |

## D. Regeneración ejecutada y conservación de evidencia

| Comprobación ejecutada | Resultado | Etiqueta |
| --- | --- | --- |
| Entorno invocador | 5.1.26100.9711; 3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)] | hecho |
| Archivos emitidos por generador | ["BOM_FIJACIONES.csv", "MODELO_API.json"] | hecho |
| Diferencias MODELO_API | 0 | hecho |
| Diferencias BOM por filas | 0 | hecho |
| Igualdad de bytes por archivo | {"BOM_FIJACIONES.csv": true, "MODELO_API.json": true} | hecho |
| Piezas / ocurrencias / uniones | [54, 83, 8] | hecho |
| Trazado en memoria sin cambio de valores | true | hecho |
| Inventor y CAD nativo | no ejecutado / no modificado por este encargo | hecho |

**hecho:** resultados completos en [COMPARACION_GENERACION.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/COMPARACION_GENERACION.json>); stdout/stderr y comando exacto en [REGISTRO_GENERACION.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/REGISTRO_GENERACION.json>). Los dos archivos regenerados se conservan bajo Control_generacion_JSON con LEEME que indica que no son CAD nativo ni entrega aceptada. No se borra evidencia.

### Comandos completos (Windows PowerShell 5.1)

**hecho:** la herramienta de terminal inicia PowerShell 7 aunque se solicite otro shell. Para la ejecución final se invocó explícitamente el ejecutable de Windows PowerShell 5.1 con el siguiente archivo; el propio archivo rechaza otras versiones:

```powershell
& 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635\ejecutar_auditoria.ps1'
```

**hecho:** dentro de Windows PowerShell 5.1, estos comandos Python también reproducen el análisis:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
$python = 'C:\Users\nicol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
Set-Location -LiteralPath 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD'
$salida = Join-Path 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635' ('Ejecucion_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))
& $python -B 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635\auditar_coherencia.py' --salida $salida --powershell $PSVersionTable.PSVersion.ToString()
```

**hecho:** el comando anterior reproduce A–D, genera una salida nueva y reescribe únicamente AUDITORIA.md de esta carpeta con el último resultado. El comando original del generador se conserva como vector de argumentos en REGISTRO_GENERACION.json; equivale al siguiente, con destino ya usado, por lo que para repetirlo debe elegirse otro destino nuevo:

```powershell
& $python -B 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\generar_p2_05.py' 'C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\Auditoria_Coherencia_20261022_185635\Ejecucion_20261022_191216_989\Control_generacion_JSON'
```

## Hallazgos numerados y severidad propuesta

**hecho:** [B] bloqueante de corrida por evidencia incompatible; [I] informativo que requiere resolución según el alcance de la próxima modificación; [C] aceptable/conservar como distinción o limitación explícita. Ninguna severidad constituye una decisión adoptada ni autoriza fabricación o uso.

### H01 [I] La declaración 10+4 no coincide con las nuevas lecturas del código

**hecho — evidencia:** [LEEME_P2_05.md:20](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/LEEME_P2_05.md:20>) → 10 campos; [generar_p2_05.py:7](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:7>) → ECU=G[; [generar_p2_04.py:124](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_04_20261016/Soporte/generar_p2_04.py:124>) → wt=G[.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H01].prueba_reproducible: {"conectados_anteriores": ["alto_panel", "ancho_cinta", "ancho_cuna", "ancho_panel", "espesor_cinta", "espesor_cuerpo_lumbar", "espesor_mejilla", "hueco_manguera"], "nuevos": ["pasador_id", "radio_redondeo_lumbar", "radio_redondeo_refuerzo", "radio_redondeo_yugo"]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Rectificar en una revisión autorizada el recuento histórico: ocho campos antes no leídos y cuatro nuevos. No contar como nuevos espesor_anclaje ni espesor_arandela, ya leídos en P2.04.

### H02 [I] Luz/alto de puentes y separación de pernos no gobiernan la geometría

**hecho — evidencia:** [calcular_p2_05.py:79](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:79>) → bridge_M=; [generar_p2_05.py:50](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:50>) → Ventanas_cinturon_y_cuna; [calcular_p2_05.py:59](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:59>) → sp=G[.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H02].prueba_reproducible: {"campos": [{"campo": "geometria.separacion_pernos", "valor": 60, "tipo": "hoja", "estado_generador": "no_leido", "leido_en_control": false, "referencias_generador": [], "referencias_calculo": [{"camino": ["geometria", "separacion_pernos"], "linea": 59, "expresion": "G['separacion_pernos']", "solo_trazabilidad": false}], "etiqueta": "hecho", "nota": "Copiado dentro de manifest.parameters; esa propagación no constituye uso geométrico. Campo analítico; distinguirlo de una cota nominal del modelo. La relación con geometría se revisa en C; no la gobierna directamente."}, {"campo": "geometria.alto_puente_cinta", "valor": 18, "tipo": "hoja", "estado_generador": "no_leido", "leido_en_control": false, "referencias_generador": [], "referencias_calculo": [{"camino": ["geometria", "alto_puente_cinta"], "linea": 81, "expresion": "G['alto_puente_cinta']", "solo_trazabilidad": false}, {"camino": ["geometria", "alto_puente_cinta"], "linea": 82, "expresion": "G['alto_puente_cinta']", "solo_trazabilidad": false}], "etiqueta": "hecho", "nota": "Copiado dentro de manifest.parameters; esa propagación no constituye uso geométrico. Campo analítico; distinguirlo de una cota nominal del modelo. La relación con geometría se revisa en C; no la gobierna directamente."}, {"campo": "geometria.luz_puente_cinta", "valor": 52, "tipo": "hoja", "estado_generador": "no_leido", "leido_en_control": false, "referencias_generador": [], "referencias_calculo": [{"camino": ["geometria", "luz_puente_cinta"], "linea": 79, "expresion": "G['luz_puente_cinta']", "solo_trazabilidad": false}], "etiqueta": "hecho", "nota": "Copiado dentro de manifest.parameters; esa propagación no constituye uso geométrico. Campo analítico; distinguirlo de una cota nominal del modelo. La relación con geometría se revisa en C; no la gobierna directamente."}]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Conectar o separar explícitamente esas hipótesis y cotas; comprobar las relaciones antes de permitir cambios de parámetros. No sustituir ahora 18 por otra dimensión.

### H03 [I] Espesor de mejilla leído, pero posiciones, grip y pasador conservan 3/6 embebidos

**hecho — evidencia:** [generar_p2_05.py:52](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:52>) → xx in [cx-B/2-3; [generar_p2_05.py:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>) → B+6-.4; [generar_p2_05.py:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:57>) → B+6,'Lumbar_.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H03].prueba_reproducible: {"nominal_actual": 3, "expresiones": ["inicio cx-B/2-3", "grip B+6", "longitud pasador B+6-.4"]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** En una revisión posterior derivar las posiciones y longitudes del espesor nominal, con tolerancias justificadas. La lectura de EM no demuestra control global.

### H04 [I] Pasador ID de cálculo desconectado de pasador_id y tolerancias embebidas

**hecho — evidencia:** [generar_p2_05.py:43](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:43>) → G['pasador_id']/2; [calcular_p2_05.py:63](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:63>) → pin_od=.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H04].prueba_reproducible: {"nominal": 5.5, "maximo_codigo": 5.6, "tolerancias_literales": 0.1}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Declarar mínimos/máximos y su origen; derivar el extremo de estudio desde el nominal autorizado. Mantener por ahora 5,6 y los valores actuales.

### H05 [I] Mejilla mínima se calcula con la pared mínima del canal

**hecho — evidencia:** [calcular_p2_05.py:65](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:65>) → Aplastamiento mejilla; [generar_p2_05.py:53](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:53>) → xx,EM,.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H05].prueba_reproducible: {"canal_minimo": 2.8, "mejilla_nominal": 3}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Separar el mínimo de mejilla o justificar expresamente su vínculo con el canal antes de variar espesores; no inventar una tolerancia.

### H06 [I] Constantes de unión, material y textil no cubiertas por las 26 magnitudes

**hecho — evidencia:** [calcular_p2_05.py:60](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:60>) → As=14.2; [calcular_p2_05.py:89](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:89>) → joint_residual=; [calcular_p2_05.py:70](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:70>) → pin_vm=; [calcular_p2_05.py:139](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:139>) → resistencia_minima_conjunto_cuna_N=; [calcular_p2_05.py:44](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:44>) → plate_sigma=; [calcular_p2_05.py:57](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:57>) → Sy/(3*local_stress).

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H06].prueba_reproducible: {"pendientes": ["As M5=14,2 mm²", "dispersión de precarga 1,25 / 0,75", "rigidez de junta 0,2 y pérdida 0,8", "brazo local 3,4 mm", "Sy arandela 200 MPa", "factor textil 5", "nu=0,33", "mínimo de puente cuna 15 mm", "coeficiente de placa k=0,43", "K local de taladro=3 literal, independiente de K_ventana"], "factores_1_5_ya_etiquetados": ["factor_palanca_union", "factor_puente_anclaje", "factor_puente_cuna"]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Incorporar los supuestos faltantes con unidad, origen y etiqueta en una revisión autorizada. No confundir el 1,25 de borde con el 1,25 de dispersión de precarga; tener texto explicativo no equivale a estar en las 26 magnitudes.

### H07 [I] Propiedades del modelo y del cálculo coinciden hoy pero tienen fuentes separadas

**hecho — evidencia:** [generar_p2_05.py:137](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:137>) → mechanical']=dict(E_MPa=69000; [calcular_p2_05.py:25](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:25>) → E=M[; [PARAMETROS_P2_05.json:83](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json:83>) → E_6061_MPa.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H07].prueba_reproducible: {"E": 69000, "Sy": 240}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Unificar o verificar explícitamente propiedades de estudio y propiedades escritas en CAD; los certificados físicos siguen pendientes.

### H08 [I] Apoyos ideales no equivalen a entidades o contactos demostrados del modelo

**hecho — evidencia:** [calcular_p2_05.py:24](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:24>) → L=G[; [generar_p2_05.py:37](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:37>) → G['pernos_y'].

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H08].prueba_reproducible: {"apoyos": [55, 435], "pernos": [35, 95, 390, 450], "fuera_luz": [35, 450]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Documentar resultantes/apoyos y transmisión por grupos de pernos. Tener pernos fuera de la luz no demuestra por sí solo una carga externa omitida; no redefinir el esquema sin evidencia.

### H09 [I] Brazo de pasador 3,4 y mínimos locales no se obtienen del modelo

**hecho — evidencia:** [calcular_p2_05.py:70](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:70>) → pin_vm=; [calcular_p2_05.py:86](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:86>) → cuna_Zin=; [calcular_p2_05.py:72](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:72>) → washer_sigma=.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H09].prueba_reproducible: {"brazo_pasador": "sin_procultad: sin origen geométrico unívoco", "puente_cuna_nominal": 16, "puente_cuna_minimo_literal": 15, "radio_carga_arandela_literal": 4}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Justificar brazo efectivo, mínimo de puente y contacto de arandela; parametrizarlos si se adopta su uso. No atribuirlos a una medición del CAD nativo.

### H10 [C] Los mínimos de estudio no deben confundirse con nominales distintos por error

**hecho — evidencia:** [calcular_p2_05.py:26](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:26>) → S=section(; [calcular_p2_05.py:80](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:80>) → tt=G.get; [calcular_p2_05.py:72](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:72>) → washer_sigma=.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H10].prueba_reproducible: {"canal": [2.8, 3], "anclaje": [5.8, 6], "arandela": [2.9, 3]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Conservar nominal/mínimo separados y las etiquetas de prediseño. La aceptación de fabricación requiere evidencia posterior.

### H11 [C] Profundidad de cuna no conectada y ventanas opcionales inactivas están declaradas

**hecho — evidencia:** [PARAMETROS_P2_05.json:93](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/PARAMETROS_P2_05.json:93>) → profundidad_cuna; [generar_p2_05.py:38](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:38>) → enumerate(G['ventanas_refuerzo_y']).

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H11].prueba_reproducible: {"ventanas": [], "profundidad": [{"campo": "profundidad_cuna", "valor_nominal_mm": 130, "motivo": "El contorno de la cuna esta fijo en generar_p2_05.py. No se encontro una correspondencia verificable entre 130 mm y el recorrido dibujado, asi que NO se conecta: conectarlo seria inventar geometria. Queda como dato de entrada sin reflejo en el CAD."}]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Conservar pendiente la profundidad; no etiquetar como obsoletos automáticamente los parámetros de una rama opcional vacía.

### H12 [C] Hay geometría estructural local sin comprobación individual de sus contornos

**hecho — evidencia:** [generar_p2_05.py:50](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:50>) → Ventanas_cinturon_y_cuna; [generar_p2_05.py:62](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:62>) → Cintas_y_aligeramiento; [calcular_p2_05.py:142](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/calcular_p2_05.py:142>) → FEA local, pandeo distorsional.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H12].prueba_reproducible: {"detalles": ["ventanas y ligamentos de placas lumbar/yugos", "ventanas de mejillas 30×11", "longitud de pasador 37,6 y condiciones de apoyo", "roscas, contacto, acceso y tolerancias", "radios sin crédito y referencias textiles"]}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Conservar el alcance parcial del cribado; preparar revisión local, tolerancias y ensayos cuando existan los datos. No dar por calculadas todas las ventanas por existir K_ventana.

### H13 [I] Espesores lumbar/anclaje leídos con inicios y cortes todavía fijos

**hecho — evidencia:** [generar_p2_05.py:8](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:8>) → Z0=-(G['espesor_anclaje']+0.7); [generar_p2_05.py:49](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:49>) → op('z',-3.7,ECU; [generar_p2_05.py:50](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/generar_p2_05.py:50>) → op('z',-6.8,G['espesor_anclaje']+.2.

**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id=H13].prueba_reproducible: {"cuna_dos_capas": "ECU+ECU=6 actual", "inicio_capa_local": -3.7, "inicio_corte": -6.8, "inicio_yugo": -6.7}. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.

**pendiente — corrección propuesta, no aplicada:** Revisar dependencia conjunta de espesores, coordenadas z y profundidad de corte antes de variar estos parámetros; la configuración actual no demuestra propagación general.

## Propuestas priorizadas y efecto sobre una próxima corrida

| Prioridad propuesta | Acción pendiente | Efecto propuesto, no adoptado |
| --- | --- | --- |
| 1 | Antes de variar espesores/diámetros: resolver H02–H05 y H13; definir qué campo controla cota nominal, mínimo y dependencias. | Bloquear una corrida con parámetros modificados si no se demuestra coherencia. Con nominales actuales D no muestra desfase; no se inventa un fallo nativo. |
| 2 | Justificar brazo3,4, alto18, mínimo15, contacto arandela y apoyos (H08/H09). Completar etiquetas y fuentes H06/H07. | Condiciona una nueva conclusión resistente y aceptación de entrega. Una regeneración idéntica no resuelve las hipótesis. |
| 3 | Corregir el recuento documental 10+4 y precisar lectura parcial/ramas inactivas (H01/H11). | Corrección documental propuesta, sin cambiar ahora valores ni ecuaciones. |
| 4 | Planificar comprobaciones locales/FEA/ensayos para H12 según geometría y datos físicos acordados. | Mantener prediseño y límites declarados. No declarar seguridad o cumplimiento demostrado. |

**pendiente real:** primera integración nativa del cierre nuevo en una carpeta nueva y con autorización; clasificación A/B/C de D-12 con recorrido/tensión reales; medidas de bomba llena/vacía, masas, centro de gravedad, reparto, excentricidad, apoyos y precarga; tolerancias/proveedores, ensayos de textiles/desgaste/radio0,5, revisión local y fatiga. Esta auditoría no los ejecuta ni los convierte en datos medidos. Se puede ordenar las fuentes y resolver decisiones documentales sin disponer todavía de la bomba; su validación física seguirá pendiente.

## Cambios permitidos y comprobación de integridad

**hecho:** los entregables nuevos están dentro de esta carpeta de auditoría. Fuera de ella solo se añadió una sección corta al LEEME_P2_05.md y una línea a CHANGELOG_SEDAC.md. Las ocho modificaciones rastreadas del encargo previo se conservaron; no se repitió su implementación. No se hace commit, no se toca DECISIONES.md ni ESTADO_ACTUAL.md en este encargo.

**hecho:** all.png queda excluido como insumo y sin abrir; se cotejan solo sus metadatos (0 bytes). Las dos carpetas ajenas de OpenCode Nueva_20261022_183218_837 y Calculo_20261022_183238_628 se conservaron intactas según autorización «sí, continúa». La línea base previa está en INTEGRIDAD_ANTES.json. El cotejo final de archivos previos, CAD, fuentes y evidencia histórica queda en VERIFICACION_INTEGRIDAD.json; consultar ese resultado para el estado al finalizar, no inferirlo de esta frase.

**hecho — resultados de ejecución:** [RESUMEN.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/RESUMEN.json>), [RESULTADOS.json](<C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/01_CAD/Prototipo_P2/P2_05_20261019/Soporte/Auditoria_Coherencia_20261022_185635/Ejecucion_20261022_191216_989/RESULTADOS.json>). La primera exploración Ejecucion_20261022_190100 se conserva; la ejecución enlazada aquí es la final, con clasificación afinada y este informe. No se elimina la exploración.
