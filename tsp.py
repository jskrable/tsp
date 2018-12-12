"""
tsp.py
10-29-2018
jack skrable
"""

import annealing as an
import output as out
import utils
import random
import cProfile
from datetime import datetime, timezone
from timeit import default_timer as timer

# init global
CITIES = []
OUTPUT = {}
DT = datetime.now()

# Get path for output results
ts = DT.strftime('%Y%m%d%H%M%S')
PATH = 'results/' + ts + '/'


def run(tour, algorithm, report, iterations):
    # Function to run a given algorithm

    global OUTPUT

    alg = an.anneal if algorithm == 'sa' else mcmc

    # Init results
    results = {}
    start = timer()

    # Check reporting switch
    if report:
        run = cProfile.run("'"+alg+"(tour,iterations)'")

    else:
        run = alg(tour, iterations)

    # Close timer and get duration
    end = timer()
    dur = end - start

    # Split return tuple
    tour = run[0]
    OUTPUT.update({'alpha': run[1]})
    efforts = run[2]

    # Plot significant partial efforts
    for i in range(len(efforts)):
        plotname = PATH + 'partial_' + str("%03d" % i)
        partial = utils.State(efforts[i]['tour'],
                              efforts[i]['temp'],
                              an.cost(efforts[i]['tour']),
                              0.5,
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


def main():
    # Main function. Parses arguments, initializes random problem, solves problem.
    
    args = utils.arg_parser()
    OUTPUT.update({'size': args.size,
                   'iterations': args.iterations
                   })
    # Create initial tour visiting each city in order of creation
    tour = []
    n = args.size
    for i in range(n):
        i = utils.City(i, random.randint(0, n**2), random.randint(0, n**2))
        tour.append(i)

    # Display or save initial problem
    problem = utils.State(tour,
                          1.0,
                          0,
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
    solution = utils.State(results['sa']['tour'],
                           0,
                           results['sa']['cost'],
                           1,
                           True,
                           PATH)
    out.plot_tsp(solution)

    # Get timestamp for output file
    ts = DT.strftime('%Y-%m-%d %H:%M:%S')
    OUTPUT.update({'timestamp': ts})

    print('writing results...')
    out.write_results('run_stats', OUTPUT)
    out.animate(PATH)
    print('complete')


if __name__ == '__main__':
    main()
