import numpy as np
import cProfile
import pickle
from time import time
from ctypes import CDLL, c_double, c_int
from vit_python import viterbi as vit_pyt


# load library containing c functions
vit_unpacking = CDLL("./libvit_unpack.so")
vit_regular = CDLL("./libviterbi.so")
reg_viterbi = vit_regular.viterbi
unp_viterbi = vit_unpacking.viterbi

# Set in and output types:
unp_viterbi.restype = None
unp_viterbi.argtypes = [np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_double, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                        np.ctypeslib.ndpointer(c_int, flags="C_CONTIGUOUS"),
                        c_int, c_int, c_int, c_int]

reg_viterbi.restype = None
reg_viterbi.argtypes = [np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_double),
                        np.ctypeslib.ndpointer(c_int),
                        np.ctypeslib.ndpointer(c_int),
                        c_int, c_int, c_int]


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


# unpack stuff
probs_to_array = np.array([
    [0.00, 0.05, 0.95],
    [0.20, 0.00, 0.80],
    [0.95, 0.05, 0.00],
], dtype=c_double)


# np.log(trans_probs_3_state)
# run!

with open("./test.bin", "rb") as file:
    data = pickle.load(file)

inp = np.array(data['x'], dtype=c_int)
init_probs_3_state = np.log(np.array(data['p'], dtype=c_double))
emission_probs_3_state = np.log(np.array(data['e'], dtype=c_double))
trans_probs_3_state = np.log(np.array(data['t'], dtype=c_double))
probs_to_array = data['t']

states = init_probs_3_state.size
emits = emission_probs_3_state.shape[1]

foo = []
for i in range(states):
    for j in range(states):
        if probs_to_array[i, j] != 0:
            foo.append(j)
            foo.append(i)
t_array = np.array(foo, dtype=c_int)


def time_unp() -> float:
    out_p = np.zeros(inp.shape, dtype=c_int)
    v_table = np.zeros((inp.size, init_probs_3_state.size), dtype=c_double)

    t1 = time()
    unp_viterbi(init_probs_3_state, trans_probs_3_state, emission_probs_3_state, t_array,
                v_table, out_p, inp, c_int(states), c_int(emits), c_int(inp.size), c_int(t_array.size//2))
    t2 = time()-t1
    return t2


def time_reg() -> float:
    out_p = np.zeros(inp.shape, dtype=c_int)
    v_table = np.zeros((inp.size, init_probs_3_state.size), dtype=c_double)

    t1 = time()
    reg_viterbi(init_probs_3_state, trans_probs_3_state, emission_probs_3_state,
                v_table, out_p, inp, c_int(states), c_int(emits), c_int(inp.size))
    t2 = time() - t1
    return t2


def time_pyt() -> float:
    out_p = np.zeros(inp.shape, dtype=c_int)
    v_table = np.zeros((inp.size, init_probs_3_state.size), dtype=c_double)
    t1 = time()
    vit_pyt(inp, v_table, trans_probs_3_state,
            emission_probs_3_state, init_probs_3_state, out_p)
    t2 = time() - t1
    return t2


funcs = [time_unp, time_reg]
foo = {fun.__name__: 0.0 for fun in funcs}
for i in range(100):
    for fun in funcs:
        foo[fun.__name__] += fun()
print(foo)

# cProfile.run("time_reg()")
# cProfile.run("time_unp()")
