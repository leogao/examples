#!/usr/bin/env python
# https://www.hackerrank.com/challenges/basic-calculator

F = float(raw_input())
S = float(raw_input())

assert -10000<=F<=10000
assert -10000<=S<=10000

Addition = lambda a,b : a + b
Subtraction = lambda a,b : a - b
Multiplication = lambda a,b : a * b
Division = lambda a,b : a/b
Integer_Division = lambda a,b : a//b

print '%.2f' % Addition(F,S)
print '%.2f' % Subtraction(F,S)
print '%.2f' % Multiplication(F,S)
print '%.2f' % Division(F,S)
print '%.2f' % Integer_Division(F,S)


