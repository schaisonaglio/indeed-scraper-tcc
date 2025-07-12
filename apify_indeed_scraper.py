import time
import json
import re
from apify_client import ApifyClient

API_TOKEN = "apify_api_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Inicializar Apify client
client = ApifyClient(API_TOKEN)

# Limpar nomes
def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|;\/]', "_", text)

# Termos procurados
search_terms = [
    "Design Thinking",  # Design centrado no usuário
    "Scrum",  # Metodologia ágil
    "Kanban",  # Gestão visual de fluxo de trabalho
    "Agile",  # Desenvolvimento ágil
    "Gestão de produtos",
    "Gestão de projetos",
    "Programação C/C++",
    "Linguagem C",
    "Desenvolvimento C",
    "Depuração de código",
    "Álgebra Booleana",
    "Aritmética binária",
    "Circuitos digitais",
    "Algoritmos",
    "Estrutura de dados",
    "Circuitos elétricos",
    "Corrente contínua",
    "Leis de Kirchhoff",
    "Análise de circuitos",
    "Teoremas de Superposição",
    "Thévenin e Norton",
    "Ferramentas SPICE",
    "Simulações Spice",
    "LT-Spice",
    "Tina-TI",
    "Pspice",
    "Circuitos analógicos",
    "HDL",  # Hardware Description Language
    "VHDL",  # Linguagem de descrição de hardware
    "FPGA",  # Circuitos programáveis
    "CMOS",  # Tecnologia de semicondutores
    "TTL",  # Transistor-Transistor Logic
    "Simulação de hardware digital",
    "Simulação e validação de hardware",
    "Programação orientada a objetos",
    "POO",
    "Java",
    "UML",  # Unified Modeling Language
    "RUP",  # Rational Unified Process
    "Git",  # Controle de versão
    "JUnit",  # Testes unitários em Java
    "Testes unitários",
    "Unit tests",
    "TDD",  # Test-Driven Development
    "Assembly",  # Linguagem de baixo nível
    "Matlab",
    "Fourier",  # Transformadas de Fourier
    "Transformada de Laplace",
    "Transformada Z",
    "Corrente alternada",
    "Fator de potência",
    "Sistemas trifásicos",
    "Potência ativa, reativa e aparente",
    "Transformadores",
    "Circuitos magnéticos e de indutância",
    "Campos eletromagnéticos",
    "Montagem de circuitos elétricos",
    "Multímetro",
    "Osciloscópio",
    "Geradores de sinal",
    "Processamento de sinais",
    "Processamento digital de sinais",
    "Transformada Discreta de Fourier",
    "Filtros digitais",
    "IIR",  # Infinite Impulse Response
    "FIR",  # Finite Impulse Response
    "Simulink",
    "Matlab/Simulink",
    "Redes de computadores",
    "Redes IP",
    "TCP/IP",
    "UDP",
    "TCP",
    "WAN",
    "MAN",
    "LAN",
    "HTTP",
    "FTP",
    "SMTP",
    "Multithread",
    "Multi thread",
    "Multi-thread",
    "Linux",
    "Memory management",
    "Gerenciamento de memória",
    "Heap",
    "Stack",
    "File system",
    "Amplificadores operacionais",
    "Transistores",
    "MOSFET",
    "Eletrônica de potência",
    "Sistemas de potência",
    "Cabo coaxial",
    "Fibra óptica",
    "Atenuação e dispersão em meios guiados",
    "Cabos trançados",
    "Par trançado",
    "Processos estocásticos",
    "Métodos estocásticos",
    "Estocásticos",
    "Probabilidade e estatística",
    "Variáveis aleatórias",
    "Sistemas distribuídos",
    "REST",  # API REST
    "SOAP",  # Web Services
    "DNS",  # Sistema de nomes de domínio
    "API",
    "Fault tolerance",
    "Tolerância a falhas",
    "Segurança em desenvolvimento de software",
    "Segurança da informação",
    "Antenas",
    "Radiofrequência",
    "Antenas dipolo",
    "Antenas yagi",
    "Antenas parabólica",
    "Amplificadores de potência",
    "Amplificadores de pequeno sinal",
    "Simulação de circuitos AC",
    "Microprocessadores",
    "Microcontroladores",
    "GPIO",  # General Purpose Input/Output
    "ADC",  # Conversor analógico-digital
    "UART",
    "Firmware",
    "JTAG",  # Interface de depuração
    "Ethernet",
    "Wi-Fi",
    "xDSL",
    "FTTH",
    "FTTX",
    "FTTN",
    "FTTC",
    "IoT",  # Internet das Coisas
    "Internet das Coisas",
    "BGP",  # Border Gateway Protocol
    "Modulação",
    "AM",  # Modulação em amplitude
    "FM",  # Modulação em frequência
    "Modulação em banda base",
    "Codificação de linha",
    "Digitalização de sinal analógico",
    "Largura de banda",
    "ASK",  # Amplitude Shift Keying
    "FSK",  # Frequency Shift Keying
    "PSK",  # Phase Shift Keying
    "QAM",  # Quadrature Amplitude Modulation
    "Sincronismo",
    "Analisadores de espectro",
    "SNR",  # Signal-to-Noise Ratio
    "BER",  # Bit Error Rate
    "Bit error rate",
    "Rádio Definido por Software",
    "Amplificadores de RF",
    "LNA de baixo ruído",
    "Filtros sintonizados de RF",
    "PLLs",  # Phase-Locked Loops
    "Figura de ruído",
    "Casamento de impedância",
    "Redes móveis",
    "Multiple Input Multiple Output",
    "FDMA",
    "TDMA",
    "CDMA",
    "OFDMA",
    "4G",
    "5G",
    "6G",
    "LPWAN",
    "LTE",
    "Sistemas Embarcados",
    "RTOS",  # Real-Time Operating System
    "Sistemas operacionais de tempo real",
    "CAN",  # Barramento de comunicação
    "Integração de software e hardware",
    "Desenvolvimento de Hardware/Software Embarcado"
]


# 3. Rodar ator Apify para cada termo
for i, term in enumerate(search_terms, 1):
    print(f"\n({i}/{len(search_terms)}) Buscando: {term[:60]}...")

    run_input = {
        "country": "BR",
        "followApplyRedirects": True,
        "location": "Santa Catarina",
        "maxItems": 50,
        "parseCompanyDetails": False,
        "position": term,
        "saveOnlyUniqueItems": True
    }

    try:
        
        run = client.actor("misceres~indeed-scraper").call(run_input=run_input)
        
        client.run(run["id"]).wait_for_finish()
        
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        
        filename = f"results_{i:02d}_{sanitize_filename(term[:40])}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dataset_items, f, ensure_ascii=False, indent=2)

        print(f"{len(dataset_items)} Resultados salvos em: {filename}")
        time.sleep(5)

    except Exception as e:
        print(f"Erro ao processar: {term}\n{e}")