'''
Utility functions used by the solver.

Author: Evan K. Friis
'''

from itertools import izip, islice, tee

def consecutive_pairs(the_list):
    ''' Generator which returns consecutive pairs from an iterable/generator
    
    Example:
    >>> list(consecutive_pairs([1,2,3,4]))
    >>> [(1,2), (2,3), (3,4)]
    '''
    # Get independent generators
    copy_1, copy_2 = tee(the_list, 2)
    for first, second in izip(copy_1, islice(copy_2, 1, None)):
        yield first, second

def operate_on_pairs(the_list, func=None):
    "Yield func(a,b) where are a and b are consecutive pairs from the_list"
    for first, second in consecutive_pairs(the_list):
        yield func(first, second)
