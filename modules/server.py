from http.server import BaseHTTPRequestHandler, HTTPServer
from modules.lib import log

from json import dumps, load
from os import path, chdir


class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html_resp = '<body style="background-color:#000000"></body>'
            self.wfile.write(bytes(html_resp, 'utf-8'))

        elif self.path == '/getManifest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            with open(path.join('..', 'manifest.json'), 'r', encoding='utf-8') as manifest:
                json_resp = load(manifest)

            self.wfile.write(bytes(dumps(json_resp), 'utf-8'))

        elif self.path.startswith('/packages/'):
            fn = self.path[10:]

            if path.exists(fn) and path.isfile(fn):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                with open(fn, 'r', encoding='utf-8') as file:
                    self.wfile.write(bytes(file.read(), 'utf-8'))

            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                self.wfile.write(bytes(f'File Not Found: {fn}', 'utf-8'))


def main(argv, origin):
    chdir(origin)

    if len(argv) < 3:
        log('red', 'ERROR', 'usage: python winpak.py -s [directory to host] [IP:PORT]')
        exit(1)
    else:
        if path.exists(argv[1]) and path.isdir(argv[1]):
            pass
        else:
            log('red', 'ERROR', "no such path / path isn't a directory")
            exit(1)

    log('', 'LOG', 'successful start')

    chdir(argv[1])

    ip = ''
    port = ''
    write_ip = True

    for i in argv[2]:
        if write_ip:
            if i != ':':
                ip += i
            else:
                write_ip = False
        else:
            port += i

    port = int(port)

    addr = (ip, port)

    server = HTTPServer(addr, Handler)
    log('green', 'SERVER', f'running server on {addr}')

    log('', 'LOG', 'HTTP logs')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log('', 'LOG', 'HTTP logs end')
        log('green', 'SERVER', 'closing server')
        server.server_close()
