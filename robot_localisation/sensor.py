"""
This module implements the sensor that tracks the robot.

"""
import numpy as np
from numpy.random import random_sample
from robot_localisation.robot import Robot
from robot_localisation.grid import *
from enum import IntEnum


class Pos(IntEnum):
    """
    The different possible types of positions the sensor can report.
    """
    true = 1
    surrounding = 2
    next_surrounding = 3
    nothing = 4


class Sensor:

    """
    The sensor approximates the location of the robot according to:
     - the true location L with probability 0.1
     - any of the 8 surrounding fields L_s with probability 0.05 each
     - any of the next 16 surrounding fields L_s2 with probability 0.025 each
     - nothing with probability 0.1
    """

    def __init__(self):
        self.surr = [
            (-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1),
            (+1, -1), (+1, 0), (+1, +1)
        ]

        self.next_surr = [
            (-2, -2), (-2, -1), (-2,  0), (-2, 1), (-2,  2),
            (-1, -2), (-1, +2), ( 0, -2), (+0, 2), (+1, -2),
            (+1, +2), (+2, -2), (+2, -1), (+2, 0), (+2,  1),
            (+2, +2)
        ]

    def get_position(self, robot):
        # todo: maybe rewrite as a generator, on each iteration
        # asking robot to move one step or should that be the
        # responsibility of the caller?
        """
        Return approximate location of the robot.
        """
        real_pos = robot.get_position()
        values = np.array(
            [Pos.true, Pos.surrounding, Pos.next_surrounding, Pos.nothing])
        probabilities = np.array([0.1, 0.4, 0.4, 0.1])
        bins = np.add.accumulate(probabilities)
        pos_type = values[np.digitize(random_sample(1), bins)][0]
        return {
            Pos.true: real_pos,
            Pos.surrounding: Sensor.surrounding(real_pos),
            Pos.next_surrounding: Sensor.next_surrounding(real_pos),
            Pos.nothing: None,
        }[pos_type]

    def surrounding(pos):
        """
        Return a random adjacent position to 'pos'.
        """
        x, y = pos
        choices = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1),
                   (x+1, y-1), (x+1, y), (x+1, y+1)]
        return choices[np.random.randint(len(choices))]

    def next_surrounding(pos):
        """
        Return a random next-adjacent position to 'pos'.
        """
        x, y = pos
        choices = [(x-2, y-2), (x-2, y-1), (x-2, y), (x-2, y+1), (x-2, y+2),
                   (x-1, y-2), (x-1, y+2), (x, y-2), (x, y+2), (x+1, y-2),
                   (x+1, y+2), (x+2, y-2), (x+2, y-1), (x+2, y), (x+2, y+1),
                   (x+2, y+2)]
        return choices[np.random.randint(len(choices))]

    def get_obs_matrix(self, position, grid_shape):
        if position is None:
            return None

        mat = np.zeros(grid_shape)
        x, y = position
        height, width = grid_shape

        # centre position
        mat[position] = 0.1

        # first surrounding
        for a, b in self.surr:
            if -1 < x+a < width and -1 < y+b < height:
                mat[x+a, y+b] = 0.05

        # second surrounding
        for a, b in self.next_surr:
            if -1 < x+a < width and -1 < y+b < height:
                mat[x+a, y+b] = 0.025

        return mat


if __name__ == '__main__':
    sens = Sensor()
    print(sens.get_obs_matrix((3, 3), (10, 10)))
    print(sens.get_obs_matrix((3, 3), (4, 4)))



