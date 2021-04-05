import argparse

from scorer import Scorer, Category, OutputFormat

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('category', help='target category.',
                        type=Category, choices=list(Category))
    parser.add_argument(
        'gold', help='filepath to gold annotation data.', type=str)
    parser.add_argument('answer', help='filepath to answer data.', type=str)

    parser.add_argument('--format', help='specify output format.',
                        type=OutputFormat, choices=list(OutputFormat),
                        default=OutputFormat.CSV)
    parser.add_argument('--ignore-link-type',
                        help='ignore link_type on evaluation,'
                        ' and eveluate only with link_page_id.',
                        action='store_true', default=False)

    args = parser.parse_args()

    scorer = Scorer(args.category, args.gold, args.answer)
    scorer.calc_score(args.ignore_link_type)

    scorer.print_score(args.format)
