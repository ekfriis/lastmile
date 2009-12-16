from ants.graph.routemap import RouteMap
from ants.graph.colony import Colony
from ants.graph.destination import Destination
from ants.metric import metric
from ants.vis import *

from ants.benchmarks.routes.sf_small import destinations

# No time prefs for now
routemap = RouteMap(destinations)

colony = Colony(routemap)

activate = None


def run():
    routes = []
    for i in range(10):
        cost, route = colony.run_ants()
        print i, route, cost
        routes.append( (cost, list(route)) )
        colony.update_pheromones()
        #print colony.pheromones
    return routes

#routes = run()
#for cost, route in routes:
#    print route, cost

if __name__ == "__main__":
    import cProfile
    cProfile.run('run()')


