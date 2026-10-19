# Anclaje SEDAC V0.1 — regla iLogic

Estado: preparada, sin ejecutar ni compilar en Inventor. No se ha creado un IPT mediante esta regla.

## Ejecutar en la pieza abierta

1. Activar una pieza estandar vacia y salir de cualquier boceto.
2. Administrar > iLogic > Anadir regla. Nombre: SEDAC_Generar_Anclaje.
3. Copiar todo el contenido de SEDAC_Anclaje_V01.iLogicVb en el editor de la regla.
4. Guardar y ejecutar la regla. Si aparece un error, conservar su texto para corregirlo.
5. Guardar la pieza como SEDAC_Anclaje_Regulable_V0.1.ipt.

Tambien se puede agregar el archivo como regla externa desde el navegador iLogic y ejecutarla.

## Geometria inicial

Todas las cotas de esta pieza son supuestos autorizados por el usuario; no son cotas de fijacion oficiales de Scotty.

- Base: 90 x 75 x 8 mm, esquinas R5 en planta.
- Paso de cinta: abertura oblonga 52 x 5 mm, centro (45; 57,5) mm.
- Cinta supuesta: 50 x 2 mm. El contorno redondeado reduce localmente la holgura en las esquinas.
- Dos ranuras verticales: ancho 6,2 mm, largo TOTAL 30 mm incluyendo extremos semicirculares.
- Centros: (12; 25) y (78; 25) mm; separacion 66 mm.
- Tornillos supuestos M5 con tuerca y arandelas comerciales; no se crean tornillos ni roscas.
- Recorrido nominal del centro de un tornillo de 5 mm: 30 - 5 = 25 mm; no garantiza bloqueo bajo carga.
- Bordes superiores e inferiores redondeados R2, incluidos los del paso de cinta.
- Coordenadas desde la esquina inferior izquierda de la envolvente exterior.

Este es un soporte de paso/retencion de un lazo de cinta; no es una hebilla autoblocante. El modo de terminar o cerrar la cinta queda pendiente. La placa, las arandelas, las tuercas y el acceso posterior tambien deben definirse antes del montaje funcional.

## Edicion y limites

Modificar los parametros SEDAC_* en Administrar > Parametros y volver a ejecutar la regla. La geometria de los bocetos se genera desde esos parametros; no son bocetos completamente acotados con actualizacion automatica. El espesor y el radio de borde si estan ligados directamente a expresiones de operaciones.

Al regenerar se eliminan y reconstruyen unicamente las tres operaciones generadas, tras comprobar nombres y estructura. No agregar operaciones o bocetos adicionales si se desea usar esta regeneracion. Guardar una copia antes de extender el modelo manualmente.

La regla actua en el documento activo, no abre ni guarda documentos automaticamente. Se detiene ante una pieza que ya contiene geometria ajena. Incluye transaccion con reversion ante errores y una comprobacion de actualizacion y solido, que solo se ejecutaran al correrla en Inventor.

PLA es el material fisico previsto para una maqueta de ajuste; no se asignan propiedades mecanicas ni se afirma resistencia a la carga de la bomba. No hay analisis estructural ni laminado realizado.

## Referencia de equipo

La ficha oficial de Scotty Alpha Backpack identifica 4000-BP como el conjunto completo: https://scottyfire.com/product/alpha-backpack/

La bolsa vacia figura con 25 x 16,5 pulgadas (635 x 419,1 mm). Esas cotas generales no determinan este anclaje ni garantizan compatibilidad. Los 76,2 mm de ancho acolchado no confirman el ancho de cinta de ajuste. No se modela una profundidad de bolsa como si fuera un dato oficial.

Referencias API consultadas: Autodesk Inventor API, SketchArcs.AddByCenterStartEndPoint, FilletFeatures.AddSimple y ExtrudeFeature.Delete.
