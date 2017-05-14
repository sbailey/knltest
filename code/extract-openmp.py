#!/usr/bin/env python

"""
Test of DESI spectral extraction code

srun -n 1 -c 256 --cpu_bind=cores python extract.py 1 4 16 64 256
srun -n 1 -c 32 --cpu_bind=cores python extract.py 1 4 16 32
"""

from __future__ import absolute_import, division, print_function
import sys, os
import platform
import optparse
import multiprocessing

import numpy as np

from specter.extract import ex2d
import specter.psf
import knltest

parser = optparse.OptionParser(usage = "%prog [options]")
parser.add_option("-p", "--psf", type=str,  help="input psf file")
parser.add_option("-n", "--numspec", type=int, default=25, help="number of spectra")
parser.add_option("-w", "--numwave", type=int, default=200, help="number of wavelengths")

opts, ntest = parser.parse_args()

#- OMP_NUM_THREADS options to test
if len(ntest) == 0:
    ntest = (1,4,16,32,64)

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
args = [image, imageivar, psf]
kwargs = dict(specmin=0, nspec=opts.numspec, wavelengths=w)

#- Wake up the code in case there is library loading overhead
flux, ivar, R = ex2d(image, imageivar, psf, 0, 2, w[0:10])

print('Running on {}/{} with {} logical cores'.format(
    platform.node(), platform.processor(), multiprocessing.cpu_count()))
print('{} spectra x {} wavelengths extracted'.format(opts.numspec, opts.numwave))
print('OMP_NUM_THREADS time')
for n in ntest:
    os.environ['OMP_NUM_THREADS'] = str(n)
    t = knltest.timeit(ex2d, args, kwargs)
    print("{:3} {:5.1f}".format(n, t), flush=True)
