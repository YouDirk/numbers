#!/usr/bin/env python3

# Numbers, some tests with numbers, using number theory.
# Copyright (C) 2022  Dirk "YouDirk" Lehmann.  All rights reserved.

import sympy as sym

from sympy import init_printing
from sympy import Wild, ZZ, QQ, CC, I, exp, pi, sqrt, cos, sin
from sympy.core.numbers import Expr, Add, Mul, Pow, Integer
from sympy.abc import x

# from sympy.printing.tree import tree

def pprint(obj):
    #sym.pprint(obj)
    print(obj)

def _simplify_add_ofcos(wexp: Expr, wadd: Expr) -> Expr:
    if not isinstance(wadd, Add): return x**wexp * wadd

    result_add = 0
    it = iter(wadd.args)

    a = next(it, None)
    b = next(it, None)
    while a != None:
        # A != NONE and B maybe NONE
        if isinstance(a, Mul) and isinstance(b, Mul) \
          and isinstance(a.args[0], Integer) and a.args[0] == b.args[0] \
          and isinstance(a.args[1], cos) \
          and isinstance(b.args[1], cos):
            result_add += a.args[0]*2 \
              * cos((b.args[1].args[0] + a.args[1].args[0])/2) \
              * cos((b.args[1].args[0] - a.args[1].args[0])/2)
            a, b = next(it, None), next(it, None); continue

        # B maybe NONE
        result_add += a

        a = b
        b = next(it, None)

    # ??? not working for n has primefactors greater than 5 (>= 7) ???
    return x**wexp * result_add
    #return x**wexp * result_add.evalf()

def main():
    init_printing(use_unicode=None, num_columns=250)

    # ---
    do_cyclotomic = False
    n = 15
    # ---

    f_n = x**n - 1

    g_n = 1
    for k in range(1, n+1):
        # cyclonomic check ...
        if do_cyclotomic and sym.igcd(k, n) != 1: continue

        g_n *= (x - exp(k*2*pi*I/n))

    print("\nf_n(x) ="); pprint(f_n)
    print("\ng_n(x) ="); pprint(g_n)

    f_zero = sym.solve(f_n)
    print("\nf_n(x_0) = 0:"); pprint(f_zero)
    g_zero = sym.solve(g_n)
    print("\ng_n(x_0) = 0:"); pprint(g_zero)

    for k in range(len(g_zero)):
        g_zero[k] = g_zero[k] \
                    .replace(exp,
                             lambda a: (cos(a/I) + I*sin(a/I))) \
                    .expand()
    f_zero = sorted(f_zero, key=lambda e: str(e))
    g_zero = sorted(g_zero, key=lambda e: str(e))

    print("\nzeros: f_n**{-1}(0) == g_n**{-1}(0) == x_0: %s"
          % (f_zero == g_zero))

    g_n = g_n.expand()
    g_n = g_n.replace(exp,
                      lambda a: (cos(a/I) + I*sin(a/I)))
    g_n = g_n.expand()
    g_n = g_n.collect(x)

    #print("\ng_n(x) ="); pprint(g_n)
    wadd = Wild('wadd'); wexp = Wild('wexp')
    g_n = g_n.replace(x**wexp * wadd, _simplify_add_ofcos)

    if g_n == f_n: print("\nequals: f_n(x) == g_n(x): True")
    else: print("\ng_n(x) ="); pprint(g_n)

main()
