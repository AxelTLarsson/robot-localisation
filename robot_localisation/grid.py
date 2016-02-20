import numpy as np


class Heading:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Grid:

    def __init__(self, height=4, width=4):
        # the grid itself will be stored as a 3 dimensional array of (x, y, h)
        # where h is the heading referring to the numbers shown in Heading
        self.shape = (height, width)
        self._grid = np.zeros((height, width, 4))
        self.states = height * width * 4

    def id_to_index(self, id):
        return ((id / 4) % self.shape[1], int((id / 4) // self.shape[1]))

    def __str__(self):
        pass


def build_transition_model(height, width):
    n = height * width * 4
    model = np.zeros((n, n))
    edges = dict()

    for i in range(n):  # let i be the current state
        # edge detection
        edges["up"] = i < width
        edges["down"] = i >= (height - 1) * width
        edges["left"] = i % width == 0
        edges["right"] = (i + 1) % width == 0
        n_edges = sum(edges.values())

        for j in range(n):  # let j be the transition state
            if i == j:
                pass
            elif abs(j - i) < 4:
                pass
            elif (i - j) / width == 4:
                model[i, j] = 0.7

    return model


def build_directional_transition_model(height, width, orientation):
    n = height * width
    model = np.zeros((n, n))
    edges = dict()
    trans = dict()

    sp = {  # dictionary denoting special connections between
            # orientations and directions
        'N': 'up',
        'S': 'down',
        'E': 'right',
        'W': 'left'
    }

    for i in range(n):  # i = current state

        # edge detection
        edges["up"] = i < width
        edges["down"] = i >= (height - 1) * width
        edges["left"] = i % width == 0
        edges["right"] = (i + 1) % width == 0
        n_edges = sum(edges.values())

        for j in range(n):  # j = transition state
            
            if i == j:
                continue
            
            trans["up"] = (i - j) / width == 1
            trans["down"] = (i - j) / width == -1
            trans["left"] = (i - j) == 1 and i % width != 0
            trans["right"] = (i - j) == -1 and (i + 1) % width != 0

            for o, m in sp.items():
                if trans[m]:
                    if orientation == o:
                        model[i, j] = 0.7
                        continue
                    elif edges[sp[orientation]]:
                        model[i, j] = 1 / (4 - n_edges)
                        continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        continue

    return model


def combine_directional_transition_models(n, e, s, w):
    """

    :param n:
    :param e:
    :param s:
    :param w:
    :return: combined model
    """
    shape = n.shape[0]*4, n.shape[1]*4
    model = np.array([i for i in zip(n.flat, e.flat, s.flat, w.flat)])
    # model.reshape(shape)

    return model


if __name__ == '__main__':
    # model = build_transition_model(2, 2)
    model = build_directional_transition_model(2, 2, 'W')
    print(model)
    print(np.sum(model, axis=1))

    n = build_directional_transition_model(2, 2, 'N')
    e = build_directional_transition_model(2, 2, 'E')
    s = build_directional_transition_model(2, 2, 'S')
    w = build_directional_transition_model(2, 2, 'W')

    model = combine_directional_transition_models(n, e, s, w)
    print(model.shape)
    print(model)
