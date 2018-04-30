from collections import Counter
from os import path
from string import ascii_lowercase
from zipfile import ZipFile, BadZipFile


def count_characters(filepath):
    '''
    Inputs:

    filepath -- string, path to a zip file with (ascii) text files


    Counts total occurences of ascii characters in compressed text files.


    Returns a dictionary with ascii characters stored as keys
    and corresponding counts stored as values.
    '''

    char_freq = Counter()

    encoding = 'ascii'

    try:

        assert filepath.endswith('.zip')

        filename = path.split(filepath)[1]

        with ZipFile(filepath, 'r') as archive:

            files = archive.namelist()

            print(filename, 'contains', len(files), 'compressed files', end='\n\n')

            for f in files:
                msg = archive.read(f).decode(encoding).lower()
                char_freq.update(msg)

    except BadZipFile:
        print('Invalid zip file:', filepath)

    except (IOError, OSError) as err:
        if not path.exists(filepath):
            print('File does not exist:', filepath)
        else:
            print('Cannot open:', filepath)
            print(err.strerror if err.strerror else err)

    except AssertionError:
        print('Expected a path to a .zip file, got:', filepath)

    items = zip(char_freq.keys(), char_freq.values())

    return {char: freq for char, freq in items if char in ascii_lowercase}
