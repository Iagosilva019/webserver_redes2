# concurrent_server.py
import socket
import hashlib
import threading
import time

HOST = ''
PORT = 80

MATRICULA = "20219015499"
NOME = "NOME_DO_ALUNO"

def compute_xcustom(matricula, nome):
    import hashlib
    return hashlib.md5(f"{matricula} {nome}".encode()).hexdigest()

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

def handle_client(conn, addr):
    start = time.time()
    try:
        data = conn.recv(8192)
        method, path, proto, headers, raw = parse_http_request(data)
        xcustom = headers.get('X-Custom-ID', None)
        if xcustom is None:
            conn.sendall(build_http_response("Missing X-Custom-ID", 400, "Bad Request"))
            return
        # simula trabalho CPU-bound/IO-bound opcional
        # time.sleep(0.01)  # se quiser testar carga
        body = f"Hello from concurrent server. You requested {path}\nX-Custom-ID={xcustom}"
        conn.sendall(build_http_response(body))
        server_time_ms = (time.time() - start) * 1000
        print(f"[CONC] {addr} {method} {path} xcustom={xcustom} serv_ms={server_time_ms:.2f}")
    except Exception as e:
        print("Handler error:", e)
    finally:
        conn.close()

def main():
    x = compute_xcustom(MATRICULA, NOME)
    print("X-Custom sample:", x)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(200)
        print("Concurrent server listening on port", PORT)
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()
