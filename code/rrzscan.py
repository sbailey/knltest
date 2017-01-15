#- Tests speed of https://github.com/sbailey/redrock zscan

if __name__ == '__main__':
    import sys
    import multiprocessing as mp
    import numpy as np
    import redrock
    import redrock.test.util
    from knltest import timeit
    
    wavestep = 2
    if (len(sys.argv) == 1) or (sys.argv[1] == 'laptop'):
        nspec = 10
        redshifts = np.linspace(0.05,1,500)
        ncpu_list = (1,2,4)
    elif (sys.argv[1] in ('cori', 'haswell')):
        nspec = 10
        redshifts = np.linspace(0.05,1,500)
        ncpu_list = (1,2,4,8,16,32,64)
    elif (sys.argv[1] == 'knl'):
        nspec = 5
        redshifts = np.linspace(0.05,1,200)
        ncpu_list = (8,32,64)
    
    template = redrock.test.util.get_template(wavestep=wavestep)
    template.redshifts = np.linspace(0.05,1,500)
    targets = list()
    for i in range(nspec):
        t = redrock.test.util.get_target(wavestep=wavestep)
        t.id = i
        targets.append(t)

    #- Wake up numba
    redrock.zscan.parallel_calc_zchi2_targets(template.redshifts[0::10], targets[0:1], template)

    ntot = len(template.redshifts) * len(targets)
    print('ncpu nthread  time    rate')
    for ncpu in ncpu_list:
        numthreads = max(1, mp.cpu_count() // ncpu)
        args = (template.redshifts, targets, template)
        kwargs = dict(ncpu=ncpu, verbose=False, numthreads=numthreads)
        t = timeit(redrock.zscan.parallel_calc_zchi2_targets, args, kwargs)
        print('{:3d}    {:3d}    {:.2f}    {:.2f}'.format(ncpu, numthreads, t, ntot/t))

    