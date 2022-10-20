#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define T(I, J) trans_[(I)*states + (J)]
#define FROM(I) trans_a_[2 * (I)]
#define TO(I) trans_a_[2 * (I) + 1]

void unpack(const double *trans_, int *trans_a_, int states)
{
    int size = 0;
    for (int i = 0; i < states; i++)
    {
        for (int j = 0; j < states; j++)
        {
            if (T(i, j) != 0)
                size += 2;
        }
    }

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
}
