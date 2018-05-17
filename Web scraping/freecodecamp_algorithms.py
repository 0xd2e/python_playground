#!/usr/bin/python3


from os import path

import pandas

from requests import get, exceptions
from bs4 import BeautifulSoup


_URL = 'https://www.freecodecamp.org'


def get_html(username):
    '''
    Inputs:

    username -- string, valid freecodecamp username


    Returns a string, an HTML document with freecodecamp
    code portfolio of the given user.
    '''

    try:

        url = '{}/{}'.format(_URL, username)

        response = get(url, timeout=3)

        response.raise_for_status()

    except exceptions.Timeout as err:
        print('Cannot get:', url)
        print('Connection timeout', end='\n\n')

    except (exceptions.ConnectionError, exceptions.HTTPError) as err:
        print(err, end='\n\n')

    else:
        response.close()

        print('\nSuccessfully get:', url)
        print('-- Status code:', response.status_code)
        print('-- Encoding:', response.encoding, end='\n\n')

        return response.text


def prepare_dataframe(html):
    '''
    Inputs:

    html -- string, an html document with user's freecodecamp code portfolio


    Returns pandas dataframe that contain information about user's solutions
    to freecodecamp JavaScript programming problems. This dataframe has
    three columns: Algorithms, Completed, Last Updated.
    '''

    try:

        soup = BeautifulSoup(html, 'lxml')

        # Required data is in the first table on the page
        table = soup.find('table')

        df = pandas.read_html(
            table.encode('utf-8'),
            flavor='lxml',
            header=0,
            skiprows=1
        )[0]

        # Last two columns contain solutions source code
        df.drop(columns=df.columns.values[-2:], inplace=True)

        df[df.columns.values[1]] = pandas.to_datetime(df[df.columns.values[1]])
        df[df.columns.values[2]] = pandas.to_datetime(df[df.columns.values[2]])

    except (TypeError, NameError, AttributeError, IndexError):
        print('Invalid freecodecamp code portfolio page', end='\n\n')

    else:
        print('\nDataframe contains {} rows and {} columns\n'.format(*df.shape))
        print(df.dtypes, df.head(), sep='\n\n', end='\n\n')

        return df


def save_dataframe(df, username, dir_path='', json_format=False):
    '''
    Inputs:

    df -- nonempty pandas dataframe

    username
    -- string, freecodecamp username or other user identifier

    dir_path
    -- string, path to a directory where data will be saved
    -- if an empty string is given (default) or the path is invalid,
       file will be saved to the directory where the script is located

    json_format
    -- boolean, file format
    -- save data as JSON if True, as CSV if False (default)


    This function does not return any value,
    just saves the dataframe to a local drive.
    '''

    try:

        assert isinstance(df, pandas.core.frame.DataFrame), \
               'Pandas dataframe is not provided'

        assert not df.empty, 'Cannot save an empty dataframe'

        file_type = 'json' if json_format else 'csv'

        file_name = 'freecodecamp_{}_solutions.{}'.format(username, file_type)

        if not path.isdir(dir_path):
            dir_path = path.dirname(__file__)

        file_path = path.abspath(dir_path)
        file_path = path.join(file_path, file_name)

        with open(file_path, 'wt') as f:

            if json_format:
                df.to_json(f, orient='records')
            else:
                df.to_csv(f)

    except (IOError, OSError) as err:
        print('Cannot save:', file_path)
        print(err.strerror if err.strerror else err, end='\n\n')

    except AssertionError as err:
        print(err, end='\n\n')

    else:
        print('\nFile saved:', file_path, end='\n\n')


if __name__ == '__main__':
    user = 'f171a9a3497c8b'
    solutions = prepare_dataframe(get_html(user))
    save_dataframe(solutions, user)
