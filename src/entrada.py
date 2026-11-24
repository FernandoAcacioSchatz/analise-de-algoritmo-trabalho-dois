import csv
import os
import random


SEMENTE = 42
N_ELEMENTOS = 100_000

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_ENTRADA = os.path.join(RAIZ, "dados", "entrada.csv")


def gera_entrada(n=N_ELEMENTOS, semente=SEMENTE):
    rng = random.Random(semente)
    valores = list(range(n))
    rng.shuffle(valores)
    return valores


def salva_entrada(valores, caminho=ARQUIVO_ENTRADA):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["valor"])
        w.writerows([v] for v in valores)


def carrega_entrada(caminho=ARQUIVO_ENTRADA):
    with open(caminho, newline="", encoding="utf-8") as f:
        leitor = csv.reader(f)
        next(leitor)
        return [int(linha[0]) for linha in leitor]


if __name__ == "__main__":
    valores = gera_entrada()
    salva_entrada(valores)
    print("arquivo gerado :", os.path.relpath(ARQUIVO_ENTRADA, RAIZ))
    print("elementos      :", len(valores))
    print("releitura igual:", carrega_entrada() == valores)
