import ants.parameters as params

import unittest

class TestParams(unittest.TestCase):

    def test_get_set(self):
        self.assertEqual(params.get_parameter('iterations'), 
                         params._ALGO['iterations'])
        params.set_parameter('iterations', 200)
        self.assertEqual(params.get_parameter('iterations'), 200)

    def test_save_load(self):
        old_iters = params.get_parameter('iterations')
        params.dump_parameters('unit_test_params.pkl')
        params.set_parameter('iterations', 200)
        self.assertEqual(params.get_parameter('iterations'), 200)
        params.load_parameters('unit_test_params.pkl')
        self.assertEqual(params.get_parameter('iterations'), old_iters)
    
    def test_wrapper(self):
        @params.use_parameters
        def my_func(non_param=5, dollar_per_km=None):
            return {'non_param': non_param, 
                    'dollar_per_km': dollar_per_km}

        result_no_spec = my_func()
        result_with_spec = my_func(non_param=7, dollar_per_km=20)

        self.assertEqual(result_no_spec['non_param'], 5)
        self.assertEqual(result_no_spec['dollar_per_km'],  
                        params.get_parameter('dollar_per_km'))

        self.assertEqual(result_with_spec['non_param'], 7)
        self.assertEqual(result_with_spec['dollar_per_km'], 20)


if __name__ == "__main__":
    unittest.main()

