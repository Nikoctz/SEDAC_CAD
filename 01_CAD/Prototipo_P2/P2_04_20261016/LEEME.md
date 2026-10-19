# SEDAC P2.04 — abrir y editar

**Archivo principal:** [Entrega/Inventor/SEDAC_P2_04.iam](Entrega/Inventor/SEDAC_P2_04.iam).

1. Extraer el ZIP completo antes de abrirlo.
2. Abrir SEDAC_P2_04.iam en Inventor 2027.1. Mantener todos los IPT junto al IAM.
3. En Representaciones > Vista, elegir **Con_arnes** o **Estructura**.
4. Para editar una pieza, abrir su IPT o hacer doble clic desde el ensamblaje. Tiene bocetos, extrusiones, radios y roscas nativas.

## Archivos útiles

- **Entrega/Inventor/*.ipt:** piezas editables; REF_ significa textil, acolchado o hebilla provisional.
- **SEDAC_P2_04_REVISION.step:** intercambio/visualización en otros programas. No conserva el historial de operaciones ni es un STL preparado para impresión.
- **VISTA_FRENTE.png, VISTA_ESPALDA.png, VISTA_ESTRUCTURA.png:** capturas del CAD real.
- **INFORME_DISENO_P2_04.md:** decisiones, cuentas y límites del diseño.
- **BOM_Y_MASAS.csv / RESUMEN_ENTREGA.json:** cantidades y presupuesto de masa.
- **PARAMETROS_P2_04.json:** entradas para cambios coordinados y regeneración.
- **Calculos/:** comprobaciones analíticas de prediseño.
- **Soporte/:** generadores reproducibles. Las iteraciones de trabajo locales no forman parte del ZIP de entrega.

## Cómo editar medidas

Los IPT contienen parámetros Oxx_Posicion y Oxx_Espesor vinculados a operaciones. Los canales tienen Altura_refuerzo. Los contornos están en bocetos nativos editables. Cambiar una longitud de pieza no desplaza automáticamente los anclajes de otras piezas.

Para una revisión coordinada, guardar una copia de esta carpeta, modificar PARAMETROS_P2_04.json, recalcular y regenerar con Soporte/CONSTRUIR_P2_04.ps1. Las medidas propuestas nuevas pueden exigir editar también las operaciones del generador: no todos los puntos de cintas y ranuras son relaciones paramétricas globales. El constructor usa Inventor 2027 instalado y Python con NumPy; las rutas de dependencias deben adaptarse en otro computador. Si no se indica Salida, la nueva generación se guarda en una iteración fechada para proteger la entrega.

## Estado

CAD rígido y protectores: **1.442 kg**. Presupuesto completo, incluyendo 0,650 kg de mochila/textiles y 0,120 kg adicionales: **2.212 kg**. No es una masa pesada ni incluye bomba/agua. Reducción comparable del CAD: 38.2 % frente a P2.03.

Prediseño, dimensiones aún propuestas. Las verificaciones no acreditan el sistema para uso con una persona. Textiles, costuras y cierres son referencias de interfaz. No hay una memoria Mathcad/PDF nueva: se ha pospuesto hasta acordar esta geometría. P2.03 y P2.02 se conservan.
