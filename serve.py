import http.server, urllib.request, urllib.error, os

OLLAMA = "http://localhost:11434"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = urllib.request.Request(OLLAMA + self.path, data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                data, status = r.read(), r.status
        except urllib.error.HTTPError as e:
            data, status = e.read(), e.code
        except Exception as e:
            data, status = str(e).encode(), 502
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Open http://localhost:8000/ai-tool-guide.html  (keep this window open)")
http.server.ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
