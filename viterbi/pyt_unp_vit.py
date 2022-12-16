from __future__ import annotations
import numpy as np
import pickle
import sys
import argparse


def viterbi(x: np.ndarray, pi: np.ndarray, emit: np.ndarray, trans: np.ndarray, v: np.ndarray, out: np.ndarray) -> None:
    states = pi.size
    emits = emit.shape[1]
    back = np.zeros(v.shape, dtype=int)

    t_arr: list[tuple[int, int]] = []
    for i in range(states):
        for j in range(states):
            if trans[i, j] != 0:
                t_arr.append((i, j))

    for k in range(states):
        v[0, k] = (emit[k, x[0]] + pi[0, k])

    for i in range(1, x.size):
        for f, t in t_arr:
            v[i, t] = max(v[i, t], trans[f, t] + emit[t, x[i]] + v[i-1, f])
            back[i, t] = f if trans[f, t] + emit[t, x[i]] + \
                v[i-1, f] >= v[i, t] else back[i, t]

    out[-1] = np.argmax(back[:, -1])
    i = out.size
    while i > 0:
        i -= 1
        out[i-1] = back[i, out[i]]


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("infile", type=argparse.FileType(
        'rb'), nargs='?', default=sys.stdin)

    args = argparser.parse_args()

    data = pickle.load(args.infile)

    x = data['x']
    pi = np.log(data['p'])
    trans = np.log(data['t'])
    emit = np.log(data['e'])

    v_table = np.log(np.zeros((x.size, pi.size)))
    out = np.zeros(x.shape, dtype=int)

    viterbi(x, pi, emit, trans, v_table, out)

    print(v_table)
    print(out)


if __name__ == "__main__":
    main()
