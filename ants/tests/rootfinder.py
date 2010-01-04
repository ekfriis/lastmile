from ants.engine.rootfinder import find_roots
import unittest
import numpy as np

class TestRootFinder(unittest.TestCase):
    def test_rootfinder(self):
        def my_rooty_func(x):
            # (x-1)(x+2)
            return x*x + x - 2

        roots = list(find_roots(my_rooty_func, np.arange(-5, 5, 0.1)))
        self.assertEqual(len(roots), 2)

        roots2 = roots[:]
        roots.sort()
        # Ensure sorted
        self.assertEqual(roots2, roots)

        self.assertAlmostEqual(roots[0], -2)
        self.assertAlmostEqual(roots[1], 1)

    def test_noroots(self):
        def norootfunc(x):
            return x*x + 3

        roots = list(find_roots(norootfunc, np.arange(-5, 5, 0.1)))
        self.assertEqual(roots, [])
