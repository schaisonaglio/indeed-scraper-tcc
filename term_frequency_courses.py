import json
import pandas as pd
import matplotlib.pyplot as plt

# ═════ CONFIGURAÇÃO ════════════════════════════════════════════════════════
json_path        = "term_frequency_report.json"
excel_path       = "CHA_apos_normalizacao_opt.xlsx"
sheet_name       = 0    # 1ª aba (ou pelo nome, se preferir)
top_n_terms      = 50   # termos de maior frequência considerados
top_n_disciplinas = 20  # nº de barras exibidas no gráfico

# ═════ Passo 1 · Carrega o relatório de frequência de termos ════════════════
with open(json_path, encoding="utf-8") as f:
    report = json.load(f)

freq_df = pd.DataFrame(report)
freq_df["term"] = freq_df["term"].str.lower()

if top_n_terms:
    freq_df = freq_df.nlargest(top_n_terms, "match_count")

# ═════ Passo 2 · Carrega a planilha ═══════════════════
cha_df = pd.read_excel(excel_path, sheet_name=sheet_name)

records = []
for _, row in cha_df.iterrows():
    disciplina = row["Disciplina"]
    raw_kw     = row["Palavras-chave"]
    if pd.notna(raw_kw):
        for kw in map(str.strip, raw_kw.lower().split(",")):
            if kw:
                records.append({"keyword": kw, "disciplina": disciplina})

keywords_df = pd.DataFrame(records)

# ═════ Passo 3 · Junta frequências e palavras-chave ═════════════════════════
merged = pd.merge(freq_df,
                  keywords_df,
                  left_on="term",
                  right_on="keyword",
                  how="inner")  # apenas termos que aparecem na planilha

# ═════ Passo 4 · Soma ocorrências por disciplina ════════════════════════════
disc_summary = (merged.groupby("disciplina")["match_count"]
                .sum()
                .reset_index()
                .sort_values("match_count", ascending=False))

# ═════ Passo 5 · Gera o gráfico ═════════════════════════════════════════════
if top_n_disciplinas:
    disc_summary = disc_summary.head(top_n_disciplinas)

plt.figure(figsize=(12, 8))
plt.barh(disc_summary["disciplina"],
         disc_summary["match_count"],
         color="#6baed6",
         edgecolor="#6baed6")
plt.gca().invert_yaxis()
plt.xlabel("Ocorrências das palavras-chave", fontsize=12)
plt.ylabel("Disciplina optativa", fontsize=12)
plt.tight_layout(pad=3)
plt.savefig("ocorrencias_por_disciplina_optativas.png", dpi=300)
plt.close()

print("Gráfico salvo em 'ocorrencias_por_disciplina_optativas.png'")
