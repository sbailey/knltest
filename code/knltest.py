#- Utility functions for KNL tests

from __future__ import division, print_function

def timeit(function, args=list(), kwargs=dict(), results=False):
    '''
    returns seconds elapsed to run function(*args, **kwargs)
    
    if results is True, returns seconds_elapsed, result_of_function
    '''
    from time import time
    t0 = time()
    r = function(*args, **kwargs)
    dt = time() - t0
    if results:
        return dt, r
    else:
        return dt

#- Get CPU that this process is running on
def get_cpu(pid=None):
    import os
    '''Determine which CPU this process is running on; returns pid, cpu'''
    if pid is None:
        pid = os.getpid()
    try:
        cpu = int(open("/proc/{pid}/stat".format(pid=os.getpid()), 'rb').read().split()[38])
    except:
        cpu = -1
    return pid, cpu

