#- Test loopsine functions with multiprocessing parallelism

from __future__ import division, print_function

import multiprocessing as mp
from loopsine import loopsine_purepy, loopsine_numpy, loopsine_numba
from knltest import timeit

#- Wake up functions in case there is loading overhead
loopsine_purepy(2)
loopsine_numpy(2)
loopsine_numba(2)

n = 10000000
args = [n,] * mp.cpu_count() * 2
ncpu = 1
print("# Testing multiprocessing sum(sin(range({})))".format(n))
print("# Processing {} batches with ncpu processes".format(len(args)))
print("# method ncpu time     rate")
while ncpu <= mp.cpu_count():
    pool = mp.Pool(ncpu)
    t1 = timeit(pool.map, (loopsine_purepy, args))
    t2 = timeit(pool.map, (loopsine_numpy, args))
    t3 = timeit(pool.map, (loopsine_numba, args))
    pool.close()
    
    r1 = len(args) / t1
    r2 = len(args) / t2
    r3 = len(args) / t3
    print('purepy {:3d} {:8.3f} {:8.3f}'.format(ncpu, t1, r1))
    print('numpy  {:3d} {:8.3f} {:8.3f}'.format(ncpu, t2, r2))
    print('numba  {:3d} {:8.3f} {:8.3f}'.format(ncpu, t3, r3))
    
    ncpu *= 2
    
    