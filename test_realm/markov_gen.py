from __future__ import annotations
import numpy as np
import argparse
import pickle
from ctypes import c_int, c_double
from sklearn.preprocessing import normalize


def main():
    argparser = argparse.ArgumentParser(
        "markov_gen", description="generate random or semi random probability matrices for hidden markov models.")
    argparser.add_argument(
        "states", type=int, help="Number of states in model")
    argparser.add_argument("emits", type=int, help="Number of emissions")
    argparser.add_argument("n", type=int, help="length of emits")
    argparser.add_argument(
        "out", type=argparse.FileType('wb'), help="output file")
    argparser.add_argument("-s", "--sparse", action="store_true",
                           help="use this if you want a sparse matrix (diagonal +/- 1)")

    args = argparser.parse_args()

    states = np.random.rand(args.states, args.states)
    if args.sparse:
        for i in range(args.states):
            for j in range(args.states):
                if not(j+2 > i > j-2):
                    states[i, j] = 0

    states = normalize(states, norm="l1", axis=1)

    emits = np.random.rand(args.states, args.emits)
    emits = normalize(emits, norm="l1", axis=1)

    pi = np.random.rand(1, args.states)
    pi = normalize(pi, norm='l1')

    x = np.random.randint(0, args.emits - 1, args.n)

    out = {"t": states, "e": emits, "p": pi, "x": x}

    pickle.dump(out, args.out)

    args.out.close()


if __name__ == "__main__":
    main()
