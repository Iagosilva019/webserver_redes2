import matplotlib.pyplot as plt
import numpy as np
import csv

def ler_log_csv(caminho, coluna_tempo='latencia_ms'):
    latencias = []
    timestamps = []
    with open(caminho, 'r') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            try:
                latencias.append(float(linha[coluna_tempo]))
                timestamps.append(float(linha['timestamp']))
            except ValueError:
                continue
    return np.array(latencias), np.array(timestamps)

def calcular_estatisticas(latencias, timestamps):
    media = np.mean(latencias)
    desvio = np.std(latencias)
    total_reqs = len(timestamps)
    if len(timestamps) > 1:
        duracao = timestamps.max() - timestamps.min()
        throughput = total_reqs / duracao if duracao > 0 else 0
    else:
        throughput = 0
    return media, desvio, throughput, total_reqs

# === Carregar dados ===
seq_lat, seq_ts = ler_log_csv('log_sequencial.csv')
conc_lat, conc_ts = ler_log_csv('log_concorrente.csv')

# === Calcular estatísticas ===
m_seq, d_seq, thr_seq, total_seq = calcular_estatisticas(seq_lat, seq_ts)
m_conc, d_conc, thr_conc, total_conc = calcular_estatisticas(conc_lat, conc_ts)

# === Mostrar no terminal ===
print(f"Sequencial -> Média: {m_seq:.2f} ms | Desvio: {d_seq:.2f} | Throughput: {thr_seq:.2f} req/s | Total: {total_seq}")
print(f"Concorrente -> Média: {m_conc:.2f} ms | Desvio: {d_conc:.2f} | Throughput: {thr_conc:.2f} req/s | Total: {total_conc}")

# === Gráfico comparativo ===
labels = ['Sequencial', 'Concorrente']
x = np.arange(len(labels))
largura = 0.25

fig, ax1 = plt.subplots(figsize=(8,5))

# Barras de tempo médio
ax1.bar(x - largura, [m_seq, m_conc], width=largura, yerr=[d_seq, d_conc], capsize=8, color='#FF7F50', label='Latência média (ms)')
ax1.set_ylabel('Latência média (ms)')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.set_title('Desempenho: Sequencial vs Concorrente')

# Barras de throughput
ax2 = ax1.twinx()
ax2.bar(x, [thr_seq, thr_conc], width=largura, color='#87CEFA', label='Throughput (req/s)')
ax2.set_ylabel('Throughput (req/s)')

# Barras de total de requisições
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # desloca eixo
ax3.bar(x + largura, [total_seq, total_conc], width=largura, color='#90EE90', label='Total de requisições')
ax3.set_ylabel('Total de requisições')

# Legenda combinada
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(handles1 + handles2 + handles3, labels1 + labels2 + labels3, loc='upper left')

plt.tight_layout()
plt.savefig('comparacao_servidores_completo.png')
plt.show()
