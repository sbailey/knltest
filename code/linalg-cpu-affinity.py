#!/usr/bin/env python

"""
Test CPU affinity when doing numpy linear algebra
"""

from __future__ import absolute_import, division, print_function
from mpi4py import MPI
comm = MPI.COMM_WORLD

import os
import numpy as np

#- Get CPU that this process is running on; works on Cori but not Mac0
def get_cpu(pid=None):
    if pid is None:
        pid = os.getpid()
    try:
        cpu = int(open("/proc/{pid}/stat".format(pid=os.getpid()), 'rb').read().split()[38])
    except:
        cpu = -1
    return cpu


start_cpu = get_cpu()

A = np.random.uniform(size=(10,10))
mid_cpu = get_cpu()
results = np.linalg.svd(A.T.dot(A))

end_cpu = get_cpu()

print('Rank {} proc {} cpu {} -> {} -> {}'.format(comm.rank, os.getpid(), start_cpu, mid_cpu, end_cpu))
