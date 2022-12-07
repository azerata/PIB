#include <stdlib.h>
#include <math.h>
#include <stdio.h>

#define E(I, J) emits_[(I)*emits + (J)]
#define T(I, J) trans_[(I)*states + (J)]
#define V(I, J) vert_[(I)*states + (J)]
#define B(I, J) back_[(I)*states + (J)]
#define MAX(A, B) (((A) > (B)) ? (A) : (B))

void viterbi(const double *trans_, const double *pi, const double *emits_, double *vert_, int *opt_p, const int *x, int states, int emits, int n)
{
    for (int k = 0; k < states; k++)
    {
        V(0, k) = pi[k] + E(x[0], k);
    }
    for (int i = 1; i < n; i++)
    {
        // generated code here
    }

    double best = -INFINITY;
    int end = 0;
    for (int k = 0; k < states; k++)
    {
        best = MAX(best, V(n - 1, k));
        end = (best = V(n - 1, k)) ? k : end;
    }
    opt_p[n - 1] = end;
    for (int i = n - 2; i > 0; i--)
    {
        double best = -INFINITY;
        int state = 0;
        for (int k = 0; k < states; k++)
        {
            if ((V(i, k) + T(k, opt_p[i + 1])) > best)
            {
                best = V(i, k);
                state = k;
            }
            opt_p[i] = state;
        }
    }
}
