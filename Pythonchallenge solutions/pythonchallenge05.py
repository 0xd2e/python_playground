#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/peak.html


import pickle

from os import path

import requests


try:

    url = 'http://www.pythonchallenge.com/pc/def/banner.p'
    req = requests.get(url, stream=True, timeout=4)

    req.raise_for_status()

    print('Successfully download:', url)

    filename = url[url.rindex('/') + 1:]
    filepath = path.dirname(__file__)
    filepath = path.abspath(filepath)
    filepath = path.join(filepath, filename)

    with open(filepath, 'wb') as f:
        f.write(req.content)

    print('File saved:', filepath)

except requests.exceptions.MissingSchema as err:
    print('Wrong URL format:', url)
    print('Probably missing protocol name (e.g. http, ftp)')

except requests.exceptions.Timeout as err:
    print('Cannot download:', url)
    print('Connection timeout')

except (requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError) as err:
    print('Cannot download:', url)
    print('Status code:', req.status_code)

except (IOError, OSError) as err:
    if err.strerror:
        print(err.strerror)
    else:
        print('Cannot save:', filepath)

except BaseException as err:
    print('Unexpected error:', err)

else:
    req.close()


try:

    with open(filepath, 'rb') as f:
        peakhell = pickle.load(f)

except pickle.PickleError as err:
    print('Invalid pickle file:', filepath)

except (IOError, OSError) as err:
    if not path.exists(filename):
        print('File does not exist:', filepath)
    elif err.strerror:
        print(err.strerror)
    else:
        print('Cannot open:', filepath)

except BaseException as err:
    print(err)

else:

    for item in peakhell:
        for thing in item:
            print(thing[0] * thing[1], sep='', end='')
        print()
