#!/usr/bin/env python3

# Numbers, some tests with numbers, using number theory.
# Copyright (C) 2022  Dirk "YouDirk" Lehmann.  All rights reserved.

from math import *

def _my_comb(n: int, k: int, l: int, out: bool=False) -> int:
    if l >= 4:
        if out: print("(")
        a = _my_comb(n, k, l-1, out)
        if out: print(") - (", end='')
        b = _my_comb(n - 2, k - 1, l-2, out)
        if out: print("\n)", end='')
        return a - b

    if out: print("c(%d, %d, %d)" % (n, k, l), end='')

    if n < 0 or k < 0: return 0

    if n < 2 or k < 1: return comb(n, k)

    return comb(n, k) - (l-1)*comb(n - 2, k - 1)

def print_cur(n: int, a: list):
    sp = str(3)
    l = len(a)

    for i in range(0, n-l + 1):
        print(("%"+sp+"s ") % (''), end='')
    for i in range(0, l):
        print(("%"+sp+"d %"+sp+"s ") % (a[i], ''), end='')
    print("")

def main():
    n = 8
    l = 6

    for i in range(1, n+1):
        cur = list(map(lambda a: _my_comb(i, a, l),
                       [k for k in range(0, i+1)]))
        print_cur(n, cur)

    print("\nn=%d, l=%d, len(d) = %d" \
          % (n, l, sum(cur[0:len(cur)-1])))

    #n, k, l = 8, 4, 7
    #print("\nn=%d, k=%d, l=%d: %d"
    #      % (n, k, l, _my_comb(n, k, l, True)))

main()
