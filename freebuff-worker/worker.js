// SEDAC CAD MCP Bridge - Worker de Cloudflare
// Reenvía peticiones a los puentes HTTP locales de Inventor y Revit
// Expuestos vía túnel (cloudflared/ngrok) en el PC del usuario

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Rutas de salud
    if (url.pathname === '/health' || url.pathname === '/') {
      return new Response(JSON.stringify({
        status: 'ok',
        service: 'SEDAC CAD MCP Bridge',
        version: '1.0.0',
        endpoints: {
          'POST /inventor/call': 'Ejecutar herramienta de Inventor',
          'POST /revit/call': 'Ejecutar herramienta de Revit',
          'GET /inventor/tools': 'Listar herramientas de Inventor',
          'GET /revit/tools': 'Listar herramientas de Revit',
          'GET /health': 'Estado del puente'
        }
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Listar herramientas de Inventor
    if (url.pathname === '/inventor/tools' && request.method === 'GET') {
      return forwardRequest(env.INVENTOR_BRIDGE_URL + '/tools', request);
    }
    
    // Listar herramientas de Revit
    if (url.pathname === '/revit/tools' && request.method === 'GET') {
      return forwardRequest(env.REVIT_BRIDGE_URL + '/tools', request);
    }
    
    // Llamar a Inventor
    if (url.pathname === '/inventor/call' && request.method === 'POST') {
      return forwardRequest(env.INVENTOR_BRIDGE_URL + '/call', request);
    }
    
    // Llamar a Revit
    if (url.pathname === '/revit/call' && request.method === 'POST') {
      return forwardRequest(env.REVIT_BRIDGE_URL + '/call', request);
    }
    
    // Ruta no encontrada
    return new Response(JSON.stringify({
      error: 'Endpoint no encontrado',
      available: [
        'GET /health',
        'GET /inventor/tools',
        'GET /revit/tools',
        'POST /inventor/call',
        'POST /revit/call'
      ]
    }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

/**
 * Reenvía la petición al puente local
 */
async function forwardRequest(upstreamUrl, request) {
  try {
    const method = request.method;
    const headers = {};
    request.headers.forEach((value, key) => {
      if (key !== 'host') {
        headers[key] = value;
      }
    });
    
    let body;
    if (request.body) {
      body = request.body;
    }
    
    const init = {
      method,
      headers,
      body: body || undefined
    };
    
    const response = await fetch(upstreamUrl, init);
    
    // Leer la respuesta del upstream
    const contentType = response.headers.get('content-type') || 'application/json';
    const responseBody = await response.arrayBuffer();
    
    return new Response(responseBody, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });
  } catch (error) {
    console.error('Error forwarding request:', error);
    return new Response(JSON.stringify({
      error: 'Error conectando al puente local',
      details: error.message
    }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
