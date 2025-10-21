import threading, csv, time, subprocess, os
import sys
import socket
import time
import hashlib

# Configurações iniciais
IP_SERVIDOR = sys.argv[1] if len(sys.argv) > 1 else "89.34.0.3"
PORTA = 80
MATRICULA = "20219015499"
NOME = "Iago da Silva Santana Sousa"

# Função para gerar o cabeçalho X-Custom-ID
def gerar_xcustom(matricula, nome):
    return hashlib.md5(f"{matricula} {nome}".encode()).hexdigest()

# Enviar requisição HTTP
def enviar_requisicao(caminho="/", metodo="GET", corpo=""):
    xcustom = gerar_xcustom(MATRICULA, NOME)
    requisicao = (
        f"{metodo} {caminho} HTTP/1.1\r\n"
        f"Host: exemplo\r\n"
        f"X-Custom-ID: {xcustom}\r\n"
        f"Content-Length: {len(corpo.encode())}\r\n\r\n{corpo}>"
    )

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    t0 = time.time()
    try:
        s.connect((IP_SERVIDOR, PORTA))
        s.sendall(requisicao.encode())
        resposta = s.recv(65536)
        t1 = time.time()
        latencia_ms = (t1 - t0) * 1000

        # Captura o código de status da resposta
        primeira_linha = resposta.split(b'\r\n', 1)[0].decode('utf-8', errors='ignore')
        partes = primeira_linha.split()
        status = partes[1] if len(partes) >= 2 else "000"

        return latencia_ms, int(status), resposta.decode('utf-8', errors='ignore')
    except Exception as e:
        return None, None, str(e)
    finally:
        s.close()

# Função executada por cada thread (cliente)
def trabalhador(id_cliente, ip_servidor, qtd_requisicoes, resultados):
    for i in range(qtd_requisicoes):
        tempo, status, _ = enviar_requisicao("/", "GET")
        resultados.append((
            id_cliente,
            i,
            tempo if tempo is not None else -1,
            status if status is not None else 0,
            time.time()
        ))

# Executar o teste completo
def executar_teste(ip_servidor, clientes=5, reqs_por_cliente=20, nome_csv=''):
    threads = []
    resultados = []

    # Cria as threads (clientes)
    for i in range(clientes):
        t = threading.Thread(target=trabalhador, args=(i, ip_servidor, reqs_por_cliente, resultados))
        threads.append(t)

    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t1 = time.time()

    duracao = t1 - t0

    # Salva os resultados em CSV
    with open(nome_csv, 'w', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(["cliente", "id_requisicao", "latencia_ms", "status", "timestamp"])
        for r in resultados:
            escritor.writerow(r)

    print(f"Teste concluído. Duração: {duracao:.2f} segundos | Total de requisições: {len(resultados)}")
    return nome_csv


if __name__ == "__main__":
    ip_servidor = IP_SERVIDOR

    # Define o nome do arquivo de log com base no IP
    if ip_servidor.endswith(".2"):
        nome_arquivo = "log_sequencial.csv"
    elif ip_servidor.endswith(".3"):
        nome_arquivo = "log_concorrente.csv"
    else:
        nome_arquivo = f"log_{ip_servidor.replace('.', '_')}.csv"

    # Executa o teste com o IP fornecido
    executar_teste(ip_servidor, clientes=5, reqs_por_cliente=20, nome_csv=nome_arquivo)
