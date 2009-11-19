''' ants.metric

Select the metric to use to determine the time and distance between nodes.

Should provide the following functions:

    lat_lng(address):
        Return a tuple continaing latitude and longitude from an address

    distance_to(address1, address2):
        Return distance (in meters) to travel *from* address1 *to* address2

    time_to(address1, address2):
        Return time (in minutes) to travel *from* address1 *to* address2

'''

from ants.geocoders import gmaps as metric
