from unittest import TestCase
from robot_localisation import grid, robot
from robot_localisation.grid import Heading


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
