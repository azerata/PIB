#include <stdlib.h>
#include <math.h>
#include <stdio.h>

#define E(I, J) emits_[(I)*emits + (J)]
#define V(I, J) vert_[(I)*states + (J)]
#define B(I, J) back_[(I)*states + (J)]
#define MAX(A, B) (((A) > (B)) ? (A) : (B))

void viterbi(const double *pi, const double *emits_, double *vert_, int *opt_p, const int *x, int states, int emits, int n)
{
    for (int k = 0; k < states; k++)
    {
        V(0, k) = pi[k] + E(x[0], k);
    }
    for (int i = 1; i < n; i++)
    {
        // generated code here
    }
}
