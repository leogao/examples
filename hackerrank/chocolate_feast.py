#!/usr/bin/env python
# https://www.hackerrank.com/challenges/chocolate-feast

def incoming( unwappers ):
    if unwappers < C1:
        return 0
    else:
        inc = unwappers/C1
        remainder = unwappers/C1 + unwappers%C1
        return inc + incoming(remainder)

# Enter your code here. Read input from STDIN. Print output to STDOUT
T = int(raw_input())
assert T<=1000
for i in range (0,T):
    A,B,C1 = [int(x) for x in raw_input().split(' ')]
    X = A / B
    answer = X + incoming(X)
    # write code to compute answer
    print answer

