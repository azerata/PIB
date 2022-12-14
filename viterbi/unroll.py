from __future__ import annotations
import numpy as np
import pathlib
import os
import sys
import argparse
import pickle
from distutils import ccompiler
from ctypes import c_int, c_double, CDLL
from shutil import rmtree


def main():
    argparser = argparse.ArgumentParser(
        "Full suite unpacking trans matrix and unrolling inner loop.")
    argparser.add_argument("infile", nargs='?',
                           type=argparse.FileType('rb'), default=sys.stdin)
    argparser.add_argument("-s", action="store_true",
                           help="use to if the t_array is included in infile.")

    args = argparser.parse_args()

    model = pickle.load(args.infile)
    emit = np.log(model['e'])
    pi = np.log(model['p'])
    x = model['x']
    states = pi.size

    # Check if the t array has already been constructed. if not, do so:
    if not args.s:
        trans = model['t']
        t_array: list[tuple[int, int, float]] = []
        for i in range(states):
            for j in range(states):
                if trans[i, j] != 0:
                    t_array.append((i, j, np.log(trans[i, j])))
    else:
        t_array = model['a']

    loop_unrolled = '\n'.join(
        f'\tV(i, {to}) = MAX(V(i, {to}), {prob} + V(i-1, {From}) + E({to}, x[i]));\n\
        B(i, {to}) = ARGMAX(V(i, {to}), B(i, {to}), {prob} + V(i-1, {From}) + E({to}, x[i]), {From} );'
        for From, to, prob in t_array)

    # Basis for the c function to run viterbi alg.
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
            V(0, k) = pi[k] + E(k, x[0]);
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
        int bb = end;
        for (int i = n; i > 0; i--)
        {
            opt_p[i - 1] = bb;
            bb = B(i - 1, bb);
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

    out_p = np.zeros(x.shape, dtype=c_int)
    v_table = np.log(np.zeros((x.size, pi.size), dtype=c_double))

    # Load .so, and call viterbi.
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

    viterbi(trans, pi, emit, v_table,
            out_p, x, c_int(states), c_int(emit.shape[1]), c_int(len(x)))

    print(v_table, '\n', out_p)
    rmtree(path)


if __name__ == "__main__":
    main()
