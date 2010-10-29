#!/usr/bin/python

import math

def sqrt_nr(a, n, accuracy):
    x = 1.0
    for i in range(n):
        xnew = (x + a/x)/2
        delta = xnew - x
        x = xnew
        print xnew, delta
        if abs(delta) < accuracy:
            break
    return x

# http://medialab.freaknet.org/martin/src/sqrt/
def sqrt_abacus(a):
    op = a
    res = 0
    one = 1 << 30
    while one != 0:
        if (op >= res + one):
            op -= res + one
            res += 2 * one
        res /= 2
        one /= 4
    return res




print math.sqrt(10)

print sqrt_nr(10, 10, 0.001)

print sqrt_abacus(2000000)
print sqrt_abacus(3000000)

