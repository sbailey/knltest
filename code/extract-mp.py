#!/usr/bin/env python

"""
Test of DESI spectral extraction code with multiprocessing parallelism

srun -n 1 -c 256 --cpu_bind=cores python extract.py 1 4 16 ...
srun -n 1 -c 32 --cpu_bind=cores python extract.py 1 4 16 32
"""

from __future__ import absolute_import, division, print_function
import sys, os
import platform
import optparse
import multiprocessing as mp
import time

import numpy as np

from specter.extract import ex2d
import specter.psf
import knltest

parser = optparse.OptionParser(usage = "%prog [options]")
parser.add_option("-p", "--psf", type=str,  help="input psf file")
parser.add_option("-n", "--numspec", type=int, default=100, help="number of spectra")
parser.add_option("-w", "--numwave", type=int, default=200, help="number of wavelengths")

opts, ntest = parser.parse_args()

#- OMP environment
os.environ['OMP_PROC_BIND']='spread'
os.environ['OMP_NUM_THREADS'] = '1'
# os.environ['OMP_PLACES'] = 'cores("1")'

#- OMP_NUM_THREADS options to test
if len(ntest) == 0:
    ntest = (1,2)

#- Load point spread function model
if opts.psf is None:
    thisdir = os.path.split(knltest.__file__)[0]
    opts.psf = thisdir + '/../etc/psfnight-r0.fits'
    assert os.path.exists(opts.psf)
    
psf = specter.psf.load_psf(opts.psf)

#- Create fake noisy image
ny, nx = psf.npix_y, psf.npix_x
image = np.random.normal(loc=0, scale=1, size=(ny,nx))
imageivar = np.ones_like(image)

#- Spectra and wavelengths to extract
w = np.arange(psf.wmin_all, psf.wmin_all+opts.numwave, 1)

#- Wake up the code in case there is library loading overhead
flux, ivar, R = ex2d(image, imageivar, psf, 0, 2, w[0:10])

#- Get params from qin, run ex2d, put results into qout
def wrap_ex2d(qin, qout):
    while True:
        i, specmin, nspec, wave = qin.get()
        results = ex2d(image, imageivar, psf, specmin, nspec, wave)
        qout.put((i, results))

#- Setup sub extractions
extract_args = list()
bundlesize = 25
wavesize = 50
iarg = 0
for specmin in range(0, opts.numspec, bundlesize):
    for i in range(0, len(w), wavesize):
        x = (iarg, specmin, bundlesize, w[i:i+wavesize])
        extract_args.append(x)
        iarg += 1

print('Running on {}/{} with {} logical cores'.format(
    platform.node(), platform.processor(), mp.cpu_count()))
print('{} spectra x {} wavelengths to extract'.format(opts.numspec, opts.numwave))
print('performing {} sub extractions'.format(len(extract_args)))
print("OMP_NUM_THREADS={}".format(os.getenv('OMP_NUM_THREADS')))
print('nproc time rate')
for nproc in ntest:
    #- Load qin
    qin = mp.Queue()
    for x in extract_args:
        qin.put(x)

    #- Start processes
    t0 = time.time()
    qout = mp.Queue()
    procs = list()
    for i in range(int(nproc)):
        p = mp.Process(target=wrap_ex2d, args=(qin, qout))
        p.start()
        procs.append(p)

    #- Pull the expected number of results from qout
    #- Note: not robust to failures, but should be fine for benchmark test
    results = list()
    for i in range(len(extract_args)):
        results.append(qout.get())

    t = time.time() - t0
    rate = opts.numspec * opts.numwave / t
    print("{:3} {:5.1f} {:5.1f}".format(nproc, t, rate), flush=True)

    #- Stop processes
    for p in procs:
        p.terminate()
    
# print('OMP_NUM_THREADS time')
# for n in ntest:
#     os.environ['OMP_NUM_THREADS'] = str(n)
#     os.environ['OMP_PLACES'] = 'cores"({})"'.format(n)
#     t = knltest.timeit(ex2d, args, kwargs)
#     print("{:3} {:5.1f}".format(n, t))