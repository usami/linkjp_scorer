import unittest
import os

from scorer import Category, Scorer


class TestHelpers(unittest.TestCase):

    def test_deduped_answers(self):
        path = os.path.dirname(__file__)
        s = Scorer(Category('airport'),
                   path + '/data/airport.json',
                   path + '/data/multi-sample.json')
        s.evaluate_answers()

        nanswers = sum(c.answered_links for c in s.counter.values())
        self.assertEqual(nanswers, 3)
