''' ChoiceMaker

Author: Evan K. Friis 

Functions to support making potential feasible delivery time choices for a
destination, given a set of sample delivery times.

'''

import numpy as np
from scipy import interpolate

from utilities import operate_on_pairs, consecutive_pairs, less, more
from rootfinder import find_roots

from itertools import izip

import matplotlib.pyplot as plt

import math


def merge_criteria(xx1, xx2, yy1, yy2):
    " Determine if two peaks, at (x1, y1) & (x2, y2) should be merged "
    # TODO tune me
    dist = abs(xx1-xx2)
    return (math.sqrt(less(yy1, yy2)/more(yy1, yy2))*dist < 100)

def peak_merger(maxima, minima, pdf, merge_criteria):
    ''' Merge any maxima that are closer than the minimum spacing 

    Lists are modified in place.  The lower maxima is merged into the higher
    one.  Any minima between merged maxima are deleted

    '''
    for first_index, (max1, max2) in enumerate(consecutive_pairs(maxima)):
        y_max1 = pdf(max1)
        y_max2 = pdf(max2)
        low_index = ((y_max1 < y_max2) and first_index or first_index+1)
        # Check if these peaks need to be merged
        if merge_criteria(max1, max2, y_max1, y_max2):
            print "Merging", max1, max2
            # Remove the lower maximum.  It's okay to modify this inside the
            # loop, as if the merge criteria is met the loop is always exited.
            del maxima[low_index]
            # Remove all minima between the two points
            minima[:] = [min for min in minima if min < max1 or min > max2]
            # Recurse down with the cleaner list
            peak_merger(maxima, minima, pdf, merge_criteria)
            # When done merging, escape this loop
            return None
    # If no merged candidates found, exit
    return None

def grow_window(start, min, max, stepsize=5):
    ''' Yield steps of window growth around start point

    Starting from start, grow a window in both directions, in steps
    of stepsize, bounded by min, and max.  Each iteration yields a tuple of 
    the current minimum and maximum of the window
    '''
    stalled = False
    low = start; high = start
    while not stalled:
        low -= stepsize
        high += stepsize
        if low < min: low = min
        if high > max: high = max
        if low == min and high == max:
            stalled = True
        yield (low, high)

def make_choices(maxima, minima, prob_func, stepsize=5, growth_min=5e-4):
    ''' Build windows from set of maxima and minima 

    The windows will grow in both directions about the maxima, until they reach
    a minima or the total change in integraged window area is less than growth_min
    in the last step
    
    '''
    windows = izip(maxima, consecutive_pairs(minima))
    # Loop over the windows to build
    for start, (min, max) in windows:
        last_area = 0.0
        total_area = 0.0
        # Grow the window in steps until we reach the end
        low=None; high=None
        for win_low, win_high in grow_window(start, min, max):
            last_area = total_area
            total_area = prob_func(win_low, win_high)
            low = win_low; high = win_high
            #if (total_area - last_area) < growth_min:
            if (last_area/total_area) > (1 - growth_min):
                # Move to next window
                break
        yield (low, high, total_area)

class ChoiceMaker(object):
    ''' Build set of time window choices 

    Takes as input an array of samples giving simulated arrival times and
    constructs feasible groupings 

    ''' 
    def __init__(self, samples):
        # Histogram the input, with 20 minute bins
        self.bin_contents, bin_edges =\
                np.histogram(samples, range=(0, 1440), bins=144, normed=1)
        # Compute the bin centers from the bin edges
        self.bin_centers = list(
            operate_on_pairs(bin_edges,func=lambda a,b: 0.5*(a+b)))
        # Build the spline over the bin contents
        self.spline = interpolate.splrep(self.bin_centers, self.bin_contents, s=0)

        threshold = np.average(self.bin_contents)

        # Find bins above threshold 
        non_zero_bins = (
            bin for val, bin in izip(self.bin_contents, self.bin_centers) 
            if val > threshold)
        # Remove any bins that are affected by spline artifacts 
        self.clean_bins = [ bin for bin in non_zero_bins if self.pdf(bin) > 0 ]


        # Find all roots (extremum - points where first derivative of pdf is
        # zero).  Also store the value of the second derivative
        my_roots = [(root, self.pdf(root, der=2)) for root in 
                    find_roots(lambda x:self.pdf(x, der=1), self.clean_bins)]

        # Split into maxima and minima
        maxima = [ root for root, second_der in my_roots if second_der < 0 ]
        minima = [ root for root, second_der in my_roots if second_der > 0 ]

        print maxima

        # Merge redundant peaks
        peak_merger(maxima, minima, self.pdf, merge_criteria)

        # Add infinite limits to prepare the windows
        minima.insert(0, -np.Inf)
        minima.append(np.Inf)

        # Make sure everything is okay
        assert(len(minima) == len(maxima)+1)

        print "Minima", minima
        print "Maxima", maxima

        # Make the choices
        self.choices = list(make_choices(maxima, minima, self.prob))

    def pdf(self, time, der=0):
        ''' Interpolated prob. density function for this histogram '''
        return interpolate.splev(time, self.spline, der=der)

    def prob(self, time0, time1):
        ''' Give *rough* integral of pdf from time0 to time1 '''
        return interpolate.splint(time0, time1, self.spline)

    def draw(self):
        plt.figure()
        x_vals = np.arange(0, 1440, 1)
        plt.plot(x_vals, self.pdf(x_vals))
        for color, (min, max, area) in zip('bgrcmy', self.choices):
            print min, max, color
            plt.axvspan(min, max, color=str(color), alpha=0.25)
        plt.show()


if __name__ == "__main__":
    samples = np.concatenate((
        np.random.normal(550.0, 20.0, 5000),
        np.random.normal(750.0, 50.0, 5000),
        np.random.normal(150.0, 50.0, 2000),
        np.random.normal(1000.0, 20.0, 2000),
        np.random.normal(700.0, 30.0, 1000)
    ))

    choice = ChoiceMaker(samples)

