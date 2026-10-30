"""
Puente HTTP para el servidor MCP de Inventor avanzado.
Expone las herramientas del servidor MCP vía HTTP para que puedan ser
accedidas remotamente (p.ej., desde un Worker de Cloudflare/Freebuff).
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from datetime import timedelta

# Configuración por defecto
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8766

# Ruta al servidor MCP de Inventor
INVENTOR_SERVER_DIR = Path(os.environ.get(
    "INVENTOR_MCP_DIR",
    r"C:\Users\nicol\MCP\Inventor_Avanzado_20261029"
))
INVENTOR_SERVER_SCRIPT = INVENTOR_SERVER_DIR / "inventor_mcp_server" / "server.py"

# Variables de entorno para el servidor MCP
INVENTOR_ENV = {
    "TEMP": os.environ.get("TEMP", r"C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"),
    "TMP": os.environ.get("TMP", r"C:\Users\nicol\MCP\Inventor_Avanzado_20261029\scratch"),
    "PYTHONUTF8": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "INVENTOR_MCP_CALL_TIMEOUT": os.environ.get("INVENTOR_MCP_CALL_TIMEOUT", "50"),
    "INVENTOR_MCP_STARTUP": os.environ.get("INVENTOR_MCP_STARTUP", 
        str(INVENTOR_SERVER_DIR / "startup-disabled.py")),
}


class InventorBridge:
    """Gestiona la sesión MCP con el servidor de Inventor."""
    
    def __init__(self, server_dir: Path, env: dict[str, str]):
        self.server_dir = server_dir
        self.env = env
        self.session: ClientSession | None = None
        self.tools: dict[str, Any] = {}
        self._lock = threading.Lock()
        self._connected = False
    
    async def connect(self) -> None:
        """Conecta al servidor MCP de Inventor."""
        params = StdioServerParameters(
            command=sys.executable,
            args=["-B", str(self.server_dir / "inventor_mcp_server" / "server.py")],
            cwd=str(self.server_dir.parent),
            env=self.env,
        )
        async with stdio_client(params, read_timeout_seconds=timedelta(seconds=150)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                self.tools = {tool.name: tool for tool in tools.tools}
                self.session = session
                self._connected = True
    
    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Ejecuta una herramienta del servidor MCP."""
        if not self.session:
            raise RuntimeError("No conectado al servidor MCP")
        
        result = await self.session.call_tool(tool_name, arguments)
        
        # Procesar resultado
        content = []
        for block in result.content:
            if getattr(block, "type", "") == "text":
                content.append({"type": "text", "text": block.text})
            elif getattr(block, "type", "") == "image":
                # Convertir imagen a base64 para HTTP
                import base64
                img_b64 = base64.b64encode(block.data).decode("ascii")
                content.append({
                    "type": "image",
                    "data": img_b64,
                    "media_type": block.mimeType or "image/png"
                })
        
        return {
            "content": content,
            "isError": result.isError,
        }
    
    def get_tools_list(self) -> list[dict[str, Any]]:
        """Devuelve la lista de herramientas disponibles."""
        return [
            {
                "name": name,
                "description": tool.description,
                "inputSchema": tool.inputSchema,
            }
            for name, tool in self.tools.items()
        ]


# Instancia global del puente
bridge: InventorBridge | None = None
bridge_ready = threading.Event()


def get_python() -> str:
    """Devuelve la ruta a Python."""
    return sys.executable


class HTTPHandler(BaseHTTPRequestHandler):
    """Manejador HTTP para el puente de Inventor."""
    
    server_version = "InventorBridge/1.0"
    
    def log_message(self, format, *args):
        # Log a stderr para diagnóstico
        print(f"[InventorBridge] {args[0]}", file=sys.stderr, flush=True)
    
    def _send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        """Endpoints GET."""
        if self.path == "/health":
            self._send_json({
                "status": "ok",
                "connected": bridge._connected if bridge else False,
                "tools_count": len(bridge.tools) if bridge else 0,
            })
        elif self.path == "/tools":
            if bridge:
                self._send_json({"tools": bridge.get_tools_list()})
            else:
                self._send_json({"error": "Puente no inicializado"}, 503)
        elif self.path == "/":
            self._send_json({
                "name": "inventor-bridge",
                "description": "Puente HTTP para el servidor MCP de Inventor avanzado",
                "version": "1.0.0",
                "endpoints": {
                    "GET /health": "Estado del puente",
                    "GET /tools": "Lista de herramientas disponibles",
                    "POST /call": "Ejecutar una herramienta",
                }
            })
        else:
            self._send_json({"error": "No encontrado"}, 404)
    
    def do_POST(self):
        """Endpoints POST."""
        if self.path == "/call":
            if not bridge:
                self._send_json({"error": "Puente no inicializado"}, 503)
                return
            
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                request = json.loads(body.decode("utf-8"))
                
                tool_name = request.get("tool")
                arguments = request.get("arguments", {})
                
                if not tool_name:
                    self._send_json({"error": "Parámetro 'tool' requerido"}, 400)
                    return
                
                if tool_name not in bridge.tools:
                    self._send_json({
                        "error": f"Herramienta '{tool_name}' no encontrada",
                        "available_tools": list(bridge.tools.keys())
                    }, 404)
                    return
                
                # Ejecutar la herramienta en un hilo async
                async def run_call():
                    return await bridge.call_tool(tool_name, arguments)
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(run_call())
                finally:
                    loop.close()
                
                self._send_json(result)
                
            except json.JSONDecodeError as e:
                self._send_json({"error": f"JSON inválido: {e}"}, 400)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "Endpoint no encontrado"}, 404)


def run_server(host: str, port: int, server_dir: Path, env: dict[str, str]):
    """Inicia el servidor HTTP del puente."""
    global bridge
    bridge = InventorBridge(server_dir, env)
    
    # Conectar al servidor MCP en un hilo de fondo
    async def connect_async():
        await bridge.connect()
        bridge_ready.set()
    
    thread = threading.Thread(target=lambda: asyncio.run(connect_async()), daemon=True)
    thread.start()
    
    server = HTTPServer((host, port), HTTPHandler)
    print(f"[InventorBridge] Escuchando en http://{host}:{port}", file=sys.stderr, flush=True)
    print(f"[InventorBridge] Conectando al servidor MCP de Inventor...", file=sys.stderr, flush=True)
    
    # Esperar a que el puente esté listo (con timeout)
    if not bridge_ready.wait(timeout=30):
        print("[InventorBridge] ADVERTENCIA: No se pudo conectar al servidor MCP en 30s", 
              file=sys.stderr, flush=True)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[InventorBridge] Deteniendo servidor...", file=sys.stderr, flush=True)
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Puente HTTP para el servidor MCP de Inventor avanzado")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Puerto (default: {DEFAULT_PORT})")
    parser.add_argument("--server-dir", type=Path, 
                        default=INVENTOR_SERVER_DIR,
                        help="Directorio del servidor MCP de Inventor")
    args = parser.parse_args()
    
    # Validar que existe el servidor MCP
    if not args.server_dir.exists():
        print(f"Error: Directorio del servidor MCP no existe: {args.server_dir}", file=sys.stderr)
        sys.exit(1)
    
    if not args.server_dir.joinpath("inventor_mcp_server", "server.py").exists():
        print(f"Error: Servidor MCP no encontrado en {args.server_dir / 'inventor_mcp_server' / 'server.py'}", 
              file=sys.stderr)
        sys.exit(1)
    
    run_server(args.host, args.port, args.server_dir, INVENTOR_ENV)


if __name__ == "__main__":
    main()
