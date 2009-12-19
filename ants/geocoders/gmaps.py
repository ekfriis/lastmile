''' ants.geocoders.gmaps

Infromterface to the google maps api.  Provides latitude/longitude lookups from
address, and driving time/distance for address pairs.

'''

from googlemaps import GoogleMaps, GoogleMapsError
from ants.geocoders.gmaps_api_key import api_key

import time
import cPickle as pickle
import gzip
import os

_LAT_LNG_CACHE = {}
_DIRECTIONS_CACHE = {}

_GMAPS = GoogleMaps(api_key)

# Verbosity
class Verbosity(object):
    def __init__(self):
        self.loud = False
    def set_loud(self, isLoud):
        self.loud = isLoud
    def is_loud(self):
        return self.loud

_VERBOSITY = Verbosity()

class MetricError(ValueError):
    ''' Exception raised when metric fails '''
    pass

def loud():
    ''' Print address as they are loaded '''
    _VERBOSITY.set_loud(True)

def quiet():
    ''' Suppress stdout '''
    _VERBOSITY.set_loud(False)

def clear():
    ''' Clear all metric lookup caches '''
    _LAT_LNG_CACHE.clear()
    _DIRECTIONS_CACHE.clear()

def save(filename='gmaps.gis.gz'):
    ''' Save cached address info to file '''
    output = gzip.GzipFile(filename, 'wb')
    pickle.dump(_LAT_LNG_CACHE, output)
    pickle.dump(_DIRECTIONS_CACHE, output)
    output.close()

def load(filename='gmaps.gis.gz'):
    ''' Load cached address info from file '''
    if _VERBOSITY.is_loud():
        print "Loading:", filename,
    if os.path.exists(filename):
        input_file = gzip.GzipFile(filename, 'rb')
        clear()
        _LAT_LNG_CACHE.update(pickle.load(input_file))
        _DIRECTIONS_CACHE.update(pickle.load(input_file))
    else:
        print "Error: could not load metric file: %s" % filename
    print " ... done"

def lat_lng(address):
    ''' Get latitude/long from an address'''
    if _VERBOSITY.is_loud():
        print "Lat/Lng:", address
    if address not in _LAT_LNG_CACHE:
        try:
            result = _GMAPS.address_to_latlng(address)
            _LAT_LNG_CACHE[address] = result
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
    if _VERBOSITY.is_loud():
        print "Dir: %s ==> %s" % (address_1, address_2)
    # Look it up on google if we haven't already
    address_pair = (address_1, address_2)
    if address_pair not in _DIRECTIONS_CACHE:
        time.sleep(0.100)
        # Validate addresses and put lat/lng in cache
        lat_lng(address_1)
        lat_lng(address_2)
        try:
            result = _GMAPS.directions(address_1, address_2)
            _DIRECTIONS_CACHE[address_pair] = result
        except GoogleMapsError as gmaps_error:
            raise MetricError(gmaps_error.args, 
                              " google maps can't get directions for %s-%s" \
                              % (address_1, address_2))
    return _DIRECTIONS_CACHE[address_pair]

