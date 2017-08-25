# Testing redrock

## Initial setup

module load python/3.5-anaconda
conda create -n rrtest python=3 numpy scipy astropy numba ipython matplotlib hdf5
source activate rrtest

#- non-conda dependencies
cd $SCRATCH/rrtest
pip install speclite
for x in desiutil desispec; do
    git clone https://github.com/desihub/$x
    cd $x && python setup.py install && cd ..
done

#- redrock & redrock templates
git clone https://github.com/desihub/redrock-templates
export RR_TEMPLATE_DIR=$(pwd)/redrock-templates
git clone https://github.com/desihub/redrock
cd redrock
git checkout sharedmem
python setup.py develop
cd ..

#- get spectra-64-4674.fits

## Basic setup

module load python/3.5-anaconda
source activate rrtest
export RR_TEMPLATE_DIR=$SCRATCH/rrtest/redrock-templates
cd $SCRATCH/rrtest

## Job script
salloc -N 1 -C haswell --qos interactive -t 1:00:00
salloc -N 1 -C knl --qos interactive -t 1:00:00

Haswell options
```
#- NOTE: not setting OMP_PLACES and OMP_PROC_BIND has best performance
OMP_PLACES=sockets is ok, but cores or threads is 3-4x worse

unset OMP_PLACES
unset OMP_PROC_BIND
export OMP_NUM_THREADS=1
export MPICH_GNI_FORK_MODE=FULLCOPY

time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 4 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 8 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 16 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 32 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 64 --ntarget 64

time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 16 --ntarget 32
time rrdesi spectra-64-4674.fits --zbest blat.fits --ncpu 16 --ntarget 128
```

KNL environment variables: use KMP_AFFINITY instead of OMP_PLACES and OMP_PROC_BIND
```
export OMP_NUM_THREADS=1
export KMP_AFFINITY=disabled
export MPICH_GNI_FORK_MODE=FULLCOPY

time rrdesi spectra-64-4674.fits --zbest foo.fits --ncpu 16 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest foo.fits --ncpu 32 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest foo.fits --ncpu 64 --ntarget 64
time rrdesi spectra-64-4674.fits --zbest foo.fits --ncpu 128 --ntarget 64
```

```
cpu   ncpu   ntarg  time
hsw   4      64     123
hsw   8      64     85
hsw   16     64     68
hsw   32     64     68
hsw   64     64     76

hsw   16     32     50
hsw   16     128    102
hsw   16     256    169

knl   16     64     380
knl   64     64     315
knl   128    64     337

knl   64     128    408
knl   64     256    598
```

Only on KNL:
```
<cori rrtest> time rrdesi spectra-64-4674.fits --zbest foo.fits --ncpu 16 --ntarget 64
/global/cscratch1/sd/sjbailey/rrtest/redrock/py/redrock/dataobj.py:161: RuntimeWarning: divide by zero encountered in true_divide
  Winv = scipy.sparse.dia_matrix((1/(weights+isbad), [0,]), (n,n))
```
Note that `isbad = (weights == 0)` so in principle `1/(weights+isbad)`
should never be a divide by zero.

but this earlier line didn't cause a warning:
```
flux = weightedflux / (weights + isbad)
```
TODO: check KNL vs. HSW outputs for consistency despite that message

