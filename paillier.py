#!/usr/bin/python3
###!/usr/bin/env python

import random

import numpy as np
import sympy as sym
import sympy.ntheory as nth

# ********************************************************************

def genkeypair(bits: int) -> dict:
    print("Generating key pair... ", end='', flush=True)
    start = 1 << (bits - 1)                  # min = 2^(l-1)
    end = 1 << bits                          # max = 2^l - 1
    p1 = nth.generate.randprime(start, end)
    p2 = nth.generate.randprime(start, end)
    #p1 = nth.generate.prevprime(end)
    #p2 = nth.generate.prevprime(p1)
    pub = p1*p2                              # P_min: 2^(2*(l-1))
    priv = (p1 - 1)*(p2 - 1)                 # P_max: 2^(2*l) - 1
    print("done.", flush=True)
    return {"public": [bits, pub], "private": [bits, priv]}

def _assert_keypair(keypair: list):
    assert(sym.igcd(keypair["public"][1], keypair["private"][1]) == 1)
    # PUB = P1*P2
    #   => !coprime(PUB, P1-1) and !coprime(PUB, P2-1)
    #   => gcd(PUB, (P1 - 1)*(P2 - 1)) == 1
    #   => gcd(PUB, PRIV) == 1

# ********************************************************************

def encode(pubkey: list, z: int) -> int:
    print("Encode... ", end='', flush=True)
    bits = pubkey[0]
    plain_end = 1 << (2*(bits - 1))     # z < P_min = 2^(2*(l-1))
    assert(z < plain_end)
    pub = pubkey[1]
    r = random.randrange(1, plain_end)
    # 1 <= R <= P-1 and !coprime(R, P)
    #   => P == P1*P2 => r != P1 and r != P2
    #   => just all 1 <= R <= P-1 are coprimes to P

    print("done.", flush=True)
    return ((pub + 1)**z * r**pub) % (pub*pub)

def _assert_encode(pubkey: list, c: int):
    bits = pubkey[0]
    assert(c < (1 << (4*bits)))
    # c < (P**2) = P1*P2*P1*P2 < 2**(4*l)

# ********************************************************************

def _mod_inverse(a: int, n: int) -> int:
    print("mod_inverse...", end='', flush=True)
    # gcd(a, n) = G = X*A + Y*N
    x, y, g = sym.core.numbers.igcdex(a, n)
    assert(g == 1)                      # A and N are coprimes
    print("done. ", end='', flush=True)
    return x % n                        # 1 = X*A (mod N) => X = A^-1

def decode(keypair: dict, c: int) -> int:
    print("Decode... ", end='', flush=True)
    bits = keypair["public"][0]
    cipher_end = 1 << (4*bits)
    assert(c < cipher_end)
    pub = keypair["public"][1]
    priv = keypair["private"][1]

    frac_float = (((c**priv) % (pub*pub)) - 1) / pub
    assert(frac_float.is_integer())     # integer division possible

    priv_mod_inverse = _mod_inverse(priv, pub) #sym.mod_inverse(priv, pub)

    print("done.", flush=True)
    return (int(frac_float)*priv_mod_inverse) % pub

# ********************************************************************

def homomorph_add(pubkey: list, c1: int, c2: int) -> int:
    print("Adding... ", end='', flush=True)
    bits = pubkey[0]
    cipher_end = 1 << (4*bits)
    assert(c1 < cipher_end and c2 < cipher_end)
    pub = pubkey[1]
    print("done.", flush=True)
    return (c1*c2) % (pub*pub)

# ********************************************************************

def main():
    bits = 8
    keypair = genkeypair(bits)
    _assert_keypair(keypair)

    z1 = (1 << 2*(bits - 1)) - 1 # 16383
    z2 = z1 - 1

    c1 = encode(keypair["public"], z1)
    _assert_encode(keypair["public"], c1)
    c2 = encode(keypair["public"], z2)
    c_sum = homomorph_add(keypair["public"], c1, c2)

    z1_dec = decode(keypair, c1)
    z2_dec = decode(keypair, c2)
    zsum_dec = decode(keypair, c_sum)

    # plain_max needs to be adapted (Z in Z_space subset Z_P)
    arith_sum = (z1 + z2) % keypair["public"][1]
    if z1 + z2 != arith_sum:
        print("\nwarning: z1 + z2 mod P fixed!")

    print("\n%s\n"
          "  z1 = %d, c1 = %d, z1_dec = %d\n"
          "  z2 = %d, c2 = %d, z2_dec = %d\n"
          "  sum = %d, c_sum = %d, zsum_dec = %d"
          % (keypair, z1, c1, z1_dec, z2, c2, z2_dec,
             arith_sum, c_sum, zsum_dec))
    print("{pub = 0x%x, priv = 0x%x}\n"
          "  z1 = 0x%x, c1 = 0x%x, z1_dec = 0x%x\n"
          "  z2 = 0x%x, c2 = 0x%x, z2_dec = 0x%x\n"
          "  sum = 0x%x, c_sum = 0x%x, zsum_dec = 0x%x"
          % (keypair["public"][1], keypair["private"][1],
             z1, c1, z1_dec, z2, c2, z2_dec, arith_sum, c_sum, zsum_dec))

    assert(z1 == z1_dec and z2 == z2_dec and arith_sum == zsum_dec)

# ********************************************************************

main()
