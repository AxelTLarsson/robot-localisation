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

    for i in range(n):  # let i be the current state
        for j in range(n):  # let j be the transition state
            if i == j:
                pass
            elif abs(j - i) < 4:
                pass
            elif (i - j) / width == 4:
                model[i, j] = 0.7

    return model


def build_directional_transition_model(height, width, direction):
    n = height * width
    model = np.zeros((n, n))
    edges = dict()
    move = dict()

    for i in range(n):  # current state

        # edge detection
        edges["left"] = i % width == 0
        edges["right"] = (i + 1) % width == 0
        edges["top"] = i < width
        edges["bottom"] = i >= (height - 1) * width

        n_edges = sum(edges.values())

        for j in range(n):  # transition state

            # for name, s in edges.items():
            #     if s:
            #         print("%s is a %s edge" % (str((i, j)), name))

            if i == j:
                pass
            elif (i - j) / width == -1:  # transition to tile below
                if direction == 'S':
                    model[i, j] = 0.7
                elif direction == 'N':
                    if edges["top"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'E':
                    if edges["right"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'W':
                    if edges["left"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)

            elif (i - j) / width == 1:  # transition to tile above
                if direction == 'N':
                    model[i, j] = 0.7
                elif direction == 'S':
                    if edges["bottom"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'E':
                    if edges["right"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'W':
                    if edges["left"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)

            elif (i - j) == -1 and (i+1)%width != 0:  # transition to the right
                if direction == 'E':
                    model[i, j] = 0.7
                elif direction == 'N':
                    if edges["top"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'S':
                    if edges["bottom"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'W':
                    if edges["left"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)

            elif (i - j) == 1 and i % width != 0:  # transition to the left
                if direction == 'W':
                    model[i, j] = 0.7
                elif direction == 'N':
                    if edges["top"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'S':
                    if edges["bottom"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)
                elif direction == 'E':
                    if edges["right"]:
                        model[i, j] = 1 / (4 - n_edges)
                    else:
                        model[i, j] = 0.3 / (3 - n_edges)

    return model


if __name__ == '__main__':
    # model = build_transition_model(2, 2)
    model = build_directional_transition_model(4, 4, 'S')
    print(model)
    print(np.sum(model, axis=1))
