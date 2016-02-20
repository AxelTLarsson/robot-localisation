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
        return (int((id / 4) // self.shape[1]),  # row
                int((id / 4) % self.shape[1]),  # column
                id % 4)  # heading

    def __str__(self):
        pass


def build_transition_model(height, width):
    n = height * width * 4
    model = np.zeros((n, n))
    edges = [0, 0, 0, 0]
    trans = [0, 0, 0, 0]
    row_length = 4 * width

    headings = [Heading.NORTH, Heading.SOUTH, Heading.EAST, Heading.WEST]
    i = 0

    while i < n:  # let i be the current state
        j = 0
        ip = i // 4  # positional value for i (irrespective of heading)

        # edge detection
        edges[Heading.NORTH] = ip < width
        edges[Heading.SOUTH] = ip >= (height - 1) * width
        edges[Heading.EAST] = (ip + 1) % width == 0
        edges[Heading.WEST] = ip % width == 0
        n_edges = sum(edges)

        while j < n:  # j = transition state
            jp = j // 4  # positional value for j (irrespective of heading)

            if ip == jp:
                j += 4  # skip forward the rest of the states in this position
                continue

            trans[Heading.NORTH] = (ip - jp) / width == 1
            trans[Heading.SOUTH] = (ip - jp) / width == -1
            trans[Heading.EAST] = (ip - jp) == -1 and (ip + 1) % width != 0
            trans[Heading.WEST] = (ip - jp) == 1 and ip % width != 0

            i_heading = i % 4
            j_heading = j % 4

            if i_heading == j_heading and trans[i_heading]:
                model[i, j] = 0.7
                j += row_length - (j % row_length)  # skip the rest of the row
                continue
            if i_heading == Heading.NORTH:
                if i_heading - j_heading == -1 and trans[Heading.EAST]:
                    # going from N to E
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == -2 and trans[Heading.SOUTH]:
                    # going from N to S
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == -3 and trans[Heading.WEST]:
                    # going from N to W
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
            if i_heading == Heading.EAST:
                if i_heading - j_heading == 1 and trans[Heading.NORTH]:
                    # going from E to N
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == -1 and trans[Heading.SOUTH]:
                    # going from E to S
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == -2 and trans[Heading.WEST]:
                    # going from N to W
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
            if i_heading == Heading.SOUTH:
                if i_heading - j_heading == 2 and trans[Heading.NORTH]:
                    # going from S to N
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == 1 and trans[Heading.EAST]:
                    # going from S to E
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == -1 and trans[Heading.WEST]:
                    # going from S to W
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
            if i_heading == Heading.WEST:
                if i_heading - j_heading == 3 and trans[Heading.NORTH]:
                    # going from W to N
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == 2 and trans[Heading.EAST]:
                    # going from W to E
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
                elif i_heading - j_heading == 0 and trans[Heading.SOUTH]:
                    # going from W to S
                    if edges[i_heading]:
                        model[i, j] = 1 / (4 - n_edges)
                        # continue
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                        # continue
            j += 1
        i += 1

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

    np.set_printoptions(precision=2, threshold=5000, linewidth=300)
    g = Grid(3, 3)
    print(g.id_to_index(28))

    t = build_transition_model(3, 3)
    s = np.sum(t, axis=1)
    print(t.shape)
    print(s.shape)
    print(np.hstack((t, s)))

    # n = build_directional_transition_model(2, 2, 'N')
    # e = build_directional_transition_model(2, 2, 'E')
    # s = build_directional_transition_model(2, 2, 'S')
    # w = build_directional_transition_model(2, 2, 'W')
    #
    # model = combine_directional_transition_models(n, e, s, w)
    # print(model.shape)
    # print(model)
