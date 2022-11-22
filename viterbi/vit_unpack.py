from __future__ import annotations
import argparse
import numpy as np
from distutils import ccompiler
from ctypes import CDLL, c_double, c_int
'''
Implementation of viterbi algorithm in c (viterbi.c), parsing input and output arrays from python. 
'''


def main():
    argparser = argparse.ArgumentParser(
        "Viterbi", description="runs viterbi algorithm on, currently still testing on hardcoded input")
    argparser.add_argument("-c", action="store_true",
                           help="add -c flag if the c library should be recompiled before running")

    args = argparser.parse_args()

    if args.c:
        # compile c functions:
        fn = "vit_unpack"
        compiler = ccompiler.new_compiler()
        # ccompiler base values use system os, and the default compiler for that os
        files = compiler.compile([fn+'.c'])
        libname = compiler.shared_object_filename(fn)
        compiler.link_shared_lib(files, fn)
        # Now grabs vit_unpack.c, compiles it and makes a shared library libvit_unpack.so
        # i am not sure why it adds lib to the front of the output name, but i despise it.
    lib = CDLL("./libvit_unpack.so")  # load library containing c functions
    viterbi = lib.viterbi

    # Set in and output types:
    viterbi.restype = None
    viterbi.argtypes = [np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                        c_int, c_int, c_int, c_int]
    '''
    input format:   viterbi(initial probability [pi],
                            transition matrix [trans_],
                            emission matrix [emits_],
                            transition array [trans_a_]
                            output matrix [vert_],
                            output optimal path [out_p]
                            input sequence [x],
                            # of [states] [emits], [input_length], [size])
    '''

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
    v_table = np.zeros((inp.size, init_probs_3_state.size), dtype=c_double)

    # unpack stuff
    probs_to_array = np.array([
        [0.00, 0.05, 0.95],
        [0.20, 0.00, 0.80],
        [0.95, 0.05, 0.00],
    ], dtype=c_double)

    foo = []
    for i in range(3):
        for j in range(3):
            if probs_to_array[i, j] != 0:
                foo.append(j)
                foo.append(i)
    t_array = np.array(foo, dtype=c_int)
    size = t_array.size//2

    # np.log(trans_probs_3_state)
    # run!
    viterbi(init_probs_3_state, trans_probs_3_state, emission_probs_3_state, t_array,
            v_table, out_p, inp, c_int(3), c_int(4), c_int(inp.size), c_int(size))
    print(v_table)
    print(out_p)


if __name__ == "__main__":
    main()
