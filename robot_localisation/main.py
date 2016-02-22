"""
This module contains the logic to run the simulation.
"""
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from robot_localisation.grid import Grid, build_transition_matrix
from robot_localisation.sensor import Sensor
from robot_localisation.robot import Robot
from robot_localisation.hmm_filter import FilterState


def help_text():
    """
    Return a helpful text explaining usage of the program.
    """
    return """
------------------------------- HMM Filtering ---------------------------------
Type a command to get started. Type 'quit' or 'q' to quit.

Valid commands (all commands are case insensitive):
    ENTER                   move the robot one step further in the simulation,
                            will also output current pose and estimated
                            position of the robot
    go <delay in seconds>   step throgh simulation with the delay specified
    help                    show this help text
    show T                  show the transition matrix T
    show f                  show the filter column vector
    show 0                  show the observation matrix
    quit | q                quit the program
-------------------------------------------------------------------------------
    """


def main():
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

    # Initialise the program
    size = (args.rows, args.columns)
    the_T_matrix = build_transition_matrix(*size)
    the_filter = FilterState(transition=the_T_matrix)
    the_sensor = Sensor()
    the_grid = Grid(*size)
    the_robot = Robot(the_grid, the_T_matrix)

    print(help_text())
    print("Grid size is {} x {}".format(size[0], size[1]))
    print(the_robot)
    sensor_value = the_sensor.get_position(the_robot)
    print("The sensor says: {}".format(sensor_value))

    # Main loop
    while True:
        user_command = str(input('> '))
        if user_command.upper() == 'QUIT' or user_command.upper() == 'Q':
            break
        elif user_command.upper() == 'HELP':
            print(help_text())
        elif user_command.upper() == 'SHOW T':
            print("todo")
        elif user_command.upper() == 'SHOW F':
            print("todo")
        elif user_command.upper() == 'SHOW O':
            print("todo")
        elif not user_command.upper():
            the_robot.step()
            print(the_robot)
            print("The sensor says: {}".format(
                the_sensor.get_position(the_robot)))
            print("The HMM filter thinks the robot is at {}".format("fix"))
            print("The Manhattan distance is: {}".format(
                manhattan(the_robot.get_position(), sensor_value)))

        else:
            print("Unknown command!")


def manhattan(pos1, pos2):
    """
    Calculate the Manhattan distance between pos1 and pos2.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1-x2) + abs(y1-y2)

if __name__ == '__main__':
    main()
