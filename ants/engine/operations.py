''' Graph Operations

Numeric utilties to build and manipulate the edge matrices used in optimizing
the route.

'''
import ants.parameters as params
import numpy as np
from ants.engine.utilities import consecutive_pairs, operate_on_pairs

def destination_cost_array(destinations, cost_func=lambda start, end: None):
    ''' Generalized construction of 2d arrays describing graph edge costs

    For a list of N destinations, returns an N*N array [cost] such that

        cost[i,j] is the cost of moving *from* node i *to* node j

    The cost_func is passed nodes i and j as parameters.

    '''
    # Initialize 2d array
    output = np.zeros([len(destinations), len(destinations)])
    # First array index is always *from*
    for index_a, start in enumerate(destinations):
        for index_b, end in enumerate(destinations):
            output[index_a, index_b] = cost_func(start, end)
    return output

@params.use_parameters
def distance_cost_array(destinations, dollar_per_km=None):
    ''' Return cost matrix due to driving distance for a list of destinations'''
    distance_cost = lambda start, end: \
            start.distance_to(end)*dollar_per_km/1000.
    return destination_cost_array(destinations, cost_func=distance_cost)

@params.use_parameters
def time_cost_array(destinations, dollar_per_hour=None):
    ''' Return cost matrix due to driving time for a list of destinations '''
    time_cost = lambda start, end: start.time_to(end)*dollar_per_hour/60.
    return destination_cost_array(destinations, cost_func=time_cost)

def times_array(destinations):
    time = lambda start, end: start.time_to(end)
    return destination_cost_array(destinations, time)

@params.use_parameters
def compatability_cost_array(destinations, cost_per_sad_customer=None, 
                             iterations=None):
    ''' Return cost matrix due to incompatability between destinations '''
    def sadness_cost(start, end):
        ''' Definte cost of sadness due to incompatibile destinations'''
        if start == end:
            return 0.
        return (1 - start.compatability_to(end, iterations=iterations))*\
                cost_per_sad_customer

    return destination_cost_array(destinations, cost_func=sadness_cost)

def quantify_route(route, cost_func):
    ''' Yield cost_func(hop) for each hop in the route 

    Only a wrapper about operate_on_pairs from utilities, for clarity
    '''
    for cost in operate_on_pairs(route, cost_func):
        yield cost

def max_sorted_masked_array(array):
    ''' Return the maximum value of a sorted masked np.array'''
    index = np.ma.flatnotmasked_edges(array)[1]
    return array[index]

def select_edge_weighted(weights):
    ''' Return index of array randomly, weighted by array contents'''
    cumsum = np.cumsum(weights)
    # Find max value of array
    throw = np.random.rand()*max_sorted_masked_array(cumsum)
    return np.searchsorted(cumsum, throw)
