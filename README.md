# Optimization of the Traveling Salesman Problem

This is a command line program that generates a randomized traveling salesman problem of a given size and attempts to optimize a solution using simulated annealing.

## Help

Use the -h or --help switch to view help text in your terminal.
- -s or --size determines the size of the problem, i.e. the number of cities to travel. The default is 20.
- -a or --sa is a switch to use the simulated annealing method. It defaults to true.
- -m or --mcmc is a switch to use the markov chain monte carlo method. It defaults to false.
- -r or --report is a switch to turn on code performance reporting using the cProfile python library.
- -i or --iterations determines the number of iterations to run at each temperature.
- -o or --output is a switch to turn on result output, saving data and graphs. It defaults to off.
