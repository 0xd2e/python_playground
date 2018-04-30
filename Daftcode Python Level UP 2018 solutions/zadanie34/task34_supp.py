import numpy as np


def show_short_info(nlvls):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path


    This function does not return any value,
    just prints common information about leaf nodes.
    '''

    nlvls = int(nlvls)

    raport = {
        'nlvls': nlvls,
        'npaths': 1 << nlvls,  # 2 ** nlvls
        'nnodes': (3 + nlvls) * nlvls // 2  # arithmetic series
    }

    raport['ndigits'] = len(str(raport['npaths']))

    # Show only a number of digits if a number of paths is too big
    option = '{npaths:,d}' if raport['ndigits'] < 14 else 'it has {ndigits:,d} digits'

    template = [
        'Number of levels: {nlvls:d}',
        'Number of leaf nodes: {nnodes:,d}',
        'Number of paths: {}'.format(option)
    ]

    # Fill in template
    template = [tmpl.format(**raport) for tmpl in template]

    print('\n'.join(template), end='\n\n')


def count_lvl_nodes(nlvls):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path


    Returns a tuple with two 1D unsigned integer numpy arrays:
    -- total number of leaf nodes in previous levels;
    -- number of leaf nodes in each level.
    '''

    # Number of leaf nodes in each level
    each_lvl_nodes = np.arange(start=2, stop=2+nlvls, step=1, dtype=np.uint32)

    # Number of leaf nodes in previous level
    prev_lvl_nodes = np.arange(start=1, stop=1+nlvls, step=1, dtype=np.uint32)

    # Adjust the first level, the one immediately after the root node
    prev_lvl_nodes[0] = 0

    # Total number of leaf nodes in all previous levels
    prev_lvl_nodes = np.add.accumulate(prev_lvl_nodes, dtype=np.uint32)

    return prev_lvl_nodes, each_lvl_nodes


def calc_lvl_totals(triangle, prev_lvl_nodes, each_lvl_nodes):
    '''
    Inputs:

    triangle -- sequence of leaf nodes

    prev_lvl_nodes -- total number of leaf nodes in previous levels

    each_lvl_nodes -- number of leaf nodes in each level

    ** all inputs are 1D unsigned integer numpy arrays


    Returns 1D unsigned integer numpy array with the sum of all nodes
    for each level (row).
    '''

    lvl_totals = [np.sum(triangle[i:i+j]) for i, j in zip(prev_lvl_nodes, each_lvl_nodes)]

    return np.fromiter(lvl_totals, dtype=np.uint32)


def calc_max_sum(triangle, prev_lvl_nodes, each_lvl_nodes):
    '''
    Inputs:

    triangle -- sequence of leaf nodes

    prev_lvl_nodes -- total number of leaf nodes in previous levels

    each_lvl_nodes -- number of leaf nodes in each level

    ** all inputs are 1D unsigned integer numpy arrays


    Returns an integer, the sum of maximum values in each level (row).
    '''

    lvl_max = [np.amax(triangle[i:i+j]) for i, j in zip(prev_lvl_nodes, each_lvl_nodes)]

    return np.sum(lvl_max, dtype=np.uint32)


def fabricate_data(nlvls, rand=False):
    '''
    Inputs:

    nlvls
    -- positive integer, number of levels
    -- number of binary steps in a single path
    -- number of bits required to represent a single path

    rand
    -- boolean, character of generated data
    -- if True, create sequence of random integers between 10 and 99
    -- if False (default), create sequence of consecutive positive integers
       such that the rightmost node has the highest value in each level
       (the rightmost path has maximum sum of elements)


    Returns a tuple with two elements:
    -- sum of maximum values in each levels (positive integer);
    -- sequence of leaf nodes (1D unsigned integer numpy array)
       arranged from left to right and top to bottom.
    '''

    # Total number of possible paths: 1 << nlvls; 2 ** nlvls

    prev_lvl_nodes, each_lvl_nodes = count_lvl_nodes(nlvls)

    # Total number of leaf nodes
    n = np.sum(each_lvl_nodes)

    if rand:
        flat_triangle = np.random.randint(low=10, high=100, size=n, dtype=np.uint32)
    else:
        flat_triangle = np.arange(start=1, stop=1+n, step=1, dtype=np.uint32)

    max_sum = calc_max_sum(flat_triangle, prev_lvl_nodes, each_lvl_nodes)

    return max_sum, flat_triangle
