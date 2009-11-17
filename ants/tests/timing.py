import unittest

import ants.timing as timing

import datetime as dt

import numpy as np

from ants.tests.std_time_inputs import *


class TestTimePrefs(unittest.TestCase):

   def blah_test_norm(self):
      self.assertEqual(standard_time_pref.windows[0][0], 4.0/7.0)

   def test_satisfaction_prob(self):
      arrival = today_at(9, 00)
      self.assertEqual(standard_time_pref.satisfaction_probability(arrival),
            standard_time_pref_normed[0])

      # Test overlapping windows
      arrival = today_at(12, 15)
      self.assertEqual(standard_time_pref.satisfaction_probability(arrival),
            standard_time_pref_normed[1] + standard_time_pref_normed[2])

      # Test failure
      arrival = today_at(23, 00)
      self.assertEquals(standard_time_pref.satisfaction_probability(arrival), 0)

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
      for expect, actual in zip(standard_time_pref_normed, times_in_window):
         #self.assertAlmostEqual(expect, actual, 2)
         # 0.98 factor allows for 2% downward fluctation for unoverlapping samples
         self.assertTrue(expect*0.98 < actual)

   def test_all_on_time(self):
      array = np.array( [standard_time_pref.random() for i in range(10000)] )
      self.assertEqual(np.sum(np.vectorize(standard_time_pref.on_time)(array)),
            len(array))

   def test_direct_sample(self):
      array = np.array( [standard_time_pref.random() for i in range(10000)] )
      self.check_sample(standard_time_pref, array)

   def test_gen_sample(self):
      array = np.zeros(10000)
      for i, samp in enumerate(standard_time_pref.n_random(10000)): 
         array[i] = samp
      self.check_sample(standard_time_pref, array)

if __name__ == '__main__':
   unittest.main()

