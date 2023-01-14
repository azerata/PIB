from __future__ import annotations
import numpy as np
import argparse
import sys
import pickle
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
    argparser.add_argument("infile", nargs='?',
                           type=argparse.FileType("rb"), default=sys.stdin)

    args = argparser.parse_args()

    if args.c:
        # compile c functions:
        fn = "viterbi"
        compiler = ccompiler.new_compiler()
        # ccompiler base values use system os, and the default compiler for that os
        files = compiler.compile([fn+'.c'])
        libname = compiler.library_filename(fn)
        compiler.link_shared_lib(files, fn)
        # Now grabs vit_unpack.c, compiles it and makes a shared library libvit_unpack.so
        # i am not sure why it adds lib to the front of the output name, but i despise it.
        print(libname)
    lib = CDLL("./libviterbi.so")  # load library containing c functions
    viterbi = lib.viterbi

    # Set in and output types, these need to correspond to the arguments of the c function
    viterbi.restype = None
    viterbi.argtypes = [np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_int),
                        np.ctypeslib.ndpointer(c_int),
                        c_int, c_int, c_int]
    '''
    input format:   viterbi(initial probability [pi],
                            transition matrix [trans_],
                            emission matrix [emits_],
                            output matrix [vert_],
                            output optimal path [out_p]
                            input sequence [x],
                            # of [states] [emits], [input_length])
    '''

    model: dict[str, np.ndarray] = pickle.load(args.infile)

    trans = np.log(model['t'])
    emits = np.log(model['e'])
    pi = np.log(model['p'])
    inp = model['x']

    out_p = np.zeros(inp.shape, dtype=c_int)
    v_table = np.zeros((inp.size, pi.size), dtype=c_double)

    # run!
    viterbi(pi, trans, emits,
            v_table, out_p, inp, c_int(emits.shape[0]), c_int(emits.shape[1]), c_int(inp.size))
    # print(v_table)
    # print(out_p)


if __name__ == "__main__":
    main()
