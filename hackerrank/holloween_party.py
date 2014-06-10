#!/usr/bin/env python
# https://www.hackerrank.com/challenges/halloween-party

T = int(raw_input())
assert 1<=T<=10

for j in xrange(T):
    ## Write code here to compute the answer using (n, k, candies)
    K = int(raw_input())
    assert 2<=K<=10**7
    pieces = (K/2)*(K/2 + K%2)
    print pieces
