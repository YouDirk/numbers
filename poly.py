#!/usr/bin/env python3

# Numbers, some tests with numbers, using number theory.
# Copyright (C) 2022  Dirk "YouDirk" Lehmann.  All rights reserved.

import sympy as sym

from sympy import ZZ, QQ
from sympy.abc import x

# For all n>0 in N:
#   (x^n - 1) mod phi_n(x) = 0
#
# But for all n>0 in N and 0<i<n, using i in N:
#   (x^i - 1) mod phi_n(x) != 0
#
# For any n in N, phi_n(x) is unique.
def main():
    n = 4
    phi_n = x**2 + 1
    #n = 7                               # n is in P
    #phi_n = x**6 + x**5 + x**4 + x**3 + x**2 + x**1 + x**0
    #n = 14                              # n=2*p with p=6 in P
    #phi_n = x**6 - x**5 + x**4 - x**3 + x**2 - x**1 + x**0
    #n = 25                              # n=p^2 with p=5 in P
    #phi_n = x**(4*5**(2-1)) + x**(3*5**(2-1)) + x**(2*5**(2-1)) \
    #        + x**(1*5**(2-1)) + + x**(0*5**(2-1))

    for i in range(n, 0, -1):
        divisor = (x**i - 1)

        result = sym.div(divisor, phi_n, domain=ZZ)
        print("%s: (x**%d - 1)/phi_%d(x) = (%s)/(%s)\n"
              "                           = (%s)\n"
              "                           + (%s)"
              % (result[1] == 0, i, n , divisor, phi_n, result[0],
                 result[1]))

main()
