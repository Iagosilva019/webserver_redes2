# sync_server.py
import socket
import hashlib
import threading
import time

HOST = ''  # escuta em todas as interfaces
PORT = 80

MATRICULA = "20219015499"
NOME = "NOME_DO_ALUNO"

def compute_xcustom(matricula, nome):
    s = f"{matricula} {nome}".encode('utf-8')
    return hashlib.md5(s).hexdigest()

def parse_http_request(data):
    try:
        text = data.decode('utf-8', errors='ignore')
        lines = text.split('\r\n')
        request_line = lines[0]
        method, path, proto = request_line.split()
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            if ':' in lines[i]:
                k, v = lines[i].split(':', 1)
                headers[k.strip()] = v.strip()
            i += 1
        return method, path, proto, headers, text
    except Exception as e:
        return None, None, None, {}, ''

def build_http_response(body, status_code=200, status_text='OK'):
    resp = f"HTTP/1.1 {status_code} {status_text}\r\n"
    resp += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
    resp += "Content-Type: text/plain; charset=utf-8\r\n"
    resp += "\r\n"
    resp += body
    return resp.encode('utf-8')

def handle_connection(conn, addr):
    start = time.time()
    data = conn.recv(8192)
    method, path, proto, headers, raw = parse_http_request(data)
    xcustom = headers.get('X-Custom-ID', None)
    # validação mínima
    if xcustom is None:
        body = "Missing X-Custom-ID"
        conn.sendall(build_http_response(body, 400, "Bad Request"))
        conn.close()
        return
    # exemplo de resposta
    body = f"Hello from sequential server. You requested {path}\nX-Custom-ID={xcustom}"
    conn.sendall(build_http_response(body))
    server_time_ms = (time.time() - start) * 1000
    # log simples
    print(f"[SYNC] {addr} {method} {path} xcustom={xcustom} serv_ms={server_time_ms:.2f}")
    conn.close()

def main():
    x = compute_xcustom(MATRICULA, NOME)
    print("X-Custom sample:", x)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print("Sequential server listening on port", PORT)
        while True:
            conn, addr = s.accept()  # bloqueante; aceita uma conexão por vez
            handle_connection(conn, addr)

if __name__ == "__main__":
    main()
