## CPU Affinity ##

2017-03-09

numpy linear algebra operations that touch OpenMP reset the CPU affinity
to CPU=0.  See `code/linalg-cpu-affinity.py`

### MPI ###

`--cpu_bind=cores` works to prevent this behavior:
```
srun -n 4 -c 64 --cpu_bind=cores python linalg-cpu-affinity.py
```
Without that option, even MPI will reset to core 0 for everyone.

### Multiprocessing ###

For multiprocessing, we can use psutil.cpu_affinity to force what CPU
each process goes to, but they still collapse back to 0.
See `code/linalg-mp-affinity.py`.

### Scratch code ###

```
module load python/3.5-anaconda
cd $SCRATCH/desi/knlcode/knltest/code

export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

salloc -N 1 -p debug -C knl,quad,cache -t 00:30:00

srun -n 4 -c 64 --cpu_bind=cores python linalg-cpu-affinity.py
srun -n 1 -c 64 --cpu_bind=cores python linalg-mp-affinity.py
```

