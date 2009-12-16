from ants.graph.routemap import RouteMap
from ants.graph.colony import Colony
from ants.graph.destination import Destination
from ants.metric import metric
from ants.vis import *

metric.load()

straight_destinations = [Destination(address) for address in 
                         ['10 Main St, Woodland, CA 95695',
                          '150 Main St, Woodland, CA 95695',
                          '550 Main St, Woodland, CA 95695',
                          '1255 Main St, Woodland, CA 95695',
                         ]]

heybuddies = [Destination(address) for address in 
              ['627 First St, Woodland, CA 95695',
               '120 Hays St, Woodland, CA 95695',
               '100 Auburn St, Woodland, CA 95695',
#               '1200 Muir, Woodland, CA 95695',
              ]]

sf = [Destination(address) for address in 
      ['1400 WASHINGTON ST #1, SAN FRANCISCO, CA',
       '1824 JACKSON   STREET B, SAN FRANCISCO, CA',
       '1740 BROADWAY APT. 204, SAN FRANCISCO, CA',
       '1690 BROADWAY STREET APT. 710, SAN FRANCISCO, CA',
       '1901 PACIFIC #8, SAN FRANCISCO, CA',
       '1700 CALIFORNIA STREET APT 708, SAN FRANCISCO, CA',
       '1505 GOUGH ST. #17, SAN FRANCISCO, CA',
       '880 BUSH APT 415, SAN FRANCISCO, CA',
       '1428 WASHINGTON ST., SAN FRANCISCO, CA',
       '900 BUSH STREET APARTMENT 718, SAN FRANCISCO, CA',
       '1248 UNION STREET, SAN FRANCISCO, CA',
       '910 BAY STREET APT # 5, SAN FRANCISCO, CA',
       '1075 LOMBARD STREET, SAN FRANCISCO, CA',
       '1001 PINE STREET #605, SAN FRANCISCO, CA',
       '1701 JACKSON   STREET #609, SAN FRANCISCO, CA' ]]


# No time prefs for now
routemap = RouteMap(sf)

metric.save()

colony = Colony(routemap)

activate = None

for i in range(5):
    print "Run: ",i
    cost, route = colony.run_ants()
    activate = plot_route(route, colony.routemap)
    colony.update_pheromones()
    #print colony.pheromones

plotter.show()


