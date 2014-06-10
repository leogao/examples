#!/usr/bin/env python
# https://www.hackerrank.com/challenges/find-second-maximum-number-in-a-list

def main():
    N = int(raw_input())
    assert 2<=N<=10
    Nlist = list(map(int,raw_input().split()))
    for Ni in Nlist:
        assert -100<=Ni<=100

    Nmax = max(Nlist)
    for i in xrange(len(Nlist)):
        if max(Nlist) == Nmax:
            Nlist.remove(Nmax)

    print max(Nlist)

if __name__=='__main__':
    main()
