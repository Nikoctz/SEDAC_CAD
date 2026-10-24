# Comparación — P2.04 / iteración anterior (OPT1) / propuesta nueva

Escala 1:1, milímetros. Masas de modelo, no pesajes. Sin bomba ni agua.

## 1. Parámetros que gobiernan

| Parámetro | P2.04 (vigente) | OPT1 (anterior) | Propuesta nueva (A) |
|---|---:|---:|---:|
| `ancho_refuerzo` B (mm) | 32 | 32 | 32 |
| `profundidad_refuerzo` D (mm) | 24 | 28 | 28 |
| `pared_refuerzo` t (mm) | 3 | 2,5 | 2,5 |
| `pared_minima` (mm) | 2,8 | 2,3 | 2,3 |
| `espesor_mejilla` EM (mm) | 3 | 3 | 3 |
| Altura de mejilla lumbar (mm) | 27,7 | 31,7 | 31,7 en 2 zonas de 24 mm; 8 en el resto |
| Altura de mejilla de yugo (mm) | 26 | 30 | 30 en 2 zonas de 24 mm; 8 en el resto |
| Material | 6061-T6 | 6061-T6 | 6061-T6 |
| Cargas, reparto, precarga | sin cambios | sin cambios | sin cambios |

## 2. Masa

| Concepto | P2.04 | OPT1 | Propuesta A (analítica, sin CAD) |
|---|---:|---:|---:|
| Canales (2) | 0,568758 | 0,532935 | 0,532935 |
| Lumbar | 0,311090 | 0,323786 | 0,323786 − aligeramiento |
| Yugos (2) | 0,249398 | 0,262090 | 0,262090 − aligeramiento |
| Casquillos (8) | 0,023029 | 0,023912 | 0,023912 |
| **Rígida + protectores** | **1,442328** | **1,432778** | **1,357208** |
| Arnés/textiles (reserva, no se toca) | 0,650000 | 0,650000 | 0,650000 |
| Reserva adicional | 0,120000 | 0,120000 | 0,120000 |
| **Presupuesto** | **2,212328** | **2,202778** | **2,127208** |
| Δ vs P2.04 | — | **−9,55 g** | −85,12 g (no admisible, ver §4) |

## 3. Márgenes y modo gobernante

| Comprobación | P2.04 | OPT1 | Umbral |
|---|---:|---:|---:|
| Refuerzo combinado, pared mínima | **2,247** | 2,321 | 2,2 |
| Pandeo local de alas | **2,247** | **2,227** | 2,2 |
| Pandeo lateral torsional ideal | 2,393 | 2,392 | 2,2 |
| Arandela presión bajo tuerca | 2,258 | 2,258 | 2,2 |
| **Mínimo del cribado** | **2,247** | **2,227** | 2,2 |
| **Modo gobernante** | tensión combinada / pandeo local (empate) | **pandeo local de alas** | — |
| Mejilla en flexión fuera de plano (comprobación **nueva**, no del cribado) | **2,19** | **2,19** | 2,2 |

La comprobación nueva de mejilla es un cribado de placa empotrada, no FEA: `Z = L·EM²/6 = 150 mm³`,
brazo 14,7 mm, V = 1118 N del propio cribado. Su resultado es **idéntico en P2.04 y OPT1**, porque Z no
depende de la altura en z y el brazo tampoco cambia. Se declara aparte: no forma parte del cierre R3.

## 3 bis. Masa de mejilla no gobernada por carga

| Mejilla por encima del alojamiento del pasador | P2.04 | OPT1 |
|---|---:|---:|
| Lumbar (4 mejillas) | 14,6 g | 27,5 g |
| Yugos (4 mejillas) | 14,3 g | 27,0 g |
| **Total** | **28,9 g** | **54,5 g** |

No entra en el presupuesto como ahorro: cumple la función de mordaza y protección de arista.

## 4. Propuesta A: por qué se descarta

Mejilla escalonada (altura completa solo en 2 zonas de 24 mm por pasador + labio de 8 mm en la boca):
ahorraría **75,57 g** sobre OPT1, pero al reducir el ancho resistente a 24 mm en el borde del escalón:

- `Z` cae de 150 a 36 mm³;
- con K = 1,5 por el escalón, el margen baja a **0,35** (falla);
- para n = 1 harían falta 68,5 mm de ancho; para n = 2,2, **150,7 mm** — más que la longitud total de la mejilla (100 mm).

**Conclusión:** el material de la mejilla está gobernado por flexión fuera de plano, no por aplastamiento.
No se puede aligerar estrechando su longitud. Se descarta y no se genera CAD de ella.
