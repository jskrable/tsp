"""
tsp.py
10-29-2018
jack skrable
"""

import random, sys, argparse, math, cProfile, copy, matplotlib.pyplot as plt
from dataclasses import dataclass
from datetime import datetime, timezone
from timeit import default_timer as timer 

# init global
CITIES = []
OUTPUT = {}
DT = datetime.now()

# dataclass for cities
@dataclass
class City:

	# attributes
	name: str
	x: int
	y: int

	# add to global list
	def add_to_list(self):
		CITIES.append(self)

# function to parse arguments sent to CLI
def arg_parser():
	# setup argument parsing with description and -h method
	parser = argparse.ArgumentParser(description='Solve the traveling salesman problem using simulated annealing and Markov Chain Monte Carlo Method')
	# add size int
	parser.add_argument('-s','--size',default=20,type=int,nargs='?', 
						help='the number of cities to travel, default 20')
	# add iterations int
	parser.add_argument('-i','--iterations',default=100,type=int,nargs='?',
						help='the number of simulations to run, default 100')
	# add annealing switch
	parser.add_argument('-a','--sa',default=True,type=bool,nargs='?',
						help='use simulated annealing method')
	# add mcmc switch
	parser.add_argument('-m','--mcmc',default=False,type=bool,nargs='?',
						help='use markov chain monte carlo method')
	# add reporting switch
	parser.add_argument('-r','--report',default=False,type=bool,nargs='?',
						help='turn on code performance reporting')
	# add reporting switch
	parser.add_argument('-o','--output',default=False,type=bool,nargs='?',
						help='turn on result output, saving data and maps')
	#parse args and return
	args = parser.parse_args()
	return args

# function to get random coordinates
def rand(size):
	return random.randint(0,size)

# function to calculate euclidian distance
def dist(a,b):
	x = abs(a.x-b.x)
	y = abs(a.y-b.y)
	return int((x**2 + y**2)**0.5)

# function to calc total tour dist
def cost(tour):
	# init total distance
	d = 0
	# append distance between each stop on tour
	for i in range(len(tour)-1):
		a = tour[i]
		b = tour[i+1]
		d += dist(a,b)

	# include cost to return to start
	d += dist(tour[0],tour[-1])

	return d

# add new city in random location
def new_city(c, n):
	global CITIES
	c = City(c,rand(n*10),rand(n*10))
	c.add_to_list()
	# popDist()
	return c

# show list of cities
def show_cities():
	global CITIES 
	print('Here is a list of the cities and their coordinates: ')
	for i, val in enumerate(CITIES):
		print(val.name, (val.x, val.y))

# plot map of cities
def plot_tsp(cities, complete, save):
	# empty arrays for coords
	x = []
	y = []
	path = 'results/'
	ts = DT.strftime('%Y%m%d%H%M%S')
	for city in cities:
		# add each cities coords
		x.append(city.x)
		y.append(city.y)
		# add city labels
		plt.annotate(xy = [city.x,city.y], s = ' ' + str(city.name))
		plt.axis('off')
	if complete:
		# add trip back to source
		x.append(cities[0].x)
		y.append(cities[0].y)	
		# use dotted line connector
		plt.plot(x,y,'bo:')
		filename = path + 'solution_' + ts + '.png'
	else:
		# use points
		plt.plot(x,y,'ro')
		filename = path + 'problem_' + ts + '.png'
	if save:
		plt.savefig(filename)
	else:
		plt.show()

# function to write results to output file
def write_results(filename):
	global OUTPUT

	data = []
	file = filename + '.txt'
	# drop tour description
	del OUTPUT['tour']

	# arrange in csv
	for key in OUTPUT:
		data.append(str(OUTPUT[key]))

	csv = ','.join(data)
	csv += '\n'
	# write results to file
	with open(file,'a+') as f:		
		print('writing output file...')
		if f.tell() == 0:
			head = []
			for key in OUTPUT:
				head.append(str(key))
			headers = ','.join(head)
			headers += '\n'
			f.write(headers)
		f.write(csv)
		f.close()
		print(file + ' written successfully.')

# function to calc alpha value to solve adequately
def calc_alpha():
	global CITIES
	# init variables
	sum_cost = 0
	n = len(CITIES)

	# loop through cities
	for origin in CITIES:
		for dest in CITIES:
			# total the distances
			sum_cost += dist(origin,dest)

	# get average distance between two cities
	mean = sum_cost / n

	# return normalized (0-1.0) alpha
	# TODO normalize between 0.8 and 0.99
	return math.exp(-1/mean)

# function to modify tour to a neighbor
def neighbor(tour):
	n = range(len(tour))
	a, b = random.sample(n,2)
	tour[a], tour[b] = tour[b], tour[a]
	return tour

# function to get acceptance prob
def acceptance(old, new, temp):
	# perfect prob if new is better
	if new < old:
		return 1.0
	# otherwise base on difference
	else:
		try: 
			# normalized difference over temp
			return math.exp((new - old)/temp)
		except OverflowError:
			# catch overflow
			return float(-math.inf)

# solve problem using simulated annealing
def anneal(tour, iterations):
	"""
	TODO use calculated alpha? 
	should calculated alpha be a different function?
	"""
	global OUTPUT
	alpha = calc_alpha()
	#alpha = 0.99
	print('calculated alpha is ' + str(alpha))
	OUTPUT.update({'alpha': alpha})
	temp = 1.0
	min_temp = 0.0001
	best_tour = tour

	while temp > min_temp:
		i = 1
		# TODO play w this
		# size of simulation per temp
		while i <= iterations:
			# copy tour and cost
			old_tour = copy.copy(tour)
			old_cost = cost(old_tour)
			# get new tour and cost
			new_tour = neighbor(old_tour)
			new_cost = cost(new_tour)
			# get acceptance probablity
			ap = acceptance(old_cost,new_cost,temp)
			# randomize acceptance
			if ap > random.random():
				# save new tour 
				tour = new_tour
				old_cost = new_cost
			# if lower than best cost
			if new_cost < cost(best_tour):
				# save best tour
				best_tour = new_tour
			# next trial at current temp
			i += 1
		# decrease temp 
		temp = temp * alpha
	return best_tour


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

# function to run a given algorithm
def run(tour, algorithm, report, iterations):

	global OUTPUT

	# set function to use
	function = anneal if algorithm == 'sa' else mcmc

	# init results
	results = {}
	start = timer()

	# check reporting switch
	if report:
		tour = cProfile.run("'"+function+"'(tour,'"+iterations+")")
	else:
		# TODO update variable to include MCMC
		tour = function(tour, iterations)
	end = timer()
	dur = end - start

	# update results
	results.update({algorithm: {
							'tour': tour,
							'duration': dur,
							'cost': cost(tour)
							}
						})

	OUTPUT.update(results[algorithm])

	return results

# function to solve tsp
def solve(tour, sa, mcmc, report, iterations):

	results = {}
	
	# use both and compare
	if sa and mcmc:
		results.update(run(tour,'sa',report,iterations))
		results.update(run(tour,'mcmc',report,iterations))

	# use simulated annealing
	elif sa:
		results.update(run(tour,'sa',report,iterations))

	# use markov chain monte carlo
	elif mcmc:
		results.update(run(tour,'mcmc',report,iterations))

	return results

"""
main: create three cities and display their info
"""

if __name__ == '__main__':

	args = arg_parser()
	OUTPUT.update({'size': args.size,
					'iterations': args.iterations
					})
	# add all cities
	for i in range(args.size):
		i = new_city(i, args.size)

	# create initial tour visiting each city in order of creation
	tour = []
	for city in CITIES:
		tour.append(city)
	plot_tsp(CITIES,False,True)

	# randomize tour
	random.shuffle(tour)
	print('initial cost of random tour is ' + str(cost(tour)))

	# solve
	results = solve(tour,args.sa,args.mcmc,args.report,args.iterations)
	
	print('cost of solved tour is ' + str(results['sa']['cost']))
	print('time to solve was ' + str(results['sa']['duration']) + ' seconds')

	# show/save solved tour
	plot_tsp(results['sa']['tour'],True,True)
	
	# get timestamp for output file
	ts = DT.strftime('%Y-%m-%d %H:%M:%S')
	OUTPUT.update({'timestamp': ts})

	# write results file
	write_results('output')

	