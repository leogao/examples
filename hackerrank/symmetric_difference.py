#!/usr/bin/env python
# https://www.hackerrank.com/challenges/sets

def main():
    M = int(raw_input())
    setM = set(map(int,raw_input().split()))

    N = int(raw_input())
    setN = set(map(int,raw_input().split()))

    DiffUnion = setM.difference(setN).union(setN.difference(setM))

    Ulist = []
    for i in xrange(len(DiffUnion)):
        Ulist.append(DiffUnion.pop())
    Ulist.sort()
    for i in Ulist:
        print i

if __name__=='__main__':
    main()
