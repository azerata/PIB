from __future__ import annotations
import os
import pathlib
import argparse
import pandas as pd
import seaborn as sns
import matplotlib as plt


def main():
    argparser = argparse.ArgumentParser(
        "script for testing running times of the viterbi implementations")
    argparser.add_argument(
        "input", type=str, help="name of folder containing input files")

    args = argparser.parse_args()

    parent_dir = pathlib.Path(__file__).parent
    data_dir = args.input
    path = os.path.join(parent_dir, data_dir)

    test_funcs: list[str] = []

    times = []
    n_size = []

    for fn in os.scandir(path):
        for fun in test_funcs:


if __name__ == "__main__":
    main()
