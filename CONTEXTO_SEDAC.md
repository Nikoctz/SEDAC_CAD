# CONTEXTO MAESTRO — PROYECTO SEDAC

Fecha de actualización: 6 de octubre de 2026

## 1. Objetivo

SEDAC es un prototipo académico para estudiar una interfaz de soporte entre un
arnés/panel y una mochila flexible Scotty 4000-BP Alpha. Los modelos actuales
son prototipos geométricos y maquetas para impresión 3D en PLA. No están
validados para soportar una mochila cargada ni para uso en una persona.

## 2. Restricción de impresión

Límite informado por el centro de innovación: **40 × 40 × 70 mm**.
Las dimensiones siempre se expresan en milímetros. El separador a escala real
y la maqueta integrada caben individualmente. El límite debe confirmarse con
el laminador si se agregan soportes o borde de adhesión.

## 3. Piezas principales

### Anclaje

- Archivo: `SEDAC_Anclaje.ipt`
- Dimensiones nominales: 90 × 75 × 8 mm.
- Ranura horizontal: 52 × 5 mm nominal, para una correa asumida de 50 × 2 mm.
- Dos ranuras verticales: 6,2 mm de ancho y 30 mm de largo total.
- Separación entre centros de ranuras verticales: 66 mm.
- Material previsto para prototipo: PLA.
- No cabe a tamaño real en 40 × 40 × 70 mm.

### Cuna/base

- Archivo: `SEDAC_Cuna_Base_V0.1.ipt`
- Dimensiones nominales: 280 × 140 × 66 mm.
- Piso nominal: 6 mm.
- Pared posterior: 60 mm sobre el piso.
- Labios laterales: 15 mm sobre el piso.
- Frente abierto y escotadura central en U de aproximadamente 60 mm de ancho y 90 mm de profundidad.
- Es una representación PLA de una futura base metálica; los 6 mm no son una especificación de chapa.
- No cabe a tamaño real en 40 × 40 × 70 mm.

### Separador

- Geometría: anillo exterior Ø18 mm, interior Ø5,5 mm, largo 6 mm.
- Archivo editable iLogic: `01_CAD/Automatizacion/SEDAC_Separador_V01.iLogicVb`.
- STL listo para impresión: `01_CAD/Exportaciones/SEDAC_Separador_18x5p5x6_V01.stl`.
- Verificación: envolvente 18 × 18 × 6 mm, malla cerrada.
- El STL no contiene unidades; importarlo seleccionando **Millimeter**.
- Para dos anclajes se habían previsto cuatro unidades físicas.

## 4. Kit de ensamblaje

- Regla: `01_CAD/Automatizacion/SEDAC_Kit_Montaje_V01.iLogicVb`.
- Ensamblaje de demostración estático; las ocurrencias quedan Grounded y no hay
  restricciones cinemáticas.
- Contiene panel provisional, dos anclajes, una base, separadores, arandelas,
  tuercas y tornillos simplificados sin roscas reales.
- El kit generado se encuentra también en `SEDAC_Kit_Montaje_V01.iam` y en la
  carpeta `01_CAD/Ensamblajes/`.
- El archivo `ESTADO.txt` de esa carpeta documenta las 40 ocurrencias.
- El ensamblaje es demostrativo: no debe interpretarse como validación mecánica.

## 5. Maqueta integrada para imprimir

Para que el kit completo quepa en el límite, se generó una maqueta como un solo
volumen conectado, con disposición aproximada 1:12 y espesores/detalles
adaptados para que sean visibles e imprimibles.

- Carpeta: `01_CAD/Exportaciones/Maqueta_Kit_1a12/`.
- STL: `SEDAC_Kit_Maqueta_1a12_ADAPTADA_mm.stl`.
- 3MF: `SEDAC_Kit_Maqueta_1a12_ADAPTADA_mm.3mf`.
- Envolvente verificada: 30 × 35 × 13,27 mm.
- El 3MF declara unidades en milímetros; el STL debe importarse indicando mm.
- Incluye panel, cuna, dos anclajes, separadores y fijaciones simplificadas.
- No es desmontable y no representa roscas ni resistencia real.
- La maqueta todavía no ha sido laminada ni impresa; revisar soportes bajo los
  anclajes y la abertura de la cuna.

## 6. Maqueta editable en Inventor

- iLogic: `01_CAD/Automatizacion/SEDAC_Maqueta_Editable_V01.iLogicVb`.
- Ejecutar en una pieza `Standard.ipt` completamente vacía.
- Después de ejecutar, guardar manualmente como `SEDAC_Maqueta_Editable_V01.ipt`.
- La regla crea operaciones nativas y un cuerpo integrado; no debe pegarse en
  una pieza que ya contenga el STL.
- La regla no se ha confirmado ejecutándose completamente en Inventor.
- Instrucciones adicionales: `01_CAD/Automatizacion/MAQUETA_EDITABLE_LEEME.md`.

## 7. Archivos que enviar a impresión

Enviar normalmente una unidad de cada STL:

1. `SEDAC_Separador_18x5p5x6_V01.stl` — escala 1:1.
2. `SEDAC_Kit_Maqueta_1a12_ADAPTADA_mm.stl` — maqueta integrada adaptada.

También puede enviarse el 3MF de la maqueta si el centro lo acepta. No enviar
los archivos iLogic o Python como archivos de impresión.

## 8. Supuestos y límites

- La mochila Scotty 4000-BP Alpha es flexible; las medidas publicadas del
  producto no sustituyen la medición del arnés, panel ni herrajes reales.
- Las medidas no verificadas físicamente son supuestos de prototipado.
- Los modelos de tornillos, tuercas y arandelas del kit son referencias visuales;
  no se deben fabricar como herrajes funcionales desde estos archivos.
- No se ha hecho análisis estructural, prueba de carga, prueba de ajuste ni
  validación de seguridad.
- Mantener los originales y regenerar versiones en carpetas nuevas; no
  sobrescribir piezas fuente sin una copia.

## 9. Cómo continuar en otro chat

Adjuntar este archivo junto con `SEDAC_CAD_proyecto.zip` y pedir:

> Continúa el proyecto SEDAC. Lee primero CONTEXTO_SEDAC.md y revisa los
> archivos CAD y documentación adjuntos. Distingue lo que está comprobado de
> lo que aún debe ejecutarse o verificarse en Inventor.
