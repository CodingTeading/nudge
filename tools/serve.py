"""시안 미리보기용 정적 서버.

Windows 의 Python 은 .js 의 MIME 을 레지스트리에서 읽어 오는데, 많은 기계에서
text/plain 으로 잡혀 있어 ES 모듈 로딩이 막힙니다. 그래서 확장자 표를 직접 고정합니다.
"""
import http.server, socketserver, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
ROOT = sys.argv[2] if len(sys.argv) > 2 else 'dist'


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.js': 'text/javascript',
        '.mjs': 'text/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.html': 'text/html',
        '.svg': 'image/svg+xml',
        '.woff2': 'font/woff2',
        '.woff': 'font/woff',
    }

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        # 시안 작업 중에는 캐시가 방해만 됩니다.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def send_head(self):
        # 조건부 요청(304)도 막아 항상 새로 내려보냅니다.
        self.headers.replace_header('If-Modified-Since', '') \
            if 'If-Modified-Since' in self.headers else None
        self.headers.replace_header('If-None-Match', '') \
            if 'If-None-Match' in self.headers else None
        return super().send_head()

    def log_message(self, fmt, *args):
        pass  # 조용히


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


with Server(('127.0.0.1', PORT), Handler) as httpd:
    print(f'serving {ROOT} on http://localhost:{PORT}', flush=True)
    httpd.serve_forever()
