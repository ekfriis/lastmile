import numpy as np
from scipy import interpolate
from scipy import optimize
import matplotlib.pyplot as plt
import itertools

def consecutive_pairs(the_list):
    for a, b in itertools.izip(the_list[:-1], the_list[1:]):
        yield (a, b)

def merge_criteria(dist_x, y_high, y_low):
    #if dist_x < 80:
    return ((y_low/y_high)*dist_x*dist_x < 60)

def peak_finding(samples):
    """ Histogram/Interpolate a set of samples and find peaks """
    # Minutes in a day = 60*24 1440
    # N bins for 20 minute bins = 72
    (y_vals, bin_edges) =\
            np.histogram(samples, range=(0, 1440), bins=72, normed=1)
    # Compute bin centers
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])

    # Suppress negligible bins
    average = np.average(y_vals)
    non_zero_bins = [ bin for val, bin in zip(y_vals, bin_centers) if val > average ]
    # Make spline
    spline0 = interpolate.splrep(bin_centers, y_vals)
    # Compute first derivative spline
    def derivative(x, der=1):
        return interpolate.splev(x, spline0, der=der)

    #To estimate roots
    def root_domains(bins, func):
        ''' Generator that yields x pairs that contain a extremum '''
        for bin1, bin2 in consecutive_pairs(bins):
            value1 = func(bin1)
            value2 = func(bin2)
            # Check if opposite sign
            if value1*value2 <= 0:
                yield (bin1, bin2)

    def find_roots(domains, func):
        ''' Yield roots of function, given a list of domains '''
        for a, b in domains:
            yield optimize.brentq(func, a, b)

    def merge_maxima(maxima, minima, func, merge_criteria=merge_criteria):
        ''' Merge any maxima that are closer than the minimum spacing 
        The lower maxima is merged into the higher one.
        Any minima between merged maxima are deleted

        '''
        for first_index, (x1, x2) in enumerate(consecutive_pairs(maxima)):
            distance = abs(x1-x2)
            y1 = func(x1)
            y2 = func(x2)
            low_index = ((y1 < y2) and first_index or first_index+1)
            high_y = ((y1 > y2) and y1 or y2)
            low_y = ((y1 > y2) and y2 or y1)
            if merge_criteria(distance, high_y, low_y):
                print "Merging ", x1, x2
                # Recurse down with the modified list
                del maxima[low_index]
                minima[:] = [min for min in minima if min < x1 or min > x2]
                merge_maxima(maxima, minima, func, merge_criteria)
                return None
        return None
    
    def prune_minima(maxima, minima):
        ''' Keep only the lowest minima between two maxima '''
        fake_maxima = maxima[:]
        fake_maxima.append(np.Inf)
        fake_maxima.insert(0,-np.Inf)
        fake_maxima = np.array(fake_maxima)
        best_minima = [-np.Inf]
        for low, high in consecutive_pairs(fake_maxima):
            lowest = None
            for min in filter(lambda x: x > low and x < high, minima):
                if min < lowest or lowest is None:
                    lowest = min
            if lowest is not None:
                best_minima.append(lowest)
        best_minima.append(np.Inf)
        return best_minima

    def windows(maxima, minima):
        #assert(len(minima) == len(maxima)+1)
        for max, (min_low, min_high) in itertools.izip(maxima,
            consecutive_pairs(minima)):
            yield (min_low, max, min_high)

    def grow_window(start, min, max, stepsize=5):
        stalled = False
        low = start
        high = start
        while not stalled:
            low -= stepsize
            high += stepsize
            if low < min:
                low = min
            if high > max:
                high = max
            if low == min and high == max:
                stalled = True
            yield (low, high)

    def make_choices(windows, spline, stepsize=5, growth_min=0.005):
        for min, start, max in windows:
            last_area = 0.0
            total_area = 0.0
            for new_min, new_max in grow_window(start, min, max):
                last_area = total_area
                total_area = interpolate.splint(new_min, new_max, spline)
                #if (total_area - last_area)/total_area < growth_min:
                if (total_area - last_area) < growth_min:
                    yield (new_min, start, new_max)
                    break

    my_roots = list(find_roots(root_domains(non_zero_bins, derivative), derivative))
    print "Roots:", my_roots

    maxima = [ root for root in my_roots if derivative(root, 2) < 0 ]
    print "Maxima:", maxima

    minima = [ root for root in my_roots if derivative(root, 2) > 0 ]
    print "Minima:", minima

    merge_maxima(maxima, minima, func=lambda x: derivative(x, der=0))
    print "Merged Max:", maxima
    print "Merged Min:", minima

    minima = prune_minima(maxima, minima)
    print "Pruned:", minima
    print "Raw Windows:", list(windows(maxima, minima))
    print "Windows:", list(make_choices(windows(maxima, minima), spline0))
    print "average:", np.average(y_vals)

    def draw(spline, choices, stepsize=1):
        plt.figure()
        x_vals = np.arange(0, 1440, 1)
        plt.plot(x_vals, interpolate.splev(x_vals, spline, der=0))
        for min, start, max in choices:
            plt.axvspan(min, max, alpha=0.2)
        plt.show()

    draw(spline0, make_choices(windows(maxima, minima), spline0))




# Generate a fake normal histogram, mean 5 width 2
samples = np.concatenate((
    np.random.normal(550.0, 20.0, 5000),
    np.random.normal(750.0, 50.0, 5000),
    np.random.normal(150.0, 50.0, 2000),
    np.random.normal(1000.0, 100.0, 5000),
    #np.random.normal(700.0, 300.0, 1000000)
))

peak_finding(samples)


