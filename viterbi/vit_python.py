from __future__ import annotations
import numpy as np
import sys
import argparse
import pickle
from ctypes import c_int, c_double
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


def main():
    argparser = argparse.ArgumentParser(
        description="python implementation of viterbi, unpacking the possible transitions")
    argparser.add_argument("infile", nargs='?',
                           type=argparse.FileType('rb'), default=sys.stdin)

    args = argparser.parse_args()
    model = pickle.load(args.infile)

    x = model['x']
    trans = np.log(model['t'])
    emit = np.log(model['e'])
    pi = np.log(model['p'])

    out_p = np.zeros(x.shape, dtype=c_int)
    v_table = np.zeros((x.size, pi.size), dtype=c_double)

    viterbi(x, v_table, trans, emit, pi, out_p)
    print(v_table)
    print(out_p)


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


def viterbi(x, v, trans, emits, pi, opt_p) -> None:
    b_table = np.zeros((x.size, pi.size), dtype=c_int)
    states = pi.size
    n = x.size

    for j in range(states):
        v[0, j] = pi[0, j]+emits[j, x[0]]

    for i in range(n-1):
        for j in range(states):
            best = -np.inf
            for k in range(states):
                best = max(best, v[i, k] + trans[k, j])
                if best == v[i, k] + trans[k, j]:
                    b_table[i+1, j] = k
            v[i+1, j] = best + emits[j, x[i+1]]

    opt_p[-1] = np.argmax(v[n-1])
    for i in range(1, n)[::-1]:
        opt_p[i-1] = b_table[i, opt_p[i]]

    return None


if __name__ == "__main__":
    main()
