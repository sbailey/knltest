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

desidev
```
# Seconds to perform sum(sin(range(10000000)))
purepy 4.8335
numpy  0.8912
numba  0.9479
```

## loopsine_mp.py

Not setting OMP_NUM_THREADS; a separate test indicated it didn't matter
for this code.

Cori Haswell 128 batches
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

Cori Haswell 64 batches
```
# Testing multiprocessing sum(sin(range(10000000)))
# Processing 64 batches with ncpu processes
# method nproc time     rate
purepy   1  123.944    0.516
numpy    1   26.375    2.427
numba    1   20.911    3.061
purepy   2   61.902    1.034
numpy    2   13.333    4.800
numba    2   10.482    6.106
purepy   4   31.524    2.030
numpy    4    6.790    9.425
numba    4    5.328   12.011
purepy   8   17.075    3.748
numpy    8    3.678   17.402
numba    8    2.931   21.834
purepy  16    9.738    6.572
numpy   16    2.234   28.654
numba   16    1.687   37.931
purepy  32    7.586    8.437
numpy   32    1.530   41.821
numba   32    1.104   57.947
purepy  64    5.349   11.964
numpy   64    0.927   69.011
numba   64    0.638  100.252

```

Cori KNL 64 batches
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

desidev:
```
# Testing multiprocessing sum(sin(range(10000000)))
# Processing 64 batches with ncpu processes
# method ncpu time     rate
purepy   1  323.538    0.198
numpy    1   57.154    1.120
numba    1   60.283    1.062
purepy   2  162.677    0.393
numpy    2   28.551    2.242
numba    2   26.425    2.422
purepy   4   81.487    0.785
numpy    4   14.278    4.482
numba    4   13.217    4.842
purepy   8   40.859    1.566
numpy    8    7.231    8.851
numba    8    6.610    9.682
purepy  16   20.462    3.128
numpy   16    3.682   17.383
numba   16    3.313   19.320
purepy  32   10.309    6.208
numpy   32    1.998   32.031
numba   32    1.679   38.128
purepy  64    7.641    8.375
numpy   64    1.703   37.570
numba   64    1.620   39.494
```