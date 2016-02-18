
import numpy as np
from robot_localisation import grid
from unittest import TestCase


class TestGrid(TestCase):

    def test_directional_transition_matrix_2x2_north(self):
        ret = grid.build_directional_transition_model(2, 2, 'N')

        correct = np.array([
            [ 0.,   0.5,  0.5,  0. ],
            [ 0.5,  0.,   0.,   0.5],
            [ 0.7,  0.,   0.,   0.3],
            [ 0.,   0.7,  0.3,  0. ],
        ])

        self.assertAlmostEqual(np.sum(ret - correct), 0)
        self.assertAlmostEqual(np.sum(ret), 4)

    def test_directional_transition_matrix_2x2_south(self):
        ret = grid.build_directional_transition_model(2, 2, 'N')

        correct = np.array([
            [ 0.,   0.3,  0.7,  0. ],
            [ 0.3,  0.,   0.,   0.7],
            [ 0.5,  0.,   0.,   0.5],
            [ 0.,   0.5,  0.5,  0. ],
        ])

        self.assertAlmostEqual(np.sum(ret - correct), 0)
        self.assertAlmostEqual(np.sum(ret), 4)

    def test_directional_transition_matrix_2x2_east(self):
        ret = grid.build_directional_transition_model(2, 2, 'N')

        correct = np.array([
            [ 0.,   0.7,  0.3,  0. ],
            [ 0.5,  0.,   0.,   0.5],
            [ 0.3,  0.,   0.,   0.7],
            [ 0.,   0.5,  0.5,  0. ],
        ])

        self.assertAlmostEqual(np.sum(ret - correct), 0)
        self.assertAlmostEqual(np.sum(ret), 4)

    def test_directional_transition_matrix_2x2_west(self):
        ret = grid.build_directional_transition_model(2, 2, 'N')

        correct = np.array([
            [ 0.,   0.5,  0.5,  0. ],
            [ 0.7,  0.,   0.,   0.3],
            [ 0.5,  0.,   0.,   0.5],
            [ 0.,   0.3,  0.7,  0. ],
        ])

        self.assertAlmostEqual(np.sum(ret - correct), 0)
        self.assertAlmostEqual(np.sum(ret), 4)

    def test_directional_transition_matrix_3x3_north(self):
        ret = grid.build_directional_transition_model(3, 3, 'N')

        correct = np.array([
         [0.,         0.5, 0.,         0.5, 0.,         0.,   0.,   0.,   0., ],
         [0.33333333, 0.,  0.33333333, 0.,  0.33333333, 0.,   0.,   0.,   0., ],
         [0.,         0.5, 0.,         0.,  0.,         0.5,  0.,   0.,   0., ],
         [0.7,        0.,  0.,         0.,  0.15,       0.,   0.15, 0.,   0., ],
         [0.,         0.7, 0.,         0.1, 0.,         0.1,  0.,   0.1,  0., ],
         [0.,         0.,  0.7,        0.,  0.15,       0.,   0.,   0.,   0.15],
         [0.,         0.,  0.,         0.7, 0.,         0.,   0.,   0.3,  0., ],
         [0.,         0.,  0.,         0.,  0.7,        0.,   0.15, 0.,   0.15],
         [0.,         0.,  0.,         0.,  0.,         0.7,  0.,   0.3,  0., ]
        ])

        self.assertAlmostEqual(np.sum(ret - correct), 0)
        self.assertAlmostEqual(np.sum(ret), 9)


