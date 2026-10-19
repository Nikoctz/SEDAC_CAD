# Guía personal de continuidad - SEDAC

## Estado actual - 17/10/2026

La propuesta local actual es **P2.04**, iniciada el 16/10 y cerrada el 17/10: estructura con dos canales abiertos, cuna textil y alas de cinturón flexibles. [Abrir entrega e instrucciones](01_CAD/Prototipo_P2/P2_04_20261016/LEEME.md).

- [Ensamblaje editable](01_CAD/Prototipo_P2/P2_04_20261016/Entrega/Inventor/SEDAC_P2_04.iam).
- Masa CAD resistente y protectores: 1.442 kg. Presupuesto con textiles y reservas: 2.212 kg; no incluye bomba/agua.
- Cálculos de prediseño y auditoría nativa incluidos. Todavía faltan medidas de bomba, selección/ensayo del arnés, tolerancias, fatiga y validación térmica/ergonómica.
- La memoria Mathcad y el PDF existentes corresponden a P2.03/P2.02; no validan P2.04. Se pospone la memoria completa hasta acordar esta geometría.
- P2.03 y versiones anteriores se conservan. Notion no fue modificado.

## Estado anterior - 16/10/2026

La revisión local actual es **P2.03**, prediseño aligerado a escala 1:1. [Abrir entrega e instrucciones](01_CAD/Prototipo_P2/P2_03_20261016/LEEME.md). Masa rígida estimada 2,333 kg, aproximadamente 26,0 % menor que P2.02; con reserva de mochila y accesorios, 2,913 kg. Aún no cumple el objetivo de 2 kg ni está validada para uso.

- [Mathcad final y PDF Beamer](06_DOCUMENTACION/Memoria_Calculo_P2_03/LEEME_MEMORIA.md).
- [Hoja personal de medición](01_CAD/Prototipo_P2/P2_03_20261016/HOJA_MEDICION_P2_03.md).
- P2.02 y su ZIP histórico siguen intactos. Los borradores P2.03 están dentro de Soporte/Iteraciones.
- Próximo paso: conseguir la bomba, medirla llena/vacía y seleccionar/pesar el arnés. No se ha actualizado Notion en esta entrega.

## Historial conservado hasta el 15/10/2026

Lo que sigue registra estados anteriores; las fechas previstas de octubre 6/7 pertenecen a ese historial.

# Guía personal de continuidad — SEDAC

**Actualizada:** 6 de octubre de 2026  
**Uso:** organización personal y navegación local. No reemplaza Notion ni convierte propuestas en especificaciones aprobadas.

## Estado rápido

- **P0 — CAD geométrico:** existen modelos del anclaje, cuna/base y separador, un ensamblaje demostrativo y una maqueta integrada adaptada aproximadamente a 1:12.
- **Envío a impresión:** según lo informado por Nicolás, se enviaron al centro el separador **1:1** y la maqueta integrada **1:12 adaptada**. Falta confirmar aceptación, laminado e impresión.
- **Prototipo funcional:** todavía no construido ni validado. P0 no demuestra resistencia, ajuste, comodidad ni seguridad.
- **Siguiente decisión de ingeniería:** medir una bomba real y comparar sus interfaces con P0 antes de cerrar P1 o P2.
- **P1/P2:** son rutas de diseño. 5052-H32, HDPE, espumas, malla y espesores mencionados en Notion siguen siendo candidatos sujetos a medición y revisión.

## Próximo bloque de trabajo

Si Consuelo consigue la bomba el miércoles 7 de octubre:

1. Confirmar marca/modelo y permiso para medirla.
2. Registrar condición de llenado, masa, instrumento y resolución.
3. Medir dimensiones generales, base, correas, tapa, bomba, manguera, controles y puntos de apoyo. Repetir cada cota dos veces.
4. Fotografiar frente, costados, espalda, base y parte superior con una regla visible; evitar incluir personas o datos identificables.
5. Completar el registro local de medición indicado abajo.
6. Comparar P0 contra la bomba real: **medida P0 | medida real | diferencia | decisión**.
7. Dejar P1/P2 abiertas hasta revisar esas diferencias.

**Pendientes personales:** respuesta del centro de impresión; modelo exacto de la bomba disponible; mediciones y fotos; revisar qué supuestos de P0 dejan de servir.

## Reglas para mantener trazabilidad

- Marcar cada dato como **medido**, **supuesto P0**, **propuesta** o **pendiente**.
- Mantener intactos los IPT/IAM fuente. Guardar nuevas iteraciones en carpetas/versiones nuevas.
- No usar espesores de PLA como espesores metálicos.
- No presentar visualizaciones conceptuales como CAD ni como evidencia de desempeño.
- IMU informa movimiento/orientación; por sí sola no mide fuerza ni presión.
- No declarar un beneficio ergonómico o de seguridad como validado antes de medir y probar.

## Mapa rápido de esta carpeta

- CONTEXTO_SEDAC.md: contexto técnico heredado de P0; algunas líneas de estado de impresión pueden quedar más antiguas que la actualización verbal del 6 de octubre.
- 01_CAD/Automatizacion/: generadores Python, reglas iLogic y sus instrucciones.
- 01_CAD/Ensamblajes/: kit de Inventor y auxiliares.
- 01_CAD/Exportaciones/: STL/3MF, verificaciones y vista de la maqueta.
- 02_PROTOTIPO/BOM/: BOM provisional del montaje geométrico.
- 02_PROTOTIPO/REGISTRO_MEDICION_BOMBA_LOCAL.md: hoja personal de captura para la medición.
- 06_DOCUMENTACION/Conceptos/: explicaciones e imágenes conceptuales.

## Dónde consultar decisiones compartidas

Notion PROYECTO SEDAC es la referencia compartida para decisiones y versiones. Esta guía guarda solo el estado operativo y los próximos pasos personales.

- [03.1 Requerimientos de diseño](https://app.notion.com/p/6c4594e1c7334fa7a705a2264399afa8)
- [03.3 Decisiones de diseño](https://app.notion.com/p/f9e7c4fa4d7a4146bb0858124edc4233)
- [03.4 CAD, materiales y fabricación](https://app.notion.com/p/3eef5e4bdb9081149933f6115b6f32b1)
- [03.5 Prototipo 0.1 y versiones](https://app.notion.com/p/951bc2fbad5048a690a15a153a2fab77)
- [Ficha de medición de la bomba](https://app.notion.com/p/3ebf5e4bdb90819b8bdce9716a5a2185)
- [03.8 Optimización de masa y materiales](https://app.notion.com/p/3f1f5e4bdb9081949942c96998f88385)

---
**Bitácora local:** anota aquí solo recordatorios personales breves; registra decisiones que afecten al equipo en Notion.
## Actualización 15/10/2026 — primera maqueta CAD P2

Ya existe una versión geométrica P2.01 de doble riel, generada en Inventor 2027.1. Incluye 12 componentes de referencia, ensamblaje IAM, miniatura IPT/STL, iLogic y vista previa.

[Instrucciones y alcance de P2](01_CAD/Prototipo_P2/P2_01_20261015/LEEME.md). Las cotas siguen siendo provisionales; no es un prototipo funcional validado. Esta entrada actualiza la situación del CAD, sin cambiar el historial P0.


## Actualización 15/10/2026 — revisión mecánica P2.02

Nuevo prediseño a escala 1:1 con estructura cerrada, cartelas, refuerzos, uniones con casquillos y ajuste discreto de hombros. [Abrir instrucciones](01_CAD/Prototipo_P2/P2_02_20261015/LEEME.md). Incluye parámetros editables, modelos nativos, STEP, cálculos y vistas. Masa representada aproximada 3,2 kg, sin arnés completo; objetivo de ligereza y validación física aún pendientes.


## Memoria de cálculo Mathcad MC01 — 15/10/2026

[Memoria editable y PDF](06_DOCUMENTACION/Memoria_Calculo_P2_02/LEEME_MEMORIA.md). Revisión de los cálculos de P2.02 con 130 variables comprobadas. Corrige la suma de esfuerzos en M8 y añade el caso de carga localizada en el borde del piso: el espesor actual de 2,5 mm no alcanza el margen 2,2 bajo ese escenario. La hoja compara 3,5 mm; el CAD conserva su geometría actual. Consultar REVISION_CALCULOS.md antes de usar los resultados preliminares anteriores.
