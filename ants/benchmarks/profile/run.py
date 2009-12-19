from ants.graph.routemap import RouteMap
from ants.graph.colony import Colony

import matplotlib.pyplot as plt
import math
import numpy as np

print "Loading geocoder"
from ants.benchmarks.routes.sf_full import destinations
#from ants.benchmarks.routes.sf_small import destinations
# No time prefs for now
print "Loading route map"
routemap = RouteMap(destinations)
colony = Colony(routemap)

def run(count=400):
    for i in range(count):
        print "Iter", i
        colony.run_ants()
        colony.update_pheromones()

    cost_routes = colony.routes_and_results.values()
    cost_routes.sort(key=lambda a: a[0])

    return cost_routes

def build_histograms(routes, routes_to_take=400, dist_fn=lambda c,b:math.exp(c/b)):
    best_cost, best_route = routes[0]
    # Count locations for stop 5
    histogram = [ [ 0 for i in range(len(best_route)) ] 
                 for i in range(len(best_route)-1) ]
    for index, (cost, route) in enumerate(routes):
        if index > routes_to_take:
            break
        for route_index, stop_number in enumerate(route):
            # Distance to best cost
            dist_to_best = dist_fn(cost, best_cost)
            histogram[stop_number][route_index] += 1.0/dist_to_best
    return histogram

def build_arrival_histograms(routes, routemap, routes_to_take=200):
    routesims = []
    best_cost, best_route = routes[0]
    for index, (cost, route) in enumerate(routes):
        if index > routes_to_take:
            break
        routesims.append(routemap.hist_arrival_times(route))
    # Stack the weighed objects together
    return np.vstack(tuple(routesims))

def plot_order_for(dest, histograms, binning_scale=1):
    plt.clf()
    histo = histograms[dest]
    n, bins, patches = plt.hist(range(len(histo)), weights=histo, bins=(colony.num_dest/binning_scale), normed=1, facecolor='green', alpha=0.75)
    plt.show()

def plot_times_for(dest, histograms, bins, **kwargs):
    plt.clf()
    n, bins, patches = plt.hist(histograms[:,dest], bins=bins, normed=1, facecolor='green', alpha=0.75, **kwargs)
    plt.show()

if __name__ == "__main__":
    #import cProfile
    #cProfile.run('run()')
    #run()
    pass

