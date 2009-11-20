import ants.timing as timing

import datetime as dt

def today_at(hours, minutes):
   today = dt.datetime.today() 
   output = dt.datetime(
         today.year,
         today.month,
         today.day,
         hours, minutes)
   return output

def normalize_list(list, norm=None):
   if not norm:
      norm = sum(list)
   norm = float(norm)
   list[:] = [ item/norm for item in list ]

standard_time_tuple = [(4, today_at(8, 00), today_at(10, 00)),
      (2, today_at(12, 00), today_at(15, 00)),
      (1, today_at(12, 00), today_at(12, 30))]

standard_time_pref = timing.TimePreferences(standard_time_tuple)

standard_time_pref_normed = [pref for pref, s, e in standard_time_tuple]
normalize_list(standard_time_pref_normed)

one_to_three = timing.TimePreferences([(1, today_at(13, 00), today_at(15, 00))])
two_to_three = timing.TimePreferences([(1, today_at(14, 00), today_at(15, 00))])
