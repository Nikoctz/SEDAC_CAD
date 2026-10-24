# Tabla de masa — antes / después (masas nativas de Inventor)

**Antes:** `P2_04_20261016/BOM_Y_MASAS.csv` — masa CAD nativa de la entrega vigente.
**Después:** `Build/MASAS_CAD.json` — masa nativa medida en esta corrida.
**Materiales:** 6061-T6 (ρ = 2,7 g/cm³) en estructura, anclajes y uniones; HDPE 0,953 g/cm³ en la
espaldera; acero en fijaciones; textil 0,75 y espuma en las referencias visuales. El constructor crea un
material `SEDAC_<material>` con la densidad del JSON y **rechaza la pieza si la masa nativa no coincide**
con volumen × densidad, de modo que no se usó el material predeterminado de Inventor.

## 1. Masa rígida y protectores por grupo

| Grupo | Antes (kg) | Después (kg) | Δ (g) | n piezas |
|---|---:|---:|---:|---:|
| estructura | 0.568758 | 0.532935 | -35.82 | 2 |
| anclajes | 0.560488 | 0.585876 | +25.39 | 3 |
| fijaciones | 0.164802 | 0.164802 | +0.00 | 32 |
| protecciones | 0.080759 | 0.080759 | +0.00 | 1 |
| uniones | 0.067520 | 0.068406 | +0.89 | 16 |
| **Total rígida + protectores** | **1.442328** | **1.432778** | **-9.55** | 54 |

Referencias visuales (textiles, acolchados, herrajes textiles): 0.481154 → 0.482846 kg.
No se suman al presupuesto: ese papel lo cumple la reserva textil de 0,65 kg.

## 2. Presupuesto del sistema auxiliar (sin bomba ni agua)

| Concepto | Antes (kg) | Después (kg) | Δ (g) |
|---|---:|---:|---:|
| Rígida + protectores | 1.442328 | 1.432778 | -9.55 |
| Arnés / textiles (reserva) | 0.650000 | 0.650000 | 0,00 |
| Reserva adicional | 0.120000 | 0.120000 | 0,00 |
| **Total** | **2.212328** | **2.202778** | **-9.55** |

## 3. Piezas que cambian (el resto es idéntico)

| Pieza | n | Material | Antes (kg/u) | Después (kg/u) | Δ total (g) |
|---|---:|---|---:|---:|---:|
| Refuerzo_C_I | 1 | 6061 | 0.284379 | 0.266467 | -17.91 |
| Refuerzo_C_D | 1 | 6061 | 0.284379 | 0.266467 | -17.91 |
| Casquillo_I_35 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_D_35 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_D_390 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_D_450 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_I_95 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_D_95 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_I_390 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| Casquillo_I_450 | 1 | 6061 | 0.002879 | 0.002989 | +0.11 |
| REF_Funda_refuerzo_I | 1 | textil | 0.009669 | 0.010515 | +0.85 (visual) |
| REF_Funda_refuerzo_D | 1 | textil | 0.009669 | 0.010515 | +0.85 (visual) |
| Yugo_superior_D | 1 | 6061 | 0.124699 | 0.131045 | +6.35 |
| Yugo_superior_I | 1 | 6061 | 0.124699 | 0.131045 | +6.35 |
| Interfaz_lumbar_aligerada | 1 | 6061 | 0.311090 | 0.323786 | +12.70 |
| **Suma de los cambios rígidos** | | | | | **-9.55** |
| **Suma de las referencias visuales** | | | | | **+1.69** |
| Suma aritmética de ambas filas | | | | | -7.86 |

## 3 bis. Dos contabilidades que no se mezclan

La tabla anterior suma dos cosas distintas y por eso las cifras parecen no cuadrar:

| Contabilidad | Qué incluye | Δ | ¿Entra en el presupuesto? |
|---|---|---:|---|
| **Rígida + protectores** | 2 canales, 4 mejillas lumbar, 4 mejillas de yugo, 8 casquillos | **−9.55 g** | **Sí** |
| **Referencias visuales** | 2 fundas textiles de refuerzo (`REF_Funda_refuerzo_*`) | +1.69 g | **No** |
| Suma aritmética de las dos | — | −7.86 g | — |

Las referencias visuales **no se suman al presupuesto**: el arnés y los textiles ya están cubiertos por la
reserva de 0,65 kg, que no se toca. Sumarlas otra vez sería doble conteo y, además, restaría capacidad a
una partida que no se ha medido. Por eso:

- el ahorro que se declara es **−9,55 g (rígido)**;
- el presupuesto va de 2,212328 a 2,202778 kg con esos −9,55 g;
- los +1,69 g de fundas son una **consecuencia de forma** (la funda envuelve un canal 4 mm más profundo),
  registrada para que la tabla cuadre, no una partida que se descuente.

## 4. Lectura

- El canal aporta -35.82 g. El resto del conjunto aporta +26.27 g, casi todo en
  **anclajes (+25.39 g)**: las mejillas del lumbar y de los yugos derivan su altura de la
  profundidad del canal y crecen con él.
- Neto real del sistema: **-9.55 g** (-0.66 % de la masa rígida).
- El cálculo por sección predecía −42,8 g en los dos canales. La masa nativa del conjunto da un
  resultado **4,5 veces menor**: la métrica válida es la masa del ensamblaje, no la de la sección.
- Estos valores son masas de modelo, no pesajes físicos. No incluyen bomba ni agua.
