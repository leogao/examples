#!/usr/bin/env python
# https://www.hackerrank.com/challenges/is-fibo

import sys

T = int(raw_input())
assert 1<=T<=10**5

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
X = 10
fibs = []
for i in xrange(X):
    fibs.append(fib(i))

for i in xrange(T):
    a = int(raw_input())
    assert 1<=a<=10**10
    if a in fibs:
        print 'isFibo'
    elif a > fibs[-1]:
        for i in xrange(1000):
            fibsv = fibs[X-2+i] + fibs[X-1+i]
            fibs.append(fibsv)
            if fibsv == a:
                print 'isFibo'
                break
            elif fibsv > a:
                print 'isNotFibo'
                break
    elif a < fibs[-1]:
        print 'isNotFibo'
