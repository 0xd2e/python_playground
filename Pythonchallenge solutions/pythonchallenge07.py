#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/oxygen.html


from os import path
from re import findall
from sys import argv

import requests
from PIL import Image


try:

    url = 'http://www.pythonchallenge.com/pc/def/oxygen.png'
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

    with Image.open(filepath, 'r') as img:

        width, height = img.size

        print()
        print('Filename: ', filename)
        print('Format:   ', img.format)
        print('Size:      {} x {} pixels ({:,d} total)'.format(width, height, width * height))
        print('Mode:     ', img.mode)
        print('Metadata: ', img.info)
        print()

        # This values were checked manually in an image editor
        left, top, right, bottom = 0, 43, 608, 52
        length = 7

        width = right - left
        height = bottom - top

        # Keep only the gray rectangles
        pixels = img.crop((left, top, right, bottom)).getdata()

        # Keep only one color channel
        pixels = [px[0] for px in pixels]

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
    ans = []

    [ans.append(chr(pixels[i])) for i in range(1, width, length)]

    ans = ''.join(ans)
    print('Secret message:', ans)

    ans = findall(r'\d+', ans)
    ans = [chr(int(i)) for i in ans]
    print('Magic word:', "".join(ans))
