#!/usr/bin/env python
# https://www.hackerrank.com/challenges/maximizing-xor

def  maxXor( l,  r):
    xorsum = []
    for i in xrange(l,r+1):
        for j in xrange(i,r+1):
            xorsum.append(i^j)
    return max(xorsum)

_l = int(raw_input());
_r = int(raw_input());

assert 1<=_l<=_r<=1000

res = maxXor(_l, _r);
print(res)
