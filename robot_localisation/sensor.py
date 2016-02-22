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
        n = grid_shape[0] * grid_shape[1] * 4
        mat = np.zeros((n,))
        x, y = position

        # index for facing north in the current position
        position_index = position_to_north_state(position, grid_shape)
        mat[position_index:position_index+4] = 0.1

        for o in self.next_surr:
            x_, y_ = x + o[0], y + o[1]
            if 0 <= x_ < grid_shape[0] and 0 <= y_ < grid_shape[1]:
                o_index = position_to_north_state((x_, y_), grid_shape)
                mat[o_index:o_index+4] = 0.025

        for o in self.surr:
            x_, y_ = x + o[0], y + o[1]
            if 0 <= x_ < grid_shape[0] and 0 <= y_ < grid_shape[1]:
                o_index = position_to_north_state((x_, y_), grid_shape)
                mat[o_index:o_index+4] = 0.05

        return np.diag(mat)


def position_to_north_state(position, grid_shape):
    return (position[0] * grid_shape[1] + position[1]) * 4


if __name__ == '__main__':
    trans = build_transition_matrix(3, 3)

    np.set_printoptions(linewidth=1000, threshold=10000)
    sens = Sensor()
    obs = sens.get_obs_matrix((1, 1), (2, 2))

    print(np.diag(obs))



