# 🛰️ Projeto GNSS - Arquitetura SIL (Software-in-the-Loop)

Este repositório contém a infraestrutura completa de uma arquitetura SIL (Software-in-the-Loop) desenvolvida para a simulação, perturbação e recepção de sinais GNSS (Global Navigation Satellite System). 

O objetivo central desta pesquisa em Engenharia de Telecomunicações é modelar os efeitos da cintilação ionosférica em sinais de rádio (banda base) e avaliar a resiliência de algoritmos de rastreio, preparando o terreno para a implementação de Filtros Bayesianos (Filtro de Kalman Estendido / Filtro de Partículas).

---

## 🏗️ Arquitetura e Fases do Projeto

A linha de montagem do laboratório está dividida em três macro-blocos de Processamento Digital de Sinais (DSP): o Transmissor, o Canal de Comunicação e o Receptor.

### ✅ Fase 1: Geração do Sinal Limpo (O Transmissor)
Utilizamos o simulador [GPS-SDR-SIM](https://github.com/osqzss/gps-sdr-sim) para gerar um fluxo de dados de sinal de banda base GNSS sintético.
* **Ferramenta:** `gnss-sdr-sim` (C)
* **Entrada:** Arquivo de efemérides RINEX da NASA (`brdc3540.14n`).
* **Saída:** Arquivo bruto de 16-bits I/Q (`gpssim.bin` - ignorado no versionamento devido ao tamanho).
* **Parâmetros:** Simulação travada em coordenadas estáticas (Fortaleza/CE).

### ✅ Fase 2: Modelagem Ionosférica (O Canal)
Simulação do clima espacial responsável por corromper a onda de rádio antes que ela atinja a antena do receptor. Baseado no modelo CPSSM (Cornell Propagation Scintillation Simulator).
* **Ferramenta:** Scripts em Python (`mock_ionosfera.py`).
* **Dinâmica:** Geração de ruído sintético representando:
  * **Amplitude (Fading):** Simulação de quedas severas de energia baseadas no índice S4.
  * **Fase:** Atrasos caóticos na propagação do sinal (Random Walk).
* **Saída:** Matrizes exportadas em `amplitude.csv` e `fase.csv`.

### ✅ Fase 3: Fusão de Dados e Cintilação
O núcleo de DSP da arquitetura. O script atua como o "colisor", aplicando a física da ionosfera sobre a onda limpa em quadratura.
* **Ferramenta:** `aplicar_cintilacao.py` (NumPy).
* **Matemática:** O script lê 1 segundo do sinal I/Q (2.6 MHz), rotaciona a fase e atenua a amplitude utilizando as matrizes de ruído geradas na Fase 2.
* **Saída:** Arquivo `onda_cintilada_1seg.bin` formatado em inteiros de 8-bits, pronto para causar perda de rastreio (Loss of Lock) em receptores clássicos.

### 🚧 Fase 4: Receptor e Rastreio Bayesiano (Em Andamento)
A etapa final de recepção e solução de navegação. 
* **Ferramenta base:** [SignalSim](https://github.com/globsky/SignalSim) (C++).
* **Objetivo Atual:** Compilar o receptor, injetar a onda cintilada gerada na Fase 3 e substituir as malhas de rastreio tradicionais (PLL/FLL) por algoritmos bayesianos para garantir a manutenção do sinal sob forte cintilação.

---

## 📂 Estrutura de Diretórios

O projeto está organizado da seguinte forma:

```text
Projeto_GNSS/
│
├── ferramentas/             # Código-fonte de terceiros (Transmissores e Receptores)
│   ├── gps-sdr-sim/         # Gerador da onda limpa (Baseband)
│   ├── cpssm/               # Simulador de cintilação de laboratório (MATLAB/Octave)
│   └── SignalSim/           # Receptor Avançado em C++
│
├── dados/                   # (Ignorado no Git) Matrizes e arquivos .bin gigantes
│   ├── amplitude.csv
│   ├── fase.csv
│   └── onda_cintilada_1seg.bin
│
├── mock_ionosfera.py        # Gera ruído sintético (Mock) para testes de arquitetura
├── aplicar_cintilacao.py    # Multiplica a onda I/Q pelo ruído da ionosfera
├── ler_onda.py              # Plota o gráfico da onda resultante
├── .gitignore               # Proteção contra upload de arquivos pesados (>100MB)
└── README.md
