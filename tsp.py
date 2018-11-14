import random

# init globals
cities = []
dist_matrix = {}

# function to get random coordinates
def randCoords():
	return (random.randint(0,50),random.randint(0,50))

# function to calculate euclidian distance
def dist(a,b):
	x = abs(a[0]-b[0])
	y = abs(a[1]-b[1])
	return int((x**2 + y**2)**0.5)

# object class to hold a city
class City(object):

	# constructor
	def __init__(self, name, coords):
		self.name = name
		self.coords = coords

	# add to global city list
	def addToList(self):
		cities.append(self)

# populates global distance matrix
def popDist():
	global cities
	n = len(cities)
	for i in range(n-1):
		for j in range(i+1,n):
			dist_matrix[i,j] = dist(cities[i].coords,cities[j].coords)
			dist_matrix[j,i] = dist_matrix[i,j]

# add new city in random location
def newCity(c):
	global cities
	c = City(c,randCoords())
	c.addToList()
	popDist()
	return c

# show list of cities
def showCities():
	global cities 
	for i, val in enumerate(cities):
		print(val.name, val.coords)

"""
main: create three cities and display their info
"""
a = newCity('a')
b = newCity('b')
c = newCity('c')

showCities()


