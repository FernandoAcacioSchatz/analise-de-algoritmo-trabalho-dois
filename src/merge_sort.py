def _merge_sort(v, buf, lo, hi):
    if lo >= hi:
        return
    meio = (lo + hi) // 2
    _merge_sort(v, buf, lo, meio)
    _merge_sort(v, buf, meio + 1, hi)

    i, j, k = lo, meio + 1, lo
    while i <= meio and j <= hi:
        if v[i] <= v[j]:
            buf[k] = v[i]
            i += 1
        else:
            buf[k] = v[j]
            j += 1
        k += 1
    while i <= meio:
        buf[k] = v[i]
        i += 1
        k += 1
    while j <= hi:
        buf[k] = v[j]
        j += 1
        k += 1
    for k in range(lo, hi + 1):
        v[k] = buf[k]


def merge_sort(v):
    n = len(v)
    if n < 2:
        return v
    buf = [0] * n
    _merge_sort(v, buf, 0, n - 1)
    return v
