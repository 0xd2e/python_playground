#!/usr/bin/python3

import numpy as np


NUMBERS = np.arange(1, 51, dtype=np.uint8)


def play_lotto():
    """
    Returns a sorted 1D numpy array with 6 unique integer numbers between 1 and 49.
    """

    return np.sort(np.random.choice(NUMBERS[:49], size=6, replace=False))


def play_eurojackpot():
    """
    Returns a tuple with two sorted 1D numpy arrays:
    first with 5 unique integer numbers between 1 and 50,
    second with 2 unique integer numbers between 1 and 10.
    """

    return (np.sort(np.random.choice(NUMBERS, size=5, replace=False)),
            np.sort(np.random.choice(NUMBERS[:10], size=2, replace=False)))


if __name__ == '__main__':
    np.random.seed()
    np.random.shuffle(NUMBERS)
    [print(('{:4d}' * 6).format(*play_lotto())) for _ in range(3)]
