#!/usr/bin/env python
# https://www.hackerrank.com/challenges/sherlock-and-the-beast

def answer(n):
    ''' 5x+3y = n, then 
        y = (n-5x)/3
    '''
    x=y=0
    while (n-5*x)%3 != 0 and y >= 0:
        x += 1
        y = (n-5*x)/3

    y = (n-5*x)/3
    if y < 0:
        return "-1"
    return '5'*(3*y) + '3'*(5*x)

def main():
    t = input()
    assert 1 <= t <= 20
    for i in range(t):
        n = input()
        assert 1 <= n <= 10**5
        print answer(n)

if __name__ == '__main__':
    main()
