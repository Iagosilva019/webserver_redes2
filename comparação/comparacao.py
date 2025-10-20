import matplotlib.pyplot as plt
import numpy as np
import csv

def ler_log_csv(caminho, coluna_tempo='latency_ms'):
    valores = []
    with open(caminho, 'r') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            try:
                valores.append(float(linha[coluna_tempo]))
            except ValueError:
                continue  # ignora linhas inválidas
    return np.array(valores)

# === Carregar dados dos logs ===
sequencial = ler_log_csv('log_sequencial.log')
concorrente = ler_log_csv('log_concorrente.log')

# === Cálculos estatísticos ===
medias = [np.mean(sequencial), np.mean(concorrente)]
desvios = [np.std(sequencial), np.std(concorrente)]

# === Mostrar no terminal ===
print(f"Sequencial -> Média: {medias[0]:.2f} ms | Desvio padrão: {desvios[0]:.2f}")
print(f"Concorrente -> Média: {medias[1]:.2f} ms | Desvio padrão: {desvios[1]:.2f}")

# === Gráfico comparativo ===
labels = ['Sequencial', 'Concorrente']
x = np.arange(len(labels))

fig, ax = plt.subplots()
ax.bar(x, medias, yerr=desvios, capsize=10, color=['#FF7F50', '#87CEFA'])
ax.set_ylabel('Tempo médio de resposta (ms)')
ax.set_title('Comparação de Desempenho: Sequencial vs Concorrente')
ax.set_xticks(x)
ax.set_xticklabels(labels)

plt.tight_layout()
plt.savefig('comparacao_servidores.png')
plt.show()
