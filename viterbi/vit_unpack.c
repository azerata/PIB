#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define T(I, J) trans_[(I)*states + (J)]
#define E(I, J) emits_[(I)*emits + (J)]
#define V(I, J) vert_[(I)*states + (J)]
#define FROM(I) trans_a_[2 * (I)]
#define TO(I) trans_a_[2 * (I) + 1]
#define B(I, J) back_[(I)*states + (J)]

double max(double a, double b)
{
    return (a < b) ? b : a;
}

void viterbi(const double *pi, const double *trans_, const double *emits_, int *trans_a_, double *vert_, int *opt_p, const int *x, int states, int emits, int n, int size)
/* input format :   viterbi(initial probability [pi],
                            transition matrix [trans_],
                            emission matrix [emits_],
                            transition array [trans_a_]
                            output matrix [vert_],
                            output optimal path [opt_p]
                            input sequence [x],
                            # of [states], [emits], [input_length], [size])
                            */
{

    int *back_ = malloc(n * states * sizeof back_);

    // Viterbi algorithm, only considering possible transitions, building the backtracking matrix while we run.
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < states; k++)
            V(i, k) = -INFINITY;
    }
    for (int k = 0; k < states; k++)
        V(0, k) = pi[k] + E(k, x[0]);

    for (int i = 0; i < n - 1; i++)
    {
        for (int k = 0; k < size; k++)
        {
            V(i + 1, TO(k)) = max(V(i + 1, TO(k)), E(TO(k), x[i + 1]) + T(FROM(k), TO(k)) + V(i, FROM(k)));

            // update B table
            if (V(i + 1, TO(k)) == E(TO(k), x[i + 1]) + T(FROM(k), TO(k)) + V(i, FROM(k)) && V(i + 1, TO(k)) != -INFINITY)
            {
                B(i + 1, TO(k)) = FROM(k);
            }
        }
    }

    // backtracking from possible trans
    double best = -INFINITY;
    int end = 0;
    for (int j = 0; j < states; j++)
    {
        best = max(best, V(n - 1, j));
        end = (V(n - 1, j) == best) ? j : end;
    }

    opt_p[n - 1] = end;

    int bb = end;
    for (int i = n; i > 0; i--)
    {
        opt_p[i - 1] = bb;
        bb = B(i - 1, bb);
    }
    free(back_);
}
