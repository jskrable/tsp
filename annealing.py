import math
import copy
import random

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

# function to calc alpha value to solve adequately
def calc_alpha(tour):
	# init variables
	sum_cost = 0
	n = len(tour)

	# loop through cities
	for origin in tour:
		for dest in tour:
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
	#global OUTPUT
	alpha = calc_alpha(tour)
	#alpha = 0.99
	print('calculated alpha is ' + str(alpha))
	#OUTPUT.update({'alpha': alpha})
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