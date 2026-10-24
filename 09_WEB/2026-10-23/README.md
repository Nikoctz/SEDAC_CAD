# SEDAC — landing

Página única, HTML + CSS + JavaScript sin dependencias ni backend. Funciona abriendo el archivo.

## Abrir

- Doble clic en `index.html`, o
- servidor local (recomendado, para que las imágenes carguen igual que en un hosting):

```
cd 09_WEB/2026-10-23
python -m http.server 8137 --bind 127.0.0.1
```

y abrir `http://127.0.0.1:8137/index.html`.

## Archivos

| Archivo | Qué contiene |
|---|---|
| `index.html` | todo el contenido y las ilustraciones SVG en línea |
| `styles.css` | paleta, tipografía, retícula y adaptación a móvil |
| `app.js` | menú móvil accesible, header al hacer scroll, sección activa, revelado |
| `assets/cad_conjunto.png` | CAD P2.04, vista isométrica del conjunto |
| `assets/cad_estructura.png` | CAD P2.04, subconjunto estructural |
| `assets/cad_frente.png` | CAD P2.04, vista frontal (no usada aún en la página) |

Las tres imágenes son capturas del **CAD vigente P2.04** (16-10-2026), no fotografías de un prototipo.

## Cambiar contenido

- Textos: directamente en `index.html`.
- Colores: variables en `:root` de `styles.css` (`--graphite`, `--paper`, `--yellow`).
- Imágenes: reemplazar los archivos de `assets/` conservando el nombre, o actualizar el `src` y el `alt`.
- El héroe y el gráfico de IMU son SVG en línea: se editan en el propio HTML.

## Límites de esta versión

- Todas las cifras son del modelo de prediseño; no hay pesajes ni ensayos.
- El gráfico de IMU es **ilustrativo** y está rotulado como tal.
- No hay datos de contacto: la página lo dice de forma explícita en vez de inventar un correo.
- No publicada y sin servicios externos conectados.
