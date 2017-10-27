#!/usr/bin/python3


from os import path
from sys import argv

import pandas
import requests

from bs4 import BeautifulSoup


URL = 'https://www.freecodecamp.org'


def get_html(username):
    '''
    Inputs:

    username -- string, valid freecodecamp username


    Returns a string, an HTML document with freecodecamp code portfolio
    of the given user.
    '''

    try:

        full_url = '{}/{}'.format(URL, username)

        response = requests.get(full_url, timeout=3)

        response.raise_for_status()

    except requests.exceptions.Timeout as err:
        print('Cannot get:', full_url)
        print('Connection timeout')

    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError) as err:
        print('Cannot get:', full_url)
        print(err)

    except BaseException as err:
        print(err)

    else:
        response.close()

        print('\nSuccessfully get:', full_url)
        print('-- Status code:', response.status_code)
        print('-- Encoding:', response.encoding)

        return response.text


def prepare_dataframe(html):
    '''
    Inputs:

    html -- string, an html document with user's freecodecamp code portfolio


    Returns pandas dataframe containing user's solutions to freecodecamp
    JavaScript programming problems. This dataframe has four columns:
    Algorithms, Completed, Last Updated, Solution links.
    '''

    try:

        soup = BeautifulSoup(html, 'lxml')

        # Required data is in the first table on the page
        table = soup.find('table')

        # This table has five columns, but the last column contains
        # duplicated data (links and titles).

        # Get unique links
        links = table.find_all('a', href=True)[::2]

        # Create absolute links
        links = [URL + link['href'] for link in links]

        df = pandas.read_html(table.encode('utf-8'),
                              flavor='lxml',
                              header=0,
                              skiprows=1)[0]

        df.drop(df.columns.values[-1], axis=1, inplace=True)

        df[df.columns.values[1]] = pandas.to_datetime(df[df.columns.values[1]])
        df[df.columns.values[2]] = pandas.to_datetime(df[df.columns.values[2]])
        df[df.columns.values[3]] = pandas.Series(links)

        # Rename column
        df.columns.values[3] += ' links'

    except (TypeError, NameError, AttributeError, IndexError) as err:
        print('Invalid freecodecamp code portfolio page')

    except BaseException as err:
        print(err)

    else:
        print('\nDataframe: {} rows, {} columns\n'.format(*df.shape))
        print(df.dtypes, df.head(), sep='\n\n', end='\n\n')

        return df


def save_dataframe(df, username, file_type='csv'):
    '''
    Inputs:

    df -- nonempty pandas dataframe

    username -- string, freecodecamp username (or other user identifier)

    file_type -- string (all lowercase), file format (extension)
              -- can be either csv or json, default is csv


    Saves the dataframe in the given format into the directory where
    the script is located.


    This function does not return any value.
    '''

    try:

        assert isinstance(df, pandas.core.frame.DataFrame), \
               'Pandas dataframe is not provided'

        assert not df.empty, 'Cannot save an empty dataframe'

        # Ensure correct file extension
        if file_type not in ('csv', 'json'):
            print('File format must be either csv or json (all lowercase letters)')
            print('-- Changing {} to csv\n'.format(file_type))
            file_type = 'csv'

        file_name = 'freecodecamp_{}_solutions.{}'.format(username, file_type)

        file_path = path.dirname(argv[0])
        file_path = path.abspath(file_path)
        file_path = path.join(file_path, file_name)

        with open(file_path, 'wt') as f:

            if file_type == 'json':
                df.to_json(f, orient='records')
            else:
                df.to_csv(f)

    except (IOError, OSError) as err:
        print('Cannot save:', file_path)

        if err.strerror:
            print(err.strerror)
        else:
            print(err)

    except (AssertionError, BaseException) as err:
        print(err)

    else:
        print('File saved:', file_path, end='\n\n')


if __name__ == '__main__':
    username = 'f171a9a3497c8b'
    solutions = prepare_dataframe(get_html(username))
    save_dataframe(solutions, username)
