'''
Utility functions used by the solver.

Author: Evan K. Friis
'''

from itertools import izip, islice

def consecutive_pairs(the_list):
    ''' Generator which returns consecutive pairs from an iterable 
    
    Example:
    >>> list(consecutive_pairs([1,2,3,4]))
    >>> [(1,2), (2,3), (3,4)]
    '''
    for first, second in izip(the_list, islice(the_list, 1, None)):
        yield first, second
