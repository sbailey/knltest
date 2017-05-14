#!/usr/bin/env python

"""
Test of DESI spectral extraction code

srun -n 1 -c 256 --cpu_bind=cores python extract.py 1 4 16 64 256
srun -n 1 -c 32 --cpu_bind=cores python extract.py 1 4 16 32
"""

from __future__ import absolute_import, division, print_function
import sys, os
import platform
import time
import optparse

import numpy as np

from specter.extract import ex2d
import specter.psf

parser = optparse.OptionParser(usage = "%prog [options]")
parser.add_option("-p", "--psf", type=str,  help="input psf file")
parser.add_option("--nwavestep", type=int, default=50, help="number of wavelengths per extraction step")
parser.add_option("--numwave", type=int, default=200, help="number of wavelengths total")
parser.add_option("--seed", type=int, default=0, help="random seed")

opts, nspec = parser.parse_args()

#- OMP_NUM_THREADS options to test
if len(nspec) == 0:
    nspec = (5, 10, 15, 20, 25)
else:
    nspec = [int(tmp) for tmp in nspec]

#- Load point spread function model
if opts.psf is None:
    thisdir = os.path.split(os.path.abspath(__file__))[0]
    opts.psf = thisdir + '/../etc/psfnight-r0.fits'
    assert os.path.exists(opts.psf)
    
psf = specter.psf.load_psf(opts.psf)

#- Create fake noisy image
np.random.seed(opts.seed)
ny, nx = psf.npix_y, psf.npix_x
image = np.random.normal(loc=0, scale=1, size=(ny,nx))
imageivar = np.ones_like(image)

#- Spectra and wavelengths to extract
wave = np.arange(psf.wmin_all, psf.wmin_all+opts.numwave, 1)

#- Wake up the code in case there is library loading overhead
flux, ivar, R = ex2d(image, imageivar, psf, 0, 2, wave[0:10])

print('Running on {}/{}'.format(
    platform.node(), platform.processor()))
if 'OMP_NUM_THREADS' not in os.environ:
    print('$OMP_NUM_THREADS not set')
else:
    print('$OMP_NUM_THREADS={}'.format(os.getenv('OMP_NUM_THREADS')))
print('nspec  rate')
for n in nspec:
    t0 = time.time()
    flux, ivar, R = ex2d(image, imageivar, psf, 0, n, wave, wavesize=opts.nwavestep)
    dt = time.time() - t0
    rate = n*len(wave) / dt
    print("{:3}  {:5.1f}".format(n, rate), flush=True)
