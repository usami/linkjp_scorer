import argparse

from scorer import Scorer, Category, OutputFormat

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('category', help='target category',
                        type=Category, choices=list(Category))
    parser.add_argument('--format', help='specify output format',
                        type=OutputFormat, choices=list(OutputFormat),
                        default=OutputFormat.CSV)

    args = parser.parse_args()

    scorer = Scorer(args.category)
    scorer.calc_score()

    scorer.print_score()
