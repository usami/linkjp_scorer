import argparse

from scorer import Scorer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    scorer = Scorer()
    scorer.calc_score()

    scorer.print_score()
