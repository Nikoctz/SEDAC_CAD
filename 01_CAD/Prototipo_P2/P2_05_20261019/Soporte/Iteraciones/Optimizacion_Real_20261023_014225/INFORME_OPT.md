# Optimización real SEDAC — iteración 2026-10-23

**Carpeta:** `.../P2_05_20261019/Soporte/Iteraciones/Optimizacion_Real_20261023_014225/`
**Inicio registrado:** 2026-10-23 01:40:55 (reloj del equipo). **Presupuesto:** 50 min.
**Base:** P2.04 (entrega vigente) + soporte P2.05 (abierta).
**Estado:** **prediseño condicionado**. No se declara seguridad, comodidad, resistencia, flexibilidad ni
fabricación validada.

> Nota de tiempo: el reloj del entorno se reajustó durante la sesión. Por eso el trabajo se ordena por
> fases verificables (con su evidencia) y no por hora de pared. La fase de CAD consumió más de lo previsto
> porque el ensamblaje impone 3 restricciones y comprueba grados de libertad en 82 ocurrencias.

---

## 0. Respuesta en cuatro líneas

1. **Creado:** un IAM nativo editable con 54 IPT, STEP, 5 vistas y verificación nativa.
2. **Comprobado:** 83 ocurrencias, 54 referencias sin ausencias, actualización correcta, masas nativas
   coincidentes, **0 interferencias** nominales, R1 y R3 del cierre en verde.
3. **Ahorro respaldado por geometría nativa: −9,55 g** (1,442328 → 1,432778 kg), **0,66 %**. No los
   −42,8 g que sugiere la sección.
4. **Pendiente:** todo lo físico (D-12, textiles, fatiga, ergonomía, liberación) y la simplificación de
   piezas/uniones, que esta iteración **no** logró.

---

## 1. Fuentes y reconciliación (fase 0–8 min)

Leído en el orden de `AGENTS.md`: `CONTEXTO_SEDAC.md`, `ESTADO_ACTUAL.md`, `DECISIONES.md`,
`CHANGELOG_SEDAC.md`; después `LEEME_P2_05.md` (§1–§12), `AUDITORIA.md`, `Correccion_Dependencias_20261022_192327/INFORME.md`,
`P2_04_20261016/BOM_Y_MASAS.csv`, `RESUMEN_ENTREGA.json` y el `MODELO_API.json` de la entrega.
`git status` ejecutado antes de escribir: los cambios sin commit de Codex/OpenCode quedaron **intactos**.

**Masas verificadas (hecho):** suma del BOM = estructura 0,568758 · anclajes 0,560488 · fijaciones 0,164802 ·
protecciones 0,080759 · uniones 0,067520 kg → **rígida 1,442328 kg**, idéntica al `RESUMEN_ENTREGA.json`.
Presupuesto 1,442328 + 0,65 + 0,12 = **2,212328 kg**. Coincide con lo declarado en el encargo.
Textiles, acolchados y herrajes textiles (0,481 kg) son **referencias visuales**: no se suman.

**Caso gobernante (hecho):** `Refuerzo combinado, pared mínima` con **2,247** frente al umbral elegido 2,2
(reserva 2,14 %). Es el que decide si un aligeramiento del canal es admisible.

**Avances de P2.05 que se incorporan:** el generador con H03 y parte de H13 (nunca ejecutado hasta hoy),
la separación generación/coherencia/cribado (D-16) y el control de cierre. **No** se incorpora la maqueta
PLA R1–R4 (escala de presentación) ni se usa su −35,2 %.

## 2. Dependencias antes de variar parámetros (fase 8–18 min)

Antes de tocar nada se comprobó **qué controla cada campo**:

| Campo | Controla en CAD | Controla en cálculo | Decisión |
|---|---|---|---|
| `profundidad_refuerzo` (D) | sección del canal **y altura de mejillas** de lumbar y yugos | `section()` usa D vía `pared_minima` | se varía, con la propagación medida |
| `pared_refuerzo` (t) | pared del canal y longitud del casquillo (B−2t) | **no** se usa: el cálculo emplea `pared_minima` | se varía junto con el mínimo |
| `pared_minima` | nada | toda la resistencia del canal | **supuesto**: t_nominal − 0,2 mm (mismo criterio que 3 → 2,8) |
| `ancho_refuerzo` (B) | canal y **GRIP = B + 2·EM** (tornillos, pasadores) | sección | **no** se varía: mueve tornillos y pasadores |

**H03/H13, primera ejecución real (hecho):** la corrección del 22/10 se ejecutó por primera vez. Propagó
como estaba previsto: mejillas crecen con D, casquillos se acortan con t, y **pasadores y tornillos no
cambian** porque GRIP = 32 + 2·3 = 38 mm se mantiene. Eso convierte «implementado sin verificar» en
comportamiento observado.

**H02/H04/H05 siguen abiertas** y **afectan a esta variante**: el mínimo propio de mejilla (H05) y las
tolerancias de pasador (H04) no están resueltos; el cribado usa `pared_minima` también para la mejilla.
Por eso la alternativa se entrega como **condicionada**, no como cerrada.

## 3. Trade study (cálculo, reproducible)

Se ejecutó **la copia del cálculo real** con un JSON por alternativa (`Soporte/alternativas.py`). No se
reimplementan ecuaciones y **V0 reproduce 2,247**, lo que valida la comparación.

| Variante | B×D×t | A (mm²) | Z (mm³) | Margen mín. | ¿Cumple 2,2? | Modo que falla |
|---|---|---:|---:|---:|---|---|
| V0 base | 32×24×3 | 208,3 | 752,4 | **2,247** | sí | — |
| **A** | 30×26×2,5 | 178,0 | 726,8 | 2,107 | **no** | combinado + pandeo local |
| **B** | 32×26×2,5 | 182,6 | 735,0 | 2,149 | **no** | combinado + pandeo local |
| Sens. | 32×24×2,5 | 173,4 | 630,4 | 1,872 | **no** | combinado + pandeo local |
| **C** | 32×28×2,5 | 191,8 | 846,8 | **2,227** | sí | pandeo local de alas (gobierna) |

**Resultado 1:** adelgazar **sin profundizar** no cumple. El canal 32×24×3 no tiene grasa uniforme.
**Resultado 2:** la única viable (C) **baja** el margen (2,247 → 2,227) y **cambia el modo gobernante** a
pandeo local de alas, que depende de t² — más sensible a la tolerancia de pared que la tensión combinada.

## 4. Alternativa construida y decisión

Se construyó la **Alternativa C**: `profundidad_refuerzo` 28, `pared_refuerzo` 2,5, `pared_minima` 2,3.
Todo lo demás —cargas, materiales, reservas, textiles, número de piezas y de uniones— **sin cambios**.
No se rigidiza nada: espaldera, cunas, cintas y acolchados quedan igual; los 8 pasadores siguen siendo los
mismos; el camino de carga bomba/cuna → lumbar → hombros/cinturón no se altera.

**Decisión: no adoptar todavía.** El balance medido (ver §5) es −9,55 g a cambio de menos reserva y de un
modo de falla más sensible. Adoptarla exige FEA local de pandeo de ala y mediciones reales; sin eso sería
cambiar margen por masa, que es lo que prohíben D-02 y D-06.

**Lo que esta iteración NO logró:** simplificar piezas o uniones. Se estudiaron y **se descartaron** por
falta de respaldo: reducir de 8 a 6 pasadores duplica la reacción por pareja (el cálculo usa `sep = 60 mm`);
las ventanas de aligeramiento en el alma fallan el cribado existente (K_ventana = 3, margen ≈ 1,3) y bajar
K sin justificación sería maquillar el resultado.

## 5. Masa antes/después (masas nativas, no cálculos de sección)

Detalle completo en [TABLA_MASAS.md](TABLA_MASAS.md).

| Concepto | Antes | Después | Δ |
|---|---:|---:|---:|
| Canales (2) | 0,568758 | 0,532935 | **−35,82 g** |
| Lumbar | 0,311090 | 0,323786 | **+12,70 g** |
| Yugos (2) | 0,249398 | 0,262090 | **+12,69 g** |
| Casquillos (8) | 0,023029 | 0,023912 | +0,89 g |
| Resto (fijaciones, protecciones, pasadores) | 0,290052 | 0,290052 | 0,00 |
| **Rígida + protectores** | **1,442328** | **1,432778** | **−9,55 g (0,66 %)** |
| **Presupuesto (sin bomba ni agua)** | **2,212328** | **2,202778** | **−9,55 g** |

**Hallazgo principal:** el ahorro de sección (−42,8 g teóricos, −35,8 g reales en los canales) **se pierde
en un 72 %** porque lumbar y yugos derivan la altura de sus mejillas de D y crecen con él. La métrica válida
es la masa del ensamblaje. Sin medirla, el resultado se habría presentado 4,5 veces mayor de lo que es.

## 6. Verificación nativa (fase 36–50 min)

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Piezas nativas | **54/54**, un sólido por pieza, operaciones actualizadas | `Build/*.ipt`, `PROGRESO.txt` |
| Masa nativa vs volumen×densidad | coincidencia exigida por pieza; el constructor **aborta** si difiere | `Build/MASAS_CAD.json` |
| Materiales | material `SEDAC_<mat>` con la densidad del JSON, no el predeterminado | `MASAS_CAD.json`, `TABLA_MASAS.md` |
| Referencias del IAM | **54 documentos únicos, 0 ausentes** | `VERIFICACION_NATIVA.json`, `REFERENCIAS_Y_ACTUALIZACION.json` |
| Actualización del ensamblaje | `Update2 = True` | `REFERENCIAS_Y_ACTUALIZACION.json` |
| Ocurrencias | **83** | `VERIFICACION_NATIVA.json` |
| Interferencias nominales | **0** (umbral 0,001 mm³), dos medidas independientes | `INTERFERENCIAS.json`, `VERIFICACION_NATIVA.json` |
| Masa del ensamblaje | **1,432778 kg** = suma de piezas | `VERIFICACION_NATIVA.json` |
| STEP | exportado (AP203/214, protocolo 3) | `Build/SEDAC_OPT_20261023_REVISION.step` |
| Vistas | frontal, posterior, estructura, **lateral e isométrica** | `Build/VISTA_*.png` |

**Alcance:** esto acredita que el ensamblaje nativo existe, actualiza y no tiene solapes nominales. **No**
acredita resistencia, fatiga, comportamiento textil ni seguridad.

## 7. Cierre documental (D-16)

`Cierre/CIERRE.json` (reevaluación con el nombre real de los archivos):

| Resultado | Estado | Motivo |
|---|---|---|
| R1 · Generación terminada | **cumple** | 54 IPT + IAM + STEP + 3 vistas exigidas, presentes y no vacíos |
| R2 · Coherencia | **no cumple** | 1 redondeo pendiente: lumbar `parcial` (D-12) |
| R3 · Cribado | **cumple** | 15/15 verificaciones ≥ 2,2; mín. **2,227**; flecha 0,666 mm; cierre residual > 0 |

**La corrida es borrador declarado** (`ESTADO_BORRADOR.txt`), no una entrega aceptada. Es el estado
correcto: el criterio de contacto A/B/C sigue sin definir y **no** se forzó el 236/472.

**Corrección de un falso negativo propio:** el primer `CIERRE.json` del build dio R1 = falso porque el
módulo de cierre busca nombres fijos `SEDAC_<version>.iam/_REVISION.step` y esta corrida usa
`SEDAC_OPT_20261023`. Se parametrizó **solo el nombre esperado** en la copia del módulo (la comprobación de
existencia y tamaño sigue igual) y se reevaluó en `Cierre/`, conservando el primer intento en
`Cierre_intento1_nombre/`. No se modificó ningún artefacto del build.

El campo `version` de `MODELO_API.json` y de `RESUMEN_ENTREGA.json` sigue diciendo **`P2.05`** porque el
generador lo fija por diseño; los archivos de CAD sí llevan el nombre de esta iteración. No se editó el
JSON a mano para «arreglar» esa etiqueta: se deja declarado.

## 8. Pendientes

- **Mediciones (bloquean todo):** bomba llena/vacía, centro de masa, apoyos reales, reparto, cintas, usuarios.
- **D-12:** recorrido/tensión de cintas y clasificación A/B/C; el redondeo de 0,5 mm sigue siendo supuesto.
- **Mecánica:** FEA local de pandeo de ala (modo gobernante de esta alternativa) y de placa lumbar; fatiga;
  dinámica; temperatura; desgaste; aplastamiento con tolerancias reales; H02/H04/H05.
- **Arquitectura (lo que daría el ahorro grande):** desacoplar las mejillas de lumbar y yugos de D. Los
  **26,3 g** que crecen hoy son la medida de esa oportunidad; requiere rediseñar la interfaz, no la sección.
- **Funcional:** liberación de emergencia con guantes, EPP, manguera, ergonomía, colocación y retirada.
- **Fabricación:** proceso real (mecanizado), radios y acabado, tolerancias de pasador, proveedores.
- **Documental:** Mathcad/PDF pospuestos; P2.05 abierta; P2.04 sigue vigente.

## 9. Herramientas usadas

- **Inventor 2027.1 vía COM/Interop** desde PowerShell (el MCP `inventor` **no** está conectado en esta
  sesión). Operaciones ejecutadas: crear piezas y operaciones, aplicar redondeos con sondeo y *abort*,
  crear roscas cosméticas, definir materiales y propiedades, ensamblar con restricciones, medir masas,
  analizar interferencias, capturar vistas, exportar STEP, leer referencias y actualizar.
- **Python 3.12 + numpy** para el cálculo de prediseño.
- **Revisión:** sin subagentes disponibles; la revisión crítica de cálculos, hipótesis y riesgos la hizo el
  agente principal. Lo que no se pudo comprobar quedó marcado, no rellenado.

## 10. Etiquetas

**hecho:** archivos, recuentos, masas nativas, interferencias, cierre. **cálculo:** trade study y
verificaciones (scripts identificados). **supuesto:** `pared_minima` = nominal − 0,2 mm. **hipótesis:**
25 kg, 3g/1g, 70/30, e = 107,5 mm, precarga 2000 N, apoyos 55/435 mm, umbral 2,2, K_borde 1,25, K_ventana 3.
