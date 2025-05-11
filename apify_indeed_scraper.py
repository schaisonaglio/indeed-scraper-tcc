import time
import json
import re
from apify_client import ApifyClient

# Replace with your actual Apify API token
API_TOKEN = "apify_api_EzI7Nbz3I29KAcgepqc4aQbgH1Jl9E4GnA4Y"

# Initialize Apify client
client = ApifyClient(API_TOKEN)

# Function to clean file names
def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|;\/]', "_", text)

# All 60 search terms (summary of course topics and skills)
search_terms = [
    "Design Thinking", # user-centric design (?)
    "Metodologias ágeis (Scrum)", # Scrum, kamban, agile etc
    "Gestão de projetos (prototipagem e desenvolvimento de soluções)",
    "Sistemas de telecomunicações (integração de conhecimentos)",
    "Desenvolvimento em C"
    "Linguagem C"
    "Algoritmos",
    "Fluxogramas e pseudocódigo",
    "Depuração de código",
    "Controle de compilação (build automation)",
    "Vetores, ponteiros e funções",
    "Chamada por valor e por referência",
    "Manipulação de arquivos em C",
    "Eletrônica Digital I",
    "Sistemas de numeração binária e códigos digitais",
    "Álgebra booleana",
    "Aritmética binária",
    "Circuitos lógicos combinacionais",
    "Linguagem de descrição de hardware (HDL, ex.: VHDL)",
    "Simulação e teste de circuitos digitais",
    "Estruturas de dados (pilha, fila, lista, árvore binária, tabela hash)",
    "Algoritmos de busca e ordenação",
    "Complexidade de algoritmos (análise de desempenho)",
    "Circuitos Elétricos I",
    "Análise de circuitos elétricos em corrente contínua (CC)",
    "Leis de Kirchhoff",
    "Análise nodal e análise de malha",
    "Teoremas de Superposição, Thévenin e Norton",
    "Máxima transferência de potência",
    "Transientes em circuitos RC, RL e RLC (regime CC)",
    "Simulação de circuitos elétricos (ferramentas SPICE)",
    "Famílias lógicas (TTL, CMOS)",
    "Dispositivos lógicos programáveis (FPGA)",
    "Circuitos sequenciais (flip-flops, registradores, contadores)",
    "Máquinas de estados finitos (FSM)",
    "VHDL (descrição de hardware sequencial e hierárquica)",
    "Testbench e simulação de hardware digital",
    "Implementação de projetos em FPGA",
    "Programação Orientada a Objetos",
    "Programação Orientada a Objetos (Java)",
    "UML (Unified Modeling Language)",
    "Processo Unificado de desenvolvimento de software (RUP)",
    "Controle de versão (Git)",
    "Testes de unidade (JUnit)",
    "Desenvolvimento orientado por testes (TDD)",
    "Arquitetura e Organização de Computadores",
    "Linguagem Assembly",
    "Assembly",
    "Modos de endereçamento",
    "Pipeline de processador",
    "Hierarquia de memória (cache, RAM)",
    "Interrupções e entrada/saída (I/O)",
    "Arquiteturas de CPU (ciclos único, múltiplo)",
    "Sinais e Sistemas",
    "Sinais de tempo contínuo e tempo discreto",
    "Sistemas lineares e invariantes no tempo (LTI)",
    "Série de Fourier",
    "Transformada de Fourier (contínua e discreta)",
    "Transformada de Laplace",
    "Transformada Z",
    "Simulação de sinais e sistemas (MATLAB)",
    "Circuitos elétricos em corrente alternada (CA)",
    "Fasores (análise fasorial)",
    "Impedância e admitância",
    "Resposta em frequência de circuitos RLC",
    "Potência ativa, reativa e aparente",
    "Fator de potência",
    "Sistemas trifásicos",
    "Simulação de circuitos AC (SPICE)",
    "Eletromagnetismo",
    "Equações de Maxwell",
    "Campos eletromagnéticos estáticos e variáveis",
    "Propagação de ondas eletromagnéticas",
    "Reflexão e transmissão de ondas (fronteiras)",
    "Circuitos magnéticos e indutância",
    "Transformadores",
    "Laboratório de Circuitos Elétricos",
    "Montagem de circuitos em protoboard",
    "Uso de multímetro (voltímetro, amperímetro, ohmímetro)",
    "Uso de osciloscópio",
    "Uso de gerador de sinais",
    "Medição de grandezas elétricas em CC e CA",
    "Medição de potência e fator de potência em CA",
    "Processamento de Sinais Digitais",
    "Amostragem de sinais",
    "Transformada Discreta de Fourier (DFT)",
    "Filtros digitais IIR e FIR",
    "Projeto de filtros digitais",
    "Simulação de sinais no MATLAB/Simulink",
    "Redes de Computadores I",
    "Redes WAN, MAN e LAN",
    "Comutação de circuitos vs. comutação de pacotes",
    "Modelo de camadas OSI e TCP/IP",
    "Protocolos de aplicação (HTTP, FTP, SMTP)",
    "Protocolos de transporte (TCP, UDP)",
    "Endereçamento IP",
    "Roteamento de pacotes IP",
    "Sistemas Operacionais",
    "Chamadas de sistema (system calls)",
    "Gerenciamento de processos e threads",
    "Comunicação e sincronização entre processos (IPC, semáforos)",
    "Gerenciamento de memória (memória virtual)",
    "Sistemas de arquivos",
    "Programação concorrente (multithreading)",
    "Escalonamento de CPU",
    "Amplificadores operacionais (amp op)",
    "Diodos semicondutores",
    "Transistores MOSFET",
    "Transistores bipolares (BJT)",
    "Fontes de alimentação (reguladores de tensão)",
    "Simulação de circuitos eletrônicos (SPICE)",
    "Meios de Transmissão Guiados",
    "Linhas de transmissão metálicas (par trançado, coaxial)",
    "Guias de onda metálicos",
    "Fibras ópticas",
    "Parâmetros de linha de transmissão (R, L, C, G, impedância)",
    "Atenuação e dispersão em meios guiados",
    "Processos Estocásticos",
    "Variáveis aleatórias discretas e contínuas",
    "Vetores aleatórios (múltiplas variáveis)",
    "Processos estocásticos (contínuos e discretos no tempo)",
    "Processo Gaussiano",
    "Processo de Poisson",
    "Cadeias de Markov",
    "Processamento de sinais aleatórios (ruído, autocorrelação)",
    "Design Thinking",
    "Metodologias ágeis (Scrum)",
    "Desenvolvimento de software distribuído",
    "Sistemas Distribuídos",
    "Comunicação entre processos em rede (RPC, sockets)",
    "Objetos distribuídos (RMI, CORBA)",
    "Serviço de nomes (DNS)",
    "Web services (APIs REST/SOAP)",
    "Sincronização distribuída (relógios lógicos, mutex)",
    "Tolerância a falhas em sistemas distribuídos",
    "Segurança em sistemas distribuídos",
    "Antenas e Propagação",
    "Propagação de ondas de radiofrequência (mecanismos e tipos)",
    "Espectro radioelétrico (faixas de frequência)",
    "Ganho e diagrama de radiação de antenas",
    "Polarização de antenas",
    "Tipos de antenas (dipolo, Yagi, parabólica)",
    "Projeto e especificação de antenas RF",
    "Amplificadores de pequeno sinal (configurações com BJT/MOSFET)",
    "Resposta em frequência de amplificadores",
    "Osciladores eletrônicos (LC, cristal)",
    "Amplificadores de potência (Classes A, B, AB, C)",
    "Simulação de circuitos AC (análise de frequência)",
    "Microprocessadores (Microcontroladores)",
    "Arquitetura de microcontroladores",
    "Programação de microcontroladores em C/C++",
    "Interrupções e temporizadores (timers)",
    "Interface de periféricos (GPIO, ADC, UART, SPI, I²C)",
    "Firmware embarcado (sistemas de recursos limitados)",
    "Depuração de software embarcado (debug JTAG)",
    "Redes de Computadores II",
    "Redes locais cabeadas (Ethernet)",
    "Redes locais sem fio (Wi-Fi)",
    "Tecnologias de acesso (xDSL, FTTH)",
    "Internet das Coisas (IoT)",
    "Sistemas de Comunicação",
    "Modulação analógica (AM, FM)",
    "Digitalização de sinal analógico (PCM)",
    "Modulação em banda base (codificação de linha)",
    "Modulação digital em banda passante (ASK, FSK, PSK, QAM)",
    "Sincronização em sistemas digitais",
    "Análise de enlace de comunicação (SNR, BER)",
    "Rádio Definido por Software (SDR)",
    "Circuitos de Rádiofrequência",
    "Amplificadores de RF (LNA de baixo ruído, PA de potência)",
    "Osciladores de RF (VCO)",
    "Filtros sintonizados de RF",
    "Misturadores de frequência (mixers)",
    "PLL (Phase-Locked Loop)",
    "Ruído em circuitos de RF (figura de ruído)",
    "Arquiteturas de transmissores/receptores (super-heteródino, homódino)",
    "Casamento de impedâncias em RF",
    "Comunicações Sem Fio",
    "Modelos de propagação em comunicações móveis (perda de percurso, desvanecimento)",
    "MIMO (Multiple Input Multiple Output)",
    "Técnicas de múltiplo acesso (FDMA, TDMA, CDMA, OFDMA)",
    "Sistemas celulares móveis (planejamento de cobertura e capacidade)",
    "Tecnologias emergentes em redes sem fio (4G, 5G, LPWAN/IoT)",
    "Sistemas Embarcados",
    "Metodologia de desenvolvimento de sistemas embarcados",
    "Sistemas operacionais de tempo real (RTOS)",
    "Ferramentas de depuração de firmware (JTAG, depurador)",
    "Barramentos e interfaces embarcadas (I²C, SPI, CAN)",
    "Projeto integrado de hardware/software embarcado",
    "Integração de software e hardware",
    "Metodologias de desenvolvimento de projetos",
    "Prototipagem de sistemas de telecomunicações",
    "Sistemas de Telecomunicações",
    "Radiodifusão (broadcast de rádio e TV)",
    "Rádio enlace (links ponto-a-ponto e ponto-multiponto)",
    "Comunicações via satélite",
    "Redes ópticas (DWDM, CWDM, GPON)",
    "TV Digital e streaming",
    "Sistemas de radar",
    "Regulamentação em telecomunicações (ANATEL)"
]

# 3. Run Apify actor for each term
for i, term in enumerate(search_terms, 1):
    print(f"\n🔍 ({i}/{len(search_terms)}) Buscando: {term[:60]}...")

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
        # Start the run
        run = client.actor("misceres~indeed-scraper").call(run_input=run_input)

        # Wait for completion
        client.run(run["id"]).wait_for_finish()

        # Download dataset
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

        # Write results to file
        filename = f"results_{i:02d}_{sanitize_filename(term[:40])}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dataset_items, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(dataset_items)} resultados salvos em: {filename}")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Erro ao processar: {term}\n{e}")