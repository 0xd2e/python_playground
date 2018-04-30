import numpy as np

from task2 import primesfrom2to, approximate_prime


def find_min_i(range_lim, const):
    '''
    Input:

    range_lim
    -- integer, upper bound of a range
    -- must be greater than or equal to 6

    const
    -- float number, constant
    -- must be greater than or equal to 0.0 and less than 1.0


    Returns the smallest integer mini that can be used as argument to
    primesfrom2to(approximate_prime(mini, const))
    so the expression will return correct value.
    '''

    primes = primesfrom2to(range_lim)
    approx = np.fromiter([approximate_prime(i, const) for i in range(1, 1 + primes.size)], dtype=np.uint64)

    mini = 0

    for i in range(6, primes.size):
        if np.all(approx[i:] > primes[i:]) and len(primesfrom2to(approximate_prime(i, const))) >= i:
            mini = i
            break

    print('Minimum amount of prime numbers (for constant {:.2f}): {:d}'.format(const, mini), end='\n\n')

    return mini


if __name__ == '__main__':

    # Numba’s JIT compiler warm up
    primesfrom2to(20)
    approximate_prime(20)

    find_min_i(654321, 0.45)
