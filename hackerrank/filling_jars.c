/*
 * https://www.hackerrank.com/challenges/filling-jars
*/

#include <stdio.h>
int main() {
    int N=0, M=0;
    long long tot = 0;
    scanf("%d %d",&N,&M);
    for(int i=0;i<M;i++){
        int a, b;
        long long k;
        scanf("%d %d %lld",&a,&b,&k);
        tot+= k*(b-a+1);
    }
    printf("%lld\n", tot/N);
    return 0;
}

