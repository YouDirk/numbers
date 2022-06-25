#!/usr/bin/env python3

# Numbers, some tests with numbers, using number theory.
# Copyright (C) 2022  Dirk "YouDirk" Lehmann.  All rights reserved.

import sympy as sym
import sympy.ntheory as nth

def coprimes(n: int) -> list:
    result = []
    for i in range(n):
        if sym.gcd(i, n) == 1:
            result.append(i)
    return result

def mod_space(n: int) -> list:
    D = list(filter(lambda i: n%i == 0, range(1, n)))

    result = []
    for d in D:
        cur_gcd2d \
            = list(filter(lambda k: sym.gcd(k, n) == d, range(1, n)))
        result.append({d: cur_gcd2d})

    return result

def main():
    m = 15
    #p1 = nth.generate.randprime(1, m)
    p1 = 2
    while (p2 := nth.generate.randprime(1, m)) == p1: pass
    while (p3 := nth.generate.randprime(1, m)) == p1 or p3 == p2: pass
    while (p4 := nth.generate.randprime(1, m)) == p1 or p4 == p2 \
           or p4 == p3: pass
    while (p5 := nth.generate.randprime(1, m)) == p1 or p5 == p2 \
           or p5 == p3 or p5 == p4: pass
    while (p6 := nth.generate.randprime(1, m)) == p1 or p6 == p2 \
           or p6 == p3 or p6 == p4 or p6 == p5: pass
    n = p1*p1*p1*p1 * p1*p4*p5*p6

    print("\np1=%d, p2=%d, p3=%d, p4=%d, p5=%d, p6=%d" \
          % (p1, p2, p3, p4, p5, p6))

    #result = nth.totient(n)
    #result = coprimes(n)

    result = mod_space(n)
    result_flat = []
    for v in result:
        for i in v[list(v)[0]]: result_flat.append(i)
    result_flat = sorted(result_flat)

    print("\nn=%d, len(d)=%d" % (n, len(result)))
    print("\nd=%s" % ({list(v)[0]: nth.primefactors(list(v)[0]) \
                       for v in result}))
    print("\n%s, %s" % (result_flat == list(range(1, n)), result_flat))

main()
