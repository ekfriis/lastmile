''' Graph Operations

Numeric utilties to build and manipulate the edge matrices used in optimizing
the route.

'''
import ants.parameters as params
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

def select_edge_weighted(weights):
    ''' Probabilistically select an index from an array where each element 
    is the relative weight. '''
    throw = np.random.rand()*np.sum(weights)
    return np.searchsorted(np.cumsum(weights), throw)

def route_hops(route):
    ''' Yield each route hop as a pair of (start, end) 
    Example: route_hops([1,2,3,4]) = [(1,2), (2,3), (3,4)]
    
    '''
    for start, end in zip(route[:-1], route[1:]):
        yield (start, end)

def quantify_route(route, cost_func):
    ''' Yield cost_func(hop) for each hop in the route '''
    for start, end in route_hops(route):
        yield cost_func(start, end)
