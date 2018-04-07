#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/return/5808.html

# If needed, use username and password from challenge 8


from os import path

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageOps

from supp import download_file


def solve11():

    filepath = download_file(
        url='http://www.pythonchallenge.com/pc/return/cave.jpg',
        username='huge',
        password='file'
    )

    filename = path.split(filepath)[1]

    try:

        with Image.open(filepath, 'r') as img:

            width, height = img.size

            template = (
                '{:<8}: {}'.format('Filename', filename),
                '{:<8}: {}'.format('Format', img.format),
                '{:<8}: {}'.format('Mode', img.mode),
                '{:<8}: {:,d} pixels'.format('Width', width),
                '{:<8}: {:,d} pixels'.format('Height', height),
                '{:<8}: {:,d} pixels'.format('Size', width * height)
            )

            pixels = np.asarray(img, dtype=np.uint8, order='F')

    except (IOError, OSError) as err:
        if not path.exists(filepath):
            print('File does not exist:', filepath)
        else:
            print('Cannot open:', filepath)
            print(err.strerror if err.strerror else err)

    else:

        print('\n'.join(template), end='\n\n')

        del template, width, height

        plt.ioff()
        plt.figure(num=filename, frameon=False, clear=True)

        plt.imshow(pixels, interpolation=None, filternorm=1)
        plt.show()

        plt.ioff()
        plt.figure(num=filename, frameon=False, clear=True)

        with Image.fromarray(pixels[0::2, 0::2]) as img:
            img.paste(ImageOps.invert(img))
            img.paste(ImageOps.autocontrast(img))
            part = np.asarray(img, dtype=np.uint8, order='F')

        plt.subplot(221)
        plt.axis('off')
        plt.imshow(part)

        plt.subplot(222)
        plt.axis('off')
        plt.imshow(pixels[1::2, 1::2])

        plt.subplot(223)
        plt.axis('off')
        plt.imshow(pixels[0::2, 1::2])

        plt.subplot(224)
        plt.axis('off')
        plt.imshow(pixels[1::2, 0::2])

        plt.show()

    print('Magic word: evil')


if __name__ == '__main__':
    solve11()
