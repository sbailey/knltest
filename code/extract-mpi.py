#!/usr/bin/env python

"""
Test of DESI spectral extraction code using MPI for parallelism

batchopts="-C haswell -p debug -t 00:20:00"
srun -n 4 -c 1 $batchopts python extract-mpi.py 1 2 4 --bundlesize 5 --numwave 50
"""

from __future__ import division, print_function
import time
t0 = time.time()

from mpi4py import MPI
comm = MPI.COMM_WORLD

import sys, os
import platform
import optparse
import multiprocessing

import numpy as np

from specter.extract import ex2d
import specter.psf
import knltest

comm.barrier()
if comm.rank == 0:
    t1 = time.time()
    print('wakeup time {:.1f}'.format(t1-t0))

parser = optparse.OptionParser(usage = "%prog [options]")
parser.add_option("-p", "--psf", type=str,  help="input psf file")
parser.add_option("-n", "--numthreads", type=str, default="1", help="set $OMP_NUM_THREADS")
# parser.add_option("-n", "--numspec", type=int, default=100, help="number of spectra")
parser.add_option("-w", "--numwave", type=int, default=200, help="number of wavelengths")
parser.add_option("--fix-total-work", action="store_true", help="Fix the total amount of work instead of work per process")
parser.add_option("-b", "--bundlesize", type=int, default=25, help="size of bundles of spectra")

opts, ntest = parser.parse_args()

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
w = np.linspace(psf.wmin_all, psf.wmax_all, 2000)

#- Wake up the code in case there is library loading overhead
flux, ivar, R = ex2d(image, imageivar, psf, 0, 2, w[0:10])

#- Setup sub extractions
extract_args = list()
iarg = 0
for specmin in range(0, psf.nspec, opts.bundlesize):
    for i in range(0, len(w), opts.numwave):
        x = (iarg, specmin, opts.bundlesize, w[i:i+opts.numwave])
        extract_args.append(x)
        iarg += 1

#- add comm.barrier() here to make sure everyone is woken up?
comm.barrier()
if comm.rank == 0:
    t2 = time.time()
    print('setup time {:.1f}'.format(t2-t1))

#- Do the extractions
os.environ['OMP_PROC_BIND']='spread'
os.environ['OMP_NUM_THREADS'] = opts.numthreads
if comm.rank == 0:
    print('Running on {}/{} with {} logical cores'.format(
        platform.node(), platform.processor(), multiprocessing.cpu_count()))
    print("bundlesize {} numwave {}".format(opts.bundlesize, opts.numwave))
    print('mpiprocs time rate', flush=True)

for nrank in ntest:
    nrank = int(nrank)
    if opts.fix_total_work:
        nmax = 128
    else:
        nmax = 2*nrank
    t0 = time.time()
    if comm.rank < nrank:
        for i in range(comm.rank, nmax, nrank):
            iarg, specmin, nspec, wave = extract_args[i]
            results = ex2d(image, imageivar, psf, specmin, nspec, wave, bundlesize=nspec)
            #- Skip details about how to get the results back to the parent process

    comm.barrier()
    if comm.rank == 0:
        t = time.time() - t0
        rate = nmax * opts.bundlesize * opts.numwave / t
        print("{:3} {:5.1f} {:5.1f}".format(nrank, t, rate), flush=True)
