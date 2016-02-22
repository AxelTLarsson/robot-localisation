import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unittest import TestCase
import unittest
from robot_localisation.main import manhattan


class TestManhattan(TestCase):

    def test_manhattan(self):
        pos1 = (0, 1)
        pos2 = (1, 1)
        self.assertEqual(manhattan(pos1, pos2), 1)
        pos1 = (10, 3)
        pos2 = (4, 7)
        self.assertEqual(manhattan(pos1, pos2), 10)

if __name__ == '__main__':
    unittest.main()
