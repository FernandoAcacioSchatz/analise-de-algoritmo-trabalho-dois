# Análise experimental de algoritmos de ordenação

Trabalho 2 da disciplina Análise de Algoritmos (FURB, Prof. Artur Ricardo Bizon).

Comparação do tempo de execução de três algoritmos de ordenação sobre a mesma entrada:

- **QR**: Quick Sort Recursivo
- **QI**: Quick Sort Iterativo (mesma partição, com pilha explícita)
- **ME**: Merge Sort (com um único vetor auxiliar)

O relatório completo está em [`relatorio/relatorio.pdf`](relatorio/relatorio.pdf).

## Estrutura

```
.
├── src/                       código dos algoritmos e da coleta
│   ├── particao.py            partição de Lomuto com mediana de três (usada pelos dois Quick Sorts)
│   ├── quick_sort_recursivo.py
│   ├── quick_sort_iterativo.py
│   ├── merge_sort.py
│   ├── entrada.py             gera, salva e carrega a entrada compartilhada
│   └── experimento.py         coleta dos tempos nos seis formatos de rodízio
├── dados/                     resultados da coleta
│   ├── entrada.csv            a lista ordenada pelos três algoritmos
│   ├── formato_QR-QI-ME.csv   um CSV por formato de rodízio (são seis)
│   ├── ...
│   └── LEIA-ME.md             ambiente, desenho, n calculado e precisão atingida
├── Graficos_Analise.ipynb     gráficos por algoritmo e por formato (matplotlib)
├── Anova_Tukey.ipynb          ANOVA e teste de Tukey nos formatos com ICs sobrepostos
└── relatorio/                 relatório no formato SBC (LaTeX)
```

## Metodologia em resumo

- **Entrada:** permutação aleatória dos inteiros de 0 a 99.999 (100.000 valores distintos), com semente 42. A mesma lista é usada pelos três algoritmos.
- **Medição:** `time.perf_counter_ns()`, com o coletor de lixo desligado durante a ordenação. A cópia da entrada e a verificação do resultado ficam fora do cronômetro.
- **Rodízio:** as seis ordens possíveis dos três algoritmos, incluindo as rotações cíclicas, para que cada algoritmo ocupe cada posição.
- **Aquecimento:** 18 rodadas descartadas antes da coleta.
- **Número de execuções:** após uma amostragem piloto de 30 rodadas por formato, calcula-se o menor `n` que garante erro relativo de 5% com 95% de confiança. O `n` de cada formato é o maior dos três algoritmos.
- **Análise:** média, desvio padrão e intervalo de confiança de 95%. Quando os ICs se sobrepõem, aplica-se ANOVA de um fator e teste de Tukey HSD.

## Como rodar

### Requisitos

- Python 3.13 (versão usada no trabalho)
- Bibliotecas: `numpy`, `scipy`, `pandas`, `matplotlib`, `ipykernel`

```
pip install numpy scipy pandas matplotlib ipykernel
```

### 1. Gerar a entrada

```
python src/entrada.py
```

Cria `dados/entrada.csv`. A coleta espera esse arquivo; se ele não existir, `experimento.py` o cria.

### 2. Rodar a coleta

```
python src/experimento.py
```

Demora cerca de 2 a 3 minutos. Gera os seis `dados/formato_*.csv` e o `dados/LEIA-ME.md`.

**Atenção:** esse comando sobrescreve os CSVs e o `LEIA-ME.md`. Cada execução mede tempos diferentes, então os números vão variar um pouco. Para uma comparação justa, feche outros programas pesados antes de rodar.

### 3. Gráficos e análise

Abra os notebooks no Jupyter ou no VS Code e use **Executar tudo**:

- `Graficos_Analise.ipynb`: gráficos por algoritmo e por formato. Lê os CSVs de `dados/`.
- `Anova_Tukey.ipynb`: decide, para cada formato, se o desafio extra (ANOVA e Tukey) é necessário, e roda a análise nesses formatos.

Os notebooks não gravam arquivos. Só leem os CSVs e mostram os resultados.

### 4. Compilar o relatório

Dentro da pasta `relatorio/`, com uma distribuição LaTeX instalada (MiKTeX ou TeX Live):

```
pdflatex relatorio.tex
bibtex relatorio
pdflatex relatorio.tex
pdflatex relatorio.tex
```

Ou, no Overleaf, envie a pasta `relatorio/` e compile com pdfLaTeX.

## Resultados principais

- O **Merge Sort** foi o mais lento em todos os formatos, com média global de cerca de 173 ms, contra cerca de 99 ms do QR e 104 ms do QI.
- O **Quick Sort Recursivo** teve a menor média global. A vantagem sobre o Iterativo é de cerca de 5%, e só é estatisticamente clara em três dos seis formatos.
- Nos três formatos com ICs sobrepostos, a ANOVA é significativa, e o teste de Tukey não encontra diferença entre QR e QI.

Detalhes e tabelas completas estão no relatório e no `dados/LEIA-ME.md`.

## Limitações

- Os tempos dependem da máquina e do estado do sistema no momento da coleta. Os resultados valem para o ambiente descrito no `LEIA-ME.md`.
- Apenas um tamanho de entrada (100.000) e uma distribuição (permutações de inteiros distintos) foram testados.
- Os algoritmos foram implementados em Python. Uma implementação em linguagem compilada teria tempos bem diferentes.
- As premissas da ANOVA (normalidade) não se confirmam em todos os grupos. Com 30 a 36 rodadas por grupo, a análise é considerada robusta, mas isso fica registrado.

## Autores

Fernando Acácio Schatz e Yuri Oliveira di Golfeto.
