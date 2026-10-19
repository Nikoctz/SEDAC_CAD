# Ejecutar el kit SEDAC

## Para imprimir una primera muestra ahora

Abrir 01_CAD/Exportaciones/SEDAC_Separador_18x5p5x6_V01.stl en el laminador, importar en MILIMETROS y comprobar que mida 18 x 18 x 6 mm. Orientar con el eje del agujero vertical. Probar una unidad antes de repetir. Se genero directamente como malla (no como exportacion del IPT); coincide con las dimensiones nominales de ambas reglas. Se comprobo cierre, orientacion de caras, volumen y envolvente. No se ha laminado ni probado fisicamente.

El registro de comprobacion esta junto al STL con sufijo _verificacion.json.

## Opcion completa: separadores, herrajes y ensamblaje

1. Guardar los archivos existentes SEDAC_Anclaje.ipt y SEDAC_Cuna_Base_V0.1.ipt en la raiz de SEDAC_CAD. Ya se localizaron alli.
2. Abrir un nuevo ensamblaje estandar: File > New > Standard (mm).iam (o plantilla de Assembly disponible).
3. Manage > iLogic > Add Rule > Text. Nombre: SEDAC_Generar_Kit.
4. Pegar TODO SEDAC_Kit_Montaje_V01.iLogicVb y Save & Run.
5. La regla crea y activa OTRO ensamblaje nuevo y lo guarda en 01_CAD/Ensamblajes/Kit_V01_fecha_hora_identificador/. El ensamblaje inicial solo sirve para ejecutar la regla.

Cada ejecucion usa una carpeta distinta; no sobrescribe la anterior. El ensamblaje referencia las dos piezas originales por ruta y genera sus auxiliares en Componentes/. No mover fuentes sin actualizar referencias. La regla no guarda cambios pendientes en las fuentes: pide guardarlos primero.

El separador queda creado por esta opcion; NO es obligatorio ejecutar tambien la regla independiente. El modelo tiene diametros 18 y 5,5 mm, longitud 6 mm. Estas tres dimensiones son parametros vinculados al boceto y extrusion.

## Opcion simple: solo separador

En una NUEVA pieza vacia, Manage > iLogic > Add Rule > Text; pegar TODO SEDAC_Separador_V01.iLogicVb. Guardar como SEDAC_Separador_6mm_V0.1.ipt. Luego editar parametros SP_* para ajustar; no volver a ejecutar en el mismo archivo ya creado.

## Estado y limites

Las reglas se revisaron como texto y se comprobo aritmeticamente el apilamiento. No se han compilado ni ejecutado en Inventor por el asistente. Si falla, enviar mensaje completo y etapa. Una ejecucion fallida conserva los archivos parciales en su carpeta, sin borrar nada ni alterar los modelos fuente.

Limite confirmado: 40 x 40 x 70 mm. SOLO el separador cabe a escala real; el anclaje y la base se conservan para montaje digital, no para imprimir en esa maquina. Revisar la ficha de herrajes disponibles antes de comprar. Ver 02_PROTOTIPO/BOM/KIT_MONTAJE_V01.md para cantidades y supuestos.
