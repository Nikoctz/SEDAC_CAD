"""
Puente HTTP para el servidor MCP de Revit.
Expone las herramientas del servidor MCP vía HTTP para que puedan ser
accedidas remotamente (p.ej., desde un Worker de Cloudflare/Freebuff).

NOTA: Este puente se conecta al complemento RevitMcpBridge vía TCP local,
no reinventa la comunicación. Solo añade una capa HTTP sobre el protocolo
existente del complemento.
"""
import argparse
import json
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
import asyncio
import socket
import struct

# Configuración por defecto
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8767

# Variables de entorno del puente Revit (heredadas del servidor MCP original)
REVIT_EXE = Path(os.environ.get("REVIT_EXE", r"C:\Program Files\Autodesk\Revit 2027\Revit.exe"))
BRIDGE_HOST = os.environ.get("REVIT_MCP_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.environ.get("REVIT_MCP_PORT", "8765"))
BRIDGE_TIMEOUT = float(os.environ.get("REVIT_MCP_TIMEOUT", "600"))
ALLOW_WRITES = os.environ.get("REVIT_MCP_ALLOW_WRITES", "0") == "1"

# Directorio del puente (para catálogo cacheado)
HERE = Path(__file__).resolve().parent
CATALOG_FILE = HERE / "catalog" / "tools.json"


def log(*args: Any) -> None:
    """Diagnóstico a stderr."""
    print(*args, file=sys.stderr, flush=True)


class BridgeError(Exception):
    """Error hablando con el complemento de Revit."""


class RevitBridge:
    """Cliente TCP del complemento dentro de Revit, con catálogo local."""
    
    def __init__(self, host: str = BRIDGE_HOST, port: int = BRIDGE_PORT, 
                 timeout: float = BRIDGE_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: socket.socket | None = None
        self._lock = threading.RLock()
        self._tools_cache: list[dict[str, Any]] | None = None
    
    def _connect(self) -> socket.socket:
        if self._sock is not None:
            return self._sock
        try:
            s = socket.create_connection((self.host, self.port), timeout=10)
            s.settimeout(self.timeout)
            self._sock = s
            return s
        except OSError as exc:
            self._sock = None
            raise BridgeError(
                f"No se pudo conectar con el puente de Revit en {self.host}:{self.port} ({exc}). "
                "Abre Revit (el complemento se carga solo) o usa la herramienta 'revit_launch'."
            ) from exc
    
    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
    
    @staticmethod
    def _send(sock: socket.socket, payload: bytes) -> None:
        sock.sendall(struct.pack(">I", len(payload)) + payload)
    
    @staticmethod
    def _recv(sock: socket.socket) -> bytes:
        header = b""
        while len(header) < 4:
            chunk = sock.recv(4 - len(header))
            if not chunk:
                raise BridgeError("El puente de Revit cerró la conexión inesperadamente.")
            header += chunk
        (length,) = struct.unpack(">I", header)
        if length < 1 or length > 16 * 1024 * 1024:
            raise BridgeError("Longitud de respuesta fuera de límite.")
        body = b""
        while len(body) < length:
            chunk = sock.recv(min(65536, length - len(body)))
            if not chunk:
                raise BridgeError("El puente de Revit cerró la conexión inesperadamente.")
            body += chunk
        return body
    
    def call(self, tool: str, params: dict[str, Any] | None = None) -> Any:
        """Ejecuta una herramienta en Revit y devuelve el resultado."""
        # Validar permisos
        if tool not in ("revit_status", "revit_list_tools", "revit_list_levels", 
                        "revit_list_categories", "revit_list_materials", "revit_list_mep_types",
                        "revit_list_families", "revit_list_views", "revit_list_types",
                        "revit_list_mep_systems", "revit_list_fill_types", "revit_get_rooms",
                        "revit_model_statistics", "revit_energy_summary", "revit_envelope_analysis",
                        "revit_material_audit", "revit_assembly_thermal_report"):
            # Herramientas de escritura requieren ALLOW_WRITES
            if not ALLOW_WRITES:
                raise BridgeError(f"Escritura no permitida. Establece REVIT_MCP_ALLOW_WRITES=1")
        
        with self._lock:
            return self._call_once(tool, params)
    
    def _call_once(self, tool: str, params: dict[str, Any] | None) -> Any:
        request = {"tool": tool, "params": params or {}}
        
        # Token de sesión si existe
        token_file = Path(os.environ.get("LOCALAPPDATA", "")) / "RevitMcpBridge" / "session.token"
        if token_file.exists():
            request["token"] = token_file.read_text(encoding="utf-8").strip()
        
        payload = json.dumps(request, ensure_ascii=False).encode("utf-8")
        sock = self._connect()
        try:
            self._send(sock, payload)
            raw = self._recv(sock)
        except (OSError, BridgeError) as exc:
            self.close()
            raise BridgeError(
                "Conexión interrumpida. Resultado desconocido; no se reintenta la operación. "
                "Consulta el modelo antes de repetirla."
            ) from exc
        
        try:
            response = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise BridgeError(f"Respuesta no válida del puente de Revit: {exc}") from exc
        
        if not response.get("ok"):
            raise BridgeError((response.get("error") or "Error desconocido en el puente de Revit.").split(" | ", 1)[0])
        
        # Validar revisión del complemento para herramientas térmicas
        if tool in ("revit_assembly_thermal_report", "revit_energy_summary", "revit_envelope_analysis"):
            if response.get("bridge_revision") != "1.1.0-review":
                raise BridgeError("Revit sigue usando el complemento anterior. Reinicia Revit manualmente y carga la revisión; no se utilizan sus cálculos térmicos antiguos.")
        
        return response.get("result")
    
    def ping(self) -> bool:
        try:
            self.call("revit_status", {})
            return True
        except BridgeError:
            return False
    
    def get_tools_list(self) -> list[dict[str, Any]]:
        """Lista las herramientas disponibles (del catálogo cacheado o del complemento)."""
        if self._tools_cache is None:
            # Intentar cargar del catálogo local
            if CATALOG_FILE.exists():
                try:
                    data = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
                    tools = data.get("tools") if isinstance(data, dict) else data
                    if tools:
                        self._tools_cache = tools
                        return tools
                except json.JSONDecodeError:
                    log(f"[RevitBridge] Catálogo cacheado ilegible: {CATALOG_FILE}")
            
            # Si no hay catálogo, intentar obtenerlo del complemento
            try:
                result = self.call("revit_list_tools", {})
                if isinstance(result, dict) and result.get("tools"):
                    self._tools_cache = result["tools"]
                    return self._tools_cache
            except BridgeError:
                pass
            
            # Fallback: devolver catálogo básico desde el archivo
            if CATALOG_FILE.exists():
                try:
                    data = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
                    tools = data.get("tools") if isinstance(data, dict) else data
                    if tools:
                        self._tools_cache = tools
                        return tools
                except json.JSONDecodeError:
                    pass
            
            return []
    
    def clear_tools_cache(self) -> None:
        """Invalida la caché de herramientas."""
        self._tools_cache = None


# Instancia global del puente
bridge: RevitBridge | None = None
bridge_ready = threading.Event()


class HTTPHandler(BaseHTTPRequestHandler):
    """Manejador HTTP para el puente de Revit."""
    
    server_version = "RevitBridge/1.0"
    
    def log_message(self, format, *args):
        print(f"[RevitBridge] {args[0]}", file=sys.stderr, flush=True)
    
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
            status = "ok" if bridge and bridge.ping() else "unhealthy"
            self._send_json({
                "status": status,
                "bridge_connected": bridge.ping() if bridge else False,
                "tools_count": len(bridge.get_tools_list()) if bridge else 0,
                "allow_writes": ALLOW_WRITES,
            })
        elif self.path == "/tools":
            if bridge:
                self._send_json({"tools": bridge.get_tools_list()})
            else:
                self._send_json({"error": "Puente no inicializado"}, 503)
        elif self.path == "/":
            self._send_json({
                "name": "revit-bridge",
                "description": "Puente HTTP para el servidor MCP de Revit",
                "version": "1.0.0",
                "endpoints": {
                    "GET /health": "Estado del puente y conexión a Revit",
                    "GET /tools": "Lista de herramientas disponibles",
                    "POST /call": "Ejecutar una herramienta",
                },
                "bridge": {
                    "host": BRIDGE_HOST,
                    "port": BRIDGE_PORT,
                    "allow_writes": ALLOW_WRITES,
                }
            })
        elif self.path.startswith("/tools/"):
            # GET /tools/{tool_name} para obtener esquema de una herramienta
            tool_name = self.path.split("/")[-1]
            if bridge:
                tools = bridge.get_tools_list()
                for t in tools:
                    if t.get("name") == tool_name:
                        self._send_json(t)
                        return
                self._send_json({"error": f"Herramienta '{tool_name}' no encontrada"}, 404)
            else:
                self._send_json({"error": "Puente no inicializado"}, 503)
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
                params = request.get("params", {})
                
                if not tool_name:
                    self._send_json({"error": "Parámetro 'tool' requerido"}, 400)
                    return
                
                # Ejecutar la herramienta
                result = bridge.call(tool_name, params)
                
                # Normalizar respuesta
                response = {
                    "ok": True,
                    "result": result,
                }
                
                # Añadir metadatos de revisión para herramientas térmicas
                if tool_name in ("revit_assembly_thermal_report", "revit_energy_summary", 
                                 "revit_envelope_analysis"):
                    response["bridge_revision"] = "1.1.0-review"
                
                self._send_json(response)
                
            except BridgeError as e:
                self._send_json({"ok": False, "error": str(e)}, 400)
            except json.JSONDecodeError as e:
                self._send_json({"error": f"JSON inválido: {e}"}, 400)
            except Exception as e:
                log(f"[RevitBridge] Error inesperado: {e}")
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "Endpoint no encontrado"}, 404)


def run_server(host: str, port: int):
    """Inicia el servidor HTTP del puente."""
    global bridge
    bridge = RevitBridge(host=BRIDGE_HOST, port=BRIDGE_PORT, timeout=BRIDGE_TIMEOUT)
    
    server = HTTPServer((host, port), HTTPHandler)
    print(f"[RevitBridge] Escuchando en http://{host}:{port}", file=sys.stderr, flush=True)
    print(f"[RevitBridge] Conectando al puente RevitMcpBridge en {BRIDGE_HOST}:{BRIDGE_PORT}...", 
          file=sys.stderr, flush=True)
    
    # Probar conexión
    if bridge.ping():
        print(f"[RevitBridge] ✓ Conectado a Revit", file=sys.stderr, flush=True)
        bridge_ready.set()
    else:
        print(f"[RevitBridge] ✗ No se pudo conectar a Revit. Asegúrate de que Revit está abierto "
              f"con el complemento cargado.", file=sys.stderr, flush=True)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[RevitBridge] Deteniendo servidor...", file=sys.stderr, flush=True)
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Puente HTTP para el servidor MCP de Revit")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Puerto (default: {DEFAULT_PORT})")
    parser.add_argument("--bridge-host", default=BRIDGE_HOST, help="Host del puente RevitMcpBridge")
    parser.add_argument("--bridge-port", type=int, default=BRIDGE_PORT, help="Puerto del puente RevitMcpBridge")
    args = parser.parse_args()
    
    # Sobrescribir variables de entorno si se pasaron por CLI
    if args.bridge_host != BRIDGE_HOST:
        os.environ["REVIT_MCP_HOST"] = args.bridge_host
    if args.bridge_port != BRIDGE_PORT:
        os.environ["REVIT_MCP_PORT"] = str(args.bridge_port)
    
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
