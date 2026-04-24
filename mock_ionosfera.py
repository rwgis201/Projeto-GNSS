import numpy as np
import os

print("Iniciando a Geração de Cintilação Simulada (Mock)...")

amostras = 6000
tempo = np.linspace(0, 60, amostras)

# Simulando o fading (S4) e o ruído de fase
amplitude = 1.0 - 0.6 * np.abs(np.sin(tempo * 0.5)) - 0.2 * np.random.rand(amostras)
amplitude = np.clip(amplitude, 0.1, 1.0)
fase = np.cumsum(np.random.randn(amostras) * 0.1)

caminho_dados = 'dados'
if not os.path.exists(caminho_dados): os.makedirs(caminho_dados)

np.savetxt(f'{caminho_dados}/amplitude.csv', amplitude, delimiter=',')
np.savetxt(f'{caminho_dados}/fase.csv', fase, delimiter=',')

print("SUCESSO! Arquivos gerados na pasta dados.")