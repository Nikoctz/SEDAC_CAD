# Configuración Final del Puente MCP para Freebuff

## Estado actual

| Componente | Estado | Notas |
|------------|--------|-------|
| Worker de Freebuff | ✅ Desplegado | https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page |
| Inventor Bridge | ✅ Corriendo | localhost:8766, pero `connected: false` (Inventor no abierto) |
| Revit Bridge | ⚠️ Inestable | localhost:8767, a veces OK, a veces no |
| Inventor | ❌ No abierto | Necesario para `connected: true` |
| Revit | ✅ Abierto | Con complemento cargado |
| Túneles | ❌ No configurados | Necesarios para acceso externo |

## Paso 1: Abrir Inventor

Para que el puente de Inventor funcione, necesitas abrir Inventor:

```powershell
# Iniciar Inventor 2026
Start-Process "C:\Program Files\Autodesk\Inventor 2026\Inventor.exe"
```

O usa el script:
```powershell
.\tools\start_inventor.ps1
```

## Paso 2: Estabilizar Revit Bridge

Si el Revit Bridge es inestable, reinicia con:
```powershell
.\tools\start_revit_clean.ps1
```

## Paso 3: Generar túneles

Necesitas exponer los puentes a internet. Usa cloudflared o ngrok:

### Con cloudflared:
```powershell
# Inventor (puerto 8766)
cloudflared tunnel --url http://localhost:8766

# Revit (puerto 8767) - en otra terminal
cloudflared tunnel --url http://localhost:8767
```

Cada túnel generará una URL como:
- `https://random-id-12345678.freebuff.dev` (Inventor)
- `https://another-id-87654321.freebuff.dev` (Revit)

### Con ngrok:
```powershell
ngrok http 8766
ngrok http 8767
```

## Paso 4: Configurar secrets en Freebuff

Una vez que tengas las URLs de los túneles, configúralas:

```bash
# Usando wrangler (requiere CLOUDFLARE_API_TOKEN)
cd freebuff-worker

wrangler secret put INVENTOR_BRIDGE_URL --value "https://TU-URL-inventor.aquí"
wrangler secret put REVIT_BRIDGE_URL --value "https://TU-URL-revit.aquí"
```

O usa la API de Cloudflare directamente:
```bash
export CLOUDFLARE_API_TOKEN="tu_token"
export CLOUDFLARE_ACCOUNT_ID="tu_account_id"

# Inventor
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/workers/scripts/secrets" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"INVENTOR_BRIDGE_URL","text":"https://tu-url-inventor","lifecycle":"persistent"}'

# Revit
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/workers/scripts/secrets" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"REVIT_BRIDGE_URL","text":"https://tu-url-revit","lifecycle":"persistent"}'
```

## Paso 5: Re-desplegar el Worker (opcional)

Si cambiaste el wrangler.jsonc:
```bash
cd freebuff-worker
wrangler deploy
```

O usa el sites_deploy de Freebuff con el manifest.json:
```
sites_deploy --site-id 5d9e1a2c-3b4f-4d6e-8a7c-9f0b1c2d3e4f --environment preview --manifest freebuff-worker/manifest.json
```

## Paso 6: Probar

Desde Freebuff (o cualquier cliente HTTP):

```bash
# Verificar que el Worker está operativo
curl https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/health

# Probar conexión a Inventor (una vez que esté abierto y túnel configurado)
curl -X POST "https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/inventor/call" \
  -H "Content-Type: application/json" \
  -d '{"tool":"status","arguments":{}}'

# Probar conexión a Revit
curl -X POST "https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/revit/call" \
  -H "Content-Type: application/json" \
  -d '{"tool":"revit_status","params":{}}'
```

## Troubleshooting

### Inventor Bridge conectado=false
- Asegúrate de que Inventor está abierto
- Reinicia el puente: `.\tools\start_inventor_bridge.ps1`

### Revit Bridge inestable
- Reinicia: `.\tools\start_revit_clean.ps1`
- Verifica que Revit está abierto y el complemento está cargado
- El puerto 8765 debe estar escuchando (Revit interno)

### Worker devuelve 502
- Verifica que las URLs de los secrets son correctas
- Verifica que los túneles estén accesibles desde internet
- Revisa los logs del Worker en Cloudflare Dashboard

### Puertos ocupados
```powershell
# Ver qué está en los puertos
netstat -ano | findstr ":8766"
netstat -ano | findstr ":8767"
netstat -ano | findstr ":8765"

# Si hay procesos extra, detenerlos
Stop-Process -Id <PID> -Force
```

## Archivos relevantes

- `freebuff-worker/worker.js` - Código del Worker de Cloudflare
- `freebuff-worker/wrangler.jsonc` - Configuración del Worker
- `freebuff-worker/manifest.json` - Manifest para deploy
- `tools/inventor-http-bridge/server.py` - Puente HTTP de Inventor
- `tools/revit-http-bridge/server.py` - Puente HTTP de Revit
- `tools/manage_bridges.ps1` - Script de gestión de puentes
- `tools/start_revit_clean.ps1` - Iniciar Revit Bridge limpio
- `tools/start_inventor.ps1` - Iniciar Inventor
