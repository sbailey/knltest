#!/usr/bin/env python

"""
Test scaling of linalg operations with matrix size
"""

from __future__ import absolute_import, division, print_function
import sys, os
import time
import numpy as np

def timeit(function, A):
    t0 = time.time()
    r = function(A)
    t1 = time.time()
    return t1-t0

Ax = list()
for n in [100,200,500,1000,2000]:
    X = np.random.uniform(size=(n,n))
    Ax.append(X.T.dot(X))

print('# n   svd    chol   eigh')
for A in Ax:
    n = A.shape[0]
    tsvd = timeit(np.linalg.svd, A)
    tcho = timeit(np.linalg.cholesky, A)
    teig = timeit(np.linalg.eigh, A)
    print('{:4d}  {:6.4f} {:6.4f} {:6.4f}'.format(n, tsvd, tcho, teig))
    


