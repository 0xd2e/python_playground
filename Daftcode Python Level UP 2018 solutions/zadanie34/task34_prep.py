from os import path

import numpy as np


def prepare_data(root_node, levels):
    '''
    Inputs:

    root_node -- integer number

    levels
    -- list with 1D unsigned integer numpy arrays
    -- each array represents a level (row) of a triangle
    -- each array contains leaf nodes


    Returns a dictionary with three 1D unsigned integer numpy arrays:
    -- single_numbers -- contains three elements (root node, number of levels,
       sum of maximum values in each levels);
    -- level_totals -- contains the sum of all nodes for each level (row);
    -- flat_triangle -- sequence of leaf nodes
       arranged from left to right and top to bottom.
    '''

    nlvls = len(levels)

    # Sum of maximum values in each level (row)
    max_sum = np.sum([np.amax(lvl) for lvl in levels])

    single_numbers = np.fromiter((root_node, nlvls, max_sum), dtype=np.uint32)

    # Sum of all nodes for each level (row)
    level_totals = np.fromiter([np.sum(lvl) for lvl in levels], dtype=np.uint32)

    flat_triangle = np.concatenate(levels)

    return {
        'single_numbers': single_numbers,
        'level_totals': level_totals,
        'flat_triangle': flat_triangle
    }


def process_text(src):
    '''
    Inputs:

    src
    -- string, path to a text file (raw data)
    -- node values must be positive integer numbers
    -- nodes must be separated by a single space
    -- each paragraph represents a level (row) of a triangle


    Process data and save result in a compressed binary file with the same
    name as source text file, but with .npz extension, and in the same folder.


    Returns a string with an absolute path to the compressed binary file
    if the file already exists or the given text data is correctly
    processed and saved, empty string otherwise.
    '''

    data = {}

    try:

        assert path.isfile(src) and src.endswith('.txt')

        # Extract file name from file path
        filename = path.split(src)[1]
        filename = path.splitext(filename)[0]

        filename += '.npz'

        tar = path.join(path.split(src)[0], filename)

        if path.isfile(tar):
            print('Data is already prepared:', tar, end='\n\n')
            return tar

        with open(file=src, mode='rt', buffering=1) as f:
            root_node = int(f.readline().strip())
            levels = [np.fromiter(line.split(), dtype=np.uint8) for line in f]

    except (IOError, OSError) as err:
        print('Cannot open:', src)
        print(err.strerror if err.strerror else err)

    except AssertionError:
        print('Expected a path to .txt file, got:', src)

    else:
        data.update(**prepare_data(root_node, levels))

    try:

        assert data, 'No data to save.'

        del data['level_totals']

        with open(file=tar, mode='wb') as f:
            np.savez_compressed(f, **data)

    except (IOError, OSError, AssertionError) as err:
        print('Cannot save:', tar)
        print(err.strerror if err.strerror else err)

    else:
        print('File saved:', tar, end='\n\n')
        return tar

    return ''


def load_data(filepath):
    '''
    Inputs:

    filepath -- string, path to a (compressed) binary file


    Returns a tuple with four elements:
    -- root node value (positive integer);
    -- number of levels (positive integer);
    -- sequence of leaf nodes (1D unsigned integer numpy array);
    -- sum of maximum values in each levels (positive integer).
    '''

    try:

        assert path.isfile(filepath) and filepath.endswith('.npz')

        with np.load(filepath) as data:
            root_node, nlvls, max_sum = data['single_numbers']
            flat_triangle = data['flat_triangle']

    except (IOError, OSError) as err:
        print('Cannot open:', filepath)
        print(err.strerror if err.strerror else err)

    except AssertionError:
        print('Expected a path to .npz file, got:', filepath)

    else:
        nlvls = int(nlvls)
        return root_node, nlvls, flat_triangle, max_sum
