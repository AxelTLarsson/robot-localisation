from unittest import TestCase
from robot_localisation.robot import Robot
from robot_localisation.sensor import Sensor
from robot_localisation.grid import Grid
from robot_localisation import grid


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
