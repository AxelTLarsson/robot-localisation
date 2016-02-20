from unittest import TestCase
from robot_localisation.robot import Robot
from robot_localisation.sensor import Sensor


class SensorTest(TestCase):

    def test_surrounding(self):
        robot = Robot()
        sensor = Sensor()

        # print('\n')
        for i in range(10000):
            p = sensor.get_position(robot)
            # print(p)
