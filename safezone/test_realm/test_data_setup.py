from __future__ import annotations
import pathlib
import os
import sys
import argparse


def main():
    argparser = argparse.ArgumentParser(
        "Setup Test Data",
        description="generate a range of data sets, with either constant number of states, or constant input length\ndumps all to binary files and puts in dir specified with --output(-o)")
    argparser.add_argument("type", choices=[
                           "sparse", "regular"], type=str, help="select type of transition matrices to generate")
    argparser.add_argument(
        "constant", type=str, help="choose which to keep constant, #states (s) or n-length (n)", choices=["n", "s"])
    argparser.add_argument("-o", "--output", type=str, default="output_data",
                           help="Name of dir to contain output files. defaults to 'output_data'")

    argparser.add_argument("emits", type=int, help="int: number of emissions")
    argparser.add_argument(
        "states", type=int, help="int: number of states in model OR minimum number of states used if n is constant")
    argparser.add_argument(
        "n", type=int, help="int: length of example input OR minimum length of n if s is constant")
    argparser.add_argument(
        "MAX", type=int, help="int: max used for either number of states OR lenght of n")

    args = argparser.parse_args()

    # setup dir
    parent_dir = pathlib.Path(__file__).parent
    data_dir = args.output
    base_name = args.output
    path = os.path.join(parent_dir, data_dir)
    os.mkdir(path)
    s = True if args.type == "sparse" else False

    # run generator
    if args.constant == 'n':
        generate_constant_n(args.emits, args.states, args.n,
                            args.MAX, os.path.join(path, base_name), s)
    elif args.constant == 's':
        generate_constane_k(args.emits, args.states, args.n,
                            args.MAX, os.path.join(path, base_name), s)


def generate_constant_n(emits: int, states: int, n: int, max: int, out: str, sparse: bool):
    step = max // 20
    s = ' -s' if sparse else ''
    for i in range(states, max+1, step):
        os.system(
            f'python markov_gen.py {i} {emits} {n} {out + "_" + str(i)}'+s)


def generate_constane_k(emits: int, states: int, n: int, max: int, out: int, sparse: bool):
    step = max // 20
    s = ' -s' if sparse else ''
    for i in range(n, max+1, step):
        os.system(
            f'python markov_gen.py {states} {emits} {i} {out + "_" + str(i)}'+s)


if __name__ == "__main__":
    main()
