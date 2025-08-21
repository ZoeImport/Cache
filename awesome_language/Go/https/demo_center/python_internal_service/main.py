import http.server
import ssl


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from the Python internal service!")
        print("Python 内部服务：收到来自认证中心的请求。")


def start_python_server():
    server_address = ('localhost', 8001)
    httpd = http.server.HTTPServer(server_address, MyHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="../certs/python-internal.crt", keyfile="../certs/python-internal.key")
    context.load_verify_locations(cafile="../certs/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("Python 内部服务正在监听 :8001...")
    httpd.serve_forever()


if __name__ == "__main__":
    start_python_server()
