from googlemaps import GoogleMaps

from ants.geocoders.gmaps_api_key import api_key

_lat_lng_cache = {}
_directions_cache = {}

_gmaps = GoogleMaps(api_key)

def clear():
   _lat_lng_cache = {}
   _directions_cache = {}

def lat_lng(address):
   ''' Get latitude/long from an address'''
   if address not in _lat_lng_cache:
      _lat_lng_cache[address] = gmaps.address_to_latlng(address)
   return _lat_lng(address)

def time_between(address_1, address_2):
   ''' Return the traveling time between two addresses in seconds '''
   # Time between the same place is always zero
   if address_1 == address_2:
      return 0
   return directions(address_1, address_2)['Directions']['Duration']['seconds']

def dist_between(address_1, address_2):
   ''' Return the distance between two addresses in meters '''
   # Dist between the same place is always zero
   if address_1 == address_2:
      return 0
   return directions(address_1, address_2)['Directions']['Distance']['meters']

def directions(address_1, address_2):
   ''' Get directions from Google '''
   # Look it up on google if we haven't already
   address_pair = (address_1, address_2)
   if address_pair not in _directions_cache:
      try:
         _directions_cache[address_pair] = _gmaps.directions(address_1, address_2)
      except GoogleMapsError:
         raise ValueError, " google maps can't find address!"
   return _directions_cache[address_pair]

