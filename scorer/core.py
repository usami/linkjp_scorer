from enum import Enum
import csv
import sys

from . import attributes
from .helpers import load_json, generate_key, link_annotation


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

        self.load_gold_data()

    def load_gold_data(self):
        self.gold = {}
        for d in load_json(self.goldpath):
            self.gold[generate_key(d, 'html')] = link_annotation(d)
            self.gold[generate_key(d, 'text')] = link_annotation(d)
            self.counter[d['attribute']].gold_links += 1

    def calc_score(self, ignore_link_type=False):
        self.evaluate_answers(ignore_link_type)
        for attr in self.attributes:
            c = self.counter[attr]
            self.score[attr] = Score(c.precision(), c.recall())

    def evaluate_answers(self, ignore_link_type=False):
        for a in load_json(self.answerpath):
            if self.evaluate(link_annotation(a),
                             self.gold.get(generate_key(a), None),
                             ignore_link_type=ignore_link_type):
                self.counter[a['attribute']].correct_links += 1
            self.counter[a['attribute']].answered_links += 1

    def evaluate(self, answer, gold, ignore_link_type=False):
        if gold is None:
            return False

        if ignore_link_type:
            return answer[0] == gold[0]
        else:
            return answer == gold

    def print_score(self, output_format, out=sys.stdout):
        macro = macro_average(self.score.values())
        micro = micro_average(self.counter.values())

        if output_format == OutputFormat.CSV:
            scorewriter = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
            scorewriter.writerow(['属性名', '精度', '再現率', 'F値'])
            for attr in self.attributes:
                score = self.score[attr]
                scorewriter.writerow([attr,
                                      "{:.3f}".format(score.precision),
                                      "{:.3f}".format(score.recall),
                                      "{:.3f}".format(score.f1)])
            scorewriter.writerow(['macro-average',
                                  "{:.3f}".format(macro.precision),
                                  "{:.3f}".format(macro.recall),
                                  "{:.3f}".format(macro.f1)])

            scorewriter.writerow(['micro-average',
                                  "{:.3f}".format(micro.precision),
                                  "{:.3f}".format(micro.recall),
                                  "{:.3f}".format(micro.f1)])

        elif output_format == OutputFormat.TABLE:
            print('{:<4} {} {:<5} {}'.format(
                '精度', '再現率', 'F値', '属性名'), file=out)
            for attr in self.attributes:
                score = self.score[attr]
                print('{:<6.3f} {:<6.3f} {:<6.3f} {}'.format(
                    score.precision, score.recall, score.f1, attr), file=out)

            print('{:<6.3f} {:<6.3f} {:<6.3f} {}'.format(
                macro.precision, macro.recall, macro.f1, 'macro-average'),
                file=out)
            print('{:<6.3f} {:<6.3f} {:<6.3f} {}'.format(
                micro.precision, micro.recall, micro.f1, 'micro-average'),
                file=out)


def micro_average(counters):
    total = Counter()
    total.correct_links = sum(c.correct_links for c in counters)
    total.gold_links = sum(c.gold_links for c in counters)
    total.answered_links = sum(c.answered_links for c in counters)
    return Score(total.precision(), total.recall())


def macro_average(scores):
    n = len(scores)
    ave_p = sum(s.precision for s in scores) / n
    ave_r = sum(s.recall for s in scores) / n
    return Score(ave_p, ave_r)
