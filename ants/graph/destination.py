''' Ants.Graph

Provides a graph node (Destination) and various utilities to construct the
edges (distances between destinations)

'''

import ants.parameters as params
from ants.metric import metric
import numpy as np

class Destination(object):
    ''' A delivery destination

    Stores an address, the latitude and longitude, and the time preferences for
    this destination.  Contains functions to determine times/distances to other
    destinations and a throw_delivery_time() function that can simulate variable
    delivery durations at this address.
    
    '''
    def __init__(self, address=None, time_pref=None, 
                 delivery_time_avg=4, delivery_time_variance=2):
        self.address = address
        self.time_pref = time_pref
        self.lat_lng = metric.lat_lng(address)
        self.lat, self.lng = self.lat_lng

        scale = float(delivery_time_variance)/delivery_time_avg
        shape = float(delivery_time_avg*delivery_time_avg) / \
                delivery_time_variance

        def gamma_func():
            ''' Destination delivery time random throw 

                 Compute our statistical distribution to use to throw expected
                 delivery times.  Use a gamma function - for gamma, with shape
                 parameter k and scale parameter theta, mean = k theta;
                 variance = k theta^2 therefore, theta = variance/mean, k =
                 mean^2/variance

            '''
            return np.random.gamma(shape, scale)

        self.random_delivery_time = gamma_func

    def throw_delivery_time(self):
        ''' Return a random value representing delivery duration '''
        return self.random_delivery_time()

    def distance_to(self, other):
        ''' Return distance (in meters) to another Destination '''
        return metric.distance_between(self.address, other.address)

    def time_to(self, other):
        ''' Return time (in minutes) to another Destination '''
        return metric.time_between(self.address, other.address)

    def satisfaction_probability(self, arrival_time):
        ''' Satisfaction probability for this destination given arrival_time '''
        if self.time_pref is None:
            return 1.
        return self.time_pref.satisfaction_probability(arrival_time)

    @params.use_parameters
    def compatability_to(self, other, iterations=None):
        ''' Determine schedule compatability to another destination 

            Compatability is defined as the average satisfaction probability of
            the other destination, taking into account the delivery time here
            (variable) and transit time (should be variable) supposing that the
            arrival time at *this* destination is distributed according to
            *this* destination's time preferences.  If either this node, or its 
            partner have no preference, return 1, for full compatability.

        '''
        if self.time_pref is None or other.time_pref is None:
            return 1.
        # Get time to other destination - eventually this should be Monte
        # Carlo'd
        transit_time = self.time_to(other)
        satisfaction_prob = 0.

        count = 0
        while count < iterations:
            count += 1
            # Throw a bunch of random arrival times, assuming a priori that the
            # time this location recieves it's package is distributed according
            # to its time preference distribution.
            arrival_time_here = self.time_pref.random()
            delivery_time_here = self.throw_delivery_time()

            # Arrival time there is deterministic
            arrival_time_there = arrival_time_here + \
                    delivery_time_here + transit_time
            # Get the probability of satisfaction for the other Destination for
            # this arrial time
            satisfaction_prob += \
                    other.satisfaction_probability(arrival_time_there)

        return satisfaction_prob/iterations

