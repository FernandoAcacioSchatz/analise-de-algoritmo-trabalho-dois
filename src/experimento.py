import csv
import gc
import itertools
import os
import platform
import sys
import time

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entrada import ARQUIVO_ENTRADA, RAIZ, carrega_entrada, gera_entrada, salva_entrada
from merge_sort import merge_sort
from quick_sort_iterativo import quick_sort_iterativo
from quick_sort_recursivo import quick_sort_recursivo

NOMES = {"QR": "Quick Sort Recursivo", "QI": "Quick Sort Iterativo", "ME": "Merge Sort"}
FUNCOES = {"QR": quick_sort_recursivo, "QI": quick_sort_iterativo, "ME": merge_sort}
SIGLAS = ["QR", "QI", "ME"]
FORMATOS = list(itertools.permutations(SIGLAS))

ERRO_RELATIVO = 0.05
CONFIANCA = 0.95
N_AQUECIMENTO = 18
N_PILOTO = 30
N_MAXIMO = 1000

DADOS = os.path.join(RAIZ, "dados")
LEIA_ME = os.path.join(DADOS, "LEIA-ME.md")

CABECALHO = ["fase", "rodada", "descartada", "formato", "posicao",
             "algoritmo", "n_elementos", "tempo_ms"]


def nome_formato(formato):
    return "-".join(formato)


def arquivo_formato(formato):
    return os.path.join(DADOS, "formato_{}.csv".format(nome_formato(formato)))


def cronometra(sigla, dados):
    v = dados.copy()
    gc.collect()
    gc.disable()
    try:
        t0 = time.perf_counter_ns()
        FUNCOES[sigla](v)
        t1 = time.perf_counter_ns()
    finally:
        gc.enable()
    return (t1 - t0) / 1e6, v


def executa_rodada(dados, esperado, rodada, formato, fase, descartada, registros):
    for posicao, sigla in enumerate(formato, 1):
        tempo, v = cronometra(sigla, dados)
        if v != esperado:
            raise AssertionError("ordenacao incorreta: {} na rodada {}".format(sigla, rodada))
        registros[formato].append([
            fase, rodada, "sim" if descartada else "nao", nome_formato(formato),
            posicao, NOMES[sigla], len(dados), tempo,
        ])


def tempos_validos(linhas, algoritmo):
    return [l[7] for l in linhas if l[2] == "nao" and l[5] == algoritmo]


def n_necessario(amostra):
    x = np.asarray(amostra, dtype=float)
    media = x.mean()
    s = x.std(ddof=1)
    razao = s / (ERRO_RELATIVO * media)
    for n in range(2, N_MAXIMO + 2):
        t = stats.t.ppf(1 - (1 - CONFIANCA) / 2, df=n - 1)
        if n >= (t * razao) ** 2:
            return n, media, s
    return N_MAXIMO + 1, media, s


def erro_atingido(amostra):
    x = np.asarray(amostra, dtype=float)
    n = len(x)
    t = stats.t.ppf(1 - (1 - CONFIANCA) / 2, df=n - 1)
    return t * x.std(ddof=1) / np.sqrt(n) / x.mean()


def salva_csv(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CABECALHO)
        for l in linhas:
            w.writerow(l[:7] + ["{:.6f}".format(l[7])])


def main():
    print("=" * 72)
    print("TRABALHO 2 - COLETA EXPERIMENTAL POR FORMATO DE RODIZIO")
    print("=" * 72)
    print("Processador :", platform.processor() or platform.machine())
    print("SO          :", platform.system(), platform.release())
    print("Python      :", platform.python_implementation(), platform.python_version())
    print("Formatos    :", len(FORMATOS), "->", ", ".join(nome_formato(f) for f in FORMATOS))
    print()

    if not os.path.exists(ARQUIVO_ENTRADA):
        salva_entrada(gera_entrada())
    dados = carrega_entrada()
    esperado = list(range(len(dados)))
    if sorted(dados) != esperado:
        raise SystemExit("entrada invalida: nao e permutacao de 0..n-1")
    print("Entrada: {} inteiros distintos, permutacao de 0 a {}, embaralhada".format(
        len(dados), len(dados) - 1))
    print()

    registros = {f: [] for f in FORMATOS}
    rodada = 0
    inicio = time.perf_counter()

    print("[1/4] Aquecimento: {} rodadas descartadas".format(N_AQUECIMENTO))
    for i in range(N_AQUECIMENTO):
        rodada += 1
        executa_rodada(dados, esperado, rodada, FORMATOS[i % len(FORMATOS)],
                       "aquecimento", True, registros)
    print("  concluido")
    print()

    print("[2/4] Amostragem piloto: {} rodadas validas por formato".format(N_PILOTO))
    for i in range(N_PILOTO * len(FORMATOS)):
        rodada += 1
        executa_rodada(dados, esperado, rodada, FORMATOS[i % len(FORMATOS)],
                       "piloto", False, registros)
        if rodada % 60 == 0:
            print("  rodada {} ({:.0f}s)".format(rodada, time.perf_counter() - inicio))
    print("  concluido")
    print()

    print("[3/4] Calculo de n por formato (erro 5%, confianca 95%)")
    n_adotado = {}
    calculo = {}
    for f in FORMATOS:
        linhas = registros[f]
        por_alg = {}
        for s in SIGLAS:
            amostra = tempos_validos(linhas, NOMES[s])
            n, media, sd = n_necessario(amostra)
            por_alg[s] = {"n": n, "media": media, "desvio": sd}
        maior = max(v["n"] for v in por_alg.values())
        n_adotado[f] = max(N_PILOTO, min(maior, N_MAXIMO))
        calculo[f] = por_alg
        print("  {:<10} " .format(nome_formato(f)) + "  ".join(
            "{}: n={}".format(s, por_alg[s]["n"]) for s in SIGLAS)
            + "  -> adotado {}".format(n_adotado[f]))
    print()

    print("[4/4] Coleta final por formato")
    restantes = {f: n_adotado[f] - N_PILOTO for f in FORMATOS}
    while any(v > 0 for v in restantes.values()):
        for f in FORMATOS:
            if restantes[f] > 0:
                rodada += 1
                executa_rodada(dados, esperado, rodada, f, "final", False, registros)
                restantes[f] -= 1
                if rodada % 60 == 0:
                    print("  rodada {} ({:.0f}s)".format(rodada, time.perf_counter() - inicio))
    print("  concluido")
    print()

    for f in FORMATOS:
        salva_csv(arquivo_formato(f), registros[f])
        print("  -> dados/{}  ({} linhas)".format(os.path.basename(arquivo_formato(f)),
                                                  len(registros[f])))

    resumo = []
    for f in FORMATOS:
        for s in SIGLAS:
            amostra = tempos_validos(registros[f], NOMES[s])
            x = np.asarray(amostra, dtype=float)
            erro = erro_atingido(amostra)
            t = stats.t.ppf(1 - (1 - CONFIANCA) / 2, df=len(x) - 1)
            margem = t * x.std(ddof=1) / np.sqrt(len(x))
            resumo.append({
                "formato": nome_formato(f), "algoritmo": NOMES[s],
                "n_calculado": calculo[f][s]["n"], "n_adotado": n_adotado[f],
                "validas": len(x), "media": x.mean(), "desvio": x.std(ddof=1),
                "ic_inf": x.mean() - margem, "ic_sup": x.mean() + margem,
                "erro_relativo": erro,
            })

    escreve_leia_me(resumo, n_adotado, calculo, rodada, time.perf_counter() - inicio)

    print("=" * 72)
    print("Coleta concluida. Documentacao: dados/LEIA-ME.md")
    print("=" * 72)


def escreve_leia_me(resumo, n_adotado, calculo, total_rodadas, duracao):
    os.makedirs(DADOS, exist_ok=True)
    linhas = []
    linhas.append("# Dados da coleta experimental\n")
    linhas.append("Gerado automaticamente por `src/experimento.py` em "
                  "{}.\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    linhas.append("## Ambiente\n")
    linhas.append("- Processador: {}".format(platform.processor() or platform.machine()))
    linhas.append("- Sistema: {} {}".format(platform.system(), platform.release()))
    linhas.append("- Python: {} {}".format(platform.python_implementation(),
                                            platform.python_version()))
    linhas.append("- Duracao total da coleta: {:.0f} s, {} rodadas\n".format(duracao, total_rodadas))
    linhas.append("## Entrada\n")
    linhas.append("- {} inteiros distintos, permutacao de 0 a {}, embaralhada com "
                  "semente 42.".format(100_000, 99_999))
    linhas.append("- Arquivo: `dados/entrada.csv`.\n")
    linhas.append("## Desenho\n")
    linhas.append("- Os 3 algoritmos (QR = Quick Sort Recursivo, QI = Quick Sort Iterativo, "
                  "ME = Merge Sort) sao executados em todas as 6 ordens possiveis, "
                  "uma ordem por formato.")
    linhas.append("- Cada rodada executa os 3 algoritmos na ordem do formato, sobre a "
                  "mesma entrada. Cada algoritmo recebe uma copia, feita fora do "
                  "cronometro.")
    linhas.append("- Aquecimento: {} rodadas descartadas, alternando os formatos.".format(
        N_AQUECIMENTO))
    linhas.append("- Amostragem piloto: {} rodadas validas por formato.".format(N_PILOTO))
    linhas.append("- Calculo de n por formato, apos o piloto: para cada algoritmo, o menor n "
                  "tal que n >= (t(0,025; n-1) * s / (0,05 * media))^2. O n do formato e o "
                  "maior dos tres, com piso em {} e teto de {}.".format(N_PILOTO, N_MAXIMO))
    linhas.append("- Coleta final: rodadas ate atingir o n adotado de cada formato, "
                  "alternando os formatos a cada passagem.")
    linhas.append("- Medicao: `time.perf_counter_ns()`, coletor de lixo desligado durante "
                  "a ordenacao.")
    linhas.append("- Verificacao: o resultado de cada ordenacao e comparado com `0..n-1` "
                  "fora do cronometro.\n")
    linhas.append("## Arquivos\n")
    for f in FORMATOS:
        linhas.append("- `dados/formato_{}.csv`: rodadas do formato {}.".format(
            nome_formato(f), " > ".join(f)))
    linhas.append("")
    linhas.append("Colunas de cada CSV:\n")
    linhas.append("- `fase`: aquecimento, piloto ou final.")
    linhas.append("- `rodada`: numero da rodada na coleta inteira.")
    linhas.append("- `descartada`: sim (aquecimento) ou nao.")
    linhas.append("- `formato`: ordem de execucao da rodada, por exemplo QR-QI-ME.")
    linhas.append("- `posicao`: posicao do algoritmo na rodada (1, 2 ou 3).")
    linhas.append("- `algoritmo`: nome do algoritmo.")
    linhas.append("- `n_elementos`: tamanho da entrada.")
    linhas.append("- `tempo_ms`: tempo de ordenacao em milissegundos.\n")
    linhas.append("## Resultado do calculo de n e precisao\n")
    linhas.append("`erro_relativo` = t * s / sqrt(N) / media, com N as rodadas validas do "
                  "algoritmo no formato. Deve ser <= 0,05 para a precisao exigida.\n")
    linhas.append("| Formato | Algoritmo | n calculado | n adotado | validas | media (ms) | "
                  "desvio (ms) | IC 95% (ms) | erro relativo |")
    linhas.append("|---|---|---|---|---|---|---|---|---|")
    for r in resumo:
        linhas.append("| {} | {} | {} | {} | {} | {:.2f} | {:.2f} | [{:.2f}; {:.2f}] | "
                      "{:.2%} |".format(
                          r["formato"], r["algoritmo"], r["n_calculado"], r["n_adotado"],
                          r["validas"], r["media"], r["desvio"], r["ic_inf"], r["ic_sup"],
                          r["erro_relativo"]))
    linhas.append("")
    linhas.append("## Observacoes\n")
    linhas.append("- Os resultados valem para o ambiente registrado acima e para a entrada "
                  "descrita. Outras condicoes exigem novos experimentos.")
    with open(LEIA_ME, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print("  -> dados/LEIA-ME.md")


if __name__ == "__main__":
    main()
