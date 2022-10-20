#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define T(I, J) trans_[(I)*states + (J)]
#define E(I, J) emits_[(I)*emits + (J)]
#define V(I, J) vert_[(I)*states + (J)]
#define FROM(I) trans_a_[2 * (I)]
#define TO(I) trans_a_[2 * (I) + 1]

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
    // unpacking
    // find size of unpacked array
    int size = 0;
    for (int i = 0; i < states; i++)
    {
        for (int j = 0; j < states; j++)
        {
            if (T(i, j) != 0)
                size += 1;
        }
    }
    /*
    // fill unpacked array
    int k = 0;

    for (int i = 0; i < states; i++)
    {
        for (int j = 0; j < states; j++)
        {
            if ((T(i, j)) != 0)
            {
                FROM(k) = i;
                TO(k) = j;
                k++;
            }
        }
    }
    */
    // is this viterbi?
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < states; k++)
            V(i, k) = E(k, x[i]);
    }

    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < size; k++)
            V(i + 1, TO(k)) += log(T(FROM(k), TO(k))) + V(i, FROM(k));
    }
    /*
    // Viterbi algorithm
    for (int j = 0; j < states; j++)
    {
        V(0, j) = E(j, x[0]) + pi[j];
    }

    for (int i = 1; i < n; i++)
    {
        for (int j = 0; j < states; j++)
        {
            double best = -INFINITY;
            for (int k = 0; k < states; k++)
            {
                best = max(best, V(i - 1, k) + T(k, j));
            }
            V(i, j) = E(j, x[i]) + best;
        }
    }
    */
    // Backtracking now included
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
        for (int j = 0; j < states; j++)
        {
            opt_p[i] = (V(i, j) + T(j, end) + E(end, x[i + 1]) == target) ? j : opt_p[i];
        }
    }
}