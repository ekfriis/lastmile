''' Root Finder

Author: Evan K. Friis

Tools for finding roots of functions
'''
from scipy import optimize
from ants.engine.utilities import consecutive_pairs

__all__ = ['find_roots', 'xfrange']

def root_domains(x_vals, func):
    ''' Yields x pairs that contain a zero crossing '''
    for x1, x2 in consecutive_pairs(x_vals):
        value1 = func(x1)
        value2 = func(x2)
        print x1, x2, value1, value2
        # Check if opposite sign
        if value1*value2 <= 0:
            yield (x1, x2)

def find_roots_in(domains, func):
    ''' Yield roots of function, given a list of domains '''
    for a, b in domains:
        yield optimize.brentq(func, a, b)

def xfrange(min, max, step):
    ''' xrange, but for floats.  Returns [min,max] by step'''
    if min > max:
        raise ValueError, "min parameter must be less than max!"
    val = min-step
    while val < max:
        val += step
        if val > max:
            val = max
        yield val

def find_roots(func, between_points):
    " Find all roots of a function between given points "
    for root in find_roots_in(root_domains(between_points, func), func):
        yield root
