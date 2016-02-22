"""
This module contains the logic to run the simulation.
"""
import sys
import os
import argparse
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from robot_localisation.grid import Grid, build_transition_matrix
from robot_localisation.robot import Robot, Sensor
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
    help                    show this help text
    show T                  show the transition matrix T
    show f                  show the filter column vector
    show O                  show the observation matrix
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
    sensor_value = None
    obs = None

    print(help_text())
    print("Grid size is {} x {}".format(size[0], size[1]))
    print(the_robot)
    print("The sensor says: {}".format(sensor_value))
    filter_est = the_grid.index_to_pose(the_filter.belief_state)
    pos_est = (filter_est[0], filter_est[1])
    print("The HMM filter thinks the robot is at {}".format(filter_est))
    print("The Manhattan distance is: {}".format(
        manhattan(the_robot.get_position(), pos_est)))
    np.set_printoptions(linewidth=1000)

    # Main loop
    while True:
        user_command = str(input('> '))
        if user_command.upper() == 'QUIT' or user_command.upper() == 'Q':
            break
        elif user_command.upper() == 'HELP':
            print(help_text())
        elif user_command.upper() == 'SHOW T':
            print(the_T_matrix)
        elif user_command.upper() == 'SHOW F':
            print(the_filter.belief_matrix)
        elif user_command.upper() == 'SHOW O':
            print(obs)
        elif not user_command:
            # take a step then approximate etc.
            the_robot.step()
            sensor_value = the_sensor.get_position(the_robot)
            obs = the_sensor.get_obs_matrix(sensor_value, size)
            the_filter.forward(obs)

            print(the_robot)
            print("The sensor says: {}".format(sensor_value))
            filter_est = the_grid.index_to_pose(the_filter.belief_state)
            pos_est = (filter_est[0], filter_est[1])
            print("The HMM filter thinks the robot is at {}".format(filter_est))
            print("The Manhattan distance is: {}".format(
                manhattan(the_robot.get_position(), pos_est)))

        else:
            print("Unknown command!")


def manhattan(pos1, pos2):
    """
    Calculate the Manhattan distance between pos1 and pos2.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1-x2) + abs(y1-y2)


def automated_run():
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10, 7))
    navg = 20
    nsteps = 10

    for size in (2, 2), (3, 3), (4, 4), (5, 5), (10, 10):

        avg_distances = np.zeros(shape=(nsteps+1,))

        for n in range(navg):

            distances = list()
            none_values = list()

            the_T_matrix = build_transition_matrix(*size)
            the_filter = FilterState(transition=the_T_matrix)
            the_sensor = Sensor()
            the_grid = Grid(*size)
            the_robot = Robot(the_grid, the_T_matrix)

            # get the manhattan distance at the start
            filter_est = the_grid.index_to_pose(the_filter.belief_state)
            pos_est = (filter_est[0], filter_est[1])
            distances.append(manhattan(the_robot.get_position(), pos_est))

            for i in range(nsteps):

                # take a step then approximate etc.
                the_robot.step()
                sensor_value = the_sensor.get_position(the_robot)
                if sensor_value is None:
                    none_values.append(i)  # keep track of where None was returned

                obs = the_sensor.get_obs_matrix(sensor_value, size)
                the_filter.forward(obs)

                filter_est = the_grid.index_to_pose(the_filter.belief_state)
                pos_est = (filter_est[0], filter_est[1])
                distances.append(manhattan(the_robot.get_position(), pos_est))

            avg_distances += np.array(distances)

        avg_distances /= navg
        base_line, = plt.plot(avg_distances, label="Grid size {}".format(size))

        # for point in none_values:
        #     plt.scatter(point, distances[point], marker='o',
        #                 color=base_line.get_color(), s=40)

    plt.legend()
    plt.xlim(0, nsteps)
    plt.ylim(0,)
    plt.ylabel("Manhattan distance")
    plt.xlabel("Steps")
    plt.title("Manhattan distance from true position and inferred position \n"
              "from the hidden Markov model (average over %s runs)" % navg)
    fig.savefig("automated_run.png")
    plt.show()


if __name__ == '__main__':
    main()
    # automated_run()
