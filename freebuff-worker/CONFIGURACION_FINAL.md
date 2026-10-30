# Configuración Final del Puente MCP para Freebuff
# Estado: Parcialmente automatizado

## Estado actual

| Componente | Estado | Acción necesaria |
|------------|--------|-----------------|
| Worker de Freebuff | ✅ Desplegado | Ninguna |
| Inventor Bridge | ✅ Corriendo | Abrir Inventor para connected=true |
| Revit Bridge | ✅ Corriendo | Ninguna (59 herramientas disponibles) |
| Revit | ✅ Abierto | Ninguna |
| Inventor | ❌ Cerrado | Abrir Inventor 2026 |
| Túneles | ❌ No funcionales | Necesario cloudflared login o ngrok authtoken |
| Secrets | ❌ Con URLs placeholder | Actualizar con URLs de túneles reales |

## Pasos ya completados

✅ Creado sitio en Freebuff: sedac-cad-mcp-bridge
✅ Desplegado Worker en preview y production
✅ Creados puentes HTTP (inventor-http-bridge, revit-http-bridge)
✅ Creados scripts de gestión (manage_bridges.ps1, run_bridges.ps1, etc.)
✅ Descargado cloudflared y ngrok
✅ Generado certificate para cloudflared

## Pasos pendientes (manuales)

### 1. Abrir Inventor (obligatorio)
```powershell
.\tools\start_inventor.ps1
```
O abrir Inventor 2026 manualmente. El puente de Inventor necesita Inventor abierto para funcionar.

### 2. Configurar túneles (requiere cuenta)

**Opción A: cloudflared (requiere login)**
```powershell
# Login (abre navegador para autenticación)
C:\Users\nicol\AppData\Local\cloudflared.exe login

# Después del login, crear los túneles
C:\Users\nicol\AppData\Local\cloudflared.exe tunnel --url http://localhost:8766
C:\Users\nicol\AppData\Local\cloudflared.exe tunnel --url http://localhost:8767
```
Las URLs se verán en la salida del comando tunnel.

**Opción B: ngrok (requiere authtoken)**
```powershell
# Configurar authtoken (reemplazar con tu token de https://dashboard.ngrok.com/get-started/your-authtoken)
C:\Users\nicol\AppData\Local\ngrok.exe config add-authtoken TU_AUTHTOKEN_AQUI

# Crear los túneles
C:\Users\nicol\AppData\Local\ngrok.exe http 8766
C:\Users\nicol\AppData\Local\ngrok.exe http 8767
```
Las URLs se verán en la salida del comando.

### 3. Actualizar secrets en Freebuff

Una vez que tengas las URLs de los túneles, actualiza los secrets:

```bash
cd freebuff-worker

# Usando wrangler (requiere CLOUDFLARE_API_TOKEN)
wrangler secret put INVENTOR_BRIDGE_URL --value "https://url-del-tunel-inventor"
wrangler secret put REVIT_BRIDGE_URL --value "https://url-del-tunel-revit"
```

### 4. Probar

```bash
# Verificar Inventor Bridge (debe mostrar connected: true)
curl http://localhost:8766/health

# Verificar Revit Bridge
curl http://localhost:8767/health

# Verificar túneles (las URLs de los túneles deben responder)
curl https://url-del-tunel-inventor/health
curl https://url-del-tunel-revit/health

# Verificar Worker desde Freebuff
curl https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/health
```

## Scripts disponibles

| Script | Descripción |
|--------|-------------|
| `tools/start_inventor.ps1` | Inicia Inventor 2026 |
| `tools/start_revit_clean.ps1` | Inicia Revit Bridge de forma estable |
| `tools/manage_bridges.ps1` | Gestión de puentes (start/stop/status/restart) |
| `tools/check_bridges.ps1` | Verifica estado de puentes y puertos |
| `tools/run_bridges.ps1` | Inicia ambos puentes |

## URLs del Worker

- **Preview:** https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page
- **Production:** https://site-b416044f13a940a7a21cbf9010026939.freebuff.page

## Endpoints del Worker

- `GET /health` - Estado del puente
- `GET /inventor/tools` - Listar herramientas de Inventor
- `GET /revit/tools` - Listar herramientas de Revit
- `POST /inventor/call` - Ejecutar herramienta de Inventor
- `POST /revit/call` - Ejecutar herramienta de Revit

## Limitaciones conocidas

1. **Inventor Bridge requiere Inventor abierto** - si Inventor cierra, el puente deja de funcionar
2. **Revit Bridge es inestable** - a veces necesita reiniciarse
3. **Túneles requieren cuenta** - cloudflared o ngrok necesitan autenticación
4. **Los puentes son locales** - si el PC se apaga o se duerme, los túneles se caen
5. **Seguridad** - los puentes están expuestos a internet vía túneles; considera añadir autenticación

## Solución de problemas

### Inventor Bridge conectado=false
- Abre Inventor 2026
- Verifica que el puente está corriendo: `curl localhost:8766/health`

### Revit Bridge inestable
- Reinicia: `.\tools\start_revit_clean.ps1`
- Verifica que Revit está abierto y el complemento está cargado
- Verifica puerto 8765: `netstat -ano | findstr :8765`

### Túneles no funcionan
- Verifica que cloudflared/ngrok están corriendo
- Verifica que tienes cuenta y authtoken/configuración correcta
- Para cloudflared: `.\cloudflared.exe login` y luego crear túneles
- Para ngrok: `.\ngrok.exe config add-authtoken TU_TOKEN` y luego `.\ngrok.exe http 8766`

### Worker devuelve 502
- Verifica que las URLs de los secrets son correctas
- Verifica que los túneles estén accesibles desde internet
- Revisa los logs del Worker en Cloudflare Dashboard

## Archivos creados

```
freebuff-worker/
├── worker.js              # Worker de Cloudflare
├── wrangler.jsonc         # Configuración (con secrets declarados)
├── manifest.json          # Manifest para deploy
├── package.json           # Dependencias
├── public/index.html      # Página de bienvenida
├── TUNNEL_SETUP.md        # Instrucciones de túnel
├── SECRETS_CONFIG.md      # Configuración de secrets
├── FINAL_SETUP.md         # Esta guía
└── cloudflared.exe        # Binario de cloudflared (descargado)
    ngrok.exe              # Binario de ngrok (descargado)

tools/
├── inventor-http-bridge/
│   ├── server.py          # Puente HTTP de Inventor
│   └── run.ps1            # Script de inicio
├── revit-http-bridge/
│   ├── server.py          # Puente HTTP de Revit
│   ├── run.ps1            # Script de inicio
│   └── catalog/tools.json # Catálogo de herramientas (59 tools)
├── manage_bridges.ps1     # Gestión de puentes
├── start_revit_clean.ps1  # Iniciar Revit Bridge
├── start_inventor.ps1     # Iniciar Inventor
└── check_bridges.ps1      # Verificar estado
```
