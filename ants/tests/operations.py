import unittest

from ants.graph.operations import *
from ants.graph.destination import Destination

import numpy as np

class TestOperations(unittest.TestCase):
    def setUp(self):
      # Approximate difference between two points is 20 mintues
      self.home = Destination('120 Hays St, Woodland, CA 95695', 
            time_pref=None,
            delivery_time_avg=5,
            delivery_time_variance=2)
      self.davis = Destination('313 K. St, Davis, CA 95616',
            time_pref=None,
            delivery_time_avg=5,
            delivery_time_variance=3)

      self.destinations = [self.home, self.davis]

    def test_distance(self):
        dist_array = distance_cost_array(self.destinations, dollar_per_km=1.0)
        # Diagonal elements must be zero
        self.assertEqual(dist_array[0,0], 0)
        self.assertEqual(dist_array[1,1], 0)
        # Woodland to davis is about 19 kilometers
        self.assertAlmostEqual(dist_array[0,1], 19, 0)
        self.assertAlmostEqual(dist_array[1,0], 19, 0) 

    def test_time(self):
        time_array = time_cost_array(self.destinations, dollar_per_hour=1.0)
        # Diagonal elements must be zero
        self.assertEqual(time_array[0,0], 0)
        self.assertEqual(time_array[1,1], 0)
        # Woodland to davis is about 20 minutes
        self.assertAlmostEqual(time_array[0,1], 1/3., 0)
        self.assertAlmostEqual(time_array[1,0], 1/3., 0) 
    