import threading, csv, time, subprocess, os
import sys
import socket
import time
import hashlib



IP_SERVIDOR = sys.argv[1] if len(sys.argv) > 1 else "89.34.0.3"
PORTA = 80
MATRICULA = "20219015499"
NOME = "Iago da Silva Santana Sousa"


def gerar_xcustom(matricula, nome):
    return hashlib.md5(f"{matricula} {nome}".encode()).hexdigest()


def enviar_requisicao(path="/", method="GET", body=""):
    xcustom = gerar_xcustom(MATRICULA, NOME)
    req = f"{method} {path} HTTP/1.1\r\nHost: example\r\nX-Custom-ID: {xcustom}\r\nContent-Length: {len(body.encode())}\r\n\r\n{body}>"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    t0 = time.time()
    try:
        s.connect((IP_SERVIDOR, PORTA))
        s.sendall(req.encode())
        data = s.recv(65536)
        t1 = time.time()
        latency_ms = (t1 - t0) * 1000
        # status code parse simples
        first_line = data.split(b'\r\n',1)[0].decode('utf-8', errors='ignore')
        status = first_line.split()[1] if len(first_line.split())>=2 else "000"
        return latency_ms, int(status), data.decode('utf-8', errors='ignore')
    except Exception as e:
        return None, None, str(e)
    finally:
        s.close()



def trabalhador(id, server_ip, count, out_list):
    for i in range(count):
        t, st, _ = enviar_requisicao("/", "GET")
        out_list.append((id, i, t if t is not None else -1, st if st is not None else 0, time.time()))


def executar_teste(ip_servidor, clientes=5, reqs_per_client=20, out_csv=''):
    threads = []
    results = []
    for i in range(clients):
        t = threading.Thread(target=trabalhador, args=(i, server_ip, reqs_per_client, results))
        threads.append(t)
    t0 = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    t1 = time.time()
    dur = t1 - t0
    with open(out_csv, 'w', newline='') as f:
        cw = csv.writer(f)
        cw.writerow(["client","req_id","latency_ms","status","ts"])
        for r in results:
            cw.writerow(r)
    print("Run finished, duration:", dur, "seconds, total requests:", len(results))
    return out_csv

if __name__ == "__main__":
    ip_servidor = IP_SERVIDOR
    # Identifica o nome do log com base no IP
    if ip_servidor.endswith(".2"):
        nome_arquivo = "log_sequencial.csv"
    elif ip_servidor.endswith(".3"):
        nome_arquivo = "log_concorrente.csv"
    else:
        nome_arquivo = f"out_{server_ip.replace('.', '_')}.csv"
        executar_teste(ip_servidor, clientes=50, reqs_per_client=50, out_csv=out_file)
