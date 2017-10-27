#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/linkedlist.php


import re

import requests

from bs4 import BeautifulSoup


try:

    url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php'
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
    soup = BeautifulSoup(req.text, 'lxml')
    req.close()


# Separate core/base URL and numeric parameter from a link like this one
# http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345
param = soup.find('a').get('href')
index = param.index('?')
param = param[index:]
index = param.index('=') + 1
url += param[:index]
param = param[index:]


# Regular expression pattern for finding a number at the end of a string
pattern = re.compile(r'\d+$')


print('Starting link:', url + param)
print('Waiting... [', sep='', end='')


try:

    with requests.Session() as s:

        for index in range(400):

            req = s.get(url + param, timeout=3)

            req.raise_for_status()

            num = pattern.search(req.text)

            if num:

                print('.', sep='', end='', flush=True)
                param = num.group()

            elif param == '16044':

                print('] [', sep='', end='', flush=True)
                param = str(int(param) // 2)

            else:

                print(']')
                break

except requests.exceptions.Timeout as err:
    print('\nCannot get:', url)
    print('Connection timeout')

except (requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError) as err:
    print('\nCannot get:', url)
    print('Status code:', req.status_code)

except BaseException as err:
    print('\nUnexpected error:', err)

else:
    print('Total number of requests:', index + 2)
    print('Magic word:', req.text)
