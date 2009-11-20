''' Parameters

Class that defines all parameters in the algorithm.  Intended for easy
serialization for use during parameter optimization.  Also single point of
defintion for 'standard' parameters.

'''

# TODO make this suck less
class Parameters(object):
    ''' Define all arbritrary algorithm parameters

    Examples might be:
        * Pheromone decay rate
        * Number of colonies
        
    '''

    def __init__(self, **parameters):
        self.params = parameters
    
    def __getattr__(self, attr_name):
        if attr_name in self.params:
            return self.params[attr_name]
        else:
            raise AttributeError, " paramter doesn't exist!"
    

STD_PARAMS = Parameters(
    # Costs 
    dollar_per_km=2.0,
    dollar_per_hour=8.0,
    cost_per_sad_customer=4.0,
    # Std. number of MC iterations
    iterations=500,
)

