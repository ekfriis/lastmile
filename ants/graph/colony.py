''' Colony - central engine of algorithm

Holds an ensemble of ants, and the pheromone matrix

'''
import numpy as np
import ants.parameters as params
import ants.graph.operations as op

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
        self.routes_and_results = []
        self.route_history = []

    def run_ants(self, include_timing=False, quiet=True):
        ''' Run N ants and update the pheromone matrix '''
        best_cost = np.Inf
        best_route = None
        # Check if we are doing the initial run w/ no timing info.
        cheapness = None
        if include_timing:
            cheapness = self.routemap.cheapness
        else:
            cheapness = self.routemap.tangible_cheapness

        # Transition matrix is pheromone for each edge times inverse cost
        # between each edge 
        transition_matrix = cheapness*self.pheromones
        for ant in range(self.num_ants):
            # Setup mask
            mask = np.array([False]*self.num_dest, dtype=bool)
            # Start at origin
            current_location = 0
            route = np.array([0], dtype=int)
            mask[0] = True

            #Run the route
            while len(route) < self.num_dest:
                # Get costs for traveling from current location to others
                # note that only costs for edges to unvisted nodes are included.
                next_location = op.select_edge_weighted(
                    np.ma.MaskedArray(
                        transition_matrix[current_location, :], mask=mask))
                # Update the route and mask
                route = np.append(route, next_location)
                mask[next_location] = True
                # Move to the new location
                current_location = next_location
            
            # When done, update the pheromone matrix for this routes cost
            cost = self.routemap.total_tangible_cost_for_route(route)
            if include_timing:
                cost += self.routemap.total_satisfaction_costs

            # Update pheromone matrix
            for start, end in op.route_hops(route):
                self.pheromones[start, end] += 1.0/cost

            if cost < best_cost:
                best_cost = cost
                best_route = route
        return best_cost, best_route

    @params.use_parameters
    def update_pheromones(self, pheromone_decay=None):
        ''' Update pheromone matrix due to evaporation '''
        self.pheromones = self.pheromones*(1-pheromone_decay)

