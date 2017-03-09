## CPU Affinity ##

2017-03-09

numpy linear algebra operations that touch OpenMP reset the CPU affinity
to CPU=0.  This happens for both MPI and multiprocessing.
For MPI, the processes start out on different CPUs but collapse to
CPU 0; see code/linalg-cpu-affinity.py .
For multiprocessing, we can use psutil.cpu_affinity to force what CPU
each process goes to, but they still collapse back to 0.
See code/extract-mp.py.


