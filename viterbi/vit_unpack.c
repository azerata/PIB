#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define T(I, J) trans_[(I)*states + (J)]
#define E(I, J) emits_[(I)*emits + (J)]
#define V(I, J) vert_[(I)*states + (J)]
#define FROM(I) trans_a_[2 * (I)]
#define TO(I) trans_a_[2 * (I) + 1]

int float_to_int(float f)
{
    int new_int = f * 1000000;
    return new_int;
}

double max(double a, double b)
{
    return (a < b) ? b : a;
}

void viterbi(const double *pi, const double *trans_, const double *emits_, int *trans_a_, double *vert_, int *opt_p, const int *x, int states, int emits, int n)
/* input format :   viterbi(initial probability [pi],
                            transition matrix [trans_],
                            emission matrix [emits_],
                            transition array [trans_a_]
                            output matrix [vert_],
                            output optimal path [opt_p]
                            input sequence [x],
                            # of [states], [emits], [input_length])
                            */
{
    // find size of unpacked array
    int size = 0;
    for (int i = 0; i < states; i++)
    {
        for (int j = 0; j < states; j++)
        {
            if (T(i, j) != -INFINITY)
                size += 1;
        }
    }

    // is this viterbi?
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

    for (int i = n - 2; i >= 0; i--)
    {
        end = opt_p[i + 1];
        double target = V(i + 1, end);
        for (int k = 0; k < size; k++)
        {
            if (TO(k) == end)
            {
                opt_p[i] = float_to_int(V(i, FROM(k)) + T(FROM(k), TO(k)) + E(TO(k), x[i + 1])) == float_to_int(target) ? FROM(k) : opt_p[i];
            }
        }
    }
}
