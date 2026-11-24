from particao import particiona


def _qs_recursivo(v, lo, hi):
    if lo < hi:
        p = particiona(v, lo, hi)
        _qs_recursivo(v, lo, p - 1)
        _qs_recursivo(v, p + 1, hi)


def quick_sort_recursivo(v):
    if len(v) > 1:
        _qs_recursivo(v, 0, len(v) - 1)
    return v
