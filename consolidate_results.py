import os
import json
import pandas as pd


folder_path = "./"

# Lista para armazenar os dados
all_items = []

# Percorrer todos os arquivos JSON
for filename in os.listdir(folder_path):
    if filename.endswith(".json") and filename.startswith("results_"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
            data = json.load(file)
            search_term = filename.split("_", 2)[2].replace(".json", "").replace("_", " ")
            for item in data:
                all_items.append({
                    "Termo de busca": search_term,
                    "Título da vaga": item.get("title"),
                    "Empresa": item.get("company"),
                    "Localização": item.get("location"),
                    "Descrição": item.get("description"),
                    "Link": item.get("url")
                })


df = pd.DataFrame(all_items)


output_file = "vagas_unificadas.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Arquivo CSV gerado: {output_file} ({len(df)} linhas)")
