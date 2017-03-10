#!/usr/bin/env python

import multiprocessing as mp
import numpy as np
import os, sys
import time

from knltest import get_cpu
import psutil

parent = psutil.Process(os.getpid())
parent.cpu_affinity([42,])

def blat(i):
    pid, c0 = get_cpu()
    #- Set affinity within child process 
    child = psutil.Process(pid)
    child.cpu_affinity([i,])
    _, c1 = get_cpu()
    A = np.random.uniform(size=(100,100))
    r = np.linalg.svd(A.T.dot(A))
    _, c2 = get_cpu()
    print(i, pid, c0, c1, c2)

    #- Let's try some more linalg 
    # child.cpu_affinity([i+10,])
    # _, c3 = get_cpu()
    # r = np.linalg.svd(A.T.dot(A))
    # _, c4 = get_cpu()
    # print(i, pid, c0, c1, c2, c3, c4)
    sys.stdout.flush()

print('Before linalg in parent process {}'.format(get_cpu()))
mp.Process(target=blat, args=[88,]).start()
mp.Process(target=blat, args=[99,]).start()

#- This causes a sticky affinity to 42 (!?!)
A = np.random.uniform(size=(100,100))
r = np.linalg.svd(A.T.dot(A))

#- Try to change to 43
parent.cpu_affinity([43,])

time.sleep(0.1)
sys.stdout.flush()
print('After linalg in parent process {}'.format(get_cpu()))
for i in range(4):
    #- Set affinity of parent process
    # parent.cpu_affinity([i,])
    p = mp.Process(target=blat, args=[i,])
    p.start()





