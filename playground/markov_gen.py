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

    # Transition probs
    states = np.random.rand(args.states, args.states).astype(c_double)
    if args.sparse:
        for i in range(args.states):
            for j in range(args.states):
                if not(j+2 > i > j-2):
                    states[i, j] = 0

    states = normalize(states, norm="l1", axis=1)

    t_array: list[tuple[int, int, float]] = []

    for i in range(args.states):
        for j in range(args.states):
            if states[i, j] != 0:
                t_array.append((i, j, np.log(states[i, j])))

    # emition probs
    emits = np.random.rand(args.states, args.emits).astype(c_double)
    emits = normalize(emits, norm="l1", axis=1)

    # initial probs
    pi = np.random.rand(1, args.states).astype(c_double)
    pi = normalize(pi, norm='l1')

    # Example input
    x = np.random.randint(0, args.emits - 1, args.n).astype(c_int)

    out = {"t": states, "e": emits, "p": pi, "x": x, "a": t_array}

    pickle.dump(out, args.out)

    args.out.close()
    # with open("./test.bin", "rb") as file:
    #    tmp = pickle.load(file)
    # for i in tmp:
    #    print(i, tmp[i])


if __name__ == "__main__":
    main()
