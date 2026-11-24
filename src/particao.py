def _mediana_de_tres(v, lo, hi):
    meio = (lo + hi) // 2
    if v[lo] > v[meio]:
        v[lo], v[meio] = v[meio], v[lo]
    if v[lo] > v[hi]:
        v[lo], v[hi] = v[hi], v[lo]
    if v[meio] > v[hi]:
        v[meio], v[hi] = v[hi], v[meio]
    v[meio], v[hi] = v[hi], v[meio]


def particiona(v, lo, hi):
    _mediana_de_tres(v, lo, hi)
    pivo = v[hi]
    i = lo - 1
    for j in range(lo, hi):
        if v[j] <= pivo:
            i += 1
            v[i], v[j] = v[j], v[i]
    v[i + 1], v[hi] = v[hi], v[i + 1]
    return i + 1
