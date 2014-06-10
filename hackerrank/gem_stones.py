#!/usr/bin/env python
# https://www.hackerrank.com/challenges/gem-stones

N = int(raw_input())
assert 1<=N<=100
src = []
lenth = []
for i in xrange(N):
    srci = raw_input()
    lenth.append(len(srci))
    src.append(srci)
min_len = min(lenth)
index = lenth.index(min_len)
gen_elements= []
src[index]
for e in list(set(src[index])):
    ok = 1
    for x in xrange(N):
        if not e in list(src[x]):
            ok = 0
            break
    if ok == 1:
        gen_elements.append(e)
print len(gen_elements)
