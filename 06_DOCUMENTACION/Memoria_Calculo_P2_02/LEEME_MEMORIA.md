# Memoria de cálculo SEDAC P2.02 — MC01

## Archivos para usar

- **Guia_SEDAC_P2_02_MC01_Beamer.pdf**: versión actual de la guía explicativa, en LaTeX Beamer, con 44 diapositivas y ecuaciones compuestas. El índice enlaza con las 17 secciones de Mathcad.
- **Guia_SEDAC_P2_02_MC01_Beamer.tex**: fuente editable autónoma de esa guía, sin archivos de imagen externos.

- **Guia_Explicada_Memoria_SEDAC_P2_02_MC01.pdf**: versión anterior de 27 páginas con desarrollos, teoría de fallas, funciones de Mathcad y ejemplos; el índice de la página 2 relaciona cada capítulo con las 17 secciones de la hoja.

- **Memoria_SEDAC_P2_02_MC01_EDITABLE.xmcd**: hoja nativa de Mathcad clásico compatible con Mathcad 15. Contiene fórmulas, unidades, entradas resaltadas y resultados editables.
- **Memoria_SEDAC_P2_02_MC01.pdf**: copia estática de consulta, de 17 páginas. Las ecuaciones y los resultados se renderizaron en Mathcad.
- **REVISION_CALCULOS.md**: cambios de método y diferencias respecto del cálculo preliminar anterior.
- **Soporte**: fuentes técnicas de generación y verificaciones. No es necesario abrirlas para trabajar con la memoria.

Abrir el XMCD con Mathcad. Modificar las entradas resaltadas y usar el comando de recalcular. Los resultados dependen del orden de lectura de la hoja; conservar las definiciones antes de sus evaluaciones.

## Contenido

1. Escenario de carga y geometría.
2. Materiales y factores provisionales.
3. Propiedades exactas de sección con radios.
4. Rieles: flexión, cortante, torsión, fluencia, flecha y estimaciones de pandeo.
5. Cartelas y M8: resultante, cortante, aplastamiento y arrancamiento.
6. Piso de cuna y carga localizada.
7. Refuerzos, puentes de cinta, yugo, diagonales y M6.
8. Resumen y límites.

## Resultado que requiere revisión del CAD

El modelo actual conserva un piso de **2,5 mm**. En el escenario adicional de un parche de 100 N sobre una franja de 50 mm, colocado en el borde delantero, tomando los ejes de los refuerzos como apoyos, el margen calculado es aproximadamente **1,22**, inferior al objetivo de **2,2**.

La hoja calcula un espesor orientativo necesario de aproximadamente **3,36 mm** bajo ese modelo y compara **3,5 mm**, con margen aproximado **2,38**. Es una propuesta de cálculo: también puede estudiarse reducir el voladizo o cambiar el apoyo. No equivale a aprobar 3,5 mm para fabricación.

La memoria no cambia el CAD ni sus parámetros automáticamente. Las hipótesis de contacto, carga puntual, unión y brazo deben revisarse con la bomba real. La resistencia a fatiga, el arnés, el fuego y las pruebas siguen pendientes.

## Verificación

- Esquema XML oficial de la instalación: válido.
- 130 valores recalculados en Mathcad y contrastados con un control independiente de evaluación.
- Hoja guardada: sin regiones con atributo de error.
- PDF: sin superposiciones ni regiones fuera de página; revisión visual de las 17 páginas.
- El motor COM de la instalación reporta 14.1.4.587. Se utilizó el formato XMCD clásico, no el formato de Mathcad Prime.

Esta verificación comprueba la ejecución y consistencia de las ecuaciones declaradas; no demuestra por sí sola la validez física de las idealizaciones.

## Fuentes

- Scotty: https://scottyfire.com/wp-content/uploads/2017/04/2017ScottyFireCatalogue_LR.pdf
- Hydro 6061: https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf
- Atlas 5052: https://atlassteels.com.au/wp-content/uploads/2021/08/Aluminium-Alloy-5052-Data-Sheet-24-06-21.pdf
- Atlas, diferencias entre especificaciones: https://www.atlassteels.com.au/documents/TN14-5052%20and%205251%20rev%20June%202013.pdf
- Bossard: https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources-old/stainless-steel-fasteners.pdf
- NASA RP-1228: https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf

Fecha: 15/10/2026. Revisión documental MC01.

