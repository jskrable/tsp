import random, sys
from dataclasses import dataclass
import matplotlib.pyplot as plt

# init globals
cities = []
dist_matrix = {}
path = []

# function to get random coordinates
def rand(size):
	return random.randint(0,size)

# function to calculate euclidian distance
def dist(a,b):
	x = abs(a[0]-b[0])
	y = abs(a[1]-b[1])
	return int((x**2 + y**2)**0.5)

# dataclass version
@dataclass
class City:

	name: str
	x: float
	y: float

	def addToList(self):
		cities.append(self)

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
		plt.plot(x,y,'ro-')
	else:
		plt.plot(x,y,'ro')
	plt.show()

"""
main: create three cities and display their info
"""
size = int(sys.argv[1])

for i in range(size):
	i = newCity(i)

"""
a = newCity('a')
b = newCity('b')
c = newCity('c')
"""

showCities()
popDist()
print(dist_matrix)
plotTSP(cities,False)


