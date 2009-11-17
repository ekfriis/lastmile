import ants.graph as graph
import ants.timing as timing

class TestDestination(unittest.TestCase):
   def setUp(self):
      # Approximate difference between two points is 20 mintues
      self.home = graph.Destination('120 Hays St, Woodland, CA 95695', 
            time_pref=None,
            delivery_time_avg=5,
            delivery_time_variance=2)
      self.davis = graph.Destination('313 K. St, Davis, CA 95616',
            time_pref=None,
            delivery_time_avg=5,
            delivery_time_variance=3)

   def test_always_compat(self):
      self.home.time_pref = timing.TimePreferences(
            (1, today_at(8, 00), today_at(8, 01)))



