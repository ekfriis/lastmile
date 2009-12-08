''' Timing

Provides TimeWindow and TimePreferences.

Timewindow describes a time interval that the customer would like the delivery
to fall in.  TimePreferences is a set of time windows, where each time window
has some priority level, indicating the desirability of that time window.  Both
classes provided a random() function, which throws random delivery times
distributed assuming the time interval/preferences are satisfied.

'''
import datetime as dt
import numpy

# TODO fix me
_TODAY = dt.datetime.today()
REFERENCE_TIME = dt.datetime(_TODAY.year, _TODAY.month, _TODAY.day)

def datetime_2_ref(time):
    ''' Convert datetime to minutes since reference time '''
    time_diff = time - REFERENCE_TIME
    return (time_diff.days*24*60 + 
            (time_diff.seconds + time_diff.microseconds*1e-6)/60.0)

def ref_2_datetime(time):
    ''' Convert reftime to datetime format '''
    return REFERENCE_TIME + dt.timedelta(seconds=time*60)

def _ensure_reftime(func):
    ''' Ensure times passed to funciton are in custom ref fmt '''
    def fix_time(self, time):
        ''' If time is a datetime object, convert it to reftime '''
        if isinstance(time, dt.datetime):
            return func(self, datetime_2_ref(time))
        else: return func(self, time)
    return fix_time

class TimeWindow(object):
    ''' Class describing a time interval for package delivery '''
    def __init__(self, start = None, end = None):
        self.start, self.end = (start, end)
        self.start_and_end = (start, end)
        self.start_ref = datetime_2_ref(start)
        self.end_ref = datetime_2_ref(end)
        self.width = end - start
        self.width_ref = self.end_ref - self.start_ref
        if not end > start:
            raise ValueError, " end time must be after start time!"

    def setup(self, start, end):
        ''' Reinitialize window'''
        self.__init__(start, end)

    @_ensure_reftime
    def is_early(self, time):
        ''' Returns true if time is early for this window '''
        return time < self.start_ref

    @_ensure_reftime
    def is_late(self, time):
        ''' Returns true if time is late for this window '''
        return time > self.end_ref

    @_ensure_reftime
    def on_time(self, time):
        ''' Returns true if time is satisfactory for this window '''
        return not self.is_early(time) and not self.is_late(time)

    def __lt__(self, other):
        return self.start_and_end < other.start_and_end
    def __le__(self, other):
        return self.start_and_end <= other.start_and_end
    def __gt__(self, other):
        return self.start_and_end > other.start_and_end
    def __ge__(self, other):
        return self.start_and_end >= other.start_and_end
    def __eq__(self, other):
        return self.start_and_end == other.start_and_end
    def __ne__(self, other):
        return self.start_and_end != other.start_and_end

    def __unicode__(self):
        return "TimeWindow %s - %s" % (self.start.ctime(), self.end.ctime())

    def random(self):
        ''' Return a random ref time uniformly distributed in this window '''
        return numpy.random.uniform(self.start_ref, self.end_ref)

class TimePreferences(object):
    ''' TimePreferences

    Holds a set of time windows, with associated priority levels.  Each 
    priority indicates the 'desirability' for that time window to be satisfied, 
    allowing ranking.  Also provides a function for generating random arrival times
    that assume this time preferences is satisfied according to the priority levels.

    '''
    def __init__(self, windows_prefs=None):
        self.windows = []
        # Add each time window
        for pref, start, end in windows_prefs:
            self.windows.append(TimeWindow(start, end))

        # Normalize preferences
        self.prefs = [pref for pref, start, end in windows_prefs]
        norm = sum(self.prefs) + 0.
        self.prefs[:] = [pref/norm for pref in self.prefs]
        self.windows_and_prefs = zip(self.prefs, self.windows)
        self.cum_prefs = numpy.cumsum(self.prefs)
      
    # Make the stochastic function that can be used to determine the expected
    # 'ideal' arrival_time distribution from the window preferences and the
    # window distributions
    def random(self):
        ''' Generate a random arrival time consistent with preferences '''
        time_window = numpy.searchsorted(self.cum_prefs, numpy.random.rand())
        return self.windows[time_window].random()
   
    def n_random(self, count):
        ''' Generator to yield a series of random numbers '''
        i = 0
        while i < count:
            i += 1
            yield self.random()

    def on_time(self, arrival_time):
        ''' Test if arrival_time meets any of the time window constraints '''
        for window in self.windows:
            if window.on_time(arrival_time):
                return True
        return False

    def satisfaction_probability(self, arrival_time):
        ''' Probability that this arrival time satisfies this time preference'''
        return sum(pref for pref, window in self.windows_and_prefs 
                if window.on_time(arrival_time) )

