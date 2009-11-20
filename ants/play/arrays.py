
import numpy as np


# Test masked arrays
my_array = np.array([2., 5., 0., 1., 5., 6., 9.])

print my_array

mask = [False, True, False, True, True, True, True]

mask[:] = [ not val for val in mask ]

my_masked_array = np.ma.masked_array(my_array, mask)

print my_masked_array

# Normalize
my_masked_array[:] = my_masked_array/np.sum(my_masked_array)

print my_masked_array

cum_sum = np.cumsum(my_masked_array)

print cum_sum

count = np.zeros(len(my_array))

for i in range(1000):
    count[np.searchsorted(cum_sum, np.random.rand())] += 1

print [x for x in enumerate(count)]

# Test Inf matrix elements

pippo = np.array( [[0, 2], [1, 0]], dtype=float )

pippo_inverted = 1/pippo

print pippo_inverted # works, diagonal is inf

print "======="
print pippo
print pippo[0, 1]
print pippo[0, :]
