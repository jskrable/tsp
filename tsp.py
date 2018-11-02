import random

city_list = ['A','B','C','D']

dist_matrix = [[0,54,10,67], # A
			   [54,0,47,21], # B
			   [10,47,0,31], # C
			   [67,21,31,0]] # D

def randCoords():
	return (random.randint(0,50),random.randint(0,50))

class City(object):
	def __init__(self, name, coords):
		self.name = name
		self.coords = coords

for i, val in enumerate(city_list):
	val = City(val,randCoords())
	print(val.name, val.coords)

