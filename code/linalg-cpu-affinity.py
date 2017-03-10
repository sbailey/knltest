#!/usr/bin/env python

"""
Test CPU affinity when doing numpy linear algebra
"""

from __future__ import absolute_import, division, print_function
from mpi4py import MPI
comm = MPI.COMM_WORLD

import os
import numpy as np
from knltest import get_cpu

#- Testing: does loading a PSF mess up MPI CPU affinity too? No, it's ok
# import knltest
# import specter.psf
# thisdir = os.path.split(knltest.__file__)[0]
# psffile = thisdir + '/../etc/psfnight-r0.fits'
# psf = specter.psf.load_psf(psffile)
#- Testing

#- Testing: does a legfit mess up MPI CPU affinity too? No, it's ok
# from numpy.polynomial.legendre import legfit
# x = np.linspace(0,1)
# y = np.sin(x)
# c = legfit(y, x, 3)   #- Break MP cpu affinity !?!
#- Testing

start_cpu = get_cpu()

A = np.random.uniform(size=(10,10))
mid_cpu = get_cpu()
results = np.linalg.svd(A.T.dot(A))

end_cpu = get_cpu()

print('Rank {} proc {} cpu {} -> {} -> {}'.format(comm.rank, os.getpid(), start_cpu, mid_cpu, end_cpu))
