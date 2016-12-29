## loopsine.py

Cori Haswell
```
<cori knltest> python code/loopsine.py 
# Seconds to perform sum(sin(range(10000000)))
purepy 1.8924
numpy  0.4111
numba  0.7110
```

Cori KNL
```
<cori knltest> python code/loopsine.py 
# Seconds to perform sum(sin(range(10000000)))
purepy 10.8509
numpy  2.1926
numba  3.0861

```

## loopsine_mp.py

Not setting OMP_NUM_THREADS; a separate test indicated it didn't matter
for this code.

Cori Haswell
```
<cori knltest> python code/loopsine_mp.py 
# Testing multiprocessing sum(sin(range(10000000)))
# Processing 128 batches with ncpu processes
# method ncpu time     rate
purepy   1  246.378    0.520
numpy    1   53.248    2.404
numba    1   41.816    3.061
purepy   2  123.157    1.039
numpy    2   26.678    4.798
numba    2   20.968    6.105
purepy   4   62.231    2.057
numpy    4   13.462    9.508
numba    4   10.608   12.066
purepy   8   34.503    3.710
numpy    8    7.317   17.492
numba    8    5.844   21.901
purepy  16   25.316    5.056
numpy   16    4.361   29.350
numba   16    3.348   38.229
purepy  32   12.202   10.490
numpy   32    2.634   48.595
numba   32    2.225   57.526
purepy  64   11.021   11.614
numpy   64    1.915   66.844
numba   64    1.309   97.779
```

Cori KNL (but a power of 2 in batches would be better)
```
<cori knltest> python code/loopsine_mp.py 
# Testing multiprocessing sum(sin(range(10000000)))
# Processing 34 batches with ncpu processes
# method ncpu time     rate
purepy   1  385.993    0.088
numpy    1   73.408    0.463
numba    1   67.903    0.501
purepy   2  215.503    0.158
numpy    2   41.260    0.824
numba    2   38.752    0.877
purepy   4  118.360    0.287
numpy    4   20.002    1.700
numba    4   17.931    1.896
purepy   8   67.597    0.503
numpy    8   13.140    2.587
numba    8   11.956    2.844
purepy  16   34.790    0.977
numpy   16    6.750    5.037
numba   16    5.998    5.668
purepy  32   22.717    1.497
numpy   32    4.955    6.862
numba   32    3.996    8.508
purepy  64   14.364    2.367
numpy   64    3.130   10.863
numba   64    2.228   15.257
purepy 128   15.531    2.189
numpy  128    3.084   11.024
numba  128    2.245   15.147
purepy 256   14.499    2.345
numpy  256    3.146   10.808
numba  256    2.217   15.336

```

Again, with a multiple of 2 (in two jobs since first timed out and had
to restart at ncpu=8):
```
<cori knltest> python code/loopsine_mp.py 
# Testing multiprocessing sum(sin(range(10000000)))
# Processing 64 batches with ncpu processes
# method ncpu time     rate
purepy   1  706.088    0.091
numpy    1  138.151    0.463
numba    1  127.948    0.500
purepy   2  352.840    0.181
numpy    2   69.558    0.920
numba    2   63.764    1.004
purepy   4  185.846    0.344
numpy    4   34.982    1.830
numba    4   31.919    2.005
purepy   8  109.140    0.586
numpy    8   17.874    3.581
numba    8   17.511    3.655
purepy  16   54.533    1.174
numpy   16    9.410    6.801
numba   16    8.425    7.597
purepy  32   27.814    2.301
numpy   32    5.945   10.765
numba   32    4.375   14.629
purepy  64   14.153    4.522
numpy   64    4.765   13.430
numba   64    2.315   27.644
```
