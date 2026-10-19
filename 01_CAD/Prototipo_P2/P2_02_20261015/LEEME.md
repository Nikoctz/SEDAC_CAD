# SEDAC P2.02 — Cómo abrir y ajustar

La revisión final está indicada en ULTIMA_EJECUCION.txt.

1. Abrir SEDAC_P2_02.iam dentro de esa carpeta, conservando todos los IPT juntos.
2. Para compartir la geometría con otros programas CAD: SEDAC_P2_02_REVISION.step.
3. Para ver el resultado: VISTA_FRENTE.png, VISTA_ESPALDA.png y VISTA_ESTRUCTURA.png.
4. Leer INFORME_DISENO.md para conocer cargas supuestas, decisiones y comprobaciones.

## Ajustar cuando llegue la bomba

Editar PARAMETROS_P2_02.json: altura, separación de rieles, cuna, espesores o escenario de carga. Después ejecutar REGENERAR_P2_02.ps1 en este computador con Inventor instalado.

La regeneración crea una carpeta nueva y recalcula la selección de perfil. No sobrescribe P2.01. Las medidas del JSON controlan la generación; las piezas no se actualizan entre sí al arrastrarlas ni cambiar un boceto. Si se modifica un IPT manualmente, ese cambio no regresa al JSON.

El generador impone un intervalo de geometría estudiado y un umbral analítico. Un cambio puede necesitar ampliar/revisar el modelo de cálculo; no basta con escalar todo. Tampoco se puede deducir resistencia de una maqueta impresa.

El script está configurado para Inventor 2027 y el Python incluido en Codex de este equipo. Al cambiar de computador, revisar esas rutas.

## Verificaciones y límites

- CALCULOS_PRELIMINARES.json: valores calculados con hipótesis.
- COMPARACION_RIELES.csv: alternativas evaluadas.
- INTERFERENCIAS.json: choques volumétricos del modelo nominal. No comprueba tolerancias, holgura de herramientas, acceso de montaje ni cables.
- REDONDEOS.json: resultado real del redondeo de cantos.
- MASAS_CAD.json: volumen de Inventor multiplicado por densidad candidata; cuenta las ocurrencias. No usar la masa del material genérico de Inventor.
- BOM_MODELO.csv: piezas representadas. El inventario de compra final de herrajes/textiles está pendiente.
- ESTADO_OK.txt: confirma generación y actualización nativa, no seguridad del equipo.

Los herrajes REF son envolventes simplificadas sin rosca. No imprimir ni fabricar tornillos a partir de ellos. El STEP es para revisión; faltan planos/desarrollos de chapa.

La masa total representada incluye materiales de contacto y herrajes aproximados; aún faltan cinturón, tirantes, cintas, hebillas y otros detalles. El objetivo de reducir la masa añadida sigue abierto. El arnés/cinturón y la bomba no están modelados como piezas funcionales.

## Historial

P2.01 sigue como maqueta geométrica inicial. Las carpetas intermedias dentro de P2.02 conservan el estudio; usar únicamente la señalada por ULTIMA_EJECUCION.txt y el ZIP de entrega. Las primeras iteraciones incluyen pruebas de perfiles diferentes o interferencias corregidas.

