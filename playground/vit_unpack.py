import numpy as np
from ctypes import CDLL, c_double, c_int
'''
Implementation of viterbi algorithm in c (viterbi.c), parsing input and output arrays from python. 
'''

lib = CDLL("./vit_unpack.so")  # load library containing c functions
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
                    c_int, c_int, c_int]
'''
input format:   viterbi(initial probability [pi],
                        transition matrix [trans_],
                        emission matrix [emits_],
                        transition array [trans_a_]
                        output matrix [vert_],
                        output optimal path [out_p]
                        input sequence [x],
                        # of [states] [emits], [input_length])
'''
inp = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0], dtype=c_int)


# try with test Data:
init_probs_3_state = np.log(np.array(
    [0.00, 0.10, 0.00],
    dtype=c_double
))

trans_probs_3_state = np.array([
    [0.00, 0.05, 0.95],
    [0.20, 0.00, 0.80],
    [0.95, 0.05, 0.00],
], dtype=c_double)

emission_probs_3_state = np.log(np.array([
    #   A     C     G     T
    [0.40, 0.15, 0.20, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.20, 0.40, 0.30, 0.10],
], dtype=c_double))

out_p = np.zeros(inp.shape, dtype=c_int)
v_table = np.zeros((inp.size, init_probs_3_state.size), dtype=c_double)

foo = []
for i in range(3):
    for j in range(3):
        if trans_probs_3_state[i, j] != 0:
            foo.append(i)
            foo.append(j)
t_array = np.array(foo, dtype=c_int)

print(t_array, "bøf")

# run!
viterbi(init_probs_3_state, trans_probs_3_state, emission_probs_3_state, t_array,
        v_table, out_p, inp, c_int(3), c_int(4), c_int(inp.size))
print(v_table)
print(out_p)
