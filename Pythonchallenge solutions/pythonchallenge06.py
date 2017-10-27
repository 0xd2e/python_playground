#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/channel.html


import re
import zipfile

from os import path
from sys import argv

import requests


try:

    url = 'http://www.pythonchallenge.com/pc/def/channel.zip'
    req = requests.get(url, stream=True, timeout=4)

    req.raise_for_status()

    print('Successfully download:', url)

    filename = url[url.rindex('/') + 1:]
    filepath = path.dirname(argv[0])
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
    del url, req, requests, argv


try:

    with zipfile.ZipFile(filepath, 'r') as archive:

        encoding = 'ascii'
        extension = '.txt'

        # Regular expression pattern for finding a number
        regexp = re.compile(r'\b\d+\b')

        files = archive.namelist()
        firstfile = archive.read('readme.txt').decode(encoding)
        firstfile = regexp.search(firstfile).group() + extension

        print()
        print(filename, 'contains', len(files), 'compressed files')
        print()
        print('First file:', firstfile)

        filename = firstfile

        while True:

            if filename in files:
                msg = archive.read(filename).decode(encoding)
                num = regexp.search(msg)
            else:
                break

            if num:
                filename = num.group() + extension
            else:
                break

        print()
        print('Secret message:', msg)
        print()

        filename = firstfile
        comments = []

        del regexp, files, firstfile, msg, re

        while True:

            try:
                comments.append(archive.getinfo(filename).comment.decode(encoding))
                filename = archive.read(filename).decode(encoding).split()[-1]
            except:
                break

            if filename.isdigit():
                filename += extension
            else:
                break

except zipfile.BadZipFile as err:
    print('Invalid zip file:', filepath)

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
    [print(char, sep='', end='') for char in comments]
