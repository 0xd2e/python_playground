#!/usr/bin/python3

from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from numpy import dtype, fromiter
from numpy.random import choice, randint, shuffle


CHAR_ENCODING = dtype('U1')
INT_TYPE = dtype('uint8')

SYMBOLS = (
    fromiter(ascii_lowercase, dtype=CHAR_ENCODING),
    fromiter(ascii_uppercase, dtype=CHAR_ENCODING),
    fromiter(digits, dtype=CHAR_ENCODING),
    fromiter(punctuation + ' ', dtype=CHAR_ENCODING)
)


def generate_password():
    """
    Returns random string with lowercase letters,
    uppercase letters, numbers, and special characters.

    String length varies between 27 and 43 characters.
    """

    # Set the number of elements of each type that will be used
    lengths = (
        randint(9, 16, dtype=INT_TYPE),
        randint(9, 16, dtype=INT_TYPE),
        randint(6, 10, dtype=INT_TYPE),
        randint(3, 5, dtype=INT_TYPE)
    )

    # i -- character category
    # j -- individual character

    password = [j for i in range(len(lengths)) for j in choice(
        SYMBOLS[i], size=lengths[i], replace=True)]

    shuffle(password)

    return ''.join(password)


if __name__ == '__main__':
    print(generate_password())
