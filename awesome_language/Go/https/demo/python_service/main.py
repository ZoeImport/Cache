import http.server
import ssl
import threading
import ctypes
import os
import time

# --- Python 服务端部分 ---
def start_python_server():
    server_address = ('localhost', 8001)
    httpd = http.server.HTTPServer(server_address, Handler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="certs/python-server.crt",
        keyfile="certs/python-server.key"
    )
    context.load_verify_locations(cafile="certs/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("Python service listening on port 8001...")
    httpd.serve_forever()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Python service received a request from Go service.")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from Python service!")

# --- Python 客户端部分（调用 Go 动态库）---
def client_request_to_go():
    # 加载编译好的 Go 动态库
    lib_path = os.path.join(os.getcwd(), '..', 'go_client_lib', 'auth.so')
    auth_lib = ctypes.CDLL(lib_path)

    # 设置 Go 函数的返回类型
    auth_lib.MakeSecureRequest.restype = ctypes.c_char_p

    url = "https://localhost:8000"
    url_bytes = url.encode('utf-8')

    print("Python service making a request to Go service via Go dynamic library...")

    # 调用 Go 动态库中的函数
    response_ptr = auth_lib.MakeSecureRequest(url_bytes)

    # 将 C 字符串转换为 Python 字符串
    response_str = ctypes.cast(response_ptr, ctypes.c_char_p).value.decode('utf-8')

    # 释放 Go 代码中分配的内存
    # 注意：这里需要确保 Go 库中提供了 free 函数
    # 为了简化，我们忽略这一步，但在生产环境中非常重要
    auth_lib.FreeString(response_ptr)
    print(f"Python service received response from Go: {response_str}")

if __name__ == "__main__":
    # 启动 Python 服务端
    python_server_thread = threading.Thread(target=start_python_server)
    python_server_thread.daemon = True
    python_server_thread.start()

    # 稍等片刻，确保服务启动
    time.sleep(2)

    # Python 服务作为客户端调用 Go 服务
    client_request_to_go()

    # 保持主线程运行
    while True:
        time.sleep(1)