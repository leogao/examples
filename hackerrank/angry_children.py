#!/usr/bin/env python
# https://www.hackerrank.com/challenges/angry-children

n = int(raw_input())
k = int(raw_input())
candies = [int(raw_input()) for i in range(0,n)]
candies.sort()
diff = []
for l in xrange(n-k):
    ## Write code here to compute the answer using (n, k, candies)
    diff.append(candies[k-1+l]-candies[l])
min_diff = min(diff)
print min_diff
