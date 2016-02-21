
from random import randint


class Robot:
    """
    Representation of the actual robot.
    """

    def __init__(self, grid_shape, position=None):
        if position is None:
            self.position = randint(grid_shape[0]), randint(grid_shape[1])
        else:
            self.position = position

    def get_position(self):
        return self.position

    def step(self):
        """
        Move one step on the grid.
        """
        self.position = self.__update_position()

    def __update_position(self):
        """
        P( keep heading | not encountering a wall) = 0.7
        P( change heading | not encountering a wall) = 0.3
        P( keep heading | encountering a wall) = 0.0
        P( change heading | encountering a wall) = 1.0
        """
        pass
