
import numpy as np


class FilterState:
    def __init__(self, n: int, transition: np.ndarray):
        """
        :param n: number of states
        :param transition: the transition matrix
        """
        self.n = n

        # initialise the belief matrix, we assume a uniform distribution
        # across all possible states (NB access to the belief matrix is done
        # via self.belief_matrix from now on and is normalised upon assignment,
        # see belief_matrix.setter)
        self._belief_matrix = np.ones(shape=(n,)) / n

        # store a reference to the transpose of the transition matrix
        self.t_T = transition.T

    @property
    def belief_matrix(self):
        """
        Store the belief matrix as a property
        """
        return self._belief_matrix

    @belief_matrix.setter
    def belief_matrix(self, value: np.ndarray):
        """
        Always perform normalisation when setting the belief matrix

        :param value: non-normalised array for the belief matrix
        """
        self._belief_matrix = value / np.sum(value)

    @property
    def belief_state(self):
        pass

    @belief_state.getter
    def belief_state(self):
        return np.argmax(self.belief_matrix)

    def forward(self, o: np.ndarray):
        self.belief_matrix = o.dot(self.t_T.dot(self.belief_matrix))

    def __str__(self):
        return str(self.belief_matrix)


if __name__ == '__main__':
    from robot_localisation import grid, sensor, robot

    size = (4, 4)

    trans_mat = grid.build_transition_matrix(*size)
    filt = FilterState(n=4*4*4, transition=trans_mat)
    sens = sensor.Sensor()
    rob = robot.Robot()
    grid = grid.Grid(*size)

    print(filt.belief_matrix.reshape(size))

    for i in range(10):
        o = sens.get_position(rob)
        filt.forward(o)
        print(filt.belief_matrix.reshape(size))
