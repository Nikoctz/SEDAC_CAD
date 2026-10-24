# LEEME — Iteración mejillas 2026-10-23

## Qué es

Estudio dirigido sobre **una sola pregunta**: si el crecimiento de mejillas al profundizar el canal
(OPT1, 2026-10-23) es requisito mecánico o material evitable. **No hay CAD nuevo**: la única variante que
producía ahorro (mejilla escalonada) falla su propia comprobación de flexión (n = 0,35) y se descarta antes
de generar geometría.

**Estado:** análisis de prediseño. No cierra P2.05, no sustituye P2.04, no libera fabricación ni uso.

## Contenido

| Archivo | Para qué |
|---|---|
| `INFORME.md` | hallazgo, alternativas descartadas, correcciones documentales y recomendación |
| `COMPARACION.md` | P2.04 / OPT1 / propuesta A: parámetros, masa, márgenes y modo gobernante |
| `Analisis/ANALISIS_MEJILLAS.json` | resultados numéricos reproducibles |
| `Analisis/RESULTADOS_OPT1.json` | cribado de OPT1 reutilizado (mismas cargas, sin recalcular hipótesis) |
| `PARAMETROS_P2_04.json` / `PARAMETROS_OPT1.json` | parámetros comparados, copiados de la iteración anterior |
| `Soporte/calcular_p2_05.py` | cálculo heredado, copia sin modificar |
| `Soporte/analisis_mejillas.py` | análisis de esta iteración: geometría de mejillas, Z, escalonado |

## Reproducir

```
cd .../Optimizacion_Mejillas_20261023_022810
python Soporte/analisis_mejillas.py
```

Reescribe `Analisis/ANALISIS_MEJILLAS.json`. No toca ninguna carpeta histórica.

## Cómo leer el resultado

- **−9,55 g** sigue siendo el único ahorro respaldado por geometría nativa (OPT1).
- El +25,39 g de anclajes **no es material prescindible**: es el área de mejilla que acompaña a la
  boca del canal. Quitarla sin rediseñar la mordaza deja el flanco sin apoyo.
- La mejilla está a **n = 2,19** en flexión fuera de plano con un cribado de placa empotrada: no hay
  holgura para aligerarla, y ese modo no estaba en el cribado histórico (H05/H12).

## Lo que falta

Contacto y clasificación A/B/C (D-12) · FEA local de mejilla y de la unión · tolerancias de pasador ·
textil, fatiga, dinámica, desgaste, liberación con guantes · mediciones de bomba y CdG.
