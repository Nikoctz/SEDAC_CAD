# Maqueta editable en Inventor

1. File > New > pieza Standard.ipt. No abrir el STL para este paso.
2. Manage > iLogic > Add Rule. Nombre: Maqueta_SEDAC.
3. En Text, pegar todo SEDAC_Maqueta_Editable_V01.iLogicVb.
4. Save & Run. Al finalizar, Ctrl+S y guardar como SEDAC_Maqueta_Editable_V01.ipt.

La regla no guarda ni sobrescribe archivos. El IPT se crea al ejecutarla en
Inventor y guardarla; el archivo iLogic por si solo no es un IPT.
No se ha ejecutado esta regla en Inventor desde el asistente.

La geometria reconstruye la maqueta adaptada a 1:12: 30 x 35 x 13.267 mm,
con un cuerpo integrado, curvas nativas y operaciones nombradas. Conserva la
disposicion y detalles del STL, con circulos geometricos en vez de poligonos.
No incluye roscas funcionales ni piezas desmontables.

Edicion: expandir una operacion y editar su boceto; Edit Feature para modificar
su extrusion. Los bocetos no estan completamente acotados. Las posiciones y
espesores no forman un sistema global de parametros enlazados: al cambiar una
zona hay que revisar sus uniones y operaciones dependientes. Los valores de
construccion estan en milimetros en el codigo. Para regenerar desde valores
cambiados usar otra pieza vacia; no ejecutar de nuevo sobre la maqueta existente.

La regla comprueba un cuerpo y la envolvente limite al finalizar. Cambios
posteriores requieren revisar dimensiones y preparar de nuevo el laminado.
Consultar el LEEME de Exportaciones/Maqueta_Kit_1a12 para material y soportes.
