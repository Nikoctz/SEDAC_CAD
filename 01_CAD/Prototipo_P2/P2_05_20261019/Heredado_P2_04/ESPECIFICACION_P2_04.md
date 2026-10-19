# Especificación previa P2.04 — 16/10/2026

UNIDADES:
- Milímetros (mm); ensamblaje maestro 1:1. Las imágenes conceptuales no aportan cotas verificadas.

TIPO DE PIEZA/PLANO:
- Sistema auxiliar desmontable para la bolsa flexible Scotty: espaldera semirrígida, dos refuerzos independientes y cuna textil.
- Inventor nativo. Modelo de prediseño editable; no liberado a fabricación ni uso.

PARÁMETROS GEOMÉTRICOS:
- Refuerzos propuestos mediante cribado mecánico: canal abierto 32 × 24 × 3 mm, longitud 480 mm, separación 190 mm. Pared mínima de cálculo 2,8 mm.
- Interfaz lumbar con cuerpo de 3 mm y refuerzos locales de 6 mm en anclajes. Yugos de hombro independientes, placa de 6 mm y mejillas de 3 mm. Ranuras dedicadas para cinturón y cuna.
- Canales sin ventanas en el alma, debido a incertidumbre del recorrido del momento. Taladros de unión Ø10,2 mm, raíces interiores de 2 mm y bordes protegidos.
- Panel HDPE de contacto 1 mm, recortado para ventilación y flexión; no se le asigna resistencia estructural.
- Cuna y cintas representadas para edición; patrones, costuras y ajuste antropométrico pendientes.
- Parámetros editables en PARAMETROS_P2_04.json. En los IPT hay bocetos/operaciones nativas y parámetros vinculados a posiciones y espesores.
- Tolerancias: pared mínima y espesor mínimo de anclaje se exploran en cálculo; tolerancias de fabricación completas no especificadas.
- Roscas: propuesta M5×55, paso 0,8, clase geométrica 6g/6H, tornillo A2-80 con tuerca metálica autofrenante de proveedor por seleccionar. Rosca nativa cosmética. Arandelas gruesas 5,3×16×3, pasadores huecos Ø10/5,5 y separadores Ø12,5/10,2 de aluminio.

OPERACIONES:
- Secuencia propuesta: mecanizar/extruir canales certificados, cortar ventanas y taladros; mecanizar interfaces con radios; preparar panel de contacto; confeccionar y ensayar textiles; ensamblar.
- El modelo geométrico no define un proceso de doblado de 6061-T6 ni acredita resistencia en soldaduras.
- Comprobar sólidos, actualización, masas, referencias y colisiones nominales de piezas rígidas en Inventor.

MATERIAL Y FABRICACIÓN:
- 6061-T6 para canales e interfaces; Sy de prediseño 240 MPa a temperatura ambiente según ficha de extrusión Hydro.
- Acero inoxidable A2-80 para tornillos; prueba de tuercas y par prevalente pendientes.
- HDPE solo para contacto; textiles y acolchados son propuestas sin especificación térmica cerrada.
- Acabado: radios de contacto y protección textil; anodizado/aislamiento de metales diferentes pendientes de definición.
- Disponibilidad comercial de la sección y coste de proceso pendientes.

ENTREGABLES:
- IAM y todos sus IPT, parámetros, regenerador, informe breve y registros analíticos/de Inventor, vistas reales del CAD y ZIP portable.
- Mathcad/PDF completos se posponen hasta acordar la geometría, conforme a la preferencia previa del usuario.

DATOS FALTANTES CRÍTICOS:
- Bomba llena/vacía, centro de masa, interferencias con tapa/manguera/costuras y tallas de usuarios: bloquean cerrar el diseño fabricable y el ajuste real, no esta maqueta parametrizada.
- Textiles, hebillas, anclajes y temperatura de servicio: bloquean validar el conjunto para uso.
- No se solicita repetir medidas que el usuario ya indicó no poder obtener aún.

SUPUESTOS:
- Escenario anterior conservado: 25 kg totales transportados, 3 g verticales totales, 1 g horizontal y reparto 70/30; e=107,5 mm sin reducirla por conveniencia.
- Modelo nuevo del refuerzo apoyado por cinturón y arnés de hombro, con envolvente de momento excéntrico aplicado desde ambos extremos y fuerza horizontal. Esta condición requiere confirmación física.
- Flexibilidad buscada en alas del cinturón, textil y refuerzos separados. No se acredita confort ni vida de fatiga.
- Las dimensiones no medidas son decisiones provisionales de prediseño, reemplazables tras medición.

