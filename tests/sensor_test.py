from unittest import TestCase
from robot_localisation.robot import Robot
from robot_localisation.sensor import Sensor
from robot_localisation.grid import Grid
from robot_localisation import grid
import numpy as np


class SensorTest(TestCase):

    def test_surrounding(self):
        size = (4, 4)

        trans_mat = grid.build_transition_matrix(*size)
        robot = Robot(Grid(4, 4), trans_mat)
        sensor = Sensor()

        # print('\n')
        for i in range(10000):
            p = sensor.get_position(robot)
            # print(p)

    def test_get_obs_matrix_with_4x4(self):
        sens = Sensor()
        obs = sens.get_obs_matrix(position=(1, 1), grid_shape=(4, 4))

        obs_vec = np.diag(obs)
        self.assertEqual(len(obs_vec.nonzero()[0]), 64)

    def test_get_obs_matrix_with_2x2(self):
        sens = Sensor()

        obs = sens.get_obs_matrix(position=(1, 1), grid_shape=(2, 2))
        obs_vec = np.diag(obs)
        ans = np.array([
            0.05, 0.05, 0.05, 0.05,  # square (0, 0)
            0.05, 0.05, 0.05, 0.05,  # square (0, 1)
            0.05, 0.05, 0.05, 0.05,  # square (1, 0)
            0.1,  0.1,  0.1,  0.1  # square (1, 1)
        ])
        self.assertEqual(np.sum(obs_vec - ans), 0)

        obs = sens.get_obs_matrix(position=(0, 1), grid_shape=(2, 2))
        obs_vec = np.diag(obs)
        ans = np.array([
            0.05, 0.05, 0.05, 0.05,  # square (0, 0)
            0.1,  0.1,  0.1,  0.1,   # square (0, 1)
            0.05, 0.05, 0.05, 0.05,  # square (1, 0)
            0.05, 0.05, 0.05, 0.05,  # square (1, 1)
        ])
        self.assertEqual(np.sum(obs_vec - ans), 0)
