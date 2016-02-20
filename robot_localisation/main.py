"""
This module contains the logic to run the simulation.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import argparse
from robot_localisation.grid import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Robot localisation with HMM')
    parser.add_argument(
        '-r', '--rows',
        type=int,
        help='the number of rows on the grid, default is 4',
        default=4)
    parser.add_argument(
        '-c', '--columns',
        type=int,
        help='the number of columns on the grid, default is 4',
        default=4)
    args = parser.parse_args()
    the_grid = Grid(height=args.rows, width=args.columns) # or something
    print(the_grid)
