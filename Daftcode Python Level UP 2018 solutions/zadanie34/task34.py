from multiprocessing import Pool
from operator import itemgetter

import numpy as np
from numba import jit

from zadanie34.binary_genetic_algorithm import run
from zadanie34.task34_supp import count_lvl_nodes


# Terms that are used interchangeably: level/row, path/route, triangle/pyramid.
# Each path is a sequence of steps from top (first element) to bottom (last element).
# Each step is a binary decision: 0 for left, 1 for right.
# Each node is an integer number between 10 and 99.


@jit
def fitness(population, triangle, prev_lvl_nodes, max_sum):
    '''
    Inputs:

    population -- 2D boolean numpy array, sequence of chromosomes

    triangle
    -- 1D unsigned integer numpy array, sequence of leaf nodes
       arranged from left to right and top to bottom

    prev_lvl_nodes
    -- 1D unsigned integer numpy array, total number of leaf nodes
       in all previous levels

    max_sum
    -- positive integer, sum of maximum values in each level
    -- maximum theoretical (not necessarily feasible) sum of path nodes


    Returns 1D numpy array of real numbers with a score, between 0 and 1,
    for each chromosome in population.
    '''

    # Translate path (sequence of steps) to indexes of numbers (visited leaf nodes)
    indexes = prev_lvl_nodes + np.add.accumulate(population, axis=1, dtype=prev_lvl_nodes.dtype)

    return np.sum(triangle[indexes], axis=1, dtype=np.float32) / max_sum


@jit(nopython=False, cache=True, parallel=False)
def evolutionary_method(nlvls, max_sum, triangle, psize=100, ngen=101, cprob=0.7, mprob=0.05):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    max_sum
    -- positive integer, sum of maximum values in each level (row)
    -- maximum theoretical (not necessarily feasible) sum of path nodes

    triangle
    -- 1D unsigned integer numpy array, sequence of leaf nodes
       arranged from left to right and top to bottom

    psize
    -- positive integer number (default is 100), must be even
    -- total number of chromosomes in a generation

    ngen
    -- positive integer number (default is 101)
    -- maximum number of generations

    cprob
    -- positive real number (default is 0.7)
    -- crossover (recombination) probability
    -- probability that a pair of chromosomes will exchange
       part of bit sequences

    mprob
    -- positive real number (default is 0.05)
    -- mutation rate
    -- probability that a bit will be inverted


    Returns a tuple with two elements:
    -- the largest sum of leaf nodes (single positive integer number);
    -- optimal path (1D unsigned integer numpy array with ones and zeros).
    '''

    # Total number of nodes in previous levels
    prev_lvl_nodes = count_lvl_nodes(nlvls)[0]

    best_path = run(
        fit_func=fitness,
        crs_prob=cprob,
        mut_prob=mprob,
        chrom_length=nlvls,
        pop_size=psize,
        iterations=ngen,
        fit_args=(triangle, prev_lvl_nodes, max_sum),
        threshold=1.0
    )

    indexes = prev_lvl_nodes + np.add.accumulate(best_path, dtype=prev_lvl_nodes.dtype)

    return np.sum(triangle[indexes]), best_path.astype(np.uint8)


@jit
def brute_force(nlvls, max_sum, triangle, start, stop):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    max_sum
    -- positive integer, sum of maximum values in each level (row)
    -- maximum theoretical (not necessarily feasible) sum of path nodes

    triangle
    -- 1D unsigned integer numpy array, sequence of leaf nodes
       arranged from left to right and top to bottom

    start
    -- non-negative integer, lower bound for paths
    -- start of interval is inclusive

    stop
    -- postive integer, upper bound for paths
    -- end of interval is exclusive


    Returns a tuple with two elements:
    -- the largest sum of leaf nodes (single positive integer number);
    -- optimal path (1D unsigned integer numpy array with ones and zeros).
    '''

    assert start < stop

    # Total number of nodes in previous levels
    prev_lvl_nodes = count_lvl_nodes(nlvls)[0]

    # Template for converting an integer to a binary string
    template = '{:0{:d}b}'

    grand_total = 0
    best_path = np.zeros(shape=nlvls, dtype=np.uint8)

    for num in range(start, stop):

        # Convert number to steps made in current path
        steps = np.fromiter(template.format(num, nlvls), dtype=best_path.dtype)

        # Translate steps to indexes of numbers (visited leaf nodes)
        indexes = prev_lvl_nodes + np.add.accumulate(steps)

        total = np.sum(triangle[indexes])

        if grand_total < total:
            grand_total = total
            best_path = steps

            if grand_total == max_sum:
                break

    return grand_total, best_path


def parallel_brute_force(nlvls, max_sum, triangle, nproc):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    max_sum
    -- positive integer, sum of maximum values in each level (row)
    -- maximum theoretical (not necessarily feasible) sum of path nodes

    triangle
    -- 1D unsigned integer numpy array, sequence of leaf nodes
       arranged from left to right and top to bottom

    nproc -- positive integer, number of worker processes


    Returns a tuple with two elements:
    -- the largest sum of leaf nodes (single positive integer number);
    -- optimal path (1D unsigned integer numpy array with ones and zeros).
    '''

    # Total number of possible paths
    npaths = 1 << nlvls  # 2 ** nlvls

    limits = np.linspace(start=0, stop=npaths, num=nproc+1, endpoint=True, dtype=np.uint32)

    partitions = zip(limits[:-1], limits[1:])

    argpack = tuple((nlvls, max_sum, triangle, start, stop) for start, stop in partitions)

    with Pool(processes=nproc) as workers:

        results = [workers.apply_async(func=brute_force, args=task) for task in argpack]

        grand_total, best_path = max([res.get() for res in results], key=itemgetter(0))

    return grand_total, best_path


@jit
def bottom_up_method(nlvls, max_sum, triangle):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    max_sum
    -- positive integer, sum of maximum values in each level (row)
    -- maximum theoretical (not necessarily feasible) sum of path nodes
    -- this parameter is present only to preserve compatibility

    triangle
    -- 1D unsigned integer numpy array, sequence of leaf nodes
       arranged from left to right and top to bottom


    Returns a tuple with two elements:
    -- the largest sum of leaf nodes (single positive integer number);
    -- optimal path (1D unsigned integer numpy array with ones and zeros).
    '''

    # Indexes of first element in rows and number of elements in each row
    start, stop = count_lvl_nodes(nlvls)

    # Indexes of the first and last elements in each row, starting from the bottom row
    start = start[::-1]
    stop = stop[::-1] + start

    n = start[0]
    m = stop[0]

    # Initialize totals with nodes from the last row and insure that a range
    # of a data type is enough to handle this values (prevent oveflow)
    totals = triangle[n:m].astype(np.uint32)

    steps = np.empty(shape=m-n, dtype=np.unicode_)

    for n, m in zip(start[1:], stop[1:]):

        left = totals[:-1]
        right = totals[1:]

        side = right > left  # right if True, left if False

        # Choose a route (left or right node) and add it to a node above
        totals = np.where(side, right, left) + triangle[n:m]

        steps = np.core.defchararray.add(
            np.where(side, steps[1:], steps[:-1]),
            side.astype(np.uint8).astype(steps.dtype)
        )

    m = int(totals[1] > totals[0])

    # Steps made in the highest sum path, from top to bottom
    best_path = str(m) + steps[m][::-1]

    return totals[m], np.fromiter(best_path, dtype=np.uint8)


@jit
def simple_bottom_up(nlvls, triangle):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    triangle
    -- 1D unsigned integer numpy array, sequence of leaf nodes
       arranged from left to right and top to bottom


    Returns a positive integer number, the largest sum of leaf nodes.
    '''

    # Indexes of first element in rows and number of elements in each row
    start, stop = count_lvl_nodes(nlvls)

    # Indexes of the first and last elements in each row, starting from the bottom row
    start = start[::-1]
    stop = stop[::-1] + start

    n = start[0]
    m = stop[0]

    # Initialize totals with nodes from the last row and insure that a range
    # of a data type is enough to handle this values (prevent oveflow)
    lvl = triangle[n:m].astype(np.uint32)

    for n, m in zip(start[1:], stop[1:]):

        # Choose a route (left or right node) and add it to a node above
        lvl = np.fmax(lvl[:-1], lvl[1:]) + triangle[n:m]

    return np.amax(lvl)
