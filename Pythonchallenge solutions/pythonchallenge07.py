#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/oxygen.html


from os import path
from re import findall

from PIL import Image

from supp import download_file


def solve07():

    filepath = download_file(url='http://www.pythonchallenge.com/pc/def/oxygen.png')

    filename = path.split(filepath)[1]

    try:

        with Image.open(filepath, 'r') as img:

            width, height = img.size

            template = (
                '{:<8}: {}'.format('Filename', filename),
                '{:<8}: {}'.format('Format', img.format),
                '{:<8}: {}'.format('Mode', img.mode),
                '{:<8}: {:d} pixels'.format('Width', width),
                '{:<8}: {:d} pixels'.format('Height', height),
                '{:<8}: {:,d} pixels'.format('Size', width * height),
                '{:<8}: {}'.format('Metadata', img.info)
            )

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
        if not path.exists(filepath):
            print('File does not exist:', filepath)
        else:
            print('Cannot open:', filepath)
            print(err.strerror if err.strerror else err)

    else:

        print('\n'.join(template), end='\n\n')

        del template, left, top, right, bottom, img

        ans = [chr(pixels[i]) for i in range(1, width, length)]
        ans = ''.join(ans)
        print('Secret message:', ans)

        ans = findall(r'\d+', ans)
        ans = [chr(int(i)) for i in ans]
        ans = ''.join(ans)
        print('Magic word:', ans)


if __name__ == '__main__':
    solve07()
