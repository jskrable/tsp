"""
tsp.py
10-29-2018
jack skrable
"""

import random, sys, argparse, math, cProfile
from dataclasses import dataclass
import matplotlib.pyplot as plt

# init globals
cities = []
dist_matrix = {}
path = []

# function to parse arguments sent to CLI
def argParser():
	# setup argument parsing with description and -h method
	parser = argparse.ArgumentParser(description='Solve the traveling salesman problem using Markov Chain Monte Carlo Method')
	# add size int
	parser.add_argument('-s','--size',default=20,type=int,nargs='?', 
						help='the number of cities to travel')
	# add iterations int
	parser.add_argument('-i','--iterations',default=10000,type=int,nargs='?',
						help='the number of simulations to run')

	# add iterations int
	parser.add_argument('-r','--report',default=False,type=bool,nargs='?',
						help='turn on code performance reporting')
	#parse args and return
	args = parser.parse_args()
	return args.size, args.iterations, args.report

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

# dataclass version
@dataclass
class City:

	name: str
	x: float
	y: float

	def addToList(self):
		cities.append(self)

# add new city in random location
def newCity(c):
	global cities
	c = City(c,rand(100),rand(100))
	c.addToList()
	# popDist()
	return c

# show list of cities
def showCities():
	global cities 
	print('Here is a list of the cities and their coordinates: ')
	for i, val in enumerate(cities):
		print(val.name, (val.x, val.y))

# plot map of cities
def plotTSP(cities, complete):
	# empty arrays for coords
	x = []
	y = []
	for city in cities:
		# add each cities coords
		x.append(city.x)
		y.append(city.y)
		# add city labels
		plt.annotate(xy = [city.x,city.y], s = ' ' + str(city.name))
	if complete:
		# add trip back to source
		x.append(cities[0].x)
		y.append(cities[0].y)	
		# use dotted line connector
		plt.plot(x,y,'bo:')
	else:
		# use points
		plt.plot(x,y,'ro')
	# display	
	plt.show()

# function to modify tour to a neighbor
def neighbor(tour):
	n = range(len(tour))
	a, b = random.sample(n,2)
	tour[a], tour[b] = tour[b], tour[a]
	return tour

# solve problem using simulated annealing
def anneal(tour):
	best_tour = tour
	old_cost = cost(tour)
	temp = 1.0
	min_temp = 0.00001
	# TODO play w this
	alpha = 0.99
	while temp > min_temp:
		i = 1
		# TODO play w this
		while i <= 10000:
			new_tour = neighbor(tour)
			new_cost = cost(new_tour)
			ap = round(math.e**((new_cost-old_cost)/temp), 20)
			if ap > random.random():
				tour = new_tour
				old_cost = new_cost
			if new_cost > cost(best_tour):
				best_tour = new_tour
			i += 1
		temp = temp * alpha
	return best_tour



"""
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


"""
main: create three cities and display their info
"""
args = argParser()
size = args[0]
iterations = args[1]
report = args[2]

# add all citites
for i in range(size):
	i = newCity(i)

# create initial tour visiting each city in order of creation
tour = []
for city in cities:
	tour.append(city)
#print('total tour distance is: ')
#print(cost(tour))
# print list of cities
# showCities()
# plot cities
plotTSP(cities,False)

# randomize tour
random.shuffle(tour)
print('initial cost of random tour is ')
print(cost(tour))
# solve w/ annealing
if report:
	cProfile.run('anneal(tour)')
else:
	tour = anneal(tour)
print('cost of solved tour is ')
print(cost(tour))

# show solved tour
plotTSP(tour,True)


sum