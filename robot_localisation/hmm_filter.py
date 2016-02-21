
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
        # the belief matrix is the "f_{1:t}" at init "f_{1:0}" = P(X_0)
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
    grid = grid.Grid(*size)
    rob = robot.Robot(grid, trans_mat)

    print(filt.belief_matrix.reshape(size))

    real_pos = rob.get_position()
    sens_pos = sens.get_position(rob)
    obs = sens.get_obs_matrix(sens_pos, size)
    filt.forward(obs)
    print(filt.belief_matrix.reshape(size))

