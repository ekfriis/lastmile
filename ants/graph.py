import datetime as dt
from ants.geocoders import gmaps as metric
import numpy as np

class Destination(object):
   ''' A delivery destination '''
   def __init__(self, address=None, time_pref=None, delivery_time_avg=4, delivery_time_variance=2):
      self.address = address
      self.time_pref = time_pref
      self.lat, self.lng = metric.lat_lng(address)

      # Compute our statistical distribution to use to throw
      #  expected delivery times.  Use a gamma function - for gamma,
      #  with shape parameter k and scale parameter theta, 
      #  mean = k theta; variance = k theta^2
      #  therefore, theta = variance/mean, k = mean^2/variance

      scale = float(delivery_time_variance)/delivery_time_avg
      shape = float(delivery_time_avg*delivery_time_avg)/delivery_time_variance

      def gamma_func():
         return np.random.gamma(shape, scale)

      self.random_delivery_time = gamma_func

   def throw_delivery_time(self):
      return self.random_delivery_time()

   def distance_to(self, other):
      return metric.distance_between(self.address, other.address)

   def time_to(self, other):
      return metric.time_between(self.address, other.address)


   def compatability_to(self, other, n=500):
      ''' Determine schedule compatability to another destination '''
      transit_time = self.time_to(other)

      satisfaction_prob = 0.

      for i in range(n):
         arrival_time_here = self.time_pref.random()
         delivery_time_here = self.throw_delivery_time()

         arrival_time_there = arrival_time_here + delivery_time_here + transit_time
         satisfaction_prob += other.satisfaction_probability(arrival_time_there)

      return satisfaction_prob/n

