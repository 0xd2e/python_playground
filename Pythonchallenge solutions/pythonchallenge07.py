#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/oxygen.html


from os import path
from re import findall

from PIL import Image

from utils import download_file


def solve07():

    filepath = download_file(url='http://www.pythonchallenge.com/pc/def/oxygen.png', binf=True)

    filename = path.basename(filepath)

    try:

        if not path.exists(filepath):
            raise IOError('File does not exist')

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
            nums = [px[0] for px in pixels]

            # Keep only one number for each rectangle
            nums = nums[1:width:length]

    except (IOError, OSError) as err:
        print('Cannot open:', filepath if filepath else '[not downloaded]')
        print(err.strerror if err.strerror else err)

    else:

        print('\n'.join(template), end='\n\n')

        del template, left, top, right, bottom, length, width, height, pixels, img

        text_parts = [chr(n) for n in nums]
        ans = ''.join(text_parts)
        print('Secret message:', ans)

        text_parts = findall(r'\d+', ans)
        text_parts = [chr(int(i)) for i in text_parts]
        ans = ''.join(text_parts)
        print('Magic word:', ans)


if __name__ == '__main__':
    solve07()
