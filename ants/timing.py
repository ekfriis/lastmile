import datetime as dt
import numpy
import random

# TODO fix me
_today = dt.datetime.today()
reference_time = dt.datetime(_today.year, _today.month, _today.day)

def datetime_2_ref(time):
    ''' Convert datetime to minutes since reference time '''
    tz = time - reference_time
    return tz.days*24*60 + (tz.seconds + tz.microseconds*1e-6)/60.0

def ref_2_datetime(time):
    return reference_time + dt.timedelta(seconds=time*60)

def _ensure_reftime(func):
    ''' Ensure times passed to funciton are in custom ref fmt '''
    def fix_time(self, time):
        if isinstance(time, dt.datetime):
            return func(self, datetime_2_ref(time))
        else: return func(self, time)
    return fix_time

class TimeWindow(object):
    def __init__(self, start = None, end = None):
        self.start_and_end = (start, end)
        self.start_ref = datetime_2_ref(start)
        self.end_ref = datetime_2_ref(end)
        self.width = end - start
        self.width_ref = self.end_ref - self.start_ref
        if not end > start:
            raise ValueError, " end time must be after start time!"

    @_ensure_reftime
    def is_early(self, time):
        return time < self.start_ref

    @_ensure_reftime
    def is_late(self, time):
        return time > self.end_ref

    @_ensure_reftime
    def on_time(self, time):
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
        return "TimeWindow %s - %s" % (self.start.ctime(), self.start)

    def random(self):
        return numpy.random.uniform(self.start_ref, self.end_ref)

class TimePreferences(object):
    def __init__(self, windows_prefs=[]):
        self.windows = []
        # Add each time window
        for index, (pref, start, end) in enumerate(windows_prefs):
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
        time_window = numpy.searchsorted(self.cum_prefs, numpy.random.rand())
        return self.windows[time_window].random()
   
    def n_random(self, n):
        for i in range(n):
            yield self.random()

    def on_time(self, arrival_time):
        ''' Test if arrival_time meets any of the time window constraints '''
        for window in self.windows:
            if window.on_time(arrival_time):
                return True
        return False

    def satisfaction_probability(self, arrival_time):
        return sum(pref for pref, window in self.windows_and_prefs 
                if window.on_time(arrival_time) )

