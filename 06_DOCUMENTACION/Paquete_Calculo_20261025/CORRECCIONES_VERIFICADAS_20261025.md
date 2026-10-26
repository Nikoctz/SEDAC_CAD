# Corrección del paquete documental — 2026-10-25

## Alcance autorizado

**HECHO:** corrección documental y de unidades del paquete creado por OpenCode, recálculo con Mathcad y preparación de una entrega seleccionada para commits locales. El usuario autorizó después actualizar Notion. No se autoriza ni realiza push. No se modifica el CAD, los parámetros ni los generadores del prototipo.

**HECHO:** el paquete de trabajo original está en la carpeta hermana `SEDAC_Paquete_Calculo_20261025`. La copia seleccionada para Git se integra en `06_DOCUMENTACION/Paquete_Calculo_20261025/`. Se excluyen cachés, bloqueos y el ZIP anterior. El respaldo íntegro previo se conserva en `99_Sesion_Trabajo/Correccion_Verificada_20261025_204349/PAQUETE_ANTES.zip` del paquete externo.

## Cambios

- **HECHO / CÁLCULO:** corregida la descripción del modo gobernante del caso base. `Sy_al = 240 MPa` es menor que `sig_placa ≈ 477,699 MPa`; el empate entre `n_local` y `n_combinado ≈ 2,2471` procede del límite de fluencia en `min(Sy_al, sig_placa)`. No acredita pandeo local elástico gobernante ni dos comprobaciones físicas independientes.
- **HECHO / SUPUESTO:** conservados y explicados los diámetros efectivos del pasador 9,9/5,6 mm, heredados de `calcular_p2_05.py:63,71`. No son mediciones ni tolerancias aprobadas. No se sustituyeron por el taladro de 10,2 mm.
- **HECHO:** `mlat = Q_lado*L_luz/4` se presenta como momento en N·mm, sin cambiar la ecuación.
- **HECHO:** corregida la referencia a `01_CAD/Prototipo_P2/P2_04_20261016/BOM_Y_MASAS.csv`. La masa CAD es de modelo, no pesaje.
- **HECHO:** corregidos README, guion y generadores de los documentos; regenerados DOCX y fuente Mathcad, exportado el PDF desde Word y guardado el XMCD editable con Mathcad. Excel se modificó únicamente en la cita de `02_Variables!G26`.
- **HECHO:** el README distingue el caso base D=24 mm del estudio OPT1 y aclara que registrar símbolos al final de Mathcad no actualiza automáticamente entradas anteriores.

## Verificación ejecutada

- **HECHO:** apertura del DOCX corregido en Word: 1849 párrafos, 26 tablas; exportación PDF de 27 páginas y cotejo del número de objetos Page para ese PDF, no un parser universal.
- **HECHO:** apertura del XLSX de 12 hojas en Excel; comparación de entradas y fórmulas salvo la cita corregida. El control final relee el archivo guardado y compara también con el respaldo anterior.
- **CÁLCULO:** Mathcad recalculó y guardó el editable y la exportación HTML; 177 resultados cotejados, cero fuera de tolerancia y cero no numéricos en el conjunto controlado.
- **CÁLCULO:** reejecución de `comparar_control.py`: 11 magnitudes y 15 márgenes cotejados; peor error relativo 8,06·10⁻¹⁶. El registro JSON contiene los resultados reproducibles.
- **HECHO:** `99_Sesion_Trabajo/VERIFICACION_OFFICE.json` conserva el resultado de apertura nativa; `VERIFICACION_FINAL.json` conserva el cierre estructural, regresión numérica y comparación de entradas/fórmulas. Las 177 variables intermedias no son 177 ensayos físicos.

## Límites y pendientes

**HECHO:** P2.04 sigue vigente y P2.05 abierta. El control Python comparte expresiones con el generador Mathcad: comprueba implementación, no valida independientemente el modelo mecánico.

**PENDIENTE:** mediciones de bomba, centro de masa, arnés, apoyos y piezas; revisión del profesor, inventario instrumental, cotizaciones, criterios de ensayo y parada, fabricación y banco. El PDF de la hoja Mathcad como anexo permanece pendiente: el PDF del informe y el HTML de Mathcad no lo sustituyen.

**HECHO:** no hay datos de ensayo nuevos, validación física, liberación a fabricación ni autorización para probar con personas. Los cambios ajenos previos del repositorio se excluyen de los commits de este encargo.
