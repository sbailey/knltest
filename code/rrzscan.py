#- Tests speed of https://github.com/sbailey/redrock zscan

if __name__ == '__main__':
    import sys
    import multiprocessing as mp
    import numpy as np
    import redrock
    import redrock.test.util
    from knltest import timeit
    
    if (len(sys.argv) == 1) or (sys.argv[1] == 'laptop'):
        wavestep = 2
        redshifts = np.linspace(0.05,1,500)
        nspec = 10
    
    template = redrock.test.util.get_template(wavestep=wavestep)
    template.redshifts = np.linspace(0.05,1,500)
    targets = list()
    for i in range(nspec):
        t = redrock.test.util.get_target(wavestep=wavestep)
        t.id = i
        targets.append(t)

    #- Wake up numba
    redrock.zscan.parallel_calc_zchi2_targets(template.redshifts[0::10], targets[0:1], template)

    print('ncpu nthread  time    rate')
    for ncpu in (1,2,4):
        numthreads = max(1, mp.cpu_count() // ncpu)
        args = (template.redshifts, targets, template)
        kwargs = dict(ncpu=ncpu, verbose=False, numthreads=numthreads)
        t = timeit(redrock.zscan.parallel_calc_zchi2_targets, args, kwargs)
        print('{:3d}    {:3d}    {:.2f}    {:.2f}'.format(ncpu, numthreads, t, len(targets)/t))

    