import numpy as np
from ctypes import CDLL, c_double, c_int

lib = CDLL("./viterbi.so")
viterbi = lib.viterbi
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
                        input sequence [x]  ) 
                        # of [states] [emits], [input_length]
'''
x = np.array([1, 2, 0, 1], dtype=c_int)

pi = np.log(np.array([[1],
                      [0]], dtype=c_double))

t = np.log(np.array([[0.7, 0.3],
                     [0.2, 0.8]], dtype=c_double))

e = np.log(np.array([[0.1, 0.9],
                    [0.7, 0.3]], dtype=c_double))
v = np.zeros((x.size, pi.size), dtype=c_double)

p = np.zeros(x.shape, dtype=c_int)
# print(v)
#viterbi(pi, t, e, v, p, x, c_int(pi.size), c_int(e.shape[0]), c_int(x.size))
# print(v)
# print(p)

inp = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0], dtype=c_int)

init_probs_3_state = np.log(np.array(
    [0.00, 0.10, 0.00],
    dtype=c_double
))

trans_probs_3_state = np.log(np.array([
    [0.00, 1.00, 0.00],
    [0.00, 0.00, 1.00],
    [1.00, 0.00, 0.00],
], dtype=c_double))

emission_probs_3_state = np.log(np.array([
    #   A     C     G     T
    [0.40, 0.15, 0.20, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.20, 0.40, 0.30, 0.10],
], dtype=c_double))

sanity_check = np.log(np.array([[0.40, 0.25, 0.20],
                                [0.15, 0.25, 0.40],
                                [0.20, 0.25, 0.30],
                                [0.25, 0.25, 0.10]], dtype=c_double))

out_p = np.zeros(inp.shape, dtype=c_int)
v_table = np.zeros((inp.size, init_probs_3_state.size), dtype=c_double)

viterbi(init_probs_3_state, trans_probs_3_state, emission_probs_3_state,
        v_table, out_p, inp, c_int(3), c_int(4), c_int(inp.size))
print(v_table)
print(out_p)
