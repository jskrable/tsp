import argparse
from dataclasses import dataclass


@dataclass
class City:

    # Attributes
    name: str
    x: int
    y: int


@dataclass
class State:

    # Attributes
    tour: list
    temp: float
    cost: float
    complete: float
    save: bool
    path: str


def arg_parser():
        # function to parse arguments sent to CLI
    # setup argument parsing with description and -h method
    parser = argparse.ArgumentParser(
        description='Solve traveling salesman problem using simulated annealing')
    # add size int
    parser.add_argument('-s', '--size', default=20, type=int, nargs='?',
                        help='the number of cities to travel, default 20')
    # add iterations int
    parser.add_argument('-i', '--iterations', default=100, type=int, nargs='?',
                        help='the number of simulations to run, default 100')
    # add annealing switch
    parser.add_argument('-a', '--sa', default=True, type=bool, nargs='?',
                        help='use simulated annealing method')
    # add mcmc switch
    parser.add_argument('-m', '--mcmc', default=False, type=bool, nargs='?',
                        help='use markov chain monte carlo method')
    # add reporting switch
    parser.add_argument('-r', '--report', default=False, type=bool, nargs='?',
                        help='turn on code performance reporting')
    # add reporting switch
    parser.add_argument('-o', '--output', default=False, type=bool, nargs='?',
                        help='turn on result output, saving data and maps')
    # parse args and return
    args = parser.parse_args()
    return args
