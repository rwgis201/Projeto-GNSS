import numpy as np
import matplotlib.pyplot as plt

print("Lendo a onda gerada pelo gps-sdr-sim...")

# Carrega o arquivo binário (ele usa formato inteiro de 8 bits)
# Vamos ler apenas as primeiras 200.000 amostras para o gráfico não travar o PC
dados_brutos = np.fromfile('ferramentas\gnss-sdr-sim\gpssim.bin', dtype=np.int8, count=200000)

# O rádio intercala os dados: [I, Q, I, Q, I, Q...]
# Vamos separar os pares!
I = dados_brutos[0::2] # Pega os pares (In-Phase)
Q = dados_brutos[1::2] # Pega os ímpares (Quadrature)

print("Gerando o gráfico da sua onda...")

# Criação do gráfico
plt.figure(figsize=(10, 5))
plt.plot(I[:500], label='Onda I (In-Phase)', color='blue', alpha=0.7)
plt.plot(Q[:500], label='Onda Q (Quadrature)', color='red', alpha=0.7)

plt.title('As primeiras 500 amostras do seu Sinal GNSS')
plt.xlabel('Tempo (Amostras)')
plt.ylabel('Amplitude (Energia do sinal)')
plt.legend()
plt.grid(True)
#plt.show()
plt.savefig('grafico_onda.png')