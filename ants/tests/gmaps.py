import ants.geocoders.gmaps as metric 
import unittest

class TestGmaps(unittest.TestCase):
   def setUp(self):
      self.home = '120 Hays St, Woodland, CA 95696'
      self.davis = '313 K St, Davis, CA 95616'
   
   def test_time(self):
      time = metric.time_between(self.home, self.davis)
      time = time/60.
      # should be about 20 minutes
      self.assertTrue( 18 < time < 22 )

   def test_distance(self):
      dist = metric.distance_between(self.home, self.davis)
      # 12 miles = 19312 meters
      self.assertTrue( 19000 < dist < 19550 )

   def test_same_dest(self):
      self.assertEqual(metric.distance_between(self.home, self.home), 0)
      self.assertEqual(metric.time_between(self.home, self.home), 0)

   def test_lat_lng(self):
      lat, lng = metric.lat_lng(self.home)
      self.assertAlmostEquals(lat, 38.667304, 2)
      self.assertAlmostEquals(lng, -121.780917, 2)

if __name__ == "__main__":
   unittest.main()
