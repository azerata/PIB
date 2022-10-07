#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define STATES states
#define EMITS emits
#define N n

#define T(I, J) trans_[(I)*STATES + (J)]
#define E(I, J) emits_[(I)*EMITS + (J)]
#define V(I, J) vert_[(I)*STATES + (J)]

double max(double a, double b)
{
    return (a < b) ? b : a;
}

void viterbi(const double *pi, const double *trans_, const double *emits_, double *vert_, int *opt_p, const int *x, int states, int emits, int n)
/* input format :   viterbi(initial probability [pi],
                            transition matrix [trans_],
                            emission matrix [emits_],
                            output matrix [vert_],
                            output optimal path [opt_p]
                            input sequence [x],)
                            # of [states] [emits], [input_length]
                            */
{
    // Viterbi algorithm
    printf("%f\n", *vert_);
    for (int j = 0; j < states; j++)
    {
        V(0, j) = E(j, x[0]) + pi[j];
    }

    for (int i = 1; i < n; i++)
    {
        for (int j = 0; j < states; j++)
        {
            double best = -10000.0;
            for (int k = 0; k < states; k++)
            {
                best = max(best, V(i - 1, k) + T(k, j));
            }
            V(i, j) = E(j, x[i]) + best;
        }
    }
    // Backtracking now included
    double best = -1000.0;
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
            printf("%lf, %lf, %lf ==? %lf, %d\n", T(j, end), V(i, j),
                   V(i, j) + T(j, end) + E(end, x[i + 1]),
                   target, opt_p[i]);
        }
        printf("\n");
    }
}

/*
int main(void)
{
    // Allocating space for parameters
    double *pi = malloc(STATES * sizeof *pi);
    double *trans_ = malloc(STATES * STATES * sizeof *trans_);
    double *emits_ = malloc(STATES * EMITS * sizeof *emits_);

    // fake input
    int x[N] = {1, 2, 0, 1};

    // Setting parameters (must depend on input)
    for (int i = 0; i < STATES; i++)
    {
        pi[i] = log(0.0);
    }
    pi[0] = log(1.0);

    for (int i = 0; i < STATES; i++)
    {
        for (int j = 0; j < STATES; j++)
        {
            T(i, j) = log(1.0 / STATES);
        }
    }
    for (int i = 0; i < STATES; i++)
    {
        for (int j = 0; j < EMITS; j++)
        {
            E(i, j) = log(1.0 / EMITS);
        }
    }

    // Viterbi (sans backtracking)
    double *vert_ = malloc(N * STATES * sizeof *vert_);

    for (int j = 0; j < STATES; j++)
    {
        V(0, j) = E(j, x[0]) + pi[j];
    }

    for (int i = 1; i < N; i++)
    {
        for (int j = 0; j < STATES; j++)
        {
            double best = 0.0;
            for (int k = 0; k < STATES; k++)
            {
                best = max(best, V(i - 1, k) + T(k, j));
            }
            V(i, j) = E(j, x[i]) + best;
        }
    }

    // Printing Viterbi table
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < STATES; j++)
        {
            printf("%f ", V(i, j));
        }
        printf("\n");
    }

    // Backtracking
    int *opt_p = malloc(N * sizeof opt_p);

    double best = 0.0;
    int end = 0;
    for (int j = 0; j < STATES; j++)
    {
        best = max(best, V(N, j));
        end = (V(N, j) == best) ? j : end;
    }

    for (int i = N - 1; i > 0; i--)
    {
        for (int j = 0; j < STATES; j++)
        {
            opt_p[i] = (V(i - 1, j) + T(j, end) == V(i, end)) ? j : opt_p[i];
        }
    }

    for (int i = 0; i < N; i++)
    {
        printf("%d\n", opt_p[i]);
    }

    // Always remember to clean up your room
    free(pi);
    free(trans_);
    free(emits_);
    free(vert_);
    free(opt_p);

    return 0;
}
*/