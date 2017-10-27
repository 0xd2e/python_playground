#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/ocr.html


from collections import Counter
from os import path
from sys import argv

import requests

from bs4 import BeautifulSoup, Comment


try:

    url = 'http://www.pythonchallenge.com/pc/def/ocr.html'
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

    filename = 'mess.txt'
    filepath = path.dirname(argv[0])
    filepath = path.abspath(filepath)
    filepath = path.join(filepath, filename)

    text = soup.find_all(string=lambda txt: isinstance(txt, Comment))[1]
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


char_freq = Counter()
rare_chars = []
ans = []


try:

    with open(filepath, mode='rt', buffering=1) as f:

        # Count character occurrences
        [char_freq.update(line) for line in f]

        # Find rare characters
        [rare_chars.append(char[0]) for char in char_freq.items() if char[1] < 50]

        # Set file pointer back to the beginning of the file
        f.seek(0, 0)

        # List rare characters in order of occurrences
        [ans.append(char) for line in f for char in line if char in rare_chars]

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
    print('Magic word:', ''.join(ans))
