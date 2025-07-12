import pandas as pd
import re

df = pd.read_excel("Objetivos_UCs.xlsx")

# Classificacao CHA
def classificar_cha(frase):
    frase = frase.lower()
    if any(kw in frase for kw in ["compreender", "conhecer", "entender", "estudar", "analisar", "identificar"]):
        return "C"
    elif any(kw in frase for kw in ["aplicar", "usar", "utilizar", "projetar", "resolver", "desenvolver", "implementar", "programar", "calcular", "montar"]):
        return "H"
    elif any(kw in frase for kw in ["demonstrar", "atuar", "posicionar", "cooperar", "valorizar", "respeitar", "trabalhar"]):
        return "A"
    else:
        return "?"

# Classifica frases
def aplicar_cha_em_texto(texto):
    frases = re.split(r'[.;]\s*', texto.strip())
    cha = {"C": [], "H": [], "A": []}
    for frase in frases:
        if not frase.strip():
            continue
        tipo = classificar_cha(frase)
        if tipo in cha:
            cha[tipo].append(frase.strip())
    return cha

# Aplica classificacao sobre objetivos
def aplicar_cha_linha(row):
    cha_obj = aplicar_cha_em_texto(str(row["Objetivos"]))

    return pd.Series({
        "Conhecimentos": "; ".join(cha_obj["C"]),
        "Habilidades": "; ".join(cha_obj["H"]),
        "Atitudes": "; ".join(cha_obj["A"])
    })

# Aplicar 
df_cha = df.apply(aplicar_cha_linha, axis=1)
df_final = pd.concat([df, df_cha], axis=1)

# Salvar e exibir
df_final.to_excel("CHA.xlsx", index=False)
print("Arquivo salvo: CHA.xlsx")
