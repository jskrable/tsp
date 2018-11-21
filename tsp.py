import random, sys, argparse
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
	#parse args and return
	args = parser.parse_args()
	return args.size, args.iterations

# function to get random coordinates
def rand(size):
	return random.randint(0,size)

# function to calculate euclidian distance
def dist(a,b):
	x = abs(a[0]-b[0])
	y = abs(a[1]-b[1])
	return int((x**2 + y**2)**0.5)

# function to calc total tour dist
def tourDist(tour):
	d = 0
	for i in range(len(tour)-1):
		a = (cities[i].x,cities[i].y)
		b = (cities[i+1].x,cities[i+1].y)
		d = d + dist(a,b)
	return d

# dataclass version
@dataclass
class City:

	name: str
	x: float
	y: float

	def addToList(self):
		cities.append(self)
"""
@dataclass
class Problem:

	initial: bool
	goal: bool


@dataclass
class State:

	path: list
	actions: list

@dataclass
class Node:

	depth: int
	parent: object
	state: object
"""

# populates global distance matrix
def popDist():
	global cities
	n = len(cities)
	for i in range(n-1):
		for j in range(i+1,n):
			a = (cities[i].x,cities[i].y)
			b = (cities[j].x,cities[j].y)
			dist_matrix[i,j] = dist(a,b)
			dist_matrix[j,i] = dist_matrix[i,j]

# add new city in random location
def newCity(c):
	global cities
	c = City(c,rand(100),rand(100))
	c.addToList()
	popDist()
	return c

# show list of cities
def showCities():
	global cities 
	print('Here is a list of the cities and their coordinates: ')
	for i, val in enumerate(cities):
		print(val.name, (val.x, val.y))

# plot map of cities
def plotTSP(cities, complete):
	x = []
	y = []
	for city in cities:
		x.append(city.x)
		y.append(city.y)
		plt.annotate(xy = [city.x,city.y], s = ' ' + str(city.name))
	if complete:
		x.append(cities[0].x)
		y.append(cities[0].y)	
		plt.plot(x,y,'bo-')
	else:
		plt.plot(x,y,'ro')
	plt.show()

# solve problem using mcmc
def mcmc(cities,iterations):
	# get initial tour in order of city name
	tour = []
	for city in cities:
		tour.append(city)
	# get initial tour distance
	dist = tourDist(tour)
	#for i in range(iterations):



"""
main: create three cities and display their info
"""
args = argParser()
size = args[0]
iterations = args[1]

for i in range(size):
	i = newCity(i)

tour = []
for city in cities:
	tour.append(city)

print('total tour distance is: ')
print(tourDist(tour))

showCities()
popDist()
# print(dist_matrix)
plotTSP(cities,False)
plotTSP(tour,True)


