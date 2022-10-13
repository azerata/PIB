#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define T(I, J) trans_[(I)*states + (J)]
#define FROM(I) trans_a_[2 * (I)]
#define TO(I) trans_a_[2 * (I) + 1]

void unpack(const double *trans_, double *trans_a_)
{
}