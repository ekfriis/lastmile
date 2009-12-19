''' Colony - central engine of algorithm

Holds an ensemble of ants, and the pheromone matrix

'''
import numpy as np
import ants.parameters as params
import ants.engine.operations as op

class Colony(object):
    ''' Colony - an ensemble of ants
    Colony manages the ants as the solve the routing problem.  Stores a
    copy of the route map, and each ant as it iterates.

    '''
    @params.use_parameters
    def __init__(self, routemap=None, num_ants=None, initial_pheromone=None):
        self.routemap = routemap
        self.num_dest = routemap.num_destinations()
        self.num_ants = num_ants
        # Initialize pheromone array as ndest*ndest
        self.pheromones = np.array(
            [[initial_pheromone]*self.num_dest]*self.num_dest, dtype=float)
        self.routes_and_results = {}

    def run_ants(self, include_timing=False):
        ''' Run N ants and update the pheromone matrix '''
        # Check if we are doing the initial run w/ no timing info.
        cheapness = None
        if include_timing:
            cheapness = self.routemap.cheapness
        else:
            cheapness = self.routemap.tangible_cheapness

        # Transition matrix is pheromone for each edge times inverse cost
        # between each edge 
        transition_matrix = cheapness*self.pheromones

        # Route initializer 
        # Start at origin
        route_init = [0]
        # All tbd points excepting the origin
        route_init.extend( [-1]*(self.num_dest-1) )
        # Return to origin at end
        route_init.append(0)

        for ant in range(self.num_ants):
            # Setup mask
            mask = np.array([False]*self.num_dest, dtype=bool)
            # Start at origin
            current_location = 0
            # Initialize route
            route = np.array(route_init, dtype=int)
            # Mark the origin as visited in the mask
            mask[0] = True

            # Index of route position
            route_index = 1
            while route_index < self.num_dest:
                # Get costs for traveling from current location to others
                # note that only costs for edges to unvisted nodes are included.
                next_location = op.select_edge_weighted(
                    np.ma.MaskedArray(
                        transition_matrix[current_location, :], mask=mask))
                # Update the route and mask
                route[route_index] = next_location
                mask[next_location] = True
                # Move to the new location
                current_location = next_location
                route_index += 1
            
            # When done, update the pheromone matrix for this routes cost
            cost = self.routemap.total_tangible_cost_for_route(route)

            if include_timing:
                cost += self.routemap.total_satisfaction_costs

            route_tuple = tuple(route)
            if tuple(route) not in self.routes_and_results:
                self.routes_and_results[route_tuple] = (cost, route) 

            # Update pheromone matrix
            for start, end in op.route_hops(route):
                self.pheromones[start, end] += 1.0/cost

    @params.use_parameters
    def update_pheromones(self, pheromone_decay=None):
        ''' Update pheromone matrix due to evaporation '''
        self.pheromones = self.pheromones*(1-pheromone_decay)

