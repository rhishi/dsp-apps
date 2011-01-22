import math

def rotate_left32(x, r):
    assert (x < 1 << 32)
    assert (0 <= r)
    r %= 32
    x &= 0xFFFFFFFF
    leftpart = (x << r) & 0xFFFFFFFF
    rightpart = x >> (32 - r)
    result = leftpart + rightpart
    assert (result == leftpart | rightpart)
    return result

for x in [1, 1024, 5]:
    for r in range(34):
        result = rotate_left32(x, r)
        # print "rotate_left32 test: ", "%d %d %x" % (x, r, result)
        assert (r%32 != 0 or x == result)


def add32(x, y):
    assert (x < 1 << 32)
    assert (y < 1 << 32)
    result = (x + y) & 0xFFFFFFFF
    return result

# print "add32 test: ", add32(1073741824, 1073741824)
# print "add32 test: ", add32(1073741824, add32(1073741824, 1073741824))
# print "add32 test: ", add32(1073741824, add32(1073741824, add32(1073741824, 1073741824)))

# r specifies the per-round rotation amounts
R = []
R[ 0:16] = [ 7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22 ]
R[16:32] = [ 5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20 ]
R[32:48] = [ 4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23 ]
R[48:64] = [ 6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 ]

print "R =", R

KfromRFC = [
    # Round 1
    0xd76aa478, # 1
    0xe8c7b756, # 2
    0x242070db, # 3
    0xc1bdceee, # 4
    0xf57c0faf, # 5
    0x4787c62a, # 6
    0xa8304613, # 7
    0xfd469501, # 8
    0x698098d8, # 9
    0x8b44f7af, # 10
    0xffff5bb1, # 11
    0x895cd7be, # 12
    0x6b901122, # 13
    0xfd987193, # 14
    0xa679438e, # 15
    0x49b40821, # 16
    
    # Round 2
    0xf61e2562, # 17
    0xc040b340, # 18
    0x265e5a51, # 19
    0xe9b6c7aa, # 20
    0xd62f105d, # 21
    0x2441453, # 22
    0xd8a1e681, # 23
    0xe7d3fbc8, # 24
    0x21e1cde6, # 25
    0xc33707d6, # 26
    0xf4d50d87, # 27
    0x455a14ed, # 28
    0xa9e3e905, # 29
    0xfcefa3f8, # 30
    0x676f02d9, # 31
    0x8d2a4c8a, # 32
    
    # Round 3
    0xfffa3942, # 33
    0x8771f681, # 34
    0x6d9d6122, # 35
    0xfde5380c, # 36
    0xa4beea44, # 37
    0x4bdecfa9, # 38
    0xf6bb4b60, # 39
    0xbebfbc70, # 40
    0x289b7ec6, # 41
    0xeaa127fa, # 42
    0xd4ef3085, # 43
    0x4881d05, # 44
    0xd9d4d039, # 45
    0xe6db99e5, # 46
    0x1fa27cf8, # 47
    0xc4ac5665, # 48
    
    # Round 4
    0xf4292244, # 49
    0x432aff97, # 50
    0xab9423a7, # 51
    0xfc93a039, # 52
    0x655b59c3, # 53
    0x8f0ccc92, # 54
    0xffeff47d, # 55
    0x85845dd1, # 56
    0x6fa87e4f, # 57
    0xfe2ce6e0, # 58
    0xa3014314, # 59
    0x4e0811a1, # 60
    0xf7537e82, # 61
    0xbd3af235, # 62
    0x2ad7d2bb, # 63
    0xeb86d391, # 64
]

# Use binary integer part of the sines of integers (Radians) as constants:
K = []
for i in range(64):
    k = long(math.floor(abs(math.sin(i + 1)) * (2**32))) & 0xFFFFFFFF
    K.append(k)
    assert (k == KfromRFC[i])

print "K =", map(lambda k: "%8x" % k, K)

def F(x, y, z):
    result = (x & y) | (~x & z)
    return result

def G(x, y, z):
    result = (x & z) | (y & ~z)
    return result

def H(x, y, z):
    result = x ^ y ^ z
    return result

def I(x, y, z):
    result = y ^ (x | ~z)
    return result

def md5_round_one_index(i):
    index = i
    return i

def md5_round_two_index(i):
    index = (5 * i + 1) % 16
    return index

def md5_round_three_index(i):
    index = (3 * i + 5) % 16
    return index

def md5_round_four_index(i):
    index = (7 * i) % 16
    return index

def md5_index(i):
    if i < 16:
        index = md5_round_one_index(i)
    elif i < 32:
        index = md5_round_two_index(i)
    elif i < 48:
        index = md5_round_three_index(i)
    else:
        index = md5_round_four_index(i)
    return index

for r in range(4):
    print "indexing pattern for round", r+1, ":",
    for i in range(r*16, r*16 + 16):
        print "%2d" % md5_index(i),
    print



# Block of 512 bits, divided into 16 32-bit words.  There are 4
# rounds.  Each round has 16 operations that use all 16 input words.

def md5_operation(blockwords, i, a, b, c, d):
    assert (0 <= i and i < 64)
    assert (len(blockwords) == 16)
    if i < 16:
        f = F(b, c, d)
    elif i < 32:
        f = G(b, c, d)
    elif i < 48:
        f = H(b, c, d)
    else:
        f = I(b, c, d)
    g = md5_index(i)
    datum = blockwords[g]
    assert (datum < 1 << 32)
    datum &= 0xFFFFFFFF
    konstant = K[i]
    rotation = R[i]
    # print "operation %2d: %08x %08x %08x %08x" % (i, a, b, c, d),
    # print "x[%2d] = %08x" % (g, datum),
    # print "rotate %2d" % rotation,
    # print "constant %08x" % konstant,
    # print
    mai = add32(a, f)
    ket = add32(mai, konstant)
    man = add32(ket, datum)
    ruc = rotate_left32(man, rotation)
    san = add32(ruc, b)
    anew = d
    bnew = san
    cnew = b
    dnew = c
    return (anew, bnew, cnew, dnew)

def md5_block(blockwords, h0, h1, h2, h3):
    print "md5_block: blockwards = ", blockwords
    assert (len(blockwords) == 16)
    assert (h0 < 1 << 32)
    assert (h1 < 1 << 32)
    assert (h2 < 1 << 32)
    assert (h3 < 1 << 32)
    a, b, c, d = h0, h1, h2, h3
    for i in range(64):
        a, b, c, d = md5_operation(blockwords, i, a, b, c, d)
    h0new = add32(h0, a)
    h1new = add32(h1, b)
    h2new = add32(h2, c)
    h3new = add32(h3, d)
    return (h0new, h1new, h2new, h3new)


# Initial values of state variables

def md5_stream(streamwords):
    assert (len(streamwords) % 16 == 0)
    h = [0, 0, 0, 0]
    h[0] = 0x67452301
    h[1] = 0xEFCDAB89
    h[2] = 0x98BADCFE
    h[3] = 0x10325476
    for i in range(0, len(streamwords), 16):
        blockwords = streamwords[i:i+16]
        h[0:4] = md5_block(blockwords, h[0], h[1], h[2], h[3])
    print "h = ", map(lambda x: "%08x" % x, h)
    digest = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(16):
        g = h[i/4]
        s = 8 * (i%4)
        digest[i] = (g >> s) & 0xFF
    print "digest = ", digest
    digeststr = reduce(lambda x,y: x + y, map(lambda d: "%02x" % d, digest))
    return digeststr

def string_to_stream(str):
    assert(len(str) % 64 == 0)
    l = list(str)
    s = map(ord, l) 
    return s

def md5(str):
    stream = string_to_stream(str)
    h = md5_stream(stream)
    return h

import hashlib
strings = [
    "1234567812345678123456781234567812345678123456781234567812345678",
    "abcdefghijklmnopqrstuvwxyz            ABCDEFGHIJKLMNOPQRSTUVWXYZ",
]

for s in strings:
    stream = string_to_stream(s)
    print "string_to_stream: ", s, "==>", stream

print
print
print "md5 test"
print

for s in strings:
    h1 = hashlib.md5(s).hexdigest()
    h2 = md5(s)
    print h1, len(s), s
    print h2, len(s), s
    print

# s = "abcd"
# print map(lambda c: (c), list(s))

