#- Utility functions for KNL tests

from __future__ import division, print_function
from time import time

def timeit(function, args=list(), kwargs=dict(), results=False):
    '''
    returns seconds elapsed to run function(*args, **kwargs)
    
    if results is True, returns seconds_elapsed, result_of_function
    '''
    t0 = time()
    r = function(*args, **kwargs)
    dt = time() - t0
    if results:
        return dt, r
    else:
        return dt
    