import numpy as np
from robot_localisation.grid import Heading
from numpy.random import random_sample


class Robot:
    """
    Representation of the actual robot.
    """

    def __init__(self, grid, transition_matrix):
        """
        The robot starts at a random position drawn from
        a uniform distribution over the fields on the grid.
        The transition matrix is needed to compute the next
        step for the robot to make.
        """
        # pose = (row, col, heading)
        self.pose = (np.random.randint(0, grid.shape[0]),
                     np.random.randint(0, grid.shape[1]),
                     Heading(np.random.randint(0, 4)))
        self.grid = grid
        self.transition_matrix = transition_matrix

    def get_position(self):
        """
        Return the true position of the robot. I.e. the (x, y) from
        the pose (x, y, h).
        """
        x, y, h = self.pose
        return (x, y)

    def get_pose(self):
        """
        Return the current pose of the robot.
        """
        return self.pose

    def __str__(self):
        return "I am a robot at {}".format(str(self.pose))

    def step(self):
        """
        Move one step on the grid.

        P( keep heading | not encountering a wall) = 0.7
        P( change heading | not encountering a wall) = 0.3
        P( keep heading | encountering a wall) = 0.0
        P( change heading | encountering a wall) = 1.0

        This is all coded in the transition matrix which we
        reuse here for this purpose.
        """
        # Reuse the transition matrix
        probabilities = self.transition_matrix[
            self.grid.pose_to_index(self.pose)]
        values = np.array(
            list(range(0, self.grid.shape[0] * self.grid.shape[1] * 4)))
        bins = np.add.accumulate(probabilities)
        new_index = values[np.digitize(random_sample(1), bins)][0]
        self.pose = self.grid.index_to_pose(new_index)
