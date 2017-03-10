#!/usr/bin/env python

"""
Test of DESI spectral extraction code at various matrix sizes
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

thisdir = os.path.split(knltest.__file__)[0]
psffile = thisdir + '/../etc/psfnight-r0.fits'
assert os.path.exists(psffile)
    
psf = specter.psf.load_psf(psffile)

#- Create fake noisy image
ny, nx = psf.npix_y, psf.npix_x
image = np.random.normal(loc=0, scale=1, size=(ny,nx))
imageivar = np.ones_like(image)

#- Spectra and wavelengths to extract
w = np.arange(psf.wmin_all, psf.wmax_all, 1)

#- Wake up the code in case there is library loading overhead
flux, ivar, R = ex2d(image, imageivar, psf, 0, 2, w[0:10])

#- Do extractions, while modeling edge effects that would be needed when
#- doing smaller bundle sizes (i.e. nspec+2)
print('nwave nflux ntot rate')
for nspec in [2,5,10]:
    for nwave in [5,10,20]:
        args = (image, imageivar, psf, 0, (nspec+2)*2, w[0:nwave*2])
        kwargs = dict(bundlesize=nspec+2, wavesize=nwave)
        t = knltest.timeit(ex2d, args, kwargs)
        rate = nspec*nwave/t
        print('{:3d} {:3d} {:4d} {:f}'.format(nspec, nwave, nspec*nwave, rate))
