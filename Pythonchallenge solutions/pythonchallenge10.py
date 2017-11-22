#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/return/bull.html

# If needed, use username and password from challenge 8


from itertools import groupby


def calc_seq_len(n, a):
    '''
    Inputs:
    n -- positive integer, number of the element in the sequence
    a -- string with the natural number, starting element

    Returns the number of characters in the n-th element of look-and-say sequence.

    More info on this sequence: https://en.wikipedia.org/wiki/Look-and-say_sequence
    '''

    if __debug__:
        assert isinstance(n, int)
        assert isinstance(a, str)
        assert n > 0
        assert a.isdigit()

    for _ in range(n):
        a = ''.join('{:d}{}'.format(len(''.join(g)), k) for k, g in groupby(a))

    return len(a)


if __name__ == '__main__':

    # Pattern from http://www.pythonchallenge.com/pc/return/sequence.txt
    # a = [1, 11, 21, 1211, 111221]

    print('Magic word:', calc_seq_len(30, '1'))
