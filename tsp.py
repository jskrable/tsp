"""
tsp.py
10-29-2018
jack skrable
"""

import annealing as an
import output as out
import random
import argparse
import cProfile
from dataclasses import dataclass
from datetime import datetime, timezone
from timeit import default_timer as timer

# init global
CITIES = []
OUTPUT = {}
DT = datetime.now()

# Get path for output results
ts = DT.strftime('%Y%m%d%H%M%S')
PATH = 'results/' + ts + '/'


@dataclass
class City:

    # Attributes
    name: str
    x: int
    y: int

    # Add to global list
    def add_to_list(self):
        CITIES.append(self)


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


def rand(size):
    # function to get random coordinates
    return random.randint(0, size)


def new_city(c, n):
    # add new city in random location
    global CITIES
    c = City(c, rand(n**2), rand(n**2))
    c.add_to_list()
    # popDist()
    return c


def show_cities():
    # show list of cities
    global CITIES
    print('Here is a list of the cities and their coordinates: ')
    for i, val in enumerate(CITIES):
        print(val.name, (val.x, val.y))


"""
TODO WRITE THIS DAMN THING
# solve problem using mcmc
def mcmc(cities,iterations):
    # get initial tour in order of city name
    tour = []
    for city in cities:
        tour.append(city)
    # get initial tour distance
    dist = cost(tour)
    for i in range(iterations):
"""


def run(tour, algorithm, report, iterations):
    # Function to run a given algorithm

    global OUTPUT

    function = an.anneal if algorithm == 'sa' else mcmc

    # Init results
    results = {}
    start = timer()

    # TODO add handling for efforts graphs here
    # Check reporting switch
    if report:
        run = cProfile.run("'"+function+"'(tour,'"+iterations+")")

    else:
        run = function(tour, iterations)

    # Close timer and get duration
    end = timer()
    dur = end - start

    # Split return tuple
    tour = run[0]
    OUTPUT.update({'alpha': run[1]})
    efforts = run[2]

    # Plot significant partial efforts
    for i in range(len(efforts)):
        plotname = PATH + 'temp_' + str("%03d"%i)
        partial = State(efforts[i]['tour'],
                        efforts[i]['temp'],
                        0.5,
                        an.cost(efforts[i]['tour']),
                        True,
                        plotname)
        out.plot_tsp(partial)

    # Update results
    results.update({algorithm: {
        'tour': tour,
        'duration': dur,
        'cost': an.cost(tour)
    }
    })

    OUTPUT.update(results[algorithm])

    return results


def solve(tour, sa, mcmc, report, iterations):
        # Function to solve problem

    results = {}

    # Use both and compare
    if sa and mcmc:
        results.update(run(tour, 'sa', report, iterations))
        results.update(run(tour, 'mcmc', report, iterations))

    # Use simulated annealing
    elif sa:
        results.update(run(tour, 'sa', report, iterations))

    # Use markov chain monte carlo
    elif mcmc:
        results.update(run(tour, 'mcmc', report, iterations))

    return results


"""
Main function. Parses arguments, initializes random problem, solves problem.
"""
if __name__ == '__main__':
    args = arg_parser()
    OUTPUT.update({'size': args.size,
                   'iterations': args.iterations
                   })
    # Add all cities
    for i in range(args.size):
        i = new_city(i, args.size)

    # Create initial tour visiting each city in order of creation
    tour = []
    for city in CITIES:
        tour.append(city)

    # Display or save initial problem
    problem = State(CITIES,
                    1.0,
                    an.cost(tour),
                    0,
                    True,
                    PATH)
    out.plot_tsp(problem)

    # Randomize tour
    # TODO Add a heuristic here???
    # Start with a better tour???
    random.shuffle(tour)

    print('initial cost of random tour is ' + str(an.cost(tour)))
    print('optimizing tour...')

    results = solve(tour, args.sa, args.mcmc, args.report, args.iterations)

    print('cost of solved tour is ' + str(results['sa']['cost']))
    print('time to solve was ' + str(results['sa']['duration']) + ' seconds')

    # Display or save solved tour
    solution = State(results['sa']['tour'],
                     0,
                     results['sa']['cost'],
                     1,
                     True,
                     PATH)
    out.plot_tsp(solution)

    # Get timestamp for output file
    ts = DT.strftime('%Y-%m-%d %H:%M:%S')
    OUTPUT.update({'timestamp': ts})

    out.write_results('run_stats', OUTPUT)
