import unittest
import os

import scorer


class TestScorer(unittest.TestCase):

    def setUp(self):

        self.goldpath = os.path.dirname(__file__) + '/data/airport.json'
        self.s = scorer.Scorer(scorer.Category('airport'),
                               self.goldpath,
                               'answer')

    def test_init(self):
        self.assertEqual(str(self.s.category), 'airport')
        self.assertEqual(len(self.s.attributes), 9)
        self.assertEqual(self.s.goldpath, self.goldpath)
        self.assertEqual(self.s.answerpath, 'answer')
        for c in self.s.counter.values():
            self.assertEqual(c.correct_links, 0)
            self.assertEqual(c.answered_links, 0)
        self.assertEqual(self.s.score, {})
        self.assertNotEqual(self.s.gold, {})


if __name__ == '__main__':
    unittest.main()
