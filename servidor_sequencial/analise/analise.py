# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

files = glob.glob("*.csv")
df_list = [pd.read_csv(f) for f in files]
df = pd.concat(df_list, ignore_index=True)
df['latency_ms'] = pd.to_numeric(df['latency_ms'], errors='coerce')
grouped = df.groupby('client')['latency_ms']
means = grouped.mean()
stds = grouped.std()

print("Means per client:\n", means)
print("Stds per client:\n", stds)

plt.figure()
plt.boxplot([df[df.client==c].latency_ms.dropna() for c in sorted(df.client.unique())])
plt.xlabel("Client")
plt.ylabel("Latency (ms)")
plt.title("Latency per client")
plt.savefig("boxplot_latency.png")
