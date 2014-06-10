#!/usr/bin/env python
# https://www.hackerrank.com/challenges/map-and-lambda-expression

N = int(raw_input())

#assert 0<=N<=15

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

listfibs = []
for i in xrange(N):
    listfibs.append(fib(i))

cubes = list(map(lambda x : x*x*x, listfibs))

print cubes
