from enum import Enum
import csv
import sys

from . import attributes


class Counter:

    def __init__(self):
        self.tp = 0
        self.target = 0
        self.linked = 0

    def precision(self):
        return self.tp / self.linked

    def recall(self):
        return self.tp / self.target


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

    def __str__(self):
        return self.value


class Scorer:

    def __init__(self, category):
        self.category = category
        self.attributes = attributes.set(category)
        self.score = {}

    def calc_score(self):
        for attr in self.attributes:
            self.score[attr] = Score(0.0, 0.0)

    def print_score(self, output_format='csv', out=sys.stdout):
        if output_format == OutputFormat.CSV:
            scorewriter = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
            scorewriter.writerow(['属性名', '精度', '再現率', 'F値'])
            for attr in self.attributes:
                score = self.score[attr]
                scorewriter.writerow([attr,
                                      "{:.3f}".format(score.precision),
                                      "{:.3f}".format(score.recall),
                                      "{:.3f}".format(score.f1)])


def micro_average(counters):
    total = Counter()
    total.tp = sum(c.tp for c in counters)
    total.target = sum(c.target for c in counters)
    total.linked = sum(c.linked for c in counters)
    return Score(total.precision, total.recall)


def macro_average(scores):
    n = len(scores)
    ave_p = sum(s.precision for s in scores) / n
    ave_r = sum(s.recall for s in scores) / n
    return Score(ave_p, ave_r)
