#!/usr/bin/python

import math

# http://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Digit-by-digit_calculation
def sqrt_digit_by_digit(a):
    assert (a < 1 << 32)    
    a &= 0xFFFFFFFF
    rem = 0
    root = 0
    for i in range(16):        
        twobits = a >> (30 - 2*i) & 3
        rem = twobits + (rem << 2)
        root = root << 1;
        trial = (root << 1) + 1
        if rem >= trial:
            rem = rem - trial
            root = root + 1
        assert (a >> (30 - 2*i) == root**2 + rem)
    assert (a == root**2 + rem)
    return root

print sqrt_digit_by_digit(4)
print sqrt_digit_by_digit(100)
print sqrt_digit_by_digit(2000000)
print sqrt_digit_by_digit(3000000)
print sqrt_digit_by_digit(20)
print sqrt_digit_by_digit(31)
print sqrt_digit_by_digit(15)
print sqrt_digit_by_digit(63)
print sqrt_digit_by_digit(0xFFFFFFFF)




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
    a &= 0xFFFFFFFF
    rem = a
    root = 0
    one = 1 << 30
    factor = 1 << 16
    while one != 0:
        if (rem >= root + one):
            rem -= root + one
            root += 2 * one
        root /= 2
        one /= 4
        factor /= 2
        assert (a == rem + (root/factor)**2)
    assert (factor == 1)
    assert (a == root**2 + rem)
    return root


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

