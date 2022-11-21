import argparse


def main():
    argparser = argparse.ArgumentParser(
        "Viterbi", description="runs viterbi algorithm on, currently still testing on hardcoded input")
    argparser.add_argument("-c", "--compile", action="store_true",
                           help="add -c flag if the c library should be recompiled before running")

    args = argparser.parse_args()
