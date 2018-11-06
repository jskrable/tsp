import random

cities = []

dist_matrix = {}

def randCoords():
	return (random.randint(0,50),random.randint(0,50))

def dist(a,b):
	x = abs(a[0]-b[0])
	y = abs(a[1]-b[1])
	return int((x**2 + y**2)**0.5)

class City(object):

	def __init__(self, name, coords):
		self.name = name
		self.coords = coords

	def addToList(self, name):
		cities.append(self.name)

	def popDist(self, coords):
		n = len(cities)
		for i in range(n-1):
			for j in range(i+1,n):
				dist_matrix[i,j] = dist(i.coords,j.coords)
				dist_matrix[j,i] = dist_matrix[i,j]





def newCity(c):

	c = City(c,randCoords())
	c.addToList(c)
	return c

for i, val in enumerate(city_list):
	val = City(val,randCoords())
	print(val.name, val.coords)

