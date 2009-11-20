''' Parameters

Defines all parameters in the algorithm.  Intended for easy
serialization for use during parameter optimization.  Also single point of
defintion for 'standard' parameters.

'''
import pickle

_ALGO = {
    # Costs 
    'dollar_per_km': 2.0,
    'dollar_per_hour': 8.0,
    'cost_per_sad_customer': 4.0,
    # Std. number of MC iterations
    'iterations': 500
}

def dump_parameters(filename='algo_parameters.pkl'):
    ''' Save current parameter set to a file '''
    output = file(filename, 'wb')
    pickle.dump(_ALGO, output)
    output.close()

def load_parameters(filename='algo_parameters.pkl'):
    ''' Load a saved set of parameters from a file '''
    input_file = file(filename, 'r')
    _ALGO.clear()
    _ALGO.update(pickle.load(input_file))
    input_file.close()

def get_parameter(param):
    ''' Get value for a parameter '''
    return _ALGO[param]

def set_parameter(param, value):
    ''' Set parameter value '''
    _ALGO[param] = value

def use_parameters(func):
    ''' Decorator adds parameters into functions if not supplied '''
    # Find all kwargs we might need to replace
    param_names = [ name for name in func.func_code.co_varnames 
                 if name in _ALGO.keys() ]
    # If no parameters to replace, this shouldn't be used
    if len(param_names) == 0:
        return func
    # Else monitor the parameter arguments for None values
    def wrapper(*args, **kwargs):
        ''' Replace missing parameter kwargs '''
        for param in param_names:
            if param not in kwargs or kwargs[param] is None:
                kwargs[param] = _ALGO[param]
        return func(*args, **kwargs)
    return wrapper
