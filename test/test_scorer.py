import unittest
import os

import scorer


class TestScorer(unittest.TestCase):

    def test_init(self):
        goldpath = os.path.dirname(__file__) + '/data/airport.json'
        s = scorer.Scorer(scorer.Category('airport'),
                          goldpath,
                          'answer')

        self.assertEqual(str(s.category), 'airport')
        self.assertEqual(len(s.attributes), 9)
        self.assertEqual(s.goldpath, goldpath)
        self.assertEqual(s.answerpath, 'answer')
        for c in s.counter.values():
            self.assertEqual(c.correct_links, 0)
            self.assertEqual(c.answered_links, 0)
        self.assertEqual(s.score, {})
        self.assertNotEqual(s.text_gold, {})
        self.assertNotEqual(s.html_gold, {})

    def test_duplicate_gold(self):
        goldpath = os.path.dirname(__file__) + '/data/city.json'
        s = scorer.Scorer(scorer.Category('city'),
                          goldpath,
                          'answer')

        self.assertEqual(s.counter["合併市区町村"].gold_links, 9)


if __name__ == '__main__':
    unittest.main()
