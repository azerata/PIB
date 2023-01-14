import os
import pathlib
import argparse
import pickle


def main():
    argparser = argparse.ArgumentParser(
        "quick script to veryfy that my datagen worked")
    argparser.add_argument("dir", type=str)
    args = argparser.parse_args()

    parent_dir = pathlib.Path(__file__).parent
    data_dir = args.dir
    path = os.path.join(parent_dir, data_dir)

    for fn in os.scandir(path):
        with open(fn.path, "rb") as file:
            obj = pickle.load(file)
            print(obj["t"])


if __name__ == "__main__":
    main()
