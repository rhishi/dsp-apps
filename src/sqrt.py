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
    assert (a < 1 << 32)    
    op = a & 0xFFFFFFFF
    res = 0
    one = 1 << 30
    factor = 1 << 16
    while one != 0:
        if (op >= res + one):
            op -= res + one
            res += 2 * one
        res /= 2
        one /= 4
        factor /= 2
        print op, res, one, op + (res/factor)**2
    return res


for x in [3, 4, 8, 9, 32, 33, 34, 40, 63, 64, 80]:
    n = 1 << x
    print "1 << {0} is {1:#x} {2}".format(x, n, type(n))
    print "1 << {0} - 1 is {1:#x} {2}".format(x, n-1, type(n-1))

print -1
print -1 & 0xFF



print math.sqrt(10)

print sqrt_nr(10, 10, 0.001)

print sqrt_abacus(2000000)
print sqrt_abacus(3000000)
print sqrt_abacus(20)
print sqrt_abacus(31)
print sqrt_abacus(15)
print sqrt_abacus(63)
print sqrt_abacus(0xFFFFFFFF)

