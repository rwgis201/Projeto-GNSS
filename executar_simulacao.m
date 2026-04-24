% Script de Cintilação - Versão Cloud (Octave Online)
clc; clear;

% Carrega o pacote de dados (o servidor online geralmente precisa disso)
pkg load datatypes;

disp('Iniciando o simulador CPSSM no servidor...');

% Roda a física da ionosfera
out = cpssm('constellation', 'gps', ...
            'frequency', 'L1', ...
            'sim_time', 60, ...
            's4', 0.6); 

disp('Calculo finalizado! Gerando arquivos CSV...');

% Salva os arquivos direto na raiz do seu Bucket online
csvwrite('amplitude.csv', out.amplitude);
csvwrite('fase.csv', out.phase);

disp('SUCESSO! Pode baixar os arquivos amplitude.csv e fase.csv.');