import datetime as dt
import numpy as np
from ants.geocoders import gmaps as metric

class Destination(object):
   ''' A delivery destination '''
   def __init__(address=None, time_pref=None, delivery_time_avg=0, delivery_time_error=0):
      self.address = address
      self.time_pref = time_pref
      self.lat, self.lng = metric.lat_lng(address)

   def distance_to(self, other):
      return metric.distance_between(self.address, other.address)

   def time_to(self, other):
      return metric.time_between(self.address, other.address)

   def throw_delivery_time(self):
      return numpy.random


