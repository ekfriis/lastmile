''' Route Map

Store a collection of nodes and information about their interrelations 

'''

import ants.graph.operations as op
import ants.parameters as params
import numpy as np

class RouteMap(object):
    ''' Central point for informationg aboug graph edges

    Caches matrices of distance, time, cost, and inverse cost for traveling
    between different points on the graph (i.e. delivery destinations)

    '''
    def __init__(self, destinations=None):
        self.destinations = destinations

        # Cache all the cost matrices
        # Dollar cost due to distance between nodes
        self.distances = op.distance_cost_array(destinations)

        # Dollar cost due to travel time between nodes
        self.time_costs = op.time_cost_array(destinations)

        # Travel time between nodes
        self.times = op.times_array(destinations)

        # Meta dollar cost due to schedule incompatability between nodes.  Note
        # that this cost is only used to estimate the 'cost of unsatisfaction,'
        # when the heuristic is trying to find the best route.  It gives an a
        # priori estimate of how compatabile the nodeA->nodeB transition is,
        # assuming that nodeA's arrival time is a satisfactory one.
        self.compatabilities = \
                op.compatability_cost_array(destinations)

        # Tangible (distance & time) cost matrix
        self.tangible_costs = self.distances + self.time_costs
        
        # Total cost matrix, includes meta cost for poorly compatible nodes
        self.costs = self.tangible_costs + self.compatabilities

        # 1/C(i,j) for C(i,j) in matrix, used for doing ant direction choice
        self.cheapness = 1.0/self.costs
        self.tangible_cheapness = 1.0/self.tangible_costs

    def random_start_time(self):
        ''' Throw a departure time from the origin '''
        return self.destinations[0].time_pref.random()

    def num_destinations(self):
        ''' Get the number of destinations to service '''
        return len(self.destinations)

    def cheapness_for_destinations(self, start_index):
        ''' Return inverse cost for all possible destinations from start '''
        return self.cheapness[start_index, :]

    def tangible_cost_for_edge(self, start_index, end_index):
        ''' Return the tangible cost to travel from start to end '''
        return self.tangible_costs[start_index, end_index]

    def time_for_edge(self, start, end):
        ''' Return the time of travel from start to end '''
        return self.times[start, end]

    def total_tangible_cost_for_route(self, route):
        ''' Return total tangible cost for a route '''
        return sum(op.quantify_route(
            route, cost_func=self.tangible_cost_for_edge))

    def sim_arrival_times(self, route, start_time=0):
        output = [0]*len(route)
        current_time = start_time
        # Departure from origin
        output[0] = current_time
        for start, end in op.route_hops(route):
            # Sim delivery time @ start
            current_time += self.destinations[end].throw_delivery_time()
            # Travel from start to end
            current_time += self.time_for_edge(start, end)
            output[end] = current_time
        return output

    def hist_arrival_times(self, route, iterations=500):
        # First axis is sim#, second is destination index
        return np.array(
            [self.sim_arrival_times(route) for i in range(iterations)])

    @params.use_parameters
    def total_satisfaction_costs(self, route, iterations=None, 
                                 cost_per_sad_customer=None):
        ''' Simulate the route and determine average satisfaction '''
        total_satisfaction = 0.
        for iteration in range(iterations):
            # Pull a random start time from the base
            current_time = self.destinations[route[0]].time_pref.random()
            for start, end in op.route_hops(route):
                # Time to move from start to end
                current_time = self.time_for_edge(start, end)
                # Get our current customer
                customer = self.destinations[end]
                # Find if customer at end was satisfied
                total_satisfaction += \
                        customer.satisfaction_probability(current_time)
                # Throw a random delivery time for this customer
                current_time += customer.throw_delivery_time()
        # Normalize satisfaction
        normalization = iterations*1.0
        return (1-(total_satisfaction / normalization))*cost_per_sad_customer


