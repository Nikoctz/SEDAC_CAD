# Primera corrección de dependencias — P2.05, 2026-10-22

## Alcance y autorización

**hecho:** el responsable indicó «ok, pasa al siguiente paso» después de recibir la auditoría y la propuesta de resolver dependencias antes de variar dimensiones. Se aplica una primera corrección de código sobre H03 y parte de H13. No se cambian valores del JSON ni ecuaciones del cálculo resistente.

**hecho:** se leyeron CONTEXTO_SEDAC.md, ESTADO_ACTUAL.md, DECISIONES.md y CHANGELOG_SEDAC.md, después el generador, los parámetros y los hallazgos de la auditoría. Se cotejó el estado de Git y las huellas de 4725 archivos previos antes de la edición. Los cambios anteriores del mismo agente y las excepciones ajenas autorizadas permanecían concordantes.

## Qué se implementó

| Elemento | Expresión anterior | Expresión nueva | Estado |
| --- | --- | --- | --- |
| Inicio exterior de mejilla | cx−B/2−3 | cx−B/2−EM | **hecho:** implementado en lumbar/yugos y puntos relacionados |
| Agarre de la unión | B+6 | GRIP=B+2×EM | **hecho:** usado por tornillos, cortes y pasador |
| Longitud de pasador | B+6−0,4 | GRIP−0,4 | **hecho:** retranqueos existentes conservados |
| Inicio de capas locales | −3,7 | Z_CAPA=Z0+ECU | **hecho:** se enlaza con la cara superior de la placa lumbar |
| Inicio de cortes en z | −6,8 | Z_CORTE=Z0−0,1 | **hecho:** sobrepaso existente conservado |
| Inicio de placa de yugo | −6,7 | Z0 | **hecho:** misma referencia ya usada por la placa lumbar |
| Contorno de mejilla lumbar en z | inicio −3,7; altura D+3,7 | inicio Z_CAPA; altura D−Z_CAPA | **hecho:** conserva extremo superior en D |

**cálculo de intención, no comparación de salidas ejecutada:** con B=32, EM=3, ECU=3 y espesor_anclaje=6, GRIP=38 mm; pasador=37,6 mm; Z0=−6,7 mm; Z_CAPA=−3,7 mm; Z_CORTE=−6,8 mm. Son relaciones aritméticas con los nominales existentes. Todavía no se ha comprobado la serialización exacta ni la salida completa del generador modificado.

**hecho:** el cambio completo está en [CAMBIO_GENERADOR.diff](CAMBIO_GENERADOR.diff); la fuente previa queda en [generar_p2_05_ANTES.py](generar_p2_05_ANTES.py), con fines de comparación. Esa copia no es un generador autónomo para ejecutar desde esta carpeta: sus rutas relativas corresponden a su ubicación original.

## Qué no queda resuelto

- **pendiente:** H03 implementado, pero no verificado mediante regeneración ni variaciones de parámetros. No se declara cerrado.
- **pendiente:** H13 solo parcial. La segunda capa de cuna sigue con espesor ECU y, por tanto, el espesor nominal local sigue siendo 2×ECU; no se lo sustituyó por espesor_anclaje sin justificar esa intención. Tampoco se resolvieron las demás coordenadas fijas ni el contacto real.
- **pendiente:** H02 (puentes y separación de pernos), H04 (ID máximo y tolerancias de pasador), H05 (mínimo propio de mejilla), H06–H09 y los demás límites de la auditoría. El mínimo 2,8 mm del canal no queda validado para la mejilla por esta edición.
- **supuesto existente:** sobrepasos 0,1 mm, retranqueos 0,2 mm por extremo y radio 0,5 mm siguen sin validación física. No se crean nuevas tolerancias ni se afirman ajustes correctos para variantes.

## Qué se comprobó en este paso

**hecho:** lectura del diff y cotejo de integridad de archivos. REGISTRO_INTEGRIDAD.json conserva los resultados: archivos previos cambiados, fuentes protegidas, CAD, evidencia de OpenCode, auditoría anterior y metadatos de all.png.

**hecho:** no se añadieron ni ejecutaron pruebas, no se ejecutó el generador modificado, no se regeneraron JSON/BOM de control y no se abrió Inventor. Los resultados idénticos de la auditoría anterior corresponden exclusivamente al generador anterior; no son evidencia de esta corrección. El auditor anterior contiene búsquedas de expresiones que ahora cambiaron y deberá adaptarse si se quiere repetir sobre estas fuentes. Se preservó su carpeta como evidencia histórica.

**hecho:** archivos existentes modificados en este paso: Soporte/generar_p2_05.py, LEEME_P2_05.md §12, ESTADO_ACTUAL.md (seguimiento fechado) y una línea de CHANGELOG_SEDAC.md. Los demás entregables se crean dentro de esta carpeta. DECISIONES.md no se modifica: esta edición no adopta valores físicos ni una decisión de rediseño.

## Próxima comprobación pendiente

**pendiente:** en una verificación posterior, ejecutar ambas versiones con los mismos parámetros y salidas nuevas; comparar MODELO_API.json y BOM_FIJACIONES.csv completos, y después comprobar la propagación de las relaciones modificadas sin tocar los parámetros del proyecto. No atribuir los resultados anteriores al código nuevo. Solo tras esa evidencia se podrá declarar la corrección comprobada en la descripción; seguirán pendientes la integración nativa y la validación física.

**hecho:** no hubo commit, push, borrados ni modificaciones CAD. P2.04 sigue vigente; P2.05 permanece abierta.
