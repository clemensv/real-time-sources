"""Local dev server for antwerp-waterbus.html with az CLI token proxy."""
import http.server, json, os, subprocess, sys

RESOURCE = os.environ.get("KQL_CLUSTER", "")
if not RESOURCE:
    print("ERROR: Set KQL_CLUSTER env var to the Fabric Eventhouse query URI.")
    sys.exit(1)
PORT = 8765

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/token":
            try:
                r = subprocess.run(
                    ["az", "account", "get-access-token", "--resource", RESOURCE, "-o", "json"],
                    capture_output=True, text=True, timeout=30,
                )
                if r.returncode != 0:
                    self.send_error(500, r.stderr[:200])
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(r.stdout.encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        if "/token" in str(args):
            sys.stderr.write(f"[token] {args[0]}\n")

print(f"Serving on http://localhost:{PORT}")
print(f"Open http://localhost:{PORT}/antwerp-waterbus.html")
http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
