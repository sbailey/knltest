#!/usr/bin/env python

"""
Test numpy vs. alternatives for a few calculations
"""

from __future__ import absolute_import, division, print_function
import numpy as np
import numba
import time
import numpy.core.umath

from pylab import *
ion()

def outer1(x, y, out):
    return np.multiply(x[:, None], y[None, :], out)
    
@numba.jit
def outer2(x, y, out):
    for i in range(len(x)):
        for j in range(len(y)):
            out[i,j] = x[i] * y[j]
    return out

def sum1(x):
    return numpy.core.umath.add.reduce(x)

@numba.jit
def numbadot(x, y):
    r = 0.0
    for i in range(len(x)):
        r += x[i] * y[i]
    return r

@numba.jit
def sum2(x):
    r = 0.0
    for i in range(len(x)):
        r += x[i]
    return r

def timeit(func, *args, **kwargs):
    t0 = time.time()
    blat = func(*args, **kwargs)
    return time.time() - t0

#-------------------------------------------------------------------------
nx = [10, 30, 100, 300, 1000, 3000, 10000]
tx0, tx1, tx2 = list(), list(), list()
txa, txb, txc, txd, txe, txf = list(), list(), list(), list(), list(), list()

for n in nx:
    print(n)
    t0 = list()
    t1 = list()
    t2 = list()
    ta = list()
    tb = list()
    tc = list()
    td = list()
    te = list()
    tf = list()
    for i in range(7):
        x = np.random.uniform(size=n)
        y = np.random.uniform(size=n)
        out = np.empty(shape=(n,n))
        t0.append(timeit(np.outer, x, y, out=out))
        t1.append(timeit(outer1, x, y, out=out))
        t2.append(timeit(outer2, x, y, out=out))
        
        ta.append(timeit(np.dot, x, y))
        tb.append(timeit(np.multiply, x, y))
        tc.append(timeit(np.sum, x))
        td.append(timeit(sum1, x))
        te.append(timeit(sum2, x))
        tf.append(timeit(numbadot, x, y))
    
    tx0.append(np.median(t0))
    tx1.append(np.median(t1))
    tx2.append(np.median(t2))

    txa.append(np.median(ta))
    txb.append(np.median(tb))
    txc.append(np.median(tc))
    txd.append(np.median(td))
    txe.append(np.median(te))
    txf.append(np.median(tf))

#-------------------------------------------------------------------------
figure(figsize=(6,8))
subplot(311)
plot(nx, tx0, label='numpy')
plot(nx, tx1, label='custom')
plot(nx, tx2, label='numba')
loglog(); ylabel('time'); title('outer(x,y) comparison')
legend(loc='upper left')

subplot(312)
plot(nx, txa, label='dot')
plot(nx, txb, label='multiply')
plot(nx, txc, label='sum')
plot(nx, txf, label='numba dot')
loglog(); ylabel('time'); title('dot / multiply / sum')
legend(loc='upper left')

subplot(313)
plot(nx, txc, label='numpy sum')
plot(nx, txd, label='umath sum')
plot(nx, txe, label='numba sum')
loglog(); xlabel('n'); ylabel('time'); title('sum comparison')
legend(loc='upper left')

tight_layout()
show()
# savefig('numpy-speed.pdf')
