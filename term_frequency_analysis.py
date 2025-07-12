import os
import json
import re
from collections import defaultdict

# Termos de busca
search_terms = [
    "Radiodifusão",  # Transmissão de rádio e TV
    "Rádio enlace",  # Comunicação ponto a ponto e multiponto
    "Ponto a ponto",
    "Ponto multiponto",
    "Multiponto",
    "DWDM",  # Dense Wavelength Division Multiplexing
    "CWDM",  # Coarse Wavelength Division Multiplexing
    "GPON",  # Gigabit-capable Passive Optical Network
    "Regulamentação ANATEL",  # Normas brasileiras de telecomunicações
    "Antenas de alta frequência",
    "Projeto de antenas",
    "Micro-ondas",
    "Miniaturização de antenas",
    "Antenas microstrip",
    "Smart antennas",
    "Antenas fractais",
    "Medições de antenas",
    "Sistemas de comunicações RF",
    "Comunicações móveis",
    "Engenharia de radiofrequência",
    "RF design",
    "Microwave engineering",
    "High-frequency measurements",
    "Sistemas de radar",
    "Radar CW",
    "Radar pulsado",
    "Phased array SAR",  # Synthetic Aperture Radar com phased array
    "Sinais de RF CW",
    "Sinais de RF pulsado",
    "Radar secundário",
    "Radar naval",
    "Radar aéreo",
    "Radar satelital",
    "Radar ambiental",
    "Radar militar",
    "Radar geográfico",
    "Radar para policiamento",
    "Análise de sinais de radar",
    "Especificação de sistemas de radar",
    "Comunicações via satélite",
    "Sistemas satelitais",
    "Segmento espacial",
    "Segmento terrestre",
    "Link budget",
    "Enlace satelital",
    "Cubesats",
    "Nanosatélites",
    "Satélites de relay",
    "Payload de satélites",
    "Bus de satélites",
    "Aplicações satelitais",
    "Engenharia de micro-ondas",
    "Parâmetros de espalhamento",
    "Carta de Smith",
    "Transformação de impedância",
    "Circuitos em micro-ondas",
    "Ressonadores",
    "Acopladores direcionais",
    "Filtros de micro-ondas",
    "Estruturas periódicas",
    "Amplificadores de micro-ondas",
    "Osciladores de micro-ondas",
    "Simulação de RF",
    "Ferramentas de simulação (HFSS, CST, ADS)",
    "Análise de circuitos de alta frequência",
    "Desempenho de redes",
    "Teoria de filas",
    "Cadeias de Markov",
    "Simulação a eventos discretos",
    "Simulação por eventos discretos",
    "Geração de números randômicos",
    "Medição ativa e passiva",
    "Simuladores de redes",
    "Tuning de parâmetros de rede",
    "Modelagem analítica",
    "NS-3",  # Network Simulator 3
    "OMNeT++",  # Simulador de redes
    "Planejamento de capacidade de redes",
    "Análise preditiva de redes",
    "Internet das Coisas",
    "IoT",
    "Arquitetura de dispositivos",
    "Conectividade IoT",
    "MQTT",
    "CoAP",
    "Hardware embarcado",
    "Sensores e atuadores",
    "Redes de sensores sem fio",
    "AWS IoT",
    "Azure IoT",
    "Desenvolvimento de aplicações IoT",
    "Teoria dos grafos",
    "Percurso euleriano",
    "Percurso hamiltoniano",
    "Árvores geradoras mínimas",
    "Árvore de extensão mínima",
    "AGM",  # Algoritmo de Kruskal/Prim para árvores mínimas
    "Coloração de grafos",
    "Redes de fluxo",
    "Fluxo máximo",
    "Fluxo com custo",
    "Banco de dados relacional",
    "RDBMS",  # Relational Database Management System
    "Modelagem de dados",
    "Álgebra relacional",
    "SQL",
    "Normalização",
    "SGBD",  # Sistema de Gerenciamento de Banco de Dados
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "Desenvolvimento com banco de dados",
    "Aplicações desktop e web com banco de dados",
    "Bancos de dados NoSQL",
    "MongoDB",
    "Administração de banco de dados",
    "Design de banco de dados",
    "Otimização de queries",
    "Engenharia de software",
    "Análise orientada a objetos",
    "Projeto orientado a objetos",
    "UML",
    "Modelagem de software",
    "Levantamento de requisitos",
    "Casos de uso",
    "Arquitetura de software",
    "Padrões de projeto",
    "Frameworks",
    "Desenvolvimento ágil",
    "Metodologias ágeis",
    "Scrum",
    "Kanban",
    "Testes de software",
    "Gerenciamento de projetos de software",
    "Inteligência artificial",
    "Aprendizado de máquina",
    "Machine learning",
    "Deep learning",
    "Preparação de dados",
    "Análise de dados",
    "Modelos preditivos",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Avaliação de modelos",
    "Agentes inteligentes",
    "Classificação",
    "Regressão",
    "Redes neurais artificiais",
    "Algoritmos supervisionados e não supervisionados",
    "Projeto de protocolos",
    "Especificação de protocolos",
    "Comunicação de rede",
    "Máquinas de estados",
    "FSM",  # Finite State Machine
    "Modelagem de protocolos",
    "Codificação de mensagens",
    "Programação assíncrona",
    "Model checking",
    "Verificação formal",
    "Protocolos de comunicação",
    "Implementação de protocolos",
    "Propriedades de protocolos",
    "Redes de computadores",
    "Protocolos personalizados",
    "Técnicas de modelagem de protocolos",
    "Sistemas de controle",
    "Controle clássico",
    "Controle digital",
    "Análise de sistemas",
    "Resposta transitória",
    "Resposta em regime permanente",
    "Lugar das raízes",
    "Resposta em frequência",
    "Controladores PID",
    "Espaço de estados",
    "Projeto de controle",
    "Simulação de sistemas de controle",
    "Matlab",
    "Simulink",
    "Compatibilidade eletromagnética",
    "CEM",  # Compatibilidade Eletromagnética
    "Interferência eletromagnética",
    "EMI",
    "Emissões irradiadas",
    "Emissões conduzidas",
    "Suscetibilidade eletromagnética",
    "Blindagem eletromagnética",
    "Diafonia",
    "Descargas eletrostáticas",
    "Normas EMC",
    "Medições eletromagnéticas",
    "Espectro eletromagnético",
    "Princípios eletromagnéticos",
    "Eletrônica de potência",
    "Conversores estáticos",
    "Retificadores monofásicos e trifásicos",
    "Variadores de tensão",
    "CA-CC",
    "CA-CA",
    "CC-CC",
    "CC-CA",
    "MOSFET",
    "IGBT",
    "Tiristores",
    "Fontes chaveadas",
    "Filtros ativos",
    "UPS",  # Uninterruptible Power Supply
    "Correção de fator de potência",
    "Acionamento de motores",
    "Inversores de frequência",
    "Simulação de conversores",
    "Reatores eletrônicos",
    "Teoria da informação",
    "Codificação de fonte",
    "Codificação de canal",
    "Códigos corretores de erro",
    "Shannon",
    "Capacidade do canal",
    "Entropia",
    "Compressão de dados",
    "Detecção e correção de erros",
    "Códigos de Hamming",
    "Códigos convolucionais",
    "Códigos LDPC"  # Low-Density Parity-Check
]


# Diretório contendo os arquivos JSON gerados
data_dir = "."

# Dicionário para armazenar as contagens
counts = {term: {"matches": 0, "jobs": set()} for term in search_terms}

# Percorra todos os arquivos JSON
for filename in os.listdir(data_dir):
    if filename.endswith(".json") and filename.startswith("results_"):
        with open(os.path.join(data_dir, filename), encoding="utf-8") as f:
            try:
                jobs = json.load(f)
            except json.JSONDecodeError:
                print(f"Aviso: falha ao ler {filename}. Pulando.")
                continue

        # Para cada vaga, combine todos os campos relevantes em um único texto
        for job in jobs:
            text = " ".join([
                str(job.get("title", "")),
                str(job.get("description", "")),
                str(job.get("skills", "")),
                str(job.get("requirements", "")),
            ]).lower()

            # Verifique presença de cada termo
            for term in search_terms:
                if re.search(r'\b' + re.escape(term.lower()) + r'\b', text):
                    counts[term]["matches"] += 1
                    counts[term]["jobs"].add(job.get("id") or job.get("link") or filename)

# Exporte resultados consolidados
report = []
for term, info in counts.items():
    report.append({
        "term": term,
        "match_count": info["matches"],
        "unique_jobs": len(info["jobs"])
    })

# Salve o relatório final
with open("term_frequency_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Análise concluída. Verifique 'term_frequency_report.json'.")
