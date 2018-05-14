from timeit import default_timer

import numpy as np

from zadanie34.task34_utils import fabricate_data, count_lvl_nodes


def prep_test_cases(nlvls):
    '''
    Input:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path


    In each prepared test case, the sum of level maximum values (max_sum)
    lies on a valid (feasible) path and is also the largest sum of leaf nodes.


    Returns a tuple with three lists of the same length:
    -- common arguments (nlvls, max_sum, triangle);
    -- correct paths (1D unsigned integer numpy arrays with ones and zeros);
    -- correct sums of leaf nodes (positive integer numbers).
    '''

    params = []
    paths = []
    answers = []

    prev_lvl_nodes = count_lvl_nodes(nlvls)[0]

    max_sum, triangle = fabricate_data(nlvls, False)
    steps = np.ones(shape=nlvls, dtype=np.uint8)
    indexes = prev_lvl_nodes + np.add.accumulate(steps)

    params.append((nlvls, max_sum, np.copy(triangle)))
    paths.append(steps)
    answers.append(max_sum)

    num = 100 if triangle.size < 99 else triangle.size

    max_sum = num * nlvls

    steps = np.zeros(shape=nlvls, dtype=np.uint8)
    triangle[prev_lvl_nodes] = num

    params.append((nlvls, max_sum, triangle))
    paths.append(steps)
    answers.append(max_sum)

    for rand in (False, True, True):

        triangle = fabricate_data(nlvls, rand)[1]

        steps = np.random.randint(low=0, high=2, size=nlvls, dtype=np.uint8)
        indexes = prev_lvl_nodes + np.add.accumulate(steps)
        triangle[indexes] = num

        params.append((nlvls, max_sum, triangle))
        paths.append(steps)
        answers.append(max_sum)

    triangle = np.zeros(shape=triangle.size, dtype=triangle.dtype)
    triangle[indexes] = 1

    params.append((nlvls, max_sum, triangle))
    paths.append(steps)
    answers.append(nlvls)

    return params, paths, answers


def test_output(fn, nlvls, verbose, *fnargs):
    '''
    Input:

    fn
    -- reference to a function
    -- can take only positional arguments
    -- first three arguments must be: nlvls, max_sum, triangle

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    verbose -- boolean, each individual test case will be printed if True

    fnargs -- additional argument(s) require by tested function


    Returns True if all values returned by the given function are correct,
    False if at least one value is incorrect.
    '''

    case_params, case_paths, case_answers = prep_test_cases(nlvls)

    results = []

    for param, path, answer in zip(case_params, case_paths, case_answers):

        output_total, output_path = fn(*param, *fnargs)

        results.append(np.all(output_path == path) and output_total == answer)

        if verbose:
            print('Expected:', path, answer)
            print('Returned:', output_path, output_total, end='\n\n')

    raport = {
        'func': fn.__name__,
        'ncases': len(results),
        'result': np.all(results)
    }

    template = [
        'Tested function: {func}',
        'Number of test cases: {ncases:d}',
        'Function passed all tests: {result}'
    ]

    # Fill in template
    template = [tmpl.format(**raport) for tmpl in template]

    print('\n'.join(template), end='\n\n')

    return raport['result']


def test_speed(fn, nrep, nlvls, max_sum, triangle, *fnargs):
    '''
    Input:

    fn
    -- reference to a function
    -- can take only positional arguments
    -- first three arguments must be: nlvls, max_sum, triangle

    nrep -- positive integer, number of executions (test iterations)

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    max_sum
    -- positive integer, sum of maximum values in each level (row)
    -- maximum theoretical (not necessarily feasible) sum of path nodes

    triangle -- 1D unsigned integer numpy array, sequence of leaf nodes

    fnargs -- additional argument(s) require by tested function


    Measures the time it takes to execute the given function
    with provided arguments desired number of times.


    This function does not return any value,
    just prints the result to the screen.
    '''

    times = np.zeros(shape=nrep, dtype=np.float64)

    for i in range(nrep):
        times[i] = default_timer()
        fn(nlvls, max_sum, triangle, *fnargs)
        times[i] = default_timer() - times[i]

    raport = {
        'func': fn.__name__,
        'iter': nrep,
        'nlvls': nlvls,
        'min': np.amin(times),
        'max': np.amax(times),
        'sum': np.sum(times),
        'avg': np.mean(times),
        'std': np.std(times),
        'med': np.median(times)
    }

    template = [
        'Tested function: {func}',
        'Number of iterations: {iter:d}',
        'Number of levels: {nlvls:d}',
        'Total time: {sum:10.6f}',
        'Min: {min:10.6f}',
        'Avg: {avg:10.6f}',
        'Max: {max:10.6f}'
    ]

    if 'evolution' in fn.__name__:
        raport['psize'] = fnargs[0]
        raport['ngen'] = fnargs[1]
        template[2:2] = ['Number of generations per iteration: {ngen:d}']
        template[3:3] = ['Number of chromosomes in population: {psize:d}']
    elif len(fnargs) == 1:
        raport['nproc'] = fnargs[0]
        template[2:2] = ['Number of processes: {nproc:d}']

    # Fill in template
    template = [tmpl.format(**raport) for tmpl in template]

    print('\n'.join(template), end='\n\n')
