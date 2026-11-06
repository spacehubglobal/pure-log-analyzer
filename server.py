"""Local web server for the log analyzer. Standard library only.

Run:  python server.py [port]
"""
import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from analyzer import analyze

ROOT = Path(__file__).parent
MAX_UPLOAD = 200 * 1024 * 1024  # 200 MB


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, (ROOT / "index.html").read_text(encoding="utf-8"), "text/html")
        elif self.path == "/sample":
            data = (ROOT / "sample_logs" / "This_Is_A_Sample.log").read_bytes()
            self._send(200, json.dumps(analyze(data)))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/analyze":
            return self._send(404, json.dumps({"error": "not found"}))
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > MAX_UPLOAD:
            return self._send(413, json.dumps({"error": "File empty or larger than 200 MB"}))
        try:
            self._send(200, json.dumps(analyze(self.rfile.read(length))))
        except Exception as exc:  # keep the server alive on bad input
            self._send(500, json.dumps({"error": str(exc)}))

    def log_message(self, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    for p in range(port, port + 20):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            break
        except OSError:
            continue
    else:
        sys.exit("No free port found.")
    url = f"http://127.0.0.1:{p}"
    print(f"Semantic Log Analyzer running at {url}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
