import json
import matplotlib.pyplot as plt

with open("term_frequency_report.json", encoding="utf-8") as f:
    report = json.load(f)

# 2. Ordena
report_sorted = sorted(report, key=lambda x: x["match_count"], reverse=True)

# 3. Seleciona os 50 termos mais frequentes
top_n = 50
top_terms = report_sorted[:top_n]
terms = [item["term"] for item in top_terms]
counts = [item["match_count"] for item in top_terms]
jobs = [item["unique_jobs"] for item in top_terms]

# 4. Calcular o total de descrições de vagas
total_jobs = sum(jobs)

# 5. Gera gráfico
plt.figure(figsize=(14, 8))
plt.bar(terms, counts, color='skyblue')
plt.xlabel("Palavras-chave", fontsize=16)
plt.ylabel("Número de ocorrências nas vagas", fontsize=16)
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout(pad=6.0)
plt.savefig("top50_frequencia_termos.png")
