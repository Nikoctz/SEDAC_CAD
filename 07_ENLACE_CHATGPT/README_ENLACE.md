# Enlace ChatGPT ↔ SEDAC_CAD

Un proyecto ChatGPT **sólo de chat** no puede leer las carpetas de este PC. (Sí puede leer
**Notion**, que es otra cosa y no se pega: Notion lleva los requisitos y el paquete lleva el
estado técnico del repositorio.) Este enlace resuelve lo que ChatGPT **no** ve, con **un archivo
de ida** y **un archivo de vuelta**, y con una regla que evita el fallo que ya nos mordió una
vez: *un relato que contradice a su propio dato*.

## La regla de oro

1. **El repositorio manda.** ChatGPT lee e interpreta; no es autoridad. Ante cualquier
   conflicto, vale lo que diga `ESTADO_ACTUAL.md`.
2. **ChatGPT no produce `hecho`.** Todo lo que vuelva de allí entra como `supuesto` o
   `hipótesis` hasta que un archivo o un cálculo de este repositorio lo respalde.
3. **Los números no se copian a mano.** Los escribe `GENERAR_PAQUETE.ps1` leyéndolos de los
   archivos del proyecto. Así ChatGPT no puede «recordar mal» una masa.

## Ciclo de trabajo (5 pasos)

1. Escribe tus dudas en `PREGUNTAS.md` (se pegan solas dentro del paquete).
2. Ejecuta el generador:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\07_ENLACE_CHATGPT\GENERAR_PAQUETE.ps1
   ```

   Salida: `PAQUETE_CHATGPT.md`, listo para pegar entero (o subirlo como documento del
   proyecto ChatGPT, si tu plan tiene esa opción).
3. Pega el paquete en tu proyecto ChatGPT y trabaja allí.
4. Cuando responda, guarda la respuesta como `Entrada_AAAAMMDD.md` partiendo de
   `PLANTILLA_ENTRADA.md`. **Esa respuesta es un borrador externo, no un dato.**
5. Pide a tu agente local (Codex u OpenCode) que revise esa entrada y la funda, marcada, en
   `DECISIONES.md` / `ESTADO_ACTUAL.md` / `CHANGELOG_SEDAC.md`. **Nada entra directo.**

## Qué NO debe salir de este PC

- Rutas absolutas de este equipo (`C:\...`). El generador lo revisa por su cuenta y, si
  encuentra algo, escribe `AVISO_PRIVACIDAD.txt` y avisa por pantalla.
- El contenido de `.codex/config.toml` (ya excluido de Git precisamente por eso).
- Nombres de personas, fotos con datos identificables, datos de terceros.

Nota: el paquete incluye `ESTADO_ACTUAL.md`, `DECISIONES.md` y `CHANGELOG_SEDAC.md`
**literales**. Si algún día uno de esos documentos contiene un nombre personal, el aviso de
privacidad lo señalará y habrá que decidir si se envía.

## Archivos

| archivo | qué es | ¿se edita? |
|---|---|---|
| `GENERAR_PAQUETE.ps1` | genera el paquete leyendo el repositorio | sí, si hace falta |
| `PAQUETE_CHATGPT.md` | salida del generador: lo que se pega | **no** (se regenera) |
| `PREGUNTAS.md` | tus preguntas para ChatGPT | sí, cada vez |
| `PLANTILLA_ENTRADA.md` | modelo para la respuesta de vuelta | copiar, no editar |
| `INSTRUCCIONES_PROYECTO.md` | reglas permanentes, se pegan en el campo «Instrucciones» del proyecto ChatGPT | sí, si cambia el papel de Notion o del paquete |
| `Entrada_AAAAMMDD.md` | respuestas recibidas | las crea quien recoge |
| `AVISO_PRIVACIDAD.txt` | solo aparece si hay algo que revisar | automático |

## Si algún día quieres menos copiar/pegar

La vía 2 es subir el repositorio a un **GitHub privado** y conectar el proyecto ChatGPT a ese
repositorio (solo lectura): entonces ChatGPT lee los archivos reales y sólo hay que traer la
respuesta de vuelta. Implica que el CAD y la documentación salgan de este PC, así que es una
decisión del responsable, no del agente.
