# Informe — ¿es evitable el crecimiento de las mejillas con la profundidad del canal?

Iteración: `Optimizacion_Mejillas_20261023_022810`. Inicio registrado 2026-10-23 02:20:10.
Alcance: análisis de prediseño; **no** cierra P2.05, **no** sustituye P2.04, **no** libera fabricación.

## 1. Lo que se investigó y por qué

En OPT1 el canal mejoró (−35,82 g) pero los anclajes crecieron (+25,39 g) y las uniones +0,89 g: neto −9,55 g.
La pregunta era si ese crecimiento es un requisito o un defecto de forma.

**Regla geométrica encontrada en el generador** (`generar_p2_05.py`):

- lumbar: `rect(18, Z_CAPA, 100, D-Z_CAPA)` → altura de mejilla = `D − Z_CAPA`;
- yugo: `rect(376, −2, 98, D+2)` → altura = `D + 2`;
- casquillo: longitud `B − 2t`.

Con `Z_CAPA = −3,7 mm`: la mejilla lumbar pasa de **27,7** a **31,7 mm** al ir de D=24 a D=28.

## 2. Cuánto de ese crecimiento es necesario

| Concepto | Valor | Etiqueta |
|---|---:|---|
| Altura necesaria para alojar el pasador y su arandela (`Z_PIN + r + 2,5`) | ≈ 20,2 mm | cálculo |
| Altura que implementa P2.04 (`D − Z_CAPA`) | 27,7 mm | hecho |
| Altura que implementa OPT1 | 31,7 mm | hecho |
| Δ de masa de mejillas predicho por geometría | **25,66 g** | cálculo |
| Δ de masa de mejillas medido en Inventor | **25,39 g** | hecho |
| Desviación | 0,27 g (1,1 %) | cálculo |

El crecimiento es **íntegramente área de mejilla**; no hay otra causa. La geometría lo explica.

**Necesario por transmisión de cargas:** no. La resistencia de la mejilla a flexión fuera de plano depende
de `Z = L·EM²/6` — **no de la altura**. La altura solo aporta: (a) alojamiento del pasador y la arandela,
(b) cobertura del flanco del canal hasta la boca, (c) protección de la arista del canal frente al textil.
Los 4 mm añadidos no aumentan ningún margen resistente.

**Necesario por función:** sí, mientras se mantenga la regla actual de "mejilla hasta la boca del canal".
Congelar la mejilla en 24 mm dejaría 4 mm de flanco del canal fuera de la mordaza: apoyo y protección
parciales, que es justo lo que no se debe hacer sin medir.

## 3. Las dos alternativas, y por qué ninguna supera los −9,55 g con respaldo

### Alternativa 1 — mejilla escalonada (descartada)

Altura completa solo alrededor de los pasadores (2 × 24 mm) + labio de 8 mm en la boca.

| | Valor |
|---|---:|
| Ahorro de masa (analítico) | 75,57 g |
| Z en el borde del escalón | 36 mm³ (antes 150) |
| Margen con K = 1,5 | **0,35** → no cumple |
| Ancho necesario para n = 1 | 68,5 mm |
| Ancho necesario para n = 2,2 | 150,7 mm (mejilla de 100 mm) |

Falla por su propia comprobación. El material de la mejilla trabaja a flexión fuera de plano; estrecharla
la mata. **No se generó CAD:** sería entregar una pieza que no cumple.

### Alternativa 2 — conservar el canal de P2.04 y aligerar solo anclajes

Misma geometría escalonada aplicada con D=24: ahorro 62,35 g, con el **mismo fallo** de margen (0,35), porque
la comprobación depende de `L`, no de `D`. Tampoco procede.

### Dónde está el premio de verdad (no es ahorro todavía)

Masa de mejilla por encima del requisito del pasador y su arandela (hasta 22,2 mm desde la raíz en el
lumbar y 21,5 mm en el yugo). No aporta a `Z` ni al aplastamiento: sostiene la mordaza y protege la arista.

| | Lumbar | Yugos | Total |
|---|---:|---:|---:|
| P2.04 | 14,6 g | 14,3 g | **28,9 g** |
| OPT1 | 27,5 g | 27,0 g | **54,5 g** |

**No se descuenta del presupuesto.** Es la magnitud del premio si la mordaza se sustituye por un concepto
que no dependa de `D`; hoy esa función está cumplida por esa masa y quitarla sin sustituto deja el flanco
sin apoyo.

## 4. Hallazgo que sí cambia el estado del proyecto

La mejilla lumbar, con un modelo de placa empotrada, está en **n = 2,19** — por debajo del umbral 2,2 y
prácticamente igual que el canal (2,247). El cribado histórico **no incluía este modo** (H12: contornos
locales sin comprobación individual; H05: la mejilla se calculaba solo a aplastamiento con `pared_minima`).

Consecuencia práctica: **no hay margen para aligerar las mejillas** y cualquier reducción de `EM` empeora
linealmente al cuadrado. El modo entra en la lista de comprobaciones que faltan, no como validación.

## 5. Correcciones documentales de la iteración anterior

1. `LEEME_OPT.md` decía "nada más cambia" mientras la tabla mostraba 16 piezas distintas. Corregido:
   se distingue **una entrada editada** (`D`, `t`, `pared_minima`) de **dependencias propagadas**
   (mejillas de lumbar y yugos, casquillos, fundas).
2. `TABLA_MASAS.md` sumaba −7,86 g mezclando rígido con referencias visuales textiles. Corregido: −9,55 g
   es rígido (entra en presupuesto); +1,69 g son fundas de referencia (no entran, ya cubiertas por la
   reserva de 0,65 kg). Se explica por qué sumarlas sería doble conteo.

## 6. Recomendación

**No adoptar** OPT1 ni la propuesta A. Mantener **P2.04** como entrega vigente.

Si se quiere seguir por esta vía, el paso con recorrido real no es tallar la mejilla sino **cambiar su
concepto**: sustituir la mordaza continua por dos orejetas mecanizadas con un casquillo que transmita el
momento por apoyo directo en la placa, de modo que la altura deje de depender de `D`. Eso exige definir el
contacto (A/B/C, D-12) y una comprobación de la unión que hoy no existe.

## 7. Qué quedó comprobado y qué no

**Comprobado (cálculo reproducible + masas nativas previas):** la regla geométrica, el Δ de masa con 1,1 %
de desviación, que `Z` no depende de la altura, y que la variante escalonada no cumple.

**Oportunidad cuantificada, no ahorro:** 54,5 g de mejilla en OPT1 (28,9 g en P2.04) están por encima del
requisito del pasador; su función es la mordaza y la protección de arista.

**No comprobado:** contacto real mejilla-canal, aplastamiento del textil, fatiga, dinámica, desgaste,
liberación con guantes, tolerancias de pasador, FEA local. Nada de esto es validación del producto.
