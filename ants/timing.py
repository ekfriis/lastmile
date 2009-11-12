import datetime as dt
from time import mktime
import pymc

# TODO fix me
reference_time = dt.datetime.now()

def datetime_2_ref(time):
   ''' Convert datetime to seconds since reference time '''
   #return (mktime(time.timetuple()) + 1e-6*time.microsecond)
   tz = time - reference_time
   return tz.days*24*60*60 + tz.seconds + tz.microseconds*1e-6

def ref_2_datetime(time):
   return reference_time + dt.timedelta(seconds=time)

def _ensure_datetime(func):
   ''' Ensure times passed are in datetime fmt '''
   def fix_time(self, time):
      if not isinstance(time, dt.datetime):
         return func(self, ref_2_datetime(time))
      else: return func(self, time)
   return fix_time

class TimeWindow(object):
   def __init__(self, name="", start = None, end = None):
      self.name = name
      self.start_and_end = (start, end)
      self.width = end - start
      if not end > start:
         raise ValueError, " end time must be after start time!"

   def width(self):
      return self.width

   @_ensure_datetime
   def is_early(self, time):
      return time < self.start_and_end[0]

   @_ensure_datetime
   def is_late(self, time):
      return time > self.start_and_end[1]

   @_ensure_datetime
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
      return "TimeWindow <%s> %s - %s" % (self.name, self.start.ctime(), self.start)

   def make_stochastic(self, name=None):
      if not name:
         name = self.name
      midpoint = datetime_2_ref(self.start_and_end[0] + self.width/2)
      return pymc.Uniform(name, 
            datetime_2_ref(self.start_and_end[0]), 
            datetime_2_ref(self.start_and_end[1]), 
            value=midpoint)

class TimePreferences(object):
   def __init__(self, name, windows_prefs=[]):
      self.name = name
      # Normalize preferences
      norm = sum( pref for start, end, pref in windows_prefs ) + 0.
      windows_prefs[:] = [ (start, end, pref/norm) for start, end, pref in windows_prefs ]

      self.windows = []
      # Add each time window
      for index, window in enumerate(windows_prefs):
         self.windows.append(
               (pref, TimeWindow("%s_%i" % (name, index), start, end)))

   def make_pref_dist(self, name=None):
      ''' Function to build a deterministic variable that will be determined by
      the Monte Carlo '''
      if not name:
         name = self.name
         chooser = pymc.Categorical("ranking_", [pref for pref, window in
            self.windows])

         window_stoc = [ window.make_stochastic() for pref, window in self.windows];

         @pymc.deterministic
         def time_pref(value=None, ranking=chooser, windows=window_stoc):
            return windows[ranking]

   def satisfaction_probability(self, arrival_time):
      return sum( pref for pref, window in self.windows if
            window.on_time(arrival_time) )

