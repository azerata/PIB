from __future__ import annotations
import matplotlib as plt
import seaborn as sns
import sys
import argparse
import os
import pathlib


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "input", type=str, help="string: name of input folder containing data to use.")
    argparser.add_argument("-o", "--outdir", type=str,
                           help='name of output folder, default is "plots"', default="plots")
    argparser.add_argument(
        "prefix", type=str, help="prefix added to output plot")

    args = argparser.parse_args()

    # setup result folder
    parent_dir = pathlib.Path(__file__).parent
    input_dir = os.path.join(parent_dir, args.input)
    for fn in os.scandir(parent_dir):
        print(type(fn))


if __name__ == "__main__":
    main()
