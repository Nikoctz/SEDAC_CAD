# SEDAC P2.01 — Maqueta de doble riel

Creada el 15/10/2026 en la carpeta de Documentos. P0 permanece como referencia histórica.

## Abrir y usar

1. Consultar ULTIMA_EJECUCION.txt para la carpeta de la generación nativa terminada.
2. Abrir SEDAC_P2_01.iam dentro de esa carpeta. Mantener todos sus IPT en la misma carpeta.
3. Abrir SEDAC_P2_Maqueta_1a12_ADAPTADA.ipt para la miniatura de un único cuerpo.
4. VISTA_PREVIA_P2.png muestra dos vistas del diseño y la miniatura, calculadas a partir de la misma geometría. CAPTURA_INVENTOR_P2.png, si existe, es una captura real del visor.

El ensamblaje contiene 12 piezas y ocurrencias fijadas, sin restricciones de montaje. Bocetos editables, sin acotación completa. Se diseñó como maqueta preliminar; aún faltan uniones reales, arnés, cinturón y bomba.

## Si Vector pide un nuevo STL

SEDAC_P2_Maqueta_1a12_ADAPTADA_mm.stl es la maqueta de la estructura P2.
- Importar en milímetros; aproximadamente 24,37 × 35 × 11,96 mm.
- Disposición 1:12 con espesores aumentados, mínimo de representación 1,2 mm.
- Omite respaldo, pads y ranuras pequeñas.
- Malla cerrada, orientada y conectada: consultar VERIFICACION_MALLA.json.
- Requiere revisión en el laminador del laboratorio: soportes, orientación y detalle mínimo.
- Sirve para comunicar la arquitectura. No prueba resistencia, masa ni comodidad.
- El límite 40 × 40 × 70 proviene del registro anterior; confirmar que sigue vigente.

## Regenerar mediante iLogic

La regla SEDAC_P2_GENERAR.iLogicVb es autosuficiente.
1. Abrir Inventor y crear una pieza vacía para alojar la regla.
2. Administrar > iLogic > Agregar regla; pegar el contenido completo.
3. Revisar la ruta root y ejecutar.
4. La regla genera una carpeta Inventor_FECHA_ID y guarda piezas y ensamblaje nuevos.
5. Consultar ESTADO_OK.txt o ERROR.txt en esa carpeta.

No ejecutarla como regla automática de cambio de parámetros: cada ejecución crea otra versión. Para cambiar cotas, editar las llamadas Block y regenerar. Los modelos no se actualizan asociativamente entre sí.

La generación nativa se ha intentado mediante la API directa porque el enlace externo de iLogic del equipo presenta incompatibilidad COM. El estado final queda documentado en ESTADO_ENTREGA.md; entregar la regla no implica afirmar que se haya ejecutado en iLogic.

## Alcance del diseño

Leer ESPECIFICACION_P2.md antes de modificar o fabricar. Los colores representan funciones; las propiedades mecánicas de material no están asignadas ni validadas. Los pliegues están aproximados con geometría prismática: no hay desarrollo de chapa, radios, factor K ni planos de fabricación.

Archivos técnicos de apoyo: GEOMETRIA_P2.json, generar_entrega_p2.py y GENERAR_NATIVO.ps1. Cambiar el JSON por sí solo no modifica la regla ya generada. El generador Python reconstruye su geometría desde su definición inicial; cambiar esa definición si se desea mantener sincronizados regla, STL y vista.

Referencia API utilizada: https://help.autodesk.com/cloudhelp/2024/ENU/Inventor-API/files/ExtrudeDefinition.htm

