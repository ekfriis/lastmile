''' ants.geocoders.gmaps

Infromterface to the google maps api.  Provides latitude/longitude lookups from
address, and driving time/distance for address pairs.

'''

from googlemaps import GoogleMaps, GoogleMapsError
from ants.geocoders.gmaps_api_key import api_key

_LAT_LNG_CACHE = {}
_DIRECTIONS_CACHE = {}

_GMAPS = GoogleMaps(api_key)

class MetricError(ValueError):
    ''' Exception raised when metric fails '''
    pass

def clear():
    ''' Clear all metric lookup caches '''
    _LAT_LNG_CACHE.clear()
    _DIRECTIONS_CACHE.clear()

def lat_lng(address):
    ''' Get latitude/long from an address'''
    if address not in _LAT_LNG_CACHE:
        _LAT_LNG_CACHE[address] = _GMAPS.address_to_latlng(address)
    return _LAT_LNG_CACHE[address]

def time_between(address_1, address_2):
    ''' Return the traveling time between two addresses in minutes '''
    # Time between the same place is always zero
    if address_1 == address_2:
        return 0
    return directions(address_1, address_2)['Directions']\
        ['Duration']['seconds']/60.

def distance_between(address_1, address_2):
    ''' Return the distance between two addresses in meters '''
    # Dist between the same place is always zero
    if address_1 == address_2:
        return 0
    return directions(address_1, address_2)['Directions']\
        ['Distance']['meters']

def directions(address_1, address_2):
    ''' Get directions from Google '''
    # Look it up on google if we haven't already
    address_pair = (address_1, address_2)
    if address_pair not in _DIRECTIONS_CACHE:
        try:
            _DIRECTIONS_CACHE[address_pair] = ( 
                _GMAPS.directions(address_1, address_2))
        except GoogleMapsError:
            raise MetricError, " google maps can't find address!"
    return _DIRECTIONS_CACHE[address_pair]

