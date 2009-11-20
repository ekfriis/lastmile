import unittest

from ants.graph.destination import Destination
import ants.timing as timing

from ants.tests.std_time_inputs import \
        standard_time_pref, standard_time_pref_normed, today_at

class TestDestination(unittest.TestCase):
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

   def test_always_compat(self):
       self.home.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(8, 01))]
       )
       self.davis.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(9,00))]
       )

       # Time from woodland and davis is 20 minutes, so this should always 
       # be satisfied
       compatability = self.home.compatability_to(self.davis)
       self.assertAlmostEquals(compatability, 1, 1)

   def test_never_compat(self):
       self.home.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(8, 01))]
       )
       self.davis.time_pref = timing.TimePreferences(
           [(1, today_at(10, 00), today_at(11,00))]
       )

       # Time from woodland and davis is 20 minutes, so this should never 
       # be satisfied
       compatability = self.home.compatability_to(self.davis)
       self.assertAlmostEquals(compatability, 0, 1)

   def test_sometimes_compat(self):
       self.home.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(8, 01))]
       )
       self.davis.time_pref = timing.TimePreferences(
           [(1, today_at(8, 25), today_at(8, 26))]
       )

       # Time from woodland and davis is 20 minutes, so this should sometimes 
       # be satisfied
       compatability = self.home.compatability_to(self.davis)
       self.assertTrue(0 < compatability < 1)
   
   def test_multi_window(self):
       self.home.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(8, 01))]
       )
       self.davis.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(9,00)),
            (1, today_at(12, 00), today_at(13,00))]
       )
       # The first time window should always be satisfied, so we expect
       # 50% satisfaction (as the first and second windows have equal weights
       compatability = self.home.compatability_to(self.davis)
       self.assertAlmostEquals(compatability, 0.5, 1)

   def test_multi_always(self):
       self.home.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(8, 01)),
            (1, today_at(12, 00), today_at(12, 01))]
       )
       self.davis.time_pref = timing.TimePreferences(
           [(1, today_at(8, 00), today_at(9,00)),
            (1, today_at(12, 00), today_at(13,00))]
       )
       compatability = self.home.compatability_to(self.davis)
       # Is this what we want??? Maybe this should be one....
       self.assertAlmostEquals(compatability, 0.5, 5)


if __name__ == "__main__":
    import cProfile
    cProfile.run('unittest.main()')


