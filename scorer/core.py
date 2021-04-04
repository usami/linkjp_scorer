import csv
import sys

from . import attributes


class Score:

    def __init__(self):
        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0


class Scorer:

    def __init__(self, category):
        self.category = category
        self.attributes = attributes.set(category)
        self.score = {}

    def calc_score(self):
        for attr in self.attributes:
            self.score[attr] = Score()

    def print_score(self, format='csv', out=sys.stdout):
        if format == 'csv':
            scorewriter = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
            scorewriter.writerow(['属性名', '精度', '再現率', 'F値'])
            for attr in self.attributes:
                score = self.score[attr]
                scorewriter.writerow([attr,
                                      "{:.3f}".format(score.precision),
                                      "{:.3f}".format(score.recall),
                                      "{:.3f}".format(score.f1)])
