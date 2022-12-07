from __future__ import annotations
import numpy as np
import pathlib
import os
from distutils import ccompiler
from ctypes import c_int, c_double, CDLL
from shutil import rmtree

trans_probs_3_state = np.array([
    [0.00, 0.05, 0.95],
    [0.20, 0.00, 0.80],
    [0.95, 0.05, 0.00],
])

t_array: list[tuple[int, int, float]] = []
states = trans_probs_3_state.shape[0]
for i in range(states):
    for j in range(states):
        if trans_probs_3_state[i, j] != 0:
            t_array.append((i, j, np.log(trans_probs_3_state[i, j])))

loop_unrolled = '\n'.join(
    f'\tV(i, {to}) = MAX(V(i, {to}), {prob} + V(i-1, {From}) + E({to}, x[i]));\n \
        B(i, {to}) = ARGMAX(V(i, {to}), B(i, {to}), {prob} + V(i-1, {From}) + E({to}, x[i]), {From} );'
    for From, to, prob in t_array)


xxx = """
#include <stdlib.h>
#include <math.h>
#include <stdio.h>

#define E(I, J) emits_[(I)*emits + (J)]
#define T(I, J) trans_[(I)*states + (J)]
#define V(I, J) vert_[(I)*states + (J)]
#define B(I, J) back_[(I)*states + (J)]
#define MAX(A, B) (((A) > (B)) ? (A) : (B))
#define ARGMAX(A, I, B, J) (((A) > (B)) ? (I) : (J))

void viterbi(const double *trans_, const double *pi, const double *emits_, double *vert_, int *opt_p, const int *x, int states, int emits, int n)
{
    int *back_ = malloc(n * states * sizeof back_);

    for (int k = 0; k < states; k++)
    {
        V(0, k) = pi[k] + E(x[0], k);
    }
    for (int i = 1; i < n; i++)
    {
        // generated code here
{GENERATOR}
    }

    double best = V(n -1, 0);
    int end = 0;
    for (int k = 0; k < states; k++)
    {
        best = MAX(best, V(n - 1, k));
        end = (best == V(n - 1, k)) ? k : end;
    }
    opt_p[n - 1] = end;
    for (int i = n-2 ; i > 0; i--)
    {
        double best = -INFINITY;
        int state = 0;
        for (int k = 0; k < states; k++)
        {
            if ((V(i, k) + T(k, opt_p[i + 1])) > best && V(i, k) != -INFINITY)
            {
                best = V(i, k);
                state = k;
            }
            opt_p[i] = state;
        }
    }
    free(back_);
}
"""


# Setup directory
parent_dir = pathlib.Path(__file__).parent
tmp_dir = ".tmp"
fn = "tmp"
path = os.path.join(parent_dir, tmp_dir)
os.mkdir(path)

# write c source to file:
with open(str(path+f'/{fn}.c'), 'w') as file:
    file.write(xxx.replace('{GENERATOR}', loop_unrolled))

# compiler setup
compiler = ccompiler.new_compiler()
compiler.add_include_dir(path)
compiler.add_library_dir(path)

files = compiler.compile(
    [path+f'/{fn}.c'], include_dirs=[path], output_dir=path)
compiler.link_shared_lib(files, fn, output_dir=path)


# Do work here

# Input sequence
inp = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0], dtype=c_int)

# try with test Data:
init_probs_3_state = np.log(np.array(
    [0.00, 0.10, 0.00],
    dtype=c_double
))

trans_probs_3_state = np.log(np.array([
    [0.00, 0.05, 0.95],
    [0.20, 0.00, 0.80],
    [0.95, 0.05, 0.00],
], dtype=c_double))

emission_probs_3_state = np.log(np.array([
    #   A     C     G     T
    [0.40, 0.15, 0.20, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.20, 0.40, 0.30, 0.10],
], dtype=c_double))

out_p = np.zeros(inp.shape, dtype=c_int)
v_table = np.log(np.zeros((inp.size, init_probs_3_state.size), dtype=c_double))

# Load so, and call viterbi.
lib = CDLL(f"{path}/lib{fn}.so")
viterbi = lib.viterbi
viterbi.restype = None
viterbi.argtypes = (np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                    np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                    np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                    np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                    np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                    np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                    c_int, c_int, c_int)

viterbi(trans_probs_3_state, init_probs_3_state, emission_probs_3_state, v_table,
        out_p, inp, c_int(states), c_int(emission_probs_3_state.shape[1]), c_int(len(inp)))

print(v_table, '\n', out_p)
# rmtree(path)
