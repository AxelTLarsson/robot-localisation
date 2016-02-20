
import numpy as np


class FilterState:
    def __init__(self, n: int, transitions: dict):
        """
        :param n: number of states
        :param transitions: a dictionary of directional transition matrices,
            this must contain "north", "east", "south", "west"
        """
        self.n = n

        # initialise the belief matrix, we assume a uniform distribution
        # across all possible states (NB access to the belief matrix is done
        # via self.belief_matrix from now on and is normalised upon assignment,
        # see belief_matrix.setter)
        self._belief_matrix = np.ones(shape=(n,)) / n

        # store a reference to the transpose of the transition matrix
        self.transitions = transitions

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

    def forward(self, o: np.ndarray, heading: str):
        self.belief_matrix = o.dot(self.transitions[heading].T
                                   .dot(self.belief_matrix))

    def __str__(self):
        return str(self.belief_matrix)


if __name__ == '__main__':
    from robot_localisation import grid

    n = grid.build_directional_transition_model(4, 4, 'N')
    e = grid.build_directional_transition_model(4, 4, 'E')
    s = grid.build_directional_transition_model(4, 4, 'S')
    w = grid.build_directional_transition_model(4, 4, 'W')

    transitions = {
        "north": n,
        "east": e,
        "south": s,
        "west": w,
    }

    f = FilterState(n=4*4*4, transitions=transitions)



