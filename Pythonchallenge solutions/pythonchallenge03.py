#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/equality.html


import re

from os import path
from sys import argv

import requests

from bs4 import BeautifulSoup, Comment


try:

    url = 'http://www.pythonchallenge.com/pc/def/equality.html'
    req = requests.get(url, timeout=3)

    req.raise_for_status()

    print('Successfully get:', url)

except requests.exceptions.MissingSchema as err:
    print('Wrong URL format:', url)
    print('Probably missing protocol name (e.g. http, ftp)')

except requests.exceptions.Timeout as err:
    print('Cannot get:', url)
    print('Connection timeout')

except (requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError) as err:
    print('Cannot get:', url)
    print('Status code:', req.status_code)

except BaseException as err:
    print('Unexpected error:', err)

else:
    req.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(req.text, 'html.parser')
    req.close()


try:

    filename = 'letter.txt'
    filepath = path.dirname(argv[0])
    filepath = path.abspath(filepath)
    filepath = path.join(filepath, filename)

    text = soup.find_all(string=lambda txt: isinstance(txt, Comment))[0]
    text = text.strip()

    with open(filepath, 'wt') as f:
        f.write(text)

    print('File saved:', filepath)

except (IOError, OSError) as err:
    if err.strerror:
        print(err.strerror)
    else:
        print('Cannot save:', filepath)

except BaseException as err:
    print('Unexpected error:', err)


# Regular expression pattern for finding a lowercase letter
# surround by exactly three uppercase letters on each side
regexp = re.compile(r'[^A-Z][A-Z]{3}[a-z][A-Z]{3}[^A-Z]')


try:

    ans = []

    with open(filepath, mode='rt', buffering=1) as f:

        [ans.extend(regexp.findall(line)) for line in f]

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

    # Character of interest is in the center of the string that matches the pattern
    middle = len(ans[0]) // 2
    ans = [txt[middle] for txt in ans]

    print('Magic word:', ''.join(ans))
