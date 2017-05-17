#!/usr/bin/env python

"""
Compare current specter extraction to a reference run, reporting differences
"""

from __future__ import absolute_import, division, print_function
import sys, os
import time
import numpy as np

from specter.extract import ex2d
import specter.psf

def get_current_results():
    thisdir = os.path.split(os.path.abspath(__file__))[0]
    psffile = thisdir + '/../etc/psfnight-r0.fits'
    psf = specter.psf.load_psf(psffile)

    np.random.seed(0)
    ny, nx = psf.npix_y, psf.npix_x
    image = np.random.normal(loc=0, scale=1, size=(ny,nx))
    imageivar = np.ones_like(image)

    #- Spectra and wavelengths to extract
    nspec = 10
    nwave = 300
    wave = np.arange(psf.wmin_all, psf.wmin_all+nwave, 1)

    #- Wake up code, but using a different spectral range
    flux, ivar, R = ex2d(image, imageivar, psf, nspec, nspec, wave[0:10])

    #- Now do it for real
    t0 = time.time()
    flux, ivar, R = ex2d(image, imageivar, psf, 0, nspec, wave, bundlesize=nspec)
    runtime = time.time() - t0

    results = dict(flux=flux, ivar=ivar, R=R, runtime=runtime, nspec=nspec, wave=wave)
    return results

#-------------------------------------------------------------------------
import optparse

'''
Write a reference file with current extraction results:

    compare-extract.py --output ref1.npz

Compare saved results to current results (without saving current results):

    compare-extract.py ref1.npz

Compare saved results to current results and save current results:

    compare-extract.py ref1.npz --output ref2.npz

Compare two previously saved reference results:

    compare-extract.py ref1.npz ref2.npz
'''

parser = optparse.OptionParser(usage = "%prog [options]")
# parser.add_option("-i", "--input", type=str,  help="input data")
parser.add_option("-o", "--output", type=str,  help="output results for current extractions")
# parser.add_option("-v", "--verbose", action="store_true", help="some flag")

opts, reffiles = parser.parse_args()

if len(reffiles) == 0:
    assert opts.output is not None
    results = get_current_results()
    print('Saving results to {}'.format(opts.output))
    np.savez(opts.output, **results)
    sys.exit(0)
elif len(reffiles) == 1:
    ref1 = np.load(reffiles[0])
    ref2 = get_current_results()
    if opts.output is not None:
        print('Saving results to {}'.format(opts.output))
        np.savez(opts.output, **ref2)
else:
    ref1 = np.load(reffiles[0])
    ref2 = np.load(reffiles[1])
    

err = False
if ref1['nspec'] != ref2['nspec']:
    print('ERROR: nspec {} != {}'.format(ref1['nspec'], ref2['nspec']))
    err = True

if not np.allclose(ref1['wave'], ref2['wave']):
    print('ERROR: wave {}-{} != {}-{}'.format(
        ref1['wave'][[0,-1]], ref2['wave'][[0,-1]]))
    err = True
    
if ref1['flux'].shape != ref2['flux'].shape:
    print('ERROR: flux.shape {} != {}'.format(
        ref1['flux'].shape, ref2['flux'].shape))
    err = True

if err:
    sys.exit(1)

tx = ref2['runtime'] / ref1['runtime']
if np.abs(tx-1) < 0.01:
    print('Same runtime')
elif tx<1:
    tx = ref1['runtime'] / ref2['runtime']
    print('Runtime {:0.1f}x faster: {:.1f} -> {:.1f} sec'.format(
        tx, float(ref1['runtime']), float(ref2['runtime'])))
else:
    print('Runtime {:.1f}x slower: {:.1f} -> {:.1f} sec'.format(
        tx, float(ref1['runtime']), float(ref2['runtime'])))

print('Comparing results:')
print('key   exact  close')
for key in ['flux', 'ivar', 'R']:
    print('{:4s}  {:5s}  {:5s}'.format(
        key, str(np.all(ref1[key] == ref2[key])),
        str(np.allclose(ref1[key], ref2[key]))
        ))



