import unittest
import os

from scorer import Category, Scorer


class TestCategory(unittest.TestCase):

    def test_init(self):
        c = Category('airport')
        self.assertEqual(str(c), 'airport')

    def test_list(self):
        self.assertEqual(len(list(Category)), 7)


class TestAttributes(unittest.TestCase):

    def test_set(self):
        s = Scorer(Category('airport'),
                   os.path.dirname(__file__) + '/data/airport.json', 'answer')
        self.assertEqual(len(s.attributes), 9)


if __name__ == '__main__':
    unittest.main()
