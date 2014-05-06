#!/usr/bin/env python
# Problem
# https://www.hackerrank.com/contests/w2/challenges/manasa-and-stones
# Author : leogao

def manasa_stones( n, a, b ):
    last_stones = []
    for i in xrange(n):
        stone_num = i*a + (n - i - 1)*b
        last_stones.append(stone_num)
    last_stones.sort()
    for num in last_stones:
        print num, 
    print ''

def main():
    T = int(raw_input())
    assert 1<=T<=10
    source = []
    for x in xrange(T):
        N = int(raw_input())
        assert 1<=N<=10**3
        A = int(raw_input())
        assert 1<=A<=10**3
        B = int(raw_input())
        assert 1<=B<=10**3
        source.append([N,A,B])
    for y in xrange(T):
        manasa_stones(source[y][0],source[y][1],source[y][2])

if __name__=='__main__':
    main()
