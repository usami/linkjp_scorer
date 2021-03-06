from collections import defaultdict
from enum import Enum
import csv
import sys

from . import attributes
from .helpers import load_json, deduped_answers, generate_key,\
    link_annotation, csv_format, table_format


class Counter:

    def __init__(self):
        self.correct_links = 0
        self.gold_links = 0
        self.answered_links = 0

    def precision(self):
        if self.answered_links == 0:
            return 0
        return self.correct_links / self.answered_links

    def recall(self):
        if self.gold_links == 0:
            return 0
        return self.correct_links / self.gold_links


class Score:

    def __init__(self, precision, recall):
        self.precision = precision
        self.recall = recall
        if precision == recall == 0:
            self.f1 = 0
        else:
            self.f1 = 2 * self.precision * self.recall / \
                (self.precision + self.recall)


class OutputFormat(Enum):
    CSV = 'csv'
    TABLE = 'table'

    def __str__(self):
        return self.value


class Scorer:

    def __init__(self, category, goldpath, answerpath):
        self.category = category
        self.attributes = attributes.set(category)
        self.goldpath = goldpath
        self.answerpath = answerpath
        self.counter = {attr: Counter() for attr in self.attributes}
        self.score = {}
        self.text_gold = defaultdict(set)
        self.html_gold = defaultdict(set)

        self.load_gold_data()

    def load_gold_data(self):
        """Load the gold data into the scorer for easier lookup, and
        count the number of links in the gold data for each attribute.
        """

        for d in load_json(self.goldpath):
            text_key, _ = generate_key(d, 'text')
            html_key, _ = generate_key(d, 'html')

            if len(self.text_gold[text_key]) == 0:
                self.counter[d['attribute']].gold_links += 1

            self.text_gold[text_key] |= {link_annotation(d)}
            self.html_gold[html_key] |= {link_annotation(d)}

    def calc_score(self, ignore_link_type=False):
        """Calculate scores for the target attributes.

        Keyword argument:
        ignore_link_type -- ignore link type fields (default: False)
        """

        self.evaluate_answers(ignore_link_type)
        for attr in self.attributes:
            c = self.counter[attr]
            self.score[attr] = Score(c.precision(), c.recall())

    def evaluate_answers(self, ignore_link_type=False):
        """Evaluate answers and store answer counts.

        Keyword argument:
        ignore_link_type -- ignore link type fields (default: False)
        """

        for a in deduped_answers(load_json(self.answerpath)):
            key, ot = generate_key(a)
            gold = self.text_gold[key] if ot == 'text' else self.html_gold[key]
            if self.evaluate(link_annotation(a),
                             gold,
                             ignore_link_type=ignore_link_type):
                self.counter[a['attribute']].correct_links += 1
            self.counter[a['attribute']].answered_links += 1

    def evaluate(self, answer, gold, ignore_link_type=False):
        """Return True if the answer is correct.

        Keyword argument:
        ignore_link_type -- ignore link type fields (default: False)
        """

        if gold is None:
            return False

        if ignore_link_type:
            return answer[0] in [g[0] for g in gold]
        else:
            return answer in gold

    def print_score(self, output_format=OutputFormat.TABLE, out=sys.stdout):
        """Print scores for the target attributes along with
        macro and micro averages.

        Keyword arguments:
        output_format -- the output format (default: OutputFormat.TABLE)
        out -- the output stream (default: sys.stdout)
        """

        macro = macro_average(self.score.values())
        micro = micro_average(self.counter.values())

        if output_format == OutputFormat.CSV:
            scorewriter = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
            scorewriter.writerow(['?????????', '??????', '?????????', 'F???'])
            for attr in self.attributes:
                scorewriter.writerow(csv_format(attr, self.score[attr]))

            scorewriter.writerow(csv_format('macro-average', macro))
            scorewriter.writerow(csv_format('micro-average', micro))

        elif output_format == OutputFormat.TABLE:
            print('{}  {}  {}  {}'.format(
                'precision', 'recall', 'f1-score', 'attribute'), file=out)
            for attr in self.attributes:
                print(table_format(attr, self.score[attr]), file=out)

            print(table_format('macro-average', macro), file=out)
            print(table_format('micro-average', micro), file=out)

    def link_type_available(self):
        """Return True if link type field is available in the answer data."""
        a = load_json(self.answerpath)[0]
        return 'link_type' in a


def micro_average(counters):
    """Return the micro average score."""
    total = Counter()
    total.correct_links = sum(c.correct_links for c in counters)
    total.gold_links = sum(c.gold_links for c in counters)
    total.answered_links = sum(c.answered_links for c in counters)
    return Score(total.precision(), total.recall())


def macro_average(scores):
    """Return the macro average score."""
    n = len(scores)
    ave_p = sum(s.precision for s in scores) / n
    ave_r = sum(s.recall for s in scores) / n
    return Score(ave_p, ave_r)
