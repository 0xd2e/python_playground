from math import sqrt, floor, log

import numpy as np

from numba import jit


@jit(nopython=False, cache=True)
def trial_division_method(limit):
    '''
    Inputs:

    limit -- positive integer, required amount of first consecutive prime numbers


    Returns an integer, the sum of all first prime numbers.
    '''

    founded = 6

    if limit < founded:
        return sum((2, 3, 5, 7, 11, 13)[:limit])

    total = sum((2, 3, 5, 7, 11, 13))

    # Initialize candidate to odd number
    candidate = 13

    while founded < limit:

        # Test only odd numbers
        candidate += 2

        for num in range(3, floor(sqrt(candidate)) + 1, 2):
            if candidate % num is 0:
                break
        else:
            total += candidate
            founded += 1

    return total


@jit(nopython=False, cache=True)
def factor_division_method(limit):
    '''
    Inputs:

    limit
    -- integer, required amount of first consecutive prime numbers
    -- must be greater than or equal to 6


    Returns an integer, the sum of all first prime numbers.
    '''

    # Exploit the fact that every composite number has prime factors
    # that are smaller than the number itself. If the numer does not
    # have prime factors, it must be prime.

    # Leave the only even prime number for the end and focus on odd numbers
    limit -= 1

    founded = 5

    primes = np.zeros(shape=limit, dtype=np.uint32)

    primes[:founded] = (3, 5, 7, 11, 13)

    # Initialize candidate to odd number
    candidate = 13

    while founded < limit:

        # Test only odd numbers
        candidate += 2

        maxnum = floor(sqrt(candidate)) + 1

        for num in primes:
            if candidate % num is 0:
                break
            elif num > maxnum:
                primes[founded] = candidate
                founded += 1
                break

    # Now it is time to include numer two
    return np.sum(primes) + 2


@jit(nopython=False, cache=True)
def ambi_sieve(n):
    '''
    Input:

    n
    -- integer, upper bound of a range
    -- must be greater than or equal to 6


    Returns 1D numpy array of integers, all prime numbers
    between 2 (inclusive) and n (exclusive).


    This algorithm is from https://stackoverflow.com/a/2068548
    and is originally written for Python 2.

    Minor changes to the code were made to adjust it to Python 3.
    '''

    sieve = np.arange(3, n, 2, dtype=np.uint32)

    for m in range(3, floor(sqrt(n)) + 1, 2):
        if sieve[(m - 3) // 2]:
            sieve[(m * m - 3) // 2::m] = 0

    return np.r_[2, sieve[sieve > 0]]


@jit(nopython=False, cache=True)
def primesfrom2to(n):
    '''
    Input:

    n
    -- integer, upper bound of a range
    -- must be greater than or equal to 6


    Returns 1D numpy array of integers, all prime numbers
    between 2 (inclusive) and n (exclusive).


    This algorithm is from https://stackoverflow.com/a/2068548
    and is originally written for Python 2.

    Minor changes to the code were made to adjust it to Python 3.
    '''

    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=np.bool)

    for i in range(1, floor(sqrt(n)) + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False

    return np.r_[2, 3, (3 * np.nonzero(sieve)[0][1:] + 1) | 1]


@jit(nopython=True)
def approximate_prime(i, c=0.45):
    '''
    Inputs:

    i
    -- positive integer, i-th prime number
    -- it must be at least 20, when constant is 0.45

    c
    -- float number, constant
    -- must be greater than or equal to 0.0 and less than 1.0 (default is 0.45)
    -- minimum value for argument i depends on this constant


    Returns positive integer, an approximation of the i-th prime number
    that is greater than true i-th prime number.
    '''

    # Makes use of the prime number theorem and the Rosser's
    # theorem to narrow the upper bound.

    a = log(i)

    return floor(i * (a + log(a) - c))
