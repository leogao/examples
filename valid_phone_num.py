#!/usr/bin/env python
# Problem
# https://www.hackerrank.com/challenges/regex-1-validating-the-phone-number
# Author : leogao

def main():
    N = int(raw_input())
    assert 1<=N<=10
    source = []
    for x in xrange(N):
        Nx = raw_input()
        assert 1<=len(Nx)<=15
        source.append(Nx)
    for y in xrange(N):
        if len(source[y]) != 10 or source[y].isdigit() == False:
            print "NO"
            continue
        if list(source[y])[0] in ['7','8','9']:
            print "YES"
        else:
            print "NO"

if __name__=='__main__':
    main()
