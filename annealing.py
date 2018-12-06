import math
import copy
import random


def dist(a, b):
    # function to calculate euclidian distance
    x = abs(a.x-b.x)
    y = abs(a.y-b.y)
    return int((x**2 + y**2)**0.5)


def cost(tour):
    # function to calc total tour dist
    # init total distance
    d = 0
    # append distance between each stop on tour
    for i in range(len(tour)-1):
        a = tour[i]
        b = tour[i+1]
        d += dist(a, b)

    # include cost to return to start
    d += dist(tour[0], tour[-1])

    return d


def calc_alpha(tour):
    # function to calculate alpha based on average distance between cities

    sum_cost = 0
    n = len(tour)

    # loop through cities
    for origin in tour:
        for dest in tour:
            # total the distances
            sum_cost += dist(origin, dest)
            

    # get average distance between two cities
    mean = (sum_cost / n) / 100

    # return normalized (0-1.0) alpha
    # TODO normalize between 0.8 and 0.99
    # TRY MEAN??? NOT WORKING 
    return math.exp(-1/mean)

# function to modify tour to a neighbor


def neighbor(tour):
    # function to swap order of tour by 1
    n = range(len(tour))
    a, b = random.sample(n, 2)
    tour[a], tour[b] = tour[b], tour[a]
    return tour


def acceptance(old, new, temp):
    # function to get acceptance probability
    # perfect prob if new tour is better
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


def anneal(tour, iterations):
    # solve problem using simulated annealing
    """
    TODO use calculated alpha? 
    should calculated alpha be a different function?
    """
    efforts = []
    alpha = calc_alpha(tour)
    # can hardcode alpha here
    #alpha = 0.99
    print('calculated alpha is ' + str(alpha))
    temp = 1.0
    min_temp = 0.00001
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
            ap = acceptance(old_cost, new_cost, temp)
            # randomize acceptance
            if ap > random.random():
                # save new tour
                tour = new_tour
                old_cost = new_cost
            # if lower than best cost
            if new_cost < cost(best_tour):
                # save best tour
                best_tour = copy.copy(new_tour)
            # next trial at current temp
            i += 1
            if i == iterations:
                efforts.append({'temp': temp,
                                'tour': best_tour})
        # decrease temp
        temp = temp * alpha
    return best_tour, alpha, efforts
