#- Tests speed of https://github.com/sbailey/redrock zscan

if __name__ == '__main__':
    import sys, os, time
    import multiprocessing as mp
    import numpy as np
    import redrock
    import redrock.test.util
    from knltest import timeit
    
    #- Auto derive which machine we are on
    cpu_count = mp.cpu_count()
    if len(sys.argv) == 1:
        machine = 'laptop'
        if cpu_count in (32, 64):
            machine = 'haswell'
        elif cpu_count in (24, 48):
            machine = 'edison'
        elif cpu_count == 272:
            machine = 'knl'
        else:
            print("ERROR: unrecognized machine with {} cpus".format(cpu_count))
    else:
        machine = sys.argv[1]

    wavestep = 2
    if machine == 'laptop':
        nspec = 10
        redshifts = np.linspace(0.05,1,500)
        ncpu_list = (1,2,4)
    elif (machine in ('cori', 'haswell')):
        nspec = 10
        redshifts = np.linspace(0.05,1,500)
        ncpu_list = (1,2,4,8,16,32,64)
    elif (machine == 'coribig'):
        nspec = 50
        redshifts = np.linspace(0.05,1,3000)
        ncpu_list = (1,4,16,32,64)
    elif (machine == 'knl'):
        nspec = 10
        redshifts = np.linspace(0.05,1,500)
        ncpu_list = (1,4,8,16,32,64,128)
    elif (machine == 'knlfast'):
        nspec = 5
        redshifts = np.linspace(0.05,1,300)
        ncpu_list = (1,4,8,16,32,64,128)
    
    template = redrock.test.util.get_template(wavestep=wavestep)
    targets = list()
    for i in range(nspec):
        t = redrock.test.util.get_target(wavestep=wavestep)
        t.id = i
        targets.append(t)

    print('len(redshifts) = {}'.format(len(redshifts)))
    print('len(targets) = {}'.format(len(targets)))
    ntot = len(redshifts) * len(targets)

    #- Wake up numba
    redrock.zscan.parallel_calc_zchi2_targets(redshifts, targets[0:1], template,
        verbose=False, ncpu=cpu_count//2, numthreads=2)

    #- Do initial non-multiprocessing test
    print('ncpu nthread  time    rate')
    for numthreads in (1, cpu_count//2, cpu_count):
        os.environ['OMP_NUM_THREADS'] = str(numthreads)
        os.environ['KNL_NUM_THREADS'] = str(numthreads)
        t0 = time.time()
        results = redrock.zscan.calc_zchi2_targets(redshifts, targets, template)
        t = time.time() - t0
        print('{:3d}    {:3d}    {:.2f}    {:.2f}'.format(0, numthreads, t, ntot/t))

    #- Now do multiprocessing version
    for ncpu in ncpu_list:
        numthreads = max(1, cpu_count // ncpu // 1)
        args = (redshifts, targets, template)
        kwargs = dict(ncpu=ncpu, verbose=False, numthreads=numthreads)
        t = timeit(redrock.zscan.parallel_calc_zchi2_targets, args, kwargs)
        print('{:3d}    {:3d}    {:.2f}    {:.2f}'.format(ncpu, numthreads, t, ntot/t))

    
