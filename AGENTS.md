# AGENTS.md — Instrucciones para agentes AI en SEDAC_CAD

Ámbito: todo el repositorio. Aplica a cualquier agente (Codex, OpenCode u otro) que abra esta carpeta.

## 1. Lectura obligatoria antes de trabajar

Leer en este orden:

1. `CONTEXTO_SEDAC.md` — contexto heredado del proyecto (describe P0).
2. `ESTADO_ACTUAL.md` — versión vigente, estado de Git, pendientes.
3. `DECISIONES.md` — decisiones técnicas ya adoptadas.
4. `CHANGELOG_SEDAC.md` — cambios reales registrados.

`CONTEXTO_SEDAC.md` está desactualizado respecto a P2.04. **En caso de conflicto, manda `ESTADO_ACTUAL.md`.**

## 2. Regla de un solo escritor

- Solo **un** agente puede escribir o modificar el proyecto a la vez.
- Antes de modificar cualquier cosa, ejecutar `git status`.
- Si hay **cambios sin commit que el agente actual no hizo**, detenerse y avisar al responsable. No descartar, no sobrescribir, no "corregir" el trabajo ajeno.
- No ejecutar `git commit`, `git push`, `git reset`, `git checkout --`, `git clean` ni borrados sin autorización explícita.

## 3. Prohibiciones

- No modificar CAD importante (`.ipt`, `.iam`, `.step`, `.stl`, `.3mf`), parámetros ni generadores sin autorización explícita.
- No borrar archivos existentes.
- **No inventar** resultados de ensayos, FEA, propiedades de materiales, normas ni mediciones. Si falta un dato, escribir `pendiente`, no un valor plausible.
- No presentar un cálculo analítico de prediseño como validación del producto.
- No declarar seguridad, comodidad, resistencia o cumplimiento normativo que no estén demostrados.

## 4. Trazabilidad obligatoria

Marcar cada afirmación como una de estas categorías:

- **hecho** — verificable con un archivo o comando.
- **cálculo** — reproducible con un script o fórmula identificada.
- **supuesto** — valor adoptado sin medir.
- **hipótesis** — condición aún no comprobada.

Separar siempre "lo que está comprobado" de "lo que falta comprobar".

## 5. Estado del diseño

- **P2.04 es la base actual**: `01_CAD/Prototipo_P2/P2_04_20261016/`.
- **P2.05 todavía no está cerrado.**
- **NO son datos validados:** margen n = 2,2; reparto 70/30; 3 g vertical / 1 g horizontal; excentricidad e = 107,5 mm; precarga de 2000 N. Son hipótesis de prediseño.

## 6. Inventor y MCP

- El MCP `inventor` puede usarse, pero por defecto en **modo lectura**. La lectura está verificada desde Codex con Inventor 2027.1; la **escritura CAD mediante MCP no está validada**.
- Operaciones delicadas (crear, modificar o borrar operaciones; regenerar; guardar; exportar; interferencias) requieren **confirmación explícita del responsable** antes de ejecutarse.
- No sobrescribir los `.ipt`/`.iam` de la entrega. Trabajar sobre copias en carpetas nuevas por versión/fecha.

## 7. Convenciones del proyecto

- Unidades: **milímetros**. Escala maestra **1:1**.
- Nuevas iteraciones en carpetas nuevas por versión y fecha; no sobrescribir entregas.
- Generar primero borradores en `Soporte/Iteraciones/`, no en `Entrega/`.
- La memoria Mathcad/PDF se pospone hasta acordar la geometría.

## 8. Al terminar

Indicar: qué se leyó, qué se cambió (con rutas), qué se verificó y cómo, qué quedó pendiente. No hacer commit salvo autorización.
