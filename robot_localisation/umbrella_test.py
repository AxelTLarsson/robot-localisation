
import numpy as np


class TransitionModel:
    pass


class ObservationModel:
    pass


class FilterState:
    def __init__(self, n: int, transition: np.ndarray):
        """

        :param n: number of states
        """
        self.n = n  # do we need to keep this??

        # initialise the belief matrix
        self._belief_matrix = np.ones(shape=(n,)) / n

        # store a reference to the transition matrix
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
    obs_true = np.zeros((2, 2))
    obs_true[0, 0] = 0.9
    obs_true[1, 1] = 0.2
    
    obs_false = np.zeros((2, 2))
    obs_false[0, 0] = 0.1
    obs_false[1, 1] = 0.8

    trans = np.zeros((2, 2))
    trans[0, 0] = 0.7
    trans[1, 1] = 0.7
    trans[0, 1] = 0.3
    trans[1, 0] = 0.3

    filter = FilterState(n=2, transition=trans)

    # print initial values
    print(filter.belief_matrix)
    print(filter.belief_state)

    # day 1
    filter.forward(o=obs_true)
    print(filter.belief_matrix)

    # day 2
    filter.forward(o=obs_true)
    print(filter.belief_matrix)




