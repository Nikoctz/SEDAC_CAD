# SEDAC P2.05 — iteración de trabajo (coherencia CAD ↔ parámetros ↔ cálculo)

**Estado:** dos construcciones completas hechas en Inventor 2027.1. La segunda se detiene **a propósito** en el
seguro de coherencia, porque el redondeo del lumbar queda declarado como *parcial*.
La entrega vigente sigue siendo **P2.04** (`../P2_04_20261016/`), **intacta**.

Fecha: 2026-10-19 · Base: P2.04 (16/10/2026)

---

## 1. Qué se ha conseguido (todo verificable)

| Arreglo | Verificación |
|---|---|
| **Redondeo robusto.** El sondeo de aristas *siempre deshace* (`Abort`), y la aplicación real del redondeo es **una sola llamada final** con el conjunto elegido. | 4 experimentos aislados sobre el lumbar, midiendo masa CAG (ver §3) |
| **Registro con diagnóstico.** Cada pieza registra `estado` (`total`/`parcial`/`no_aplicado`), `criterio`, aristas totales/redondeadas, nº de pruebas de sondeo y la lista de aristas no admitidas. | Corrida real: 5 registros, coherentes con la masa medida |
| **Seguro de coherencia.** Si un redondeo pedido queda `aplicado ≠ true`, el constructor **se detiene** y no escribe `ESTADO_OK.txt`. Interruptor `-AceptarPendientes` para forzar la decisión a mano (deja `AVISO_REDONDEOS.txt`). | La corrida 2 se detuvo y **no** escribió `ESTADO_OK.txt` |
| **Parámetros que gobiernan de verdad.** 10 campos que no leía ningún script ahora mandan sobre la geometría, + 4 nuevos (3 radios, diámetro interior del pasador). Reservas de masa separadas de la geometría. | Modelo generado **idéntico** a P2.04 (0 diferencias fuera de `version`/`parameters`); 10 valores cambiados en copia de prueba movieron la geometría esperada |
| **`RESUMEN_ENTREGA.json` generado** (antes no lo escribía ningún script) | Escrito por el constructor desde `MASAS_CAD.json` + parámetros |
| **El constructor ejecuta también el cálculo** (antes solo generaba geometría) | `Calculos/RESULTADOS_PREDISENO.json` regenerado en cada corrida |

## 2. Resultado de la corrida definitiva (`Soporte/Iteraciones/Nueva_20261019_060807`)

```
Redondeo Refuerzo_C_I              : total    46/46   [todas],                 1 prueba
Redondeo Refuerzo_C_D              : total    46/46   [todas],                 1 prueba
Redondeo Interfaz_lumbar_aligerada : parcial 236/472  [grupo_mayor],          14 pruebas
Redondeo Yugo_superior_I           : total   248/248  [todas],                 1 prueba
Redondeo Yugo_superior_D           : total   248/248  [todas],                 1 prueba
```

- 54 piezas construidas, las 54 con masa nativa coincidente con la calculada.
- **Interferencias: 0** (umbral del verificador: 0,001 mm³).
- Masas: rígida **1,4420687346427812 kg** · presupuesto **2,2120687346427812 kg**
  (P2.04: 1,4423278471806384 / 2,2123278471806387 → **−0,2591 g**, ver §4).
- Ensamblaje: 83 ocurrencias, `RESTRICCIONES.json` idéntico en tamaño al de P2.04.
- No hay `ESTADO_OK.txt` ni `.step` ni vistas: el proceso se detuvo en el seguro, como debe.

## 3. El fallo del lumbar NO es una arista concreta (hecho, medido)

El experimento se hizo construyendo **solo esa pieza** en una copia de pruebas fuera del proyecto,
comparando volúmenes y masas en Inventor:

| Variante | Qué hace | Volumen del lumbar | Masa |
|---|---|---|---|
| A | Geometría limpia, **sin pedir redondeo** | 115 218,455919904 mm³ | 0,31108983098374 kg |
| C | Redondeo **original** de la entrega: una llamada con las 472 aristas → falla | 115 218,455919904 mm³ | 0,31108983098374 kg |
| F | Sondeo + búsqueda, **sin aplicar nada** | 115 218,455919904 mm³ | 0,31108983098374 kg |
| D | Código arreglado, aplicando el mayor subconjunto viable | 115 122,48831329 mm³ | 0,310830718445883 kg |

Conclusiones (hecho):
1. **`Abort()` deshace el redondeo perfectamente**, incluso cuando llegó a aplicarse (F = A exactamente).
   El sondeo no deja rastro. La aplicación real es la única que toca la geometría.
2. **La pieza de la entrega P2.04 estaba correcta**: su masa coincide exactamente con la geometría limpia,
   y su propio `REDONDEOS.json` declaró `aplicado: false` con el error COM. La entrega P2.04 **no tiene** el
   redondeo del lumbar, pero **lo dijo**.
3. El redondeo de las **472 aristas de una sola vez falla, pero cada mitad (236) por separado funciona**.
   No se identificó ninguna arista individualmente culpable (`aristas_omitidas: 0`).
   **Hipótesis (no comprobada):** es un límite de la herramienta al procesar 472 aristas en una sola
   operación, no una imposibilidad geométrica.
4. Lo que sí se redondeó (236 de 472) es **un subconjunto arbitrario por orden de enumeración**, no una
   decisión de diseño: coherente y declarado, pero **no es el criterio correcto**. Pendiente de decidir (§7).

## 4. Correcciones a lo que se dijo durante el trabajo

- Los **«73 aristas problemáticas»** de la primera corrida (`Nueva_20261019_055214`) **no son fiables**:
  ese sondeo confirmaba el redondeo cuando salía bien, así que modificaba el modelo mientras buscaba.
  Ese defecto **ya está corregido** y la lista fiable es la de la corrida 2 (`aristas_omitidas: 0`).
  La carpeta de la primera corrida **se conserva solo como evidencia** del fallo encontrado y corregido.
- La masa del lumbar de P2.04 **no era un defecto**: coincidía con la geometría limpia. El desvío de
  0,26 g era **mío**, y se detectó precisamente comparando la masa medida contra el BOM.

## 5. La diferencia de masa de −0,2591 g, explicada

Es **efecto del redondeo parcial declarado** en esa pieza (236 aristas de 472 con radio 0,5 mm):
el grupo `anclajes` baja 0,2591 g y las otras 53 piezas no cambian ni un microgramo.
Ahora el número que sale en `RESUMEN_ENTREGA.json` y lo que dice `REDONDEOS.json` **cuentan lo mismo**:
ese era el objetivo del frente de trabajo.

## 6. Cómo se ejecuta y qué hay que comprobar

```powershell
# intérprete por defecto: el de Codex, que es el único con numpy
powershell -ExecutionPolicy Bypass -File .\01_CAD\Prototipo_P2\P2_05_20261019\Soporte\CONSTRUIR_P2_05.ps1
```
Sin `-Salida`, cada corrida escribe en `Soporte\Iteraciones\Nueva_<fecha>`. El cálculo va a `Calculos\`.
Al terminar, comprobar en la carpeta de salida: `REDONDEOS.json`, `INTERFERENCIAS.json`,
`RESUMEN_ENTREGA.json` y que **no** exista `ERROR.txt`.

## 7. Decisión pendiente del responsable (no la puede tomar el código)

**Qué bordes del lumbar deben redondearse.** Opciones sobre la mesa:

1. **Solo el contorno exterior** (bordes que tocan las cintas, que es lo que dice el comentario original
   del generador): excluir los bordes de ventanas y recortes pequeños. Requiere definir el criterio.
2. **Investigar el límite de la herramienta**: probar si se pueden redondear las 472 en varias tandas o
   con otro radio (0,3 / 0,35). Son experimentos de ~2 min cada uno.
3. **Aceptar el parcial 236/472** documentándolo como decisión de fabricación.
4. **Dejar el lumbar sin redondeo declarado** hasta decidir, para que la corrida cierre sin avisos.

## 8. Pendiente y límites (lo que NO está resuelto)

- **Contornos de textiles, radios de esquina no listados y elementos normalizados M5** siguen definidos en
  el generador: solo gobiernan por JSON los campos listados en `geometria`.
- **`profundidad_cuna` (130 mm) queda explícitamente NO conectado** (ver `parametrizacion.pendiente`).
- **`HUELLAS_ENTREGA.json` y `ESTADO_ENTREGA.md` no los genera ningún script**: la trazabilidad de la
  entrega todavía no es reproducible de extremo a extremo.
- **Umbral de interferencias (0,001 mm³) sin tocar.** Los 8 solapes de 0,4634 mm³ del borrador CAD01
  siguen **sin investigar** (esta corrida da 0 interferencias).
- **Hipótesis de carga sin validar**: margen 2,2; reparto 70/30; 3 g / 1 g; excentricidad 107,5 mm;
  precarga 2000 N. Son prediseño (AGENTS.md §5).
- **El `.ps1` depende del python del runtime de Codex** (único con numpy instalado).
- **`grupos` y el ahorro vs P2.03** se generan, pero el dato de P2.03 es heredado, no recalculado.

## 9. Evidencia comparada P2.04 ↔ P2.05 (2026-10-19)

**La geometría es la misma (hecho).** Comparando `MODELO_API.json` de la entrega P2.04 con el de esta
corrida, normalizando números (`480` y `480.0` son el mismo valor):

- `parts` (la descripción de las 54 piezas y sus operaciones): **0 diferencias**.
- `parameters`: 12 diferencias, todas de cabecera: 4 campos nuevos (`radio_redondeo_lumbar`,
  `radio_redondeo_yugo`, `radio_redondeo_refuerzo`, `pasador_id`), 4 reorganizados (`profundidad_cuna`,
  `masa_presupuesto_textil_kg`, `masa_reserva_kg` salen de `geometria`) y 4 secciones nuevas
  (`origen`, `reservas_masa`, `referencias_historicas`, `parametrizacion`).
- Los ficheros `.ipt` son binarios: **los 54 difieren byte a byte** aunque la geometría sea la misma.
  Es lo normal (cada guardado graba estado interno) y **no es prueba de cambio**.

**El registro de la entrega P2.04 era honesto (hecho).** Su `REDONDEOS.json` dice
`Interfaz_lumbar_aligerada, radio 0.5, aplicado: false, error: "Devuelto error HRESULT E_FAIL de una
llamada a un componente COM."`, y su masa (0,31108983098374 kg) coincide con la geometría limpia.
Las dos cosas concuerdan.

**Dónde estaba la incoherencia de P2.04 (hecho).** En la misma carpeta de entrega conviven:

- `ESTADO_OK.txt`: «Actualizacion correcta de 54 piezas solidas y 83 ocurrencias…»
- `REDONDEOS.json`: un redondeo pedido que **no se aplicó**.

Es decir: sello de «correcto» junto a un pendiente declarado. El seguro de P2.05 existe precisamente para
que eso no pueda repetirse: si queda un pendiente, **no hay sello**.

**Las corridas de borrador no eran reproducibles (hecho; causa pendiente).** Declararon `aplicado: true`
para el lumbar y dieron una masa distinta en cada corrida:

| corrida | masa del lumbar (kg) | declarado |
|---|---|---|
| CAD01 | 0,390031968511812 | aplicado: true |
| CAD02 | 0,271289492582047 | aplicado: true |
| CAD05 | 0,267499817043885 | aplicado: true |
| CAD06 | 0,287976619150462 | aplicado: true |
| entrega P2.04 (sin redondeo) | 0,31108983098374 | aplicado: false |

Cuatro resultados distintos con la misma declaración no son «aplicado». **Nota:** CAD01 sale *más pesado*
que la geometría limpia, y un redondeo solo puede quitar material; por tanto aquellas corridas no diferían
solo en el redondeo. Causa **pendiente** ( probablemente la parametrización cambió entre corridas).

**Consecuencia física abierta (hecho, importante).** En la **entrega vigente (P2.04)** la pieza que toca las
cintas —el lumbar— tiene sus 472 aristas vivas: nunca se le aplicó redondeo. En la corrida de esta copia
(P2.05) sí se aplicó un **subconjunto de 236** con el criterio «grupo mayor», pero es arbitrario por orden
de enumeración (§3, punto 4), no una decisión de diseño. La decisión de qué bordes redondear sigue pendiente (§7).

---

Trazabilidad según AGENTS.md §4: cada afirmación está marcada como hecho, cálculo, supuesto o hipótesis.
Los valores «hecho» salen de archivos de este repositorio y son reproducibles con este constructor.
