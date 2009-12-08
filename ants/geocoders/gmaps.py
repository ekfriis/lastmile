''' ants.geocoders.gmaps

Infromterface to the google maps api.  Provides latitude/longitude lookups from
address, and driving time/distance for address pairs.

'''

from googlemaps import GoogleMaps, GoogleMapsError
from ants.geocoders.gmaps_api_key import api_key
import pickle
import os

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

def save(filename='gmaps.gis'):
    output = file(filename, 'wb')
    pickle.dump(_LAT_LNG_CACHE, output)
    pickle.dump(_DIRECTIONS_CACHE, output)
    output.close()

def load(filename='gmaps.gis'):
    if os.path.exists(filename):
        input = file(filename, 'rb')
        clear()
        _LAT_LNG_CACHE.update(pickle.load(input))
        _DIRECTIONS_CACHE.update(pickle.load(input))
    else:
        print "Error: could not load metric file: %s" % filename

def lat_lng(address):
    ''' Get latitude/long from an address'''
    if address not in _LAT_LNG_CACHE:
        try:
            _LAT_LNG_CACHE[address] = _GMAPS.address_to_latlng(address)
        except GoogleMapsError:
            raise MetricError, " google maps can't find address:", address
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
    # Validate addresses and put lat/lng in cache
    lat_lng(address_1)
    lat_lng(address_2)
    if address_pair not in _DIRECTIONS_CACHE:
        try:
            _DIRECTIONS_CACHE[address_pair] = ( 
                _GMAPS.directions(address_1, address_2))
        except GoogleMapsError:
            raise MetricError, \
                    " google maps can't get directions for %s-%s"%(address_1, address_2)
    return _DIRECTIONS_CACHE[address_pair]

