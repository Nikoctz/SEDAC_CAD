# Puentes HTTP para MCP locales (Inventor + Revit)

Estos puentes permiten que un **Worker de Cloudflare/Freebuff** llame a los servidores MCP locales de Inventor y Revit que corren en tu PC, expuestos vía HTTP.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     Navegador / Freebuff                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ (fetch HTTP)
┌─────────────────────────────────────────────────────────────┐
│               Workers de Cloudflare (Freebuff Sites)         │
│  - Ejecuta el código del Worker                             │
│  - Puede hacer fetch() a tu PC si está expuesto             │
└─────────────────────────────────────────────────────────────┘
                            │
                 (red TCP/IP local o tunel)
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  Inventor HTTP Bridge   │   │   Revit HTTP Bridge     │
│  localhost:8766         │   │   localhost:8767        │
│  (Python)               │   │   (Python)              │
└─────────────────────────┘   └─────────────────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  MCP Inventor (stdio)   │   │  Puente RevitMcpBridge  │
│  → Inventor COM API     │   │  → TCP 127.0.0.1:8765  │
└─────────────────────────┘   └──────────┬──────────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Revit + Addin      │
                              │   (C# COM/External)  │
                              └─────────────────────┘
```

## Requisitos previos

### Inventor HTTP Bridge

1. **Inventor 2026+** instalado y ejecutable
2. **Python 3.12+** en el venv de Inventor:
   ```
   C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe
   ```
3. **Dependencias instaladas** en ese venv:
   ```
   mcp[cli] pywin32
   ```
4. **Inventor abierto** antes de iniciar el puente (o el puente lo iniciará)

### Revit HTTP Bridge

1. **Revit 2027** instalado
2. **Complemento RevitMcpBridge** cargado en Revit (Addins/2027/)
3. **Python 3.12+** en el venv de Revit:
   ```
   C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe
   ```
4. **Revit abierto** con el complemento activo

## Instalación

### 1. Instalar dependencias

```bash
# Activar el venv de Inventor
C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\activate

# Instalar mcp (si no está)
pip install "mcp[cli]" pywin32

# Activar el venv de Revit (opcional, si se usa para el puente)
cd "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server"
.venv\Scripts\activate
pip install mcp pydantic
```

### 2. Copiar catálogo de herramientas de Revit (para el puente)

```bash
# Copiar el catálogo cacheado al directorio del puente
copy "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\catalog\tools.json" "tools\revit-http-bridge\catalog\"
```

### 3. Iniciar los puentes

**Inventor Bridge:**
```bash
cd tools\inventor-http-bridge
..\..\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe server.py --port 8766
```

**Revit Bridge:**
```bash
cd tools\revit-http-bridge
..\..\..\..\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\python.exe server.py --port 8767
```

## API HTTP

### Inventor Bridge (`http://localhost:8766`)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Info del servicio |
| `/health` | GET | Estado del puente y conexión |
| `/tools` | GET | Lista de herramientas disponibles |
| `/call` | POST | Ejecutar una herramienta |

**Ejecutar herramienta:**
```http
POST /call
Content-Type: application/json

{
  "tool": "connect",
  "arguments": {
    "visible": true
  }
}
```

**Respuesta:**
```json
{
  "content": [
    {"type": "text", "text": "Connected to Inventor 2026.1..."},
    {"type": "image", "data": "base64...", "media_type": "image/png"}
  ],
  "isError": false
}
```

### Revit Bridge (`http://localhost:8767`)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Info del servicio |
| `/health` | GET | Estado del puente y conexión a Revit |
| `/tools` | GET | Lista de herramientas disponibles |
| `/tools/{name}` | GET | Esquema de una herramienta |
| `/call` | POST | Ejecutar una herramienta |

**Ejecutar herramienta:**
```http
POST /call
Content-Type: application/json

{
  "tool": "revit_status",
  "params": {}
}
```

**Respuesta:**
```json
{
  "ok": true,
  "result": {
    "version": "2027.1",
    "build": "20261026",
    "documents": [...],
    "active_view": "...",
    "units": "metros"
  }
}
```

## Endpoints principales disponibles

### Inventor (puente HTTP)

Las herramientas se obtienen del servidor MCP local. Incluyen:

- `connect(visible, project, new_instance, pid, instance)` — Conectar a Inventor
- `status()` — Estado de conexión y documento activo
- `list_documents()` — Documentos abiertos
- `create_part(name, template, material, part_number, description)` — Nueva pieza
- `create_sketch(plane, face_index, offset)` — Nuevo sketch
- `draw_rectangle(x, y, width, height, sketch_index, corner_radius)`
- `draw_circle(x, y, diameter, sketch_index, construction)`
- `draw_line(x1, y1, x2, y2, sketch_index, construction)`
- `draw_polygon(x, y, radius, sides, sketch_index)`
- `draw_closed_profile(points, sketch_index)`
- `extrude(distance, direction, operation, sketch_index, extent_type)`
- `revolve(angle, axis, sketch_index, operation)`
- `hole(x, y, diameter, depth, tapped, pitch)` — Agujero taladrado/roscado
- `hole_linear(...)` — Agujero paramétrico desde bordes
- `fillet(radius, edge_indices)`
- `chamfer(distance, edge_indices)`
- `circular_pattern(feature_index, count, angle, axis)`
- `sheet_metal_face(sketch_index)`
- `flange(edge_indices, distance, angle)`
- `sheet_metal_cut(sketch_index)`
- `find_edge(x, y, z, ...)`
- `find_face(x, y, z, ...)`
- `list_features()`
- `delete_feature(indices)`
- `suppress_feature(indices, suppressed)`
- `get_parameters()`
- `set_parameter(name, expression)`
- `add_parameter(name, expression, units)`
- `save_document(path, overwrite, save_dependents)`
- `export_document(path, format, overwrite)` — STEP, STL, SAT, IGES
- `close_unsaved(include_active, confirm_close_all)`
- `activate_document(name_or_path)`
- `list_instances()` — Inventors conectados
- `call_status(wait_seconds, instance)` — Estado de llamada en curso
- `cancel_call(instance)` — Cancelar llamada en curso
- `execute_python(code, undo_on_error, timeout)` — Ejecución Python arbitraria
- `load_library(path)` — Cargar librería Python
- `reload_api()` — Recargar API sin reiniciar
- `snapshot_current(width, height)` — Captura PNG de vista actual
- `view_image(views, width, height, background, focus, sketches, up)` — Imágenes de vistas
- `inspect()` — Snapshot compacto del documento activo
- `list_edges(min_length, max_count)`
- `list_faces(min_area, max_count)`
- `transaction(action, name)`
- `create_assembly(name, ...)`
- `place_component(path, x, y, z, grounded, ...)`
- `constrain(occurrence1, geometry1, occurrence2, geometry2, kind, ...)`
- `assembly_info()`

### Revit (puente HTTP)

Según el catálogo cacheado (`tools.json`), incluye:

**Estado y catálogo:**
- `revit_status()` — Estado de Revit
- `revit_list_tools()` — Catálogo de herramientas
- `revit_list_categories()` — Categorías disponibles
- `revit_list_levels()` — Niveles del modelo
- `revit_list_views()` — Vistas del modelo
- `revit_list_materials()` — Materiales del proyecto
- `revit_list_mep_types(kind)` — Tipos MEP
- `revit_list_mep_systems()` — Sistemas MEP
- `revit_list_families(category, include_loadable)` — Familias
- `revit_list_types(category, kind)` — Tipos de elemento
- `revit_list_fill_types(kind)` — Tipos de relleno
- `revit_model_statistics()` — Estadísticas del modelo
- `revit_material_audit(include_unused)` — Auditoría de materiales

**Documentos:**
- `revit_new_project(template, save_path)` — Nuevo proyecto
- `revit_open_document(path, activate)` — Abrir .rvt
- `revit_close_document(title, path)` — Cerrar documento
- `revit_save_document(path, overwrite)` — Guardar
- `revit_regenerate_model()` — Regenerar modelo

**Elementos y consultas:**
- `revit_get_element(element_id)` — Propiedades de un elemento
- `revit_get_geometry(element_id)` — Caja acotadora, volumen, área
- `revit_get_material(material, usage)` — Propiedades termicas
- `revit_get_rooms(level, include_unbounded)` — Recintos
- `revit_query_elements(categories, level, name_contains, type_contains, filters, limit)` — Consulta
- `revit_delete_elements(element_ids)` — Eliminar elementos
- `revit_set_parameter(element_ids, param, value, number_value, bool_value)` — Parámetro
- `revit_set_wall_type(element_ids, type)` — Tipo de muro
- `revit_set_opening_size(element_ids, width_m, height_m)` — Tamaño de abertura
- `revit_fit_view(view, categories, margin_m)` — Ajustar vista

**Creación de elementos:**
- `revit_create_wall(start, end, level, type, height_m, offset_m, flip, structural, ...)` — Muro
- `revit_create_floor(points, level, type, offset_m, comments)` — Losa
- `revit_create_roof(points, level, type, offset_m)` — Cubierta
- `revit_create_foundation(points, level, wall_type, thickness_mm, depth_mm, create_footing)` — Cimiento
- `revit_create_level(name, elevation_m)` — Nivel
- `revit_create_grid(start, end, name, type)` — Eje
- `revit_create_room(level, point, name, number, comments)` — Recinto
- `revit_create_opening(wall_id, start, end)` — Vano
- `revit_create_door(wall_id, symbol, point, distance_m, level, flip, width_m, height_m, sill_m)` — Puerta
- `revit_create_window(wall_id, symbol, point, distance_m, level, flip, width_m, height_m, sill_m)` — Ventana
- `revit_create_pipe(start, end, pipe_type, level, diameter_mm, material, insulation, ...)` — Tubería
- `revit_create_duct(start, end, duct_type, level, diameter_mm, material)` — Ducto
- `revit_create_fill(profiles, points, level, type, mode, comments)` — Relleno/toposolid
- `revit_create_3d_view(name, view_family_type)` — Vista 3D
- `revit_create_plan_view(level, name, scale, view_family_type, crop_to_room_bounds, cut_plane_m)` — Planta
- `revit_create_section(start, end, name, depth_m, height_m, level)` — Sección
- `revit_create_compound_type(kind, name, layers, function, base_type)` — Tipo compuesto
- `revit_create_material(name, material_class, conductivity, density, specific_heat, color, notes, material_category)` — Material
- `revit_load_family(path)` — Cargar familia .rfa
- `revit_add_insulation_layer(type, material, thickness_m, position)` — Capa de aislamiento
- `revit_assign_material_to_type(type, layer_index, material)` — Asignar material a capa
- `revit_create_pipe_insulation(pipe_id, insulation_type, thickness_mm)` — Aislamiento tubería

**Especificaciones y exportación:**
- `revit_create_schedule_csv(category, output_path, name)` — Tabla a CSV
- `revit_export_schedule_csv(category, output_path, name)` — Exportar tabla
- `revit_export_pdf(output_path, views, combine)` — Exportar vistas a PDF
- `revit_export_view_images(output_dir, views, file_type, pixel_size, white_background)` — Exportar imágenes
- `revit_export_model(format, output_dir, name)` — Exportar modelo (IFC, DWG, DXF)

**Análisis energético:**
- `revit_energy_summary(rsi, rse)` — Resumen energético
- `revit_envelope_analysis(include_floors, rsi, rse)` — Análisis de envolvente
- `revit_assembly_thermal_report(type, rsi, rse)` — Reporte térmico
- `revit_batch(steps, stop_on_error)` — Ejecutar varias operaciones en una transacción

**Conjunto de herramientas:**
- `revit_set_active_view(view, document)` — Cambiar vista activa

## Seguridad

### ⚠️ Advertencias importantes

1. **Solo localhost por defecto**: Los puentes están configurados para escuchar solo en `127.0.0.1`. No exponer a la red pública sin medidas adicionales.

2. **Writes disabled por defecto (Revit)**: El puente Revit tiene `ALLOW_WRITES=False` por defecto. Para permitir operaciones de escritura:
   - En el puente HTTP: `--allow-writes` o variable `REVIT_MCP_ALLOW_WRITES=1`
   - O en el archivo de configuración del complemento Revit

3. **Inventor requiere confirmación**: Algunas operaciones en Inventor pueden requerir confirmación del usuario (diálogos modales). El puente las detecta y reporta, pero no las responde automáticamente.

4. **Autenticación**: Para uso remoto desde Freebuff, se recomienda añadir autenticación (API key, token, etc.) al puente HTTP. Actualmente no hay autenticación implementada.

## Exposición remota para Freebuff

Para que un **Worker de Cloudflare/Freebuff** pueda acceder a los puentes, necesitas hacerlos accesibles desde internet. Opciones:

### Opción 1: Cloudflare Tunnel (recomendado)

```bash
# Instalar cloudflared
# Iniciar túnel que exponga los puentes locales

cloudflared tunnel --url http://localhost:8766
cloudflared tunnel --url http://localhost:8767
```

Esto proporciona URLs públicas que el Worker puede usar.

### Opción 2: Ngrok

```bash
ngrok http 8766
ngrok http 8767
```

### Opción 3: Túnel manual (SSH reverse)

Si tienes un servidor VPS accesible:
```bash
ssh -R 8766:localhost:8766 user@tu-servidor
ssh -R 8767:localhost:8767 user@tu-servidor
```

### Configuración del Worker de Freebuff

En el código del Worker:
```javascript
const INVENTOR_BRIDGE_URL = "https://tus-tunnel-cloudflared-8766.trycloudflare.com";
const REVIT_BRIDGE_URL = "https://tus-tunnel-cloudflared-8767.trycloudflare.com";

// Ejecutar herramienta de Inventor
const inventorResult = await fetch(`${INVENTOR_BRIDGE_URL}/call`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    tool: "connect",
    arguments: { visible: true }
  })
}).then(r => r.json());

// Ejecutar herramienta de Revit
const revitResult = await fetch(`${REVIT_BRIDGE_URL}/call`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    tool: "revit_status",
    params: {}
  })
}).then(r => r.json());
```

## Limitaciones

1. **Latencia**: Las llamadas pasan por HTTP → TCP local → MCP stdio → COM, lo que añade latencia. Operaciones complejas en Inventir/Revit pueden tardar varios segundos.

2. **Comunicación síncrona**: El puente HTTP es síncrono para cada llamada. No hay streaming o ejecución asíncrona embebida.

3. **Tamaño de respuesta**: Imágenes y datos grandes se devuelven como base64 en JSON, lo que puede ser ineficiente para datos muy grandes.

4. **Sesiones**: Cada Worker que llame al puente comparte la misma sesión MCP. No hay aislamiento entre usuarios del Worker.

5. **Inventor requiere GUI**: Algunas operaciones requieren que Inventor tenga interfaz gráfica (no headless).

6. **Revit requiere complemento**: El puente Revit depende del complemento RevitMcpBridge C# que debe estar cargado y ejecutándose dentro de Revit.

## Ejemplo de uso complet

### 1. Iniciar Inventor y el puente

```powershell
# Iniciar Inventor
Start-Process "C:\Program Files\Autodesk\Inventor 2026\Inventor.exe"

# Esperar a que esté listo
Start-Sleep -Seconds 5

# Iniciar puente HTTP
cd C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\inventor-http-bridge
..\..\MCP\Inventor_Avanzado_20261029\.venv\Scripts\python.exe server.py --port 8766
```

### 2. Probar el puente localmente

```bash
# Verificar que está corriendo
curl http://localhost:8766/health

# Obtener lista de herramientas
curl http://localhost:8766/tools

# Conectar a Inventor
curl -X POST http://localhost:8766/call ^
  -H "Content-Type: application/json" ^
  -d "{\"tool\":\"connect\",\"arguments\":{\"visible\":true}}"

# Crear una pieza simple
curl -X POST http://localhost:8766/call ^
  -H "Content-Type: application/json" ^
  -d "{\"tool\":\"create_part\",\"arguments\":{\"name\":\"Prueba WEB\"}}"
```

### 3. Usar desde Freebuff

Después de exponer el puente con un tunnel:

```javascript
// En el Worker de Freebuff
const response = await fetch(INVENTOR_BRIDGE_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    tool: "create_sketch",
    arguments: { plane: "XY" }
  })
});
const result = await response.json();
```

## Estado actual

| Puente | Estado | Notas |
|--------|--------|-------|
| Inventor HTTP Bridge | ✅ Implementado | `tools/inventor-http-bridge/server.py` |
| Revit HTTP Bridge | ✅ Implementado | `tools/revit-http-bridge/server.py` |
| Catálogo Revit | ✅ Copiado | `tools/revit-http-bridge/catalog/tools.json` |
| Autenticación | ❌ No implementada | Requiere añadir API key o sesión |
| Túnel para Freebuff | ❌ Pendiente | Configurar cloudflared/ngrok |

## Próximos pasos

1. **Test local**: Iniciar los puentes y verificar que responden correctamente con `curl`.
2. **Exponer remotamente**: Configurar Cloudflare Tunnel o ngrok para exponer los puentes.
3. **Integrar en Worker**: Modificar el Worker de Freebuff para usar los puentes.
4. **Añadir autenticación**: Implementar API key o token de sesión para seguridad.
5. **Manejo de errores**: Añadir retry y manejo de desconexiones.
6. **Considerar CORS**: Configurar CORS adecuadamente si el Worker está en otro origen.
