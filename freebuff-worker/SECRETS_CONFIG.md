# Configuración de Secrets para el Worker

## URLs de los puentes locales

Una vez que tengas los túneles corriendo (cloudflared/ngrok), obtendrás URLs como:

- Inventor: `https://xxxx-xxxx-xxxx.freebuff.dev`
- Revit: `https://yyyy-yyyyy-yyyy.freebuff.dev`

## Configurar los secrets

### Opción 1: Usando wrangler CLI (requiere CLOUDFLARE_API_TOKEN)

```bash
cd freebuff-worker

# Configurar URL de Inventor
wrangler secret put INVENTOR_BRIDGE_URL --value "https://tu-url-inventor.aquí"

# Configurar URL de Revit
wrangler secret put REVIT_BRIDGE_URL --value "https://tu-url-revit.aquí"
```

### Opción 2: Usando la API de Cloudflare directamente

```bash
# Obtén tu API token en https://dash.cloudflare.com/profile/api-tokens
# Scope: Workers Scripts > Edit

export CLOUDFLARE_API_TOKEN="tu_token_aquí"
export CLOUDFLARE_ACCOUNT_ID="tu_account_id_aquí"

# Obtener el ID del sitio
SITE_ID="5d9e1a2c-3b4f-4d6e-8a7c-9f0b1c2d3e4f"

# Crear secret para Inventor
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/workers/scripts/secrets" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "INVENTOR_BRIDGE_URL",
    "text": "https://tu-url-inventor.aquí",
    "lifecycle": "persistent",
    "expiration": null
  }'

# Crear secret para Revit
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/workers/scripts/secrets" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "REVIT_BRIDGE_URL",
    "text": "https://tu-url-revit.aquí",
    "lifecycle": "persistent",
    "expiration": null
  }'
```

## Verificar los secrets

```bash
# Listar secrets configurados
wrangler secret list
```

## URLs del Worker

- **Preview:** https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page
- **Production:** https://site-b416044f13a940a7a21cbf9010026939.freebuff.page

## Probar después de configurar los secrets

```bash
# Verificar que el Worker puede alcanzar los puentes
curl -X POST "https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/inventor/call" \
  -H "Content-Type: application/json" \
  -d '{"tool":"status","arguments":{}}'

curl -X POST "https://site-1cad53a1e3d3461182841f3b9520229f.freebuff.page/revit/call" \
  -H "Content-Type: application/json" \
  -d '{"tool":"revit_status","params":{}}'
```

## Actualizar los secrets (si cambian las URLs de los túneles)

```bash
wrangler secret put INVENTOR_BRIDGE_URL --value "https://nueva-url-inventor.aquí"
wrangler secret put REVIT_BRIDGE_URL --value "https://nueva-url-revit.aquí"
```

Los secrets son persistentes y no se pierden al hacer deploy nuevamente.
