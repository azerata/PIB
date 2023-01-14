from __future__ import annotations
import os
import pathlib
import argparse
import pandas as pd
import seaborn as sns
import matplotlib as plt
import time
import timeit


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

    test_funcs: list[str] = ["c_regular.py", "c_unpack.py", "c_unroll.py"]
    # "c_regular.py", "c_unpack.py", "c_unroll.py","python_regular.py", "python_unpack.py"

    algs = []
    times = []
    n_size = []
    for fn in os.scandir(path):
        print(fn)
        for fun in test_funcs:
            n_size.append(int(str(fn).split('_')[-1].split("'")[0]))
            algs.append(fun)
            print(f"python {fun} {os.path.join(data_dir , fn.name)}")
            #t1 = time.process_time()
            # os.system(
            #    f"python {fun} {os.path.join(data_dir , fn.name)}")
            #t2 = time.process_time() - t1
            t2 = timeit.timeit(
                f"os.system('python {fun} {os.path.join(data_dir , fn.name)}')", number=1, setup="import os")
            times.append(t2)
    print(times, algs, n_size)

    data = pd.DataFrame({"algorithm": algs, "time": times, "n_size": n_size})
    with open(f"{args.outname}.csv", 'wt') as file:
        data.to_csv(file)

    plot = sns.lmplot(x='n_size', y='time', hue='algorithm',
                      data=data, markers='.', x_jitter=0.1)
    plot.savefig(f"{args.outname}.png")


if __name__ == "__main__":
    main()
