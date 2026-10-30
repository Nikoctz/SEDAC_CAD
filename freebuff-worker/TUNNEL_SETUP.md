# Configuración del Túnel para los Puentes MCP

## Arquitectura

```
┌─────────────────┐     ┌─────────────────────────────────┐     ┌──────────────────────┐
│  Freebuff Sites  │────▶│  Worker de Cloudflare (deploy)  │────▶│  Túnel (cloudflared) │
│  (chat/browser)  │     │  freebuff.page                  │     │  → localhost:8766    │
└─────────────────┘     └─────────────────────────────────┘     │  → localhost:8767    │
                                                                  └──────────────────────┘
                                                                             │
                                                                             ▼
                                                                  ┌──────────────────────┐
                                                                  │  Puentes HTTP locales │
                                                                  │  (Inventor/Revit)     │
                                                                  └──────────────────────┘
                                                                             │
                                                                             ▼
                                                                  ┌──────────────────────┐
                                                                  │  MCP Inventor/Revit  │
                                                                  │  (Python + COM)      │
                                                                  └──────────────────────┘
```

## Paso 1: Iniciar los puentes HTTP locales

### Inventor Bridge (puerto 8766)

```powershell
# Navegar al directorio del puente
cd C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\inventor-http-bridge

# Activar el venv de Inventor (si no está activado)
& "C:\Users\nicol\MCP\Inventor_Avanzado_20261029\.venv\Scripts\Activate.ps1"

# Iniciar el puente
python server.py --host 127.0.0.1 --port 8766
```

### Revit Bridge (puerto 8767)

```powershell
# Navegar al directorio del puente
cd C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\tools\revit-http-bridge

# Activar el venv de Revit (si no está activado)
& "C:\Users\nicol\OneDrive\Desktop\Topicos 1 Eficiencia energetica\output\mcp_revit_2026-10-26\server\.venv\Scripts\Activate.ps1"

# Iniciar el puente
python server.py --host 127.0.0.1 --port 8767
```

## Paso 2: Iniciar Cloudflare Tunnel

### Opción A: Cloudflare Tunnel (cloudflared)

```powershell
# Instalar cloudflared si no está instalado
# https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

# Iniciar túnel para Inventor (puerto 8766)
cloudflared tunnel --url http://localhost:8766 --loglevel debug

# En otra terminal, iniciar túnel para Revit (puerto 8767)
cloudflared tunnel --url http://localhost:8767 --loglevel debug
```

Cada túnel dará una URL pública del tipo:
- `https://a1b2c3d4-5678-90ab-cdef-1234567890ab.freebuff.dev` (Inventor)
- `https://e5f6g7h8-90ab-cdef-1234567890cd.freebuff.dev` (Revit)

### Opción B: Ngrok

```powershell
# Iniciar ngrok para Inventor
ngrok http 8766

# En otra terminal, iniciar ngrok para Revit
ngrok http 8767
```

## Paso 3: Configurar los Secrets en Freebuff

Una vez que tienes las URLs de los túneles, configúralas como secrets en el sitio de Freebuff:

```
Environment: preview
Name: INVENTOR_BRIDGE_URL
Value: https://<tu-url-tunel-inventor>.freebuff.dev

Environment: preview
Name: REVIT_BRIDGE_URL
Value: https://<tu-url-tunel-revit>.freebuff.dev
```

O usa la CLI:

```bash
# Desde el directorio del worker
cd freebuff-worker

# Configurar secrets (reemplaza con tus URLs reales)
wrangler secret put INVENTOR_BRIDGE_URL --value "https://tu-url-inventor"
wrangler secret put REVIT_BRIDGE_URL --value "https://tu-url-revit"
```

## Paso 4: Desplegar el Worker

```bash
cd freebuff-worker

# Login a Cloudflare (si es necesario)
wrangler login

# Desplegar
wrangler deploy
```

## Uso desde Freebuff

Una vez desplegado, el Worker estará disponible en:
- Preview: `https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page`
- Production: `https://site-b416044f13a940a7a21cbf9010026939.freebuff.page`

### Ejemplo de uso con fetch desde Freebuff

```javascript
// Ejecutar una herramienta de Inventor
const inventorResult = await fetch(
  'https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/inventor/call',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tool: 'create_part',
      arguments: { name: 'Prueba desde Freebuff' }
    })
  }
);
const inventorData = await inventorResult.json();

// Ejecutar una herramienta de Revit
const revitResult = await fetch(
  'https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/revit/call',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tool: 'revit_status',
      params: {}
    })
  }
);
const revitData = await revitResult.json();
```

## Verificación

### 1. Verificar puentes locales

```powershell
# Inventor
curl http://localhost:8766/health

# Revit
curl http://localhost:8767/health
```

### 2. Verificar túneles

Accede a las URLs de los túneles desde un navegador o con curl para confirmar que están expuestos correctamente.

### 3. Verificar Worker desplegado

```bash
curl https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/health
```

### 4. Probar una llamada completa

```bash
# Ejemplo: obtener estado de Revit
curl -X POST https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/revit/call ^
  -H "Content-Type: application/json" ^
  -d "{\"tool\":\"revit_status\",\"params\":{}}"
```

## Troubleshooting

### Túnel no conecta
- Verifica que el puente local esté corriendo: `curl localhost:8766/health`
- Verifica que cloudflared/ngrok esté corriendo y haya generado la URL
- Revisa los logs del túnel

### Worker devuelve 502
- Verifica que las URLs de los secrets sean correctas
- Verifica que los túneles estén accesibles desde internet
- Revisa los logs del Worker en Cloudflare Dashboard

### Inventor no responde
- Asegúrate de que Inventor está abierto
- Asegúrate de que el venv de Inventor tiene las dependencias: `pip install mcp pywin32`
- Revisa los logs del puente Inventor

### Revit no responde
- Asegúrate de que Revit está abierto con el complemento cargado
- Verifica que el puerto 8765 (puente Revit interno) esté disponible
- Revisa los logs del puente Revit

## Notas de seguridad

- Los puentes están configurados para localhost por defecto
- Los túneles exponen los puentes a internet - usa autenticación si es necesario
- Considera añadir rate limiting en el Worker
- Los secrets de Freebuff no se exponen en el código
