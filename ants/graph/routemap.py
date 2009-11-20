''' Route Map

Store a collection of nodes and information about their interrelations 

'''

import numpy as np
import ants.graph.operations as op
# Define paramters
from ants.parameters import STD_PARAMS as params

class RouteMap(object):
    def __init__(self, destinations=None):

        # Cache all the cost matrices
        
        # Dollar cost due to distance between nodes
        self.distances = op.distance_cost_array(destinations, 
                                                params.dollar_per_km)

        # Dollar cost due to travel time between nodes
        self.times = op.time_cost_array(destinations, params.dollar_per_hour)

        # Meta dollar cost due to schedule incompatability between nodes.
        # Note that this cost is only used to estimate the 'cost of unsatisfaction,'
        # when the heuristic is trying to find the best route.  It gives an a priori
        # estimate of how compatabile the nodeA->nodeB transition is, assuming that 
        # nodeA's arrival time is a satisfactory one.
        self.compatabilities = op.compatability_cost_array(
            destinations, params.cost_per_sad_customer)

        # Tangible (distance & time) cost matrix
        self.tangible_cost_array = self.distances + self.times
        
        # Total cost matrix, includes meta cost for poorly compatible nodes
        self.cost_array = self.tangible_cost_array + self.compatabilities

        # 1/C(i,j) for C(i,j) in matrix, used for doing ant direction choice
        self.cheapness_array = 1.0/self.cost_array
    
    def cheapness_for_destinations(index):
        return self.cheapness[index, :]

