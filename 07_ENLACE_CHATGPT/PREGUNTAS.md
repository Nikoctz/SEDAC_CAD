# Preguntas para ChatGPT — SEDAC

Escribe aquí lo que quieras preguntar. Este archivo se pega tal cual dentro de
`PAQUETE_CHATGPT.md` (sección 6). Borra las preguntas ya resueltas para que el paquete no
crezca sin control.

Reglas rápidas:

- Una pregunta por bloque, numeradas.
- Si la respuesta debe ser un número o una decisión, dilo: «quiero un número y su fórmula»,
  «quiero dos alternativas y sus contras».
- No pidas datos de este PC; pide criterio de ingeniería.

---

## Preguntas pendientes

1. **Redondeo del lumbar (472 aristas).** El redondeo pedido de 0,5 mm falla si se aplica a
   las 472 aristas de golpe, pero funciona en cada mitad (236) por separado. ¿Cuál es el
   criterio de diseño correcto para decidir qué bordes de una pieza de aluminio que queda en
   contacto con cintas textiles deben romperse, y cuáles no? Quiero un criterio aplicable
   (no una lista de aristas).

2. **Bocetos de Inventor.** Cómo acreditar que un boceto queda totalmente restringido y qué
   evidencia dejar en el repositorio para que sirva en una auditoría.

3. **Margen 2,247 frente a umbral 2,20.** Qué sensibilidades conviene estudiar y en qué orden,
   sabiendo que el reparto de carga (70/30) y la excentricidad (107,5 mm) son hipótesis sin
   medir.

4. **Protocolo de validación con usuarios reales (plazo: diciembre 2026 – enero 2027).** El
   programa de financiamiento exige un piloto de validación con usuarios reales, y el proyecto
   **no está liberado a uso con personas** ni tiene la seguridad demostrada. Propón un protocolo
   de validación **por fases** (banco de pruebas → ensayo con carga inerte → y sólo después
   personas, si procede) que sea honesto y defendible: qué se mide en cada fase, con qué
   instrumento, qué criterio de parada, qué evidencia deja cada fase y qué NO se puede afirmar
   al terminar cada una.

---

*(plantilla: qué es `[hecho]` / `[calculo]` / `[supuesto]` / `[hipotesis]` se explica dentro
del propio paquete, en su sección 0.)*
