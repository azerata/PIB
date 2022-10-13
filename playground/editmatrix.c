#include <stdio.h>
#include <stdlib.h>

void cfun(const double *indatav, size_t size, double *outdatav)
{
    size_t i;
    for (i = 0; i < size; i++)
        outdatav[i] = i;
}