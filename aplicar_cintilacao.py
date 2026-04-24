import numpy as np

print("Iniciando a Fusão: Onda Limpa + Ionosfera...")

# 1. Carrega as matrizes de ruído (100 amostras por segundo)
amp = np.loadtxt('dados/amplitude.csv', delimiter=',')
fase = np.loadtxt('dados/fase.csv', delimiter=',')

# 2. Carregando 1 SEGUNDO da onda limpa (2.6 MHz * 2 para I e Q = 5.2M valores)
# ATENÇÃO: Garanta que o caminho abaixo é onde o seu .bin está de verdade!
caminho_bin = 'ferramentas/gnss-sdr-sim/gpssim.bin' 
onda_limpa = np.fromfile(caminho_bin, dtype=np.int8, count=5200000)

print("Onda limpa carregada! Separando I e Q...")
# Separa os pares (I) e os ímpares (Q)
I = onda_limpa[0::2].astype(np.float32)
Q = onda_limpa[1::2].astype(np.float32)

# 3. Preparando o Ruído
# Pegamos apenas o 1º segundo de ruído (as primeiras 100 amostras do Mock)
amp_1s = amp[:100]
fase_1s = fase[:100]

# O gerador SDR cospe 2.600.000 amostras por segundo. 
# O ruído tem 100 amostras por segundo. 
# Precisamos "esticar" o ruído (repetir cada valor 26.000 vezes) para o tamanho bater.
amp_esticada = np.repeat(amp_1s, 26000)
fase_esticada = np.repeat(fase_1s, 26000)

print("Aplicando a Equação de Cintilação (Filtro Ionosférico)...")
# 4. A Física: Rotação de Fase e Atenuação de Amplitude
I_cintilado = amp_esticada * (I * np.cos(fase_esticada) - Q * np.sin(fase_esticada))
Q_cintilado = amp_esticada * (Q * np.cos(fase_esticada) + I * np.sin(fase_esticada))

# 5. Fechando o arquivo para o Receptor GPS
print("Empacotando a nova onda corrompida...")
onda_final = np.empty_like(onda_limpa)
# O HackRF exige números inteiros de 8-bits (-128 a 127). Cortamos os excessos com np.clip
onda_final[0::2] = np.clip(I_cintilado, -128, 127).astype(np.int8)
onda_final[1::2] = np.clip(Q_cintilado, -128, 127).astype(np.int8)

# Salva o arquivo final!
onda_final.tofile('dados/onda_cintilada_1seg.bin')

print("========================================")
print("SUCESSO ABSOLUTO! ")
print("O arquivo 'onda_cintilada_1seg.bin' nasceu na pasta dados.")
print("========================================")