import unittest

import ants.timing as timing

import datetime as dt

import numpy as np

class TestTimeWindow(unittest.TestCase):
   def setUp(self):
      self.before_five = timing.TimeWindow("before_five", 
            dt.datetime(1983, 8, 16, 8),  # Start of day
            dt.datetime(1983, 8, 16, 17))
      self.around_noon = timing.TimeWindow("around_noon",
            dt.datetime(1983, 8, 16, 11, 30),  # Start of day
            dt.datetime(1983, 8, 16, 13, 30))
      self.after_three = timing.TimeWindow("after_three",
            dt.datetime(1983, 8, 16, 15, 00),
            dt.datetime(1983, 8, 16, 19, 00))

   def test_early(self):
      # Check if a day earlier is early
      test_time = dt.datetime(1983, 8, 15, 8, 30)
      self.assertTrue(self.before_five.is_early(test_time))

      # Check if 1 minute after start of window is not early
      test_time = dt.datetime(1983, 8, 16, 8, 30)
      self.assertFalse(self.before_five.is_early(test_time))

   def test_late(self):
      # Check if a day earlier is not late
      test_time = dt.datetime(1983, 8, 15, 8, 30)
      self.assertFalse(self.before_five.is_late(test_time))

      # Check if 1 minute after end of window is late
      test_time = dt.datetime(1983, 8, 16, 17, 30)
      self.assertTrue(self.before_five.is_late(test_time))

   def test_ontime(self):
      test_time = dt.datetime(1983, 8, 16, 12) # noon
      self.assertTrue(self.around_noon.on_time(test_time))

      test_time = dt.datetime(1983, 8, 16, 17) # five
      self.assertFalse(self.around_noon.on_time(test_time))

   def test_malformed(self):
      # Make sure start of the window is before the end!
      self.assertRaises(ValueError, timing.TimeWindow, "impossible",
               dt.datetime(1983, 8, 16, 12), # 12:00
               dt.datetime(1983, 8, 16, 11, 59)) # 11:59

   def test_reftime(self):
      ref_time = timing.datetime_2_ref(
            dt.datetime(1983, 8, 16, 8, 30))
      self.assertTrue(self.before_five.on_time(ref_time))

   def test_sort(self):
      unordered = [ self.after_three, self.before_five, self.around_noon ]
      unordered.sort()
      sorted_names = [ window.name for window in unordered ]
      self.assertEquals(sorted_names, ["before_five", "around_noon", 
         "after_three"])

   def test_stochastic(self):
      stoc = self.before_five.make_stochastic()
      # Test random variables okay
      for i in range(10):
         throw = stoc.random().item()
         self.assertTrue(self.before_five.on_time(throw))

class TestTimingSupportFns(unittest.TestCase):
   def test_ref_2_dt_2_ref(self):
      time = 55
      self.assertEqual( time, 
            timing.datetime_2_ref(timing.ref_2_datetime(time)))

   def test_dt_2_ref_2_dt(self):
      time = dt.datetime(1983, 8, 16, 8, 30)
      self.assertEqual( time,
            timing.ref_2_datetime(timing.datetime_2_ref(time)))


if __name__ == '__main__':
   unittest.main()

