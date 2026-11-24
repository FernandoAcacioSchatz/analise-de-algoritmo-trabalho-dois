# Dados da coleta experimental

Gerado automaticamente por `src/experimento.py` em 2026-11-20 15:16:55.

## Ambiente

- Processador: Intel64 Family 6 Model 186 Stepping 3, GenuineIntel
- Sistema: Windows 11
- Python: CPython 3.13.13
- Duracao total da coleta: 136 s, 302 rodadas

## Entrada

- 100000 inteiros distintos, permutacao de 0 a 99999, embaralhada com semente 42.
- Arquivo: `dados/entrada.csv`.

## Desenho

- Os 3 algoritmos (QR = Quick Sort Recursivo, QI = Quick Sort Iterativo, ME = Merge Sort) sao executados em todas as 6 ordens possiveis, uma ordem por formato.
- Cada rodada executa os 3 algoritmos na ordem do formato, sobre a mesma entrada. Cada algoritmo recebe uma copia, feita fora do cronometro.
- Aquecimento: 18 rodadas descartadas, alternando os formatos.
- Amostragem piloto: 30 rodadas validas por formato.
- Calculo de n por formato, apos o piloto: para cada algoritmo, o menor n tal que n >= (t(0,025; n-1) * s / (0,05 * media))^2. O n do formato e o maior dos tres, com piso em 30 e teto de 1000.
- Coleta final: rodadas ate atingir o n adotado de cada formato, alternando os formatos a cada passagem.
- Medicao: `time.perf_counter_ns()`, coletor de lixo desligado durante a ordenacao.
- Verificacao: o resultado de cada ordenacao e comparado com `0..n-1` fora do cronometro.

## Arquivos

- `dados/formato_QR-QI-ME.csv`: rodadas do formato QR > QI > ME.
- `dados/formato_QR-ME-QI.csv`: rodadas do formato QR > ME > QI.
- `dados/formato_QI-QR-ME.csv`: rodadas do formato QI > QR > ME.
- `dados/formato_QI-ME-QR.csv`: rodadas do formato QI > ME > QR.
- `dados/formato_ME-QR-QI.csv`: rodadas do formato ME > QR > QI.
- `dados/formato_ME-QI-QR.csv`: rodadas do formato ME > QI > QR.

Colunas de cada CSV:

- `fase`: aquecimento, piloto ou final.
- `rodada`: numero da rodada na coleta inteira.
- `descartada`: sim (aquecimento) ou nao.
- `formato`: ordem de execucao da rodada, por exemplo QR-QI-ME.
- `posicao`: posicao do algoritmo na rodada (1, 2 ou 3).
- `algoritmo`: nome do algoritmo.
- `n_elementos`: tamanho da entrada.
- `tempo_ms`: tempo de ordenacao em milissegundos.

## Resultado do calculo de n e precisao

`erro_relativo` = t * s / sqrt(N) / media, com N as rodadas validas do algoritmo no formato. Deve ser <= 0,05 para a precisao exigida.

| Formato | Algoritmo | n calculado | n adotado | validas | media (ms) | desvio (ms) | IC 95% (ms) | erro relativo |
|---|---|---|---|---|---|---|---|---|
| QR-QI-ME | Quick Sort Recursivo | 25 | 67 | 67 | 97.00 | 8.99 | [94.81; 99.19] | 2.26% |
| QR-QI-ME | Quick Sort Iterativo | 33 | 67 | 67 | 102.99 | 10.50 | [100.43; 105.55] | 2.49% |
| QR-QI-ME | Merge Sort | 67 | 67 | 67 | 173.30 | 25.26 | [167.14; 179.46] | 3.55% |
| QR-ME-QI | Quick Sort Recursivo | 91 | 91 | 91 | 97.47 | 14.51 | [94.45; 100.50] | 3.10% |
| QR-ME-QI | Quick Sort Iterativo | 22 | 91 | 91 | 103.49 | 8.13 | [101.80; 105.18] | 1.64% |
| QR-ME-QI | Merge Sort | 48 | 91 | 91 | 170.74 | 17.85 | [167.02; 174.46] | 2.18% |
| QI-QR-ME | Quick Sort Recursivo | 16 | 30 | 30 | 100.76 | 9.11 | [97.36; 104.16] | 3.38% |
| QI-QR-ME | Quick Sort Iterativo | 14 | 30 | 30 | 104.26 | 8.82 | [100.96; 107.55] | 3.16% |
| QI-QR-ME | Merge Sort | 7 | 30 | 30 | 174.39 | 9.37 | [170.89; 177.90] | 2.01% |
| QI-ME-QR | Quick Sort Recursivo | 36 | 36 | 36 | 101.01 | 14.35 | [96.16; 105.87] | 4.81% |
| QI-ME-QR | Quick Sort Iterativo | 17 | 36 | 36 | 107.32 | 9.91 | [103.97; 110.68] | 3.13% |
| QI-ME-QR | Merge Sort | 7 | 36 | 36 | 173.24 | 8.89 | [170.23; 176.25] | 1.74% |
| ME-QR-QI | Quick Sort Recursivo | 16 | 30 | 30 | 99.56 | 9.22 | [96.12; 103.00] | 3.46% |
| ME-QR-QI | Quick Sort Iterativo | 14 | 30 | 30 | 103.48 | 8.89 | [100.16; 106.80] | 3.21% |
| ME-QR-QI | Merge Sort | 14 | 30 | 30 | 174.83 | 14.65 | [169.36; 180.30] | 3.13% |
| ME-QI-QR | Quick Sort Recursivo | 11 | 30 | 30 | 96.66 | 6.88 | [94.09; 99.23] | 2.66% |
| ME-QI-QR | Quick Sort Iterativo | 12 | 30 | 30 | 104.13 | 7.97 | [101.16; 107.11] | 2.86% |
| ME-QI-QR | Merge Sort | 8 | 30 | 30 | 170.29 | 9.22 | [166.84; 173.73] | 2.02% |

## Observacoes

- Os resultados valem para o ambiente registrado acima e para a entrada descrita. Outras condicoes exigem novos experimentos.
