
# Indeed Scraper

Este repositório contém um script para coleta automatizada de vagas de emprego no Indeed Brasil, com foco em busca por palavras-chave relacionadas a áreas técnicas e tecnológicas. O script utiliza a plataforma [Apify](https://apify.com/) para realizar as buscas.

## 📄 Descrição

O script `apify_indeed_scraper.py` acessa o ator `misceres~indeed-scraper` da Apify e busca por diversas palavras-chave em vagas disponíveis no estado de Santa Catarina (BR). Os resultados são salvos como arquivos `.json`, um para cada termo buscado.

---

## 🧩 Requisitos

Antes de rodar o script, é necessário:

- Ter Python 3.7+ instalado.
- Ter uma conta na [Apify](https://apify.com/).
- Ter uma chave de API válida (API Token) da Apify.
- Instalar as dependências com:

```bash
pip install apify-client
```

---

## 🔐 Configuração

1. No script `apify_indeed_scraper.py`, substitua a string:

```python
API_TOKEN = "apify_api_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

por sua chave da API da Apify, disponível em: [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations)


---

## ▶️ Como rodar

Basta executar o script com Python:

```bash
python apify_indeed_scraper.py
```

O script irá:
- Buscar por cada termo listado no array `search_terms`
- Executar o ator `misceres~indeed-scraper` para cada termo
- Salvar os resultados como arquivos `.json` nomeados com o número da iteração e o nome do termo

---

## 📁 Resultados

Os arquivos serão salvos no mesmo diretório do script, com nomes como:

```
results_01_Palavra_Chave_1.json
results_01_Palavra_Chave_2.json
...
```

---

## ⚠️ Observações

- É recomendado respeitar os limites de requisições da Apify (o script já inclui um `sleep` de 5 segundos entre buscas).
- Palavras-chave e localidade podem ser alteradas diretamente no script.
- Apenas resultados únicos são salvos (configurado via `saveOnlyUniqueItems = True`).
