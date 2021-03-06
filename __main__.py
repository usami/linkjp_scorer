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
                        default=OutputFormat.TABLE)
    parser.add_argument('--ignore-link-type',
                        help='ignore link_type on evaluation,'
                        ' and eveluate only with link_page_id.',
                        action='store_true', default=False)
    parser.add_argument('--output', help='write output to the specified path.')

    args = parser.parse_args()

    scorer = Scorer(args.category, args.gold, args.answer)
    scorer.calc_score(args.ignore_link_type)

    if args.output:
        with open(args.output, 'w') as f:
            scorer.print_score(output_format=args.format, out=f)
    else:
        scorer.print_score(output_format=args.format)
