#- Test a sum(sin(range(n))) in purepy, numpy, numba

from __future__ import division, print_function

import math
import numpy as np
import numba

from knltest import timeit

n = 10000000
def loopsine_purepy(n=n):
    total = 0.0
    for i in range(n):
        total += math.sin(i)
    return total

@numba.jit
def loopsine_numba(n=n):
    total = 0.0
    for i in range(n):
        total += math.sin(i)
    return total

def loopsine_numpy(n=n):
    return np.sum(np.sin(np.arange(n)))

if __name__ == '__main__':
    t1, r1 = timeit(loopsine_purepy, result=True)
    t2, r2 = timeit(loopsine_numpy, result=True)
    t3, r3 = timeit(loopsine_numba, result=True)
    assert np.allclose([r1, r2, r3], [r2, r3, r1])
    print('# Seconds to perform sum(sin(range({})))'.format(n))
    print('purepy {:.4f}'.format(t1))
    print('numpy  {:.4f}'.format(t2))
    print('numba  {:.4f}'.format(t3))
