import ants.engine.routemap as rm
from ants.engine.destination import Destination

import ants.tests.std_time_inputs as time_inputs

import ants.parameters as params

import unittest

class TestRouteMap(unittest.TestCase):
    # TODO refactor all these tests to inherit from a 
    def setUp(self):
        self.home = Destination('120 Hays St, Woodland, CA 95695', 
                                time_pref=time_inputs.one_to_three,
                                delivery_time_avg=5,
                                delivery_time_variance=2)
        self.davis = Destination('313 K. St, Davis, CA 95616',
                                 time_pref=time_inputs.two_to_three,
                                 delivery_time_avg=5,
                                 delivery_time_variance=3)
        self.destinations = [self.home, self.davis]
        self.routemap = rm.RouteMap(self.destinations)

    def test_matrices(self):
        self.assertEqual(self.routemap.distances[0][0], 0.)
        self.assertEqual(self.routemap.distances[1][1], 0.)
        self.assertAlmostEqual(
            self.routemap.distances[0][1], 
            19.3*params.get_parameter('dollar_per_km'), 0)
        self.assertAlmostEqual(
            self.routemap.times[0][1], 
            20.0/60.0*params.get_parameter('dollar_per_hour'), 0)

    def test_compat(self):
        self.assertTrue(self.routemap.compatabilities[0][1] > 0)
        self.assertTrue(self.routemap.compatabilities[1][0] > 0)
        self.assertEqual(self.routemap.compatabilities[0][0], 0)
        self.assertEqual(self.routemap.compatabilities[1][1], 0)
    
    def test_time_for_edge(self):
        self.assertAlmostEqual(
            self.routemap.time_for_edge(0, 1), 
            20/60.0*params.get_parameter('dollar_per_hour'), 0)

    def test_total_tangible(self):
        woodland_2_davis = [0, 1]
        self.assertAlmostEqual(
            self.routemap.total_tangible_cost_for_route(woodland_2_davis),
            0.33*params.get_parameter('dollar_per_hour') + 
            19.3*params.get_parameter('dollar_per_km'), 1)
        
if __name__ == "__main__":
    unittest.main()
