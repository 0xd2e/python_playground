#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/ocr.html


from collections import Counter
from os import path
from sys import argv

from requests import get, exceptions
from bs4 import BeautifulSoup, Comment


try:

    url = 'http://www.pythonchallenge.com/pc/def/ocr.html'
    req = get(url, timeout=3)

    req.raise_for_status()

    print('Successfully get:', url)

except exceptions.Timeout:
    print('Cannot get:', url)
    print('Connection timeout')

except (exceptions.ConnectionError, exceptions.HTTPError) as err:
    print(err)

except BaseException as err:
    print('Unexpected error:', err)

else:
    req.close()
    req.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(req.text, 'html.parser')


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
    print('Cannot save:', filepath)
    print(err.strerror if err.strerror else err)

except BaseException as err:
    print('Unexpected error:', err)


char_freq = Counter()


try:

    with open(filepath, mode='rt', buffering=1) as f:

        # Count character occurrences
        [char_freq.update(line) for line in f]  # pylint: disable=W0106

        # Find rare characters
        rare_chars = ''.join(char for char, freq in char_freq.items() if freq < 10)

        # Set file pointer back to the beginning of the file
        f.seek(0, 0)

        # List rare characters in order of occurrences
        ans = ''.join(char for line in f for char in line if char in rare_chars)

except (IOError, OSError) as err:
    if not path.exists(filename):
        print('File does not exist:', filepath)
    else:
        print('Cannot save:', filepath)
        print(err.strerror if err.strerror else err)

except BaseException as err:
    print('Unexpected error:', err)

else:
    print('Magic word:', ans)
