import numpy as np
from enum import IntEnum


class Heading(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Grid:

    def __init__(self, height, width):
        # the grid itself will be stored as a 3 dimensional array of (x, y, h)
        # where h is the heading referring to the numbers shown in Heading
        self.shape = (height, width)
        self._grid = np.zeros((height, width, 4))
        self.states = height * width * 4

    def index_to_pose(self, id):
        """
        Convert a numerical index to corresponding pose.

        E.g. index_to_pose(5) = (0, 1, North) where North is a Heading
        """
        return (int((id / 4) // self.shape[1]),  # row
                int((id / 4) % self.shape[1]),  # column
                Heading(id % 4))  # heading

    def __str__(self):
        pass

    def pose_to_index(self, pose):
        """
        Translate a pose of type (x, y, Heading) to a numerical index that can
        be used with the transition matrix.

        E.g. pose_to_index((0,1,N)) = 5 where N is a Heading
        """
        # compute square_nbr as row-major on the grid, first grid is nbr 0
        cols = self.shape[1]
        x, y, h = pose
        square_nbr = x * cols + y
        return square_nbr * 4 + int(h)


def build_transition_matrix(height, width):
    n = height * width * 4
    model = np.zeros((n, n))
    edges = [0, 0, 0, 0]
    trans = [0, 0, 0, 0]
    row_length = 4 * width  # could use this to skip some rows for optimisation

    headings = [Heading.NORTH, Heading.EAST, Heading.SOUTH, Heading.WEST]

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
                # j += row_length - (j % row_length)  # skip the rest of the row
                j += 1
                continue

            for h in headings:
                if i_heading == h:
                    if i_heading - j_heading != 0 and trans[j_heading]:
                        if edges[i_heading]:
                            model[i, j] = 1 / (4 - n_edges)
                            # continue
                        else:
                            model[i, j] = 0.3 / (3 - n_edges)
                            # continue
                    break
            j += 1
        i += 1

    return model


if __name__ == '__main__':

    np.set_printoptions(precision=2, threshold=5000, linewidth=300)
    g = Grid(3, 3)
    print(g.index_to_pose(28))

    t = build_transition_matrix(4, 4)
    s = np.sum(t, axis=1)
    print(t.shape)
    print(s.shape)
    print(t)
    print(s)
