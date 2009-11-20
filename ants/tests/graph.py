from ants.graph.destination import Destination

import unittest

import math

class TestDestination(unittest.TestCase):
   def setUp(self):
      self.home = Destination('120 Hays St, Woodland, CA 95695', 
            time_pref=None,
            delivery_time_avg=5,
            delivery_time_variance=2)
      self.davis = Destination('313 K. St, Davis, CA 95616',
            time_pref=None,
            delivery_time_avg=5,
            delivery_time_variance=3)

   def test_distance(self):
      dist = self.home.distance_to(self.davis)
      # 12 miles, about 19.3k meters
      self.assertTrue( 19000 < dist < 19500 )

   def test_time(self):
      time = self.home.time_to(self.davis)
      self.assertTrue( 18 < time < 22 )

   def test_throw(self):
      ''' Check average and variance calculated correctly '''
      n = 50000
      sum_n = sum(self.home.throw_delivery_time() for i in range(n))
      sum_squared_n = sum(x*x for x in (self.home.throw_delivery_time() for i in range(n)))

      average = float(sum_n)/n 

      variance = float(sum_squared_n)/n - average*average
      
      self.assertAlmostEquals(average, 5, 0)
      self.assertAlmostEquals(variance, 2, 0)

if __name__ == "__main__":
    unittest.main()
