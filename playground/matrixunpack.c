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
    printf("size of A: %d\n", size);

    // int *trans_a_ = malloc(size * sizeof trans_a_);
    int k = 0;

    /* on todays lecture, when you call a c function in python, don't try to malloc, because not even python knows how its memory is structured
    or atleast i guess thats why i get segfaults... */

    printf("aloccated?\n");
    for (int i = 0; i < states; i++)
    {
        for (int j = 0; j < states; j++)
        {
            if ((T(i, j)) != 0)
            {
                printf("while looping: (%d, %d)\t", i, j);
                FROM(k) = i;
                TO(k) = j;
                printf("- FROM/TO[%d] = (%d, %d)\n", k, trans_a_[FROM(k)], trans_a_[TO(k)]);
                k++;
            }
        }
    }
    for (int i = 0; i < size - 2; i++)
        printf("(%d, %d)\n", trans_a_[FROM(i)], trans_a_[TO(i)]);

    // free(trans_a_);
}
