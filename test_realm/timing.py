from __future__ import annotations
import os
import pathlib
import argparse
import pandas as pd
import seaborn as sns
import matplotlib as plt
import time


def main():
    argparser = argparse.ArgumentParser(
        "script for testing running times of the viterbi implementations")
    argparser.add_argument(
        "input", type=str, help="name of folder containing input files")
    argparser.add_argument(
        "outname", type=str, help="do not include file extension, as this is both a plot and csv")

    args = argparser.parse_args()

    parent_dir = pathlib.Path(__file__).parent
    data_dir = args.input
    path = os.path.join(parent_dir, data_dir)

    test_funcs: list[str] = ["c_regular.py", "c_unpack.py",
                             "c_unroll.py", "python_regular.py", "python_unpack.py"]

    algs = []
    times = []
    n_size = []
    for fn in os.scandir(path):
        for fun in test_funcs:
            n_size.append(str(fn).split('_')[-1])
            algs.append(fun)
            t1 = time.process_time()
            os.system(f"python {fun} {fn}")
            t2 = time.process_time() - t1
            times.append(t2)

    data = pd.DataFrame({"alg": fun, "time": times, "n_size": n_size})
    plot = sns.lmplot(x='n_size', y='time', hue='alg',
                      lowess=True, data=data, markers='.')
    plot.savefig("outplot.png")
    with open(f"{args.outname}.csv", 'wt') as file:
        data.to_csv(file)


if __name__ == "__main__":
    main()
