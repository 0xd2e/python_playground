import numpy as np

from utils import download_file
from zadanie1.task1 import count_characters
from zadanie2.task2 import primesfrom2to, approximate_prime
from zadanie34.task34_prep import process_text, load_data
from zadanie34.task34_utils import show_short_info
from zadanie34.task34 import simple_bottom_up


def solve_task1():
    '''
    Solution to a task:
    https://github.com/daftcode/python_levelup_2018/tree/master/zadania_rekrutacyjne/Zadanie_1

    This function does not return any value, just prints the answer to the screen.
    '''

    file_url = 'https://github.com/daftcode/python_levelup_2018/raw/master/zadania_rekrutacyjne/Zadanie_1/zadanie_1_words.zip'

    file_path = download_file(file_url, True)

    char_freq = count_characters(file_path)

    if char_freq:

        items = zip(char_freq.keys(), char_freq.values())

        ans = ['{}{:d}'.format(char, freq) for char, freq in items]
        ans = sorted(ans)

        print(''.join(ans), end='\n\n')

    else:
        print('Cannot find the answer', end='\n\n')


def solve_task2():
    '''
    Solution to a task:
    https://github.com/daftcode/python_levelup_2018/tree/master/zadania_rekrutacyjne/Zadanie_2

    This function does not return any value, just prints the answer to the screen.
    '''

    # Numba’s JIT compiler warm up
    primesfrom2to(20)
    approximate_prime(20)

    i = 1234567
    n = approximate_prime(i)

    primes = primesfrom2to(n)

    print('{:,d}-th prime number is {:,d}'.format(i, np.sum(primes[:i])), end='\n\n')


def solve_task3():
    '''
    Solution to a task:
    https://github.com/daftcode/python_levelup_2018/tree/master/zadania_rekrutacyjne/Zadanie_3

    This function does not return any value, just prints the answer to the screen.
    '''

    # Numba’s JIT compiler warm up
    simple_bottom_up(3, np.fromiter('123456789', dtype=np.uint8))

    url = 'https://raw.githubusercontent.com/daftcode/python_levelup_2018/master/zadania_rekrutacyjne/Zadanie_3/zadanie_3_triangle_small.txt'

    filepath = download_file(url, False)

    filepath = process_text(filepath)

    root_node, nlvls, flat_triangle = load_data(filepath)[:3]

    show_short_info(nlvls)

    output = simple_bottom_up(nlvls, flat_triangle)

    print('The highest sum of nodes:', output + root_node, end='\n\n')


def solve_task4():
    '''
    Solution to a task:
    https://github.com/daftcode/python_levelup_2018/tree/master/zadania_rekrutacyjne/Zadanie_4

    This function does not return any value, just prints the answer to the screen.
    '''

    # Numba’s JIT compiler warm up
    simple_bottom_up(3, np.fromiter('123456789', dtype=np.uint8))

    url = 'https://raw.githubusercontent.com/daftcode/python_levelup_2018/master/zadania_rekrutacyjne/Zadanie_4/zadanie_4_triangle_big.txt'

    filepath = download_file(url, False)

    filepath = process_text(filepath)

    root_node, nlvls, flat_triangle = load_data(filepath)[:3]

    show_short_info(nlvls)

    output = simple_bottom_up(nlvls, flat_triangle)

    print('The highest sum of nodes:', output + root_node, end='\n\n')


if __name__ == '__main__':

    solvers = (solve_task1, solve_task2, solve_task3, solve_task4)

    for num, sol in enumerate(solvers):
        print('___ Task {:d} ___'.format(num + 1))
        sol()
