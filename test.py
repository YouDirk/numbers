#!/usr/bin/python3
###!/usr/bin/env python

import sympy as sym

def my_gcd(a: int, b: int) -> int:
    while b != 0:
        (a, b) = (b, a % b)
    return a

# my_gcdex(a, b) -> (d, x, y)
#
#   gcd(a, b) = d = x*a + y*b
#
# It is possible that d < 0.
def my_gcdex(a: int, b: int) -> (int, int, int):
    (q, u, x, v, y) = (0, 0, 1, 1, 0)
    while b != 0:
        (q, x, y, u, v) = (a // b, u - q*x, v - q*y, x, y)
        #print("%3d %3d %3d %3d %3d %3d %3d" % (a, b, q, u, x, v, y))
        (a, b) = (b, a % b)
    return (a, x, y)

# my_gcdex(a, b) -> (d, x, y)
#
#   gcd(a, b) = d = x*a + y*b
#
# Make sure that d >= 0.
def my_gcdex_pos(a: int, b: int) -> (int, int, int):
    if a < 0: a, x_sign = -a, -1
    else: x_sign = 1

    if b < 0: b, y_sign = -b, -1
    else: y_sign = 1

    (d, x, y) = my_gcdex(a, b)
    return (d, x_sign*x, y_sign*y)

def main():
    print(my_gcd(1071, 462) == 21,
          my_gcd(44, 12) == 4,
          my_gcd(55, 34) == 1,
          my_gcd(78, 99) == 3,
          sym.gcdex(99, 78) == (-11, 14, 3),
          my_gcdex(99, 78) == (3, -11, 14),
          my_gcdex(78, 99) == (3, 14, -11),
          my_gcdex(0, 1) == (1, 0, 1),
          my_gcdex(1, 0) == (1, 1, 0),
          my_gcdex(-78, 99) == (3, -14, -11),
          my_gcdex(78, -99) == (-3, -14, -11),
          my_gcdex_pos(78, -99) == (3, 14, 11),
          my_gcdex(99, -78) == (-3, 11, 14),
          my_gcdex(-99, 78) == (3, 11, 14),
          my_gcdex_pos(99, -78) == (3, -11, -14),
          my_gcdex(-78, -99) == (-3, 14, -11),
          my_gcdex(-99, -78) == (-3, -11, 14),
          my_gcdex_pos(-78, -99) == (3, -14, 11),
          my_gcdex_pos(-99, -78) == (3, 11, -14)
          )

main()
