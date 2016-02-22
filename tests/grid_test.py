import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from robot_localisation import grid
from unittest import TestCase
import unittest


class TestGrid(TestCase):

    def test_transition_matrix_3x3(self):
        t = grid.build_transition_matrix(3, 3)

        # move in the direction of the heading
        for index in ((16, 4), (28, 16), (11, 7), (19, 15), (29, 33)):
            self.assertEqual(t[index], 0.7)

        # corner moving to another heading p=0.3
        self.assertEqual(t[1, 14], 0.3)
        self.assertEqual(t[11, 22], 0.3)
        self.assertEqual(t[10, 7], 0.3)
        self.assertEqual(t[2, 5], 0.3)
        self.assertEqual(t[25, 12], 0.3)

        # corner moving to another heading p=0.5
        self.assertEqual(t[27, 12], 0.5)
        self.assertEqual(t[26, 12], 0.5)
        self.assertEqual(t[9, 7], 0.5)
        self.assertEqual(t[9, 22], 0.5)

        # middle square to another square p=0.1
        self.assertAlmostEqual(t[16, 15], 0.1)
        self.assertAlmostEqual(t[17, 15], 0.1)
        self.assertAlmostEqual(t[17, 30], 0.1)

        # test some edge movements p=0.15
        self.assertAlmostEqual(t[23, 8], 0.15)
        self.assertAlmostEqual(t[13, 0], 0.15)
        self.assertAlmostEqual(t[13, 26], 0.15)

        self.assertAlmostEqual(np.sum(t), 36)

if __name__ == '__main__':
    unittest.main()
