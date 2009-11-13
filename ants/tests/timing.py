import unittest

import ants.timing as timing

import datetime as dt

import numpy as np

import pymc

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

   def test_random(self):
      ''' Test random variable distribution '''
      for i in range(10):
         throw = self.before_five.random()
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


def today_at(hours, minutes):
   today = dt.datetime.today() 
   output = dt.datetime(
         today.year,
         today.month,
         today.day,
         hours, minutes)
   return output

def normalize_list(list, norm=None):
   if not norm:
      norm = sum(list)
   norm = float(norm)
   list[:] = [ item/norm for item in list ]

class TestTimePrefs(unittest.TestCase):
   def setUp(self):
      self.input_tuples = \
            [(4, today_at(8, 00), today_at(10, 00)),
             (2, today_at(12, 00), today_at(15, 00)),
             (1, today_at(12, 00), today_at(12, 30))]

      self.my_pref = timing.TimePreferences("test_prefs", self.input_tuples)

      # Expected preference weights
      norm = sum( pref for pref, start, end in self.input_tuples ) + 0.
      self.expected_prefs = [ pref/norm for pref, start, end in
            self.input_tuples ]

   def test_setup(self):
      self.assertEqual(self.my_pref.name, 'test_prefs')

   def blah_test_norm(self):
      self.assertEqual(self.my_pref.windows[0][0], 4.0/7.0)

   def test_satisfaction_prob(self):
      arrival = today_at(9, 00)
      self.assertEqual(self.my_pref.satisfaction_probability(arrival),
            self.expected_prefs[0])

      # Test overlapping windows
      arrival = today_at(12, 15)
      self.assertEqual(self.my_pref.satisfaction_probability(arrival),
            self.expected_prefs[1] + self.expected_prefs[2])

      # Test failure
      arrival = today_at(23, 00)
      self.assertEquals(self.my_pref.satisfaction_probability(arrival), 0)

   # Todo, fix this! Not valid for overlapping samples. Need to compute
   #  expected overlaps
   def check_sample(self, prefs, sample):
      times_in_window = [0, 0, 0]
      for i in range(3):
         # Count number of samples that are on time for each window
         times_in_window[i] = \
               np.sum(np.vectorize(prefs.windows[i].on_time)(sample))
      normalize_list(times_in_window, norm=len(sample))

      # Check if these are close our expected prefs. This will work for 
      #  none overlapping time window preferences
      for expect, actual in zip(self.expected_prefs, times_in_window):
         #self.assertAlmostEqual(expect, actual, 2)
         # 0.98 factor allows for 2% downward fluctation for unoverlapping samples
         self.assertTrue(expect*0.98 < actual)

   def test_all_on_time(self):
      array = np.array( [self.my_pref.random() for i in range(10000)] )
      self.assertEqual(np.sum(np.vectorize(self.my_pref.on_time)(array)),
            len(array))

   def test_direct_sample(self):
      array = np.array( [self.my_pref.random() for i in range(10000)] )
      self.check_sample(self.my_pref, array)

   def test_gen_sample(self):
      array = np.zeros(10000)
      for i, samp in enumerate(self.my_pref.n_random(10000)): 
         array[i] = samp
      self.check_sample(self.my_pref, array)

if __name__ == '__main__':
   unittest.main()

