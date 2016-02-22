from unittest import TestCase
from robot_localisation import grid, robot
from robot_localisation.grid import Heading
import numpy as np


class RobotTest(TestCase):

    def test_step(self):
        size = (4, 4)

        trans_mat = grid.build_transition_matrix(*size)
        robo = robot.Robot(grid.Grid(4, 4), trans_mat)

        # Test that the robot moves somewhat according to the rules
        for i in range(100):
            fst_pose = robo.get_pose()
            robo.step()
            snd_pose = robo.get_pose()
            self.assertNotEqual(fst_pose, snd_pose)
            if snd_pose[2] == Heading.EAST:
                self.assert_pose_east_of(snd_pose, fst_pose)
            elif snd_pose[2] == Heading.NORTH:
                self.assert_pose_north_of(snd_pose, fst_pose)
            elif snd_pose[2] == Heading.SOUTH:
                self.assert_pose_south_of(snd_pose, fst_pose),
            elif snd_pose[2] == Heading.WEST:
                self.assert_pose_west_of(snd_pose, fst_pose)

    def assert_pose_north_of(self, pose1, pose2):
        """
        Assert that pose1 is ONE step north of pose2.
        """
        x1, y1, _ = pose1
        x2, y2, _ = pose2
        self.assertEqual(x1 - x2, -1)
        self.assertEqual(y1, y2)

    def assert_pose_east_of(self, pose1, pose2):
        """
        Assert that pose1 is ONE step east of pose2.
        """
        x1, y1, _ = pose1
        x2, y2, _ = pose2
        self.assertEqual(y1 - y2, 1)
        self.assertEqual(x1, x2)

    def assert_pose_south_of(self, pose1, pose2):
        """
        Assert that pose1 is ONE step south of pose2.
        """
        x1, y1, _ = pose1
        x2, y2, _ = pose2
        self.assertEqual(x1 - x2, 1)
        self.assertEqual(y1, y2)

    def assert_pose_west_of(self, pose1, pose2):
        """
        Assert that pose1 is ONE step west of pose2.
        """
        x1, y1, _ = pose1
        x2, y2, _ = pose2
        self.assertEqual(y1 - y2, -1)
        self.assertEqual(x1, x2)


class SensorTest(TestCase):

    def test_surrounding(self):
        size = (4, 4)

        trans_mat = grid.build_transition_matrix(*size)
        rob = robot.Robot(grid.Grid(4, 4), trans_mat)
        sens = robot.Sensor()

        # print('\n')
        for i in range(10000):
            p = sens.get_position(rob)
            # print(p)

    def test_get_obs_matrix_with_4x4(self):
        sens = robot.Sensor()
        obs = sens.get_obs_matrix(position=(1, 1), grid_shape=(4, 4))

        obs_vec = np.diag(obs)
        self.assertEqual(len(obs_vec.nonzero()[0]), 64)

    def test_get_obs_matrix_with_2x2(self):
        sens = robot.Sensor()

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
