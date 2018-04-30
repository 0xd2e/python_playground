from functools import wraps
from timeit import default_timer

import numpy as np

from task2 import factor_division_method, ambi_sieve, primesfrom2to, approximate_prime


def convert_range(fn):
    '''
    This decorator is to adapt a function that creates a sequence
    of prime numbers less than the given number to return the sum
    of the given amount of first consecutive prime numbers.
    '''

    @wraps(fn)
    def wrapper(i):
        return np.sum(fn(approximate_prime(i))[:i])

    return wrapper


def test_output(fn, mini):
    '''
    Input:

    fn -- reference to a function

    mini -- minimum required amount of first consecutive prime numbers


    Checks if the given function returns correct values.

    Conducts 1 test for the smallest argument and 8 random tests
    from a sequence of 86 prime numbers.


    Returns True if all values are correct, False if at least one value
    is incorrect, None if test cannot be run due to too high value
    of mini argument.
    '''

    # Number of random test cases
    num = 8

    # https://en.wikipedia.org/wiki/List_of_prime_numbers#The_first_1000_prime_numbers
    primes = np.fromiter((2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                          59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                          127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
                          191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
                          257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                          331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                          401, 409, 419, 421, 431, 433, 439, 443), dtype=np.uint32)

    if mini >= primes.size - num:
        print('Minimum amount of first consecutive prime numbers is too big for this test')
        return None

    # Do not include the smallest argument in random test
    indexes = np.arange(start=mini+1, stop=primes.size, step=1, dtype=primes.dtype)

    samples = np.random.choice(indexes, size=num, replace=False)

    # Correct values
    answers = np.fromiter([np.sum(primes[:i]) for i in samples], dtype=primes.dtype)

    # Values returned by tested function
    outputs = np.fromiter([fn(i) for i in samples], dtype=primes.dtype)

    raport = {
        'func': fn.__name__,
        'edge': np.sum(primes[:mini]) == fn(mini),
        'rand': np.all(answers == outputs),
        'mini': mini
    }

    template = [
        'Tested function: {func}',
        'Minimum amount of first consecutive prime numbers: {mini:d}',
        'Function returned correct value for the lowest argument: {edge}',
        'Function passed all random tests: {rand}'
    ]

    # Fill in template
    template = [tmpl.format(**raport) for tmpl in template]

    print('\n'.join(template), end='\n\n')

    return raport['edge'] and raport['rand']


def test_speed(fn, repeat, limit=12345):
    '''
    Input:

    fn -- reference to a function

    repeat -- positive integer, number of executions

    limit
    -- positive integer, argument for tested function
    -- required amount of first consecutive prime numbers


    Measures the time it takes to execute the given function
    with provided argument desired number of times.


    This function does not return any value,
    just prints the result to the screen.
    '''

    times = np.zeros(shape=repeat, dtype=np.float64)

    for j in range(repeat):

        t = default_timer()

        fn(limit)

        times[j] = default_timer() - t

    raport = {
        'func': fn.__name__,
        'iter': repeat,
        'lim': limit,
        'min': np.amin(times),
        'avg': np.mean(times),
        'max': np.amax(times),
        'sum': np.sum(times)
    }

    template = [
        'Tested function: {func}',
        'Number of iterations: {iter:d}',
        'Amount of primes: {lim:d}',
        'Total time: {sum:10.6f}',
        'Min: {min:10.6f}',
        'Avg: {avg:10.6f}',
        'Max: {max:10.6f}'
    ]

    # Fill in template
    template = [tmpl.format(**raport) for tmpl in template]

    print('\n'.join(template), end='\n\n')


def compare_methods(fn_list):

    i = 1234567

    for f in fn_list:
        t = default_timer()
        y = f(i)
        t = default_timer() - t
        print('{:d} {:9.6f}  {}'.format(y, t, f.__name__))
    print()


if __name__ == '__main__':

    # Apply decorator
    ambi_sieve = convert_range(ambi_sieve)
    primesfrom2to = convert_range(primesfrom2to)

    # Numba’s JIT compiler warm up
    factor_division_method(20)
    ambi_sieve(20)
    primesfrom2to(20)
    approximate_prime(20)

    functions = (factor_division_method, ambi_sieve, primesfrom2to)

    compare_methods(functions)
