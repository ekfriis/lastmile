''' Route Map

Store a collection of nodes and information about their interrelations 

'''

import numpy as np

from ants.graph.operations import *

class RouteMap(object):
    def __init__(self, destinations=None,
                 dollar_per_km=1.0,
                 dollar_per_hour=8.0,
                 cost_per_sad_customer=4.0,
                 initial_pheromone_level=0.1,
                 pheremone_evaporation=0.2):

        # Cache all the cost matrices
        self.distances = distance_cost_array(destinations, dollar_per_km)
        self.times = time_cost_array(destinations, dollar_per_hour)
        self.compatabilities = compatability_cost_array(destinations, 
                                                        cost_per_sad_customer)

        # Total cost matrix
        self.cost_array = self.distances + self.times + self.compatabilities

        # 1/C(i,j) for C(i,j) in matrix, used for doing ant direction choice
        self.cheapness_array = 1.0/self.cost_array
