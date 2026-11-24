from particao import particiona


def quick_sort_iterativo(v):
    n = len(v)
    if n < 2:
        return v

    pilha = [(0, n - 1)]
    while pilha:
        lo, hi = pilha.pop()
        if lo >= hi:
            continue
        p = particiona(v, lo, hi)

        tam_esq = (p - 1) - lo
        tam_dir = hi - (p + 1)
        if tam_esq > tam_dir:
            pilha.append((lo, p - 1))
            pilha.append((p + 1, hi))
        else:
            pilha.append((p + 1, hi))
            pilha.append((lo, p - 1))
    return v
