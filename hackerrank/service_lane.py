#!/usr/bin/env python
# https://www.hackerrank.com/challenges/service-lane

N,T = map(int,raw_input().split())
assert 2<=N<=10**5
assert 1<=T<=1000
segments = map(int,raw_input().split())

for i in xrange(T):
    a,b = map(int,raw_input().split())
    print min(segments[a:b+1])
