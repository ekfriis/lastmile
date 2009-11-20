''' Graph Operations

Numeric utilties to build and manipulate the edge matrices used in optimizing
the route.

'''

import numpy as np

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


def distance_cost_array(destinations, dollar_per_km=1.0):
    ''' Return cost matrix due to driving distance for a list of destinations'''
    distance_cost = lambda start, end: \
            start.distance_to(end)*dollar_per_km/1000.
    return destination_cost_array(destinations, cost_func=distance_cost)


def time_cost_array(destinations, dollar_per_hour=8.0):
    ''' Return cost matrix due to driving time for a list of destinations '''
    time_cost = lambda start, end: start.time_to(end)*dollar_per_hour/60.
    return destination_cost_array(destinations, cost_func=time_cost)

def compatability_cost_array(destinations, cost_per_sad_customer=4.0, 
                             iterations=500):
    ''' Return cost matrix due to incompatability between destinations '''
    sadness_cost = lambda start, end: \
            (1 - start.compatability_to(end, iterations=iterations))* \
            cost_per_sad_customer
    return destination_cost_array(destinations, cost_func=sadness_cost)

