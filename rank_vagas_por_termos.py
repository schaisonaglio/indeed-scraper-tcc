#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict

import pandas as pd

# ═════ LISTA COMPLETA DE PALAVRAS-CHAVE (disciplinas optativas) ════════════════════════════════════════════════════════

search_terms: List[str] = [
    "Radiodifusão", "Rádio enlace", "Ponto a ponto", "Ponto multiponto", "Multiponto",
    "DWDM", "CWDM", "GPON", "Regulamentação ANATEL", "Antenas de alta frequência",
    "Projeto de antenas", "Micro-ondas", "Miniaturização de antenas", "Antenas microstrip",
    "Smart antennas", "Antenas fractais", "Medições de antenas", "Sistemas de comunicações RF",
    "Comunicações móveis", "Engenharia de radiofrequência", "RF design", "Microwave engineering",
    "High-frequency measurements", "Sistemas de radar", "Radar CW", "Radar pulsado",
    "Phased array SAR", "Sinais de RF CW", "Sinais de RF pulsado", "Radar secundário",
    "Radar naval", "Radar aéreo", "Radar satelital", "Radar ambiental", "Radar militar",
    "Radar geográfico", "Radar para policiamento", "Análise de sinais de radar",
    "Especificação de sistemas de radar", "Comunicações via satélite", "Sistemas satelitais",
    "Segmento espacial", "Segmento terrestre", "Link budget", "Enlace satelital",
    "Cubesats", "Nanosatélites", "Satélites de relay", "Payload de satélites",
    "Bus de satélites", "Aplicações satelitais", "Engenharia de micro-ondas",
    "Parâmetros de espalhamento", "Carta de Smith", "Transformação de impedância",
    "Circuitos em micro-ondas", "Ressonadores", "Acopladores direcionais",
    "Filtros de micro-ondas", "Estruturas periódicas", "Amplificadores de micro-ondas",
    "Osciladores de micro-ondas", "Simulação de RF",
    "Ferramentas de simulação (HFSS, CST, ADS)", "Análise de circuitos de alta frequência",
    "Desempenho de redes", "Teoria de filas", "Cadeias de Markov",
    "Simulação a eventos discretos", "Simulação por eventos discretos",
    "Geração de números randômicos", "Medição ativa e passiva", "Simuladores de redes",
    "Tuning de parâmetros de rede", "Modelagem analítica", "NS-3", "OMNeT++",
    "Planejamento de capacidade de redes", "Análise preditiva de redes",
    "Internet das Coisas", "IoT", "Arquitetura de dispositivos", "Conectividade IoT",
    "MQTT", "CoAP", "Hardware embarcado", "Sensores e atuadores",
    "Redes de sensores sem fio", "AWS IoT", "Azure IoT", "Desenvolvimento de aplicações IoT",
    "Teoria dos grafos", "Percurso euleriano", "Percurso hamiltoniano",
    "Árvores geradoras mínimas", "Árvore de extensão mínima", "AGM",
    "Coloração de grafos", "Redes de fluxo", "Fluxo máximo", "Fluxo com custo",
    "Banco de dados relacional", "RDBMS", "Modelagem de dados", "Álgebra relacional", "SQL",
    "Normalização", "SGBD", "PostgreSQL", "MySQL", "SQLite",
    "Desenvolvimento com banco de dados", "Aplicações desktop e web com banco de dados",
    "Bancos de dados NoSQL", "MongoDB", "Administração de banco de dados",
    "Design de banco de dados", "Otimização de queries", "Engenharia de software",
    "Análise orientada a objetos", "Projeto orientado a objetos", "UML",
    "Modelagem de software", "Levantamento de requisitos", "Casos de uso",
    "Arquitetura de software", "Padrões de projeto", "Frameworks",
    "Desenvolvimento ágil", "Metodologias ágeis", "Scrum", "Kanban", "Testes de software",
    "Gerenciamento de projetos de software", "Inteligência artificial",
    "Aprendizado de máquina", "Machine learning", "Deep learning", "Preparação de dados",
    "Análise de dados", "Modelos preditivos", "TensorFlow", "PyTorch", "Scikit-learn",
    "Avaliação de modelos", "Agentes inteligentes", "Classificação", "Regressão",
    "Redes neurais artificiais", "Algoritmos supervisionados e não supervisionados",
    "Projeto de protocolos", "Especificação de protocolos", "Comunicação de rede",
    "Máquinas de estados", "FSM", "Modelagem de protocolos", "Codificação de mensagens",
    "Programação assíncrona", "Model checking", "Verificação formal",
    "Protocolos de comunicação", "Implementação de protocolos", "Propriedades de protocolos",
    "Redes de computadores", "Protocolos personalizados", "Técnicas de modelagem de protocolos",
    "Sistemas de controle", "Controle clássico", "Controle digital", "Análise de sistemas",
    "Resposta transitória", "Resposta em regime permanente", "Lugar das raízes",
    "Resposta em frequência", "Controladores PID", "Espaço de estados", "Projeto de controle",
    "Simulação de sistemas de controle", "Matlab", "Simulink",
    "Compatibilidade eletromagnética", "CEM", "Interferência eletromagnética", "EMI",
    "Emissões irradiadas", "Emissões conduzidas", "Suscetibilidade eletromagnética",
    "Blindagem eletromagnética", "Diafonia", "Descargas eletrostáticas", "Normas EMC",
    "Medições eletromagnéticas", "Espectro eletromagnético", "Princípios eletromagnéticos",
    "Eletrônica de potência", "Conversores estáticos", "Retificadores monofásicos e trifásicos",
    "Variadores de tensão", "CA-CC", "CA-CA", "CC-CC", "CC-CA", "MOSFET", "IGBT", "Tiristores",
    "Fontes chaveadas", "Filtros ativos", "UPS", "Correção de fator de potência",
    "Acionamento de motores", "Inversores de frequência", "Simulação de conversores",
    "Reatores eletrônicos", "Teoria da informação", "Codificação de fonte",
    "Codificação de canal", "Códigos corretores de erro", "Shannon", "Capacidade do canal",
    "Entropia", "Compressão de dados", "Detecção e correção de erros",
    "Códigos de Hamming", "Códigos convolucionais", "Códigos LDPC"
]

def url_limpa(url: str) -> str:
    """Remove parâmetros de query para deduplicar."""
    return re.sub(r"[?#].*$", "", url.strip()) if isinstance(url, str) else ""

def compilar(termos: List[str]) -> Dict[str, re.Pattern]:
    return {t: re.compile(re.escape(t.lower()), re.IGNORECASE) for t in termos}

def palavras_encontradas(texto: str, patterns: Dict[str, re.Pattern]) -> List[str]:
    txt = texto.lower()
    return [kw for kw, pat in patterns.items() if pat.search(txt)]

def analisar_vagas(dir_json: Path, patterns: Dict[str, re.Pattern]) -> pd.DataFrame:
    registros = []
    for arq in sorted(dir_json.glob("results_*.json")):
        try:
            vagas = json.loads(arq.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] Falha em {arq.name}: {e}")
            continue
        for vaga in vagas:
            texto = " ".join(str(vaga.get(f, "")) for f in ("title","description","skills","requirements"))
            kws = palavras_encontradas(texto, patterns)
            if kws:
                registros.append({
                    "url": vaga.get("url",""),
                    "id": vaga.get("id") or vaga.get("url") or vaga.get("link"),
                    "num_keywords": len(set(kws)),
                    "keywords": ", ".join(sorted(set(kws)))
                })
    if not registros:
        sys.exit("Nenhuma vaga contém as palavras-chave fornecidas.")
    df = pd.DataFrame(registros).drop_duplicates(subset=["url"])
    return df.sort_values(by="num_keywords", ascending=False)


def main() -> None:
    p = argparse.ArgumentParser(description="Ranqueia vagas por nº de palavras-chave distintas (lista fixa).")
    p.add_argument("--data-dir", type=Path, default=Path("."), help="Diretório com results_*.json")
    p.add_argument("--csv", type=Path, default=Path("ranked_jobs.csv"), help="CSV de saída")
    p.add_argument("--top", type=int, default=20, help="Mostrar TOP N no terminal")
    args = p.parse_args()

    patterns = compilar(search_terms)
    df = analisar_vagas(args.data_dir, patterns)

    print(f"\n=== TOP {args.top} VAGAS ===")
    print(df.head(args.top).to_string(index=False))

    df.to_csv(args.csv, index=False, encoding="utf-8")
    print(f"\nCSV salvo em: {args.csv}")

if __name__ == "__main__":
    main()
