#!/usr/bin/python3


from os import path

from requests import get, exceptions


def prepare_file_path(filename, extension, dirpath=''):
    '''
    Inputs:

    filename -- string, file name

    extension
    -- string, file extension
    -- use empty string if extension is included
       in the file name, otherwise must start with a dot

    dirpath
    -- string, directory path
    -- points to the directory where the script is located
       if empty string is given (default) or the given
       directory does not exist (invalid path)
    -- use getcwd function from os library to point to the
       current working directory


    Returns a string representing an absolute path to the file.
    '''

    extension_requirements = (
        extension.startswith('.'),
        not extension.endswith('.'),
        ' ' not in extension
    )

    if all(extension_requirements):
        filename += extension.lower()

    filepath = dirpath if path.isdir(dirpath) else path.dirname(__file__)
    filepath = path.abspath(filepath)
    filepath = path.join(filepath, filename)

    return filepath


def download_file(url, filepath='', binf=True, username='', password=''):
    '''
    Inputs:

    url -- string, link to a file

    filepath
    -- string, download locaion
    -- path to a file or directory
    -- empty string (default) will infer file name from the URL and save
       the file to the directory where the script is located

    binf
    -- boolean, file type indicator
    -- binary file is expected if True (default), text file if False

    username, password
    -- strings, authentication information (credentials)
    -- when authentication is not required, use empty strings (default)


    Returns a string with an absolute path if the file was correctly
    downloaded and saved or the file already exists, empty string otherwise.
    '''

    if path.isdir(filepath) or filepath == '':
        # Extract file name from url
        filename = url[url.rindex('/') + 1:]
        filepath = prepare_file_path(filename, '', filepath)

    if path.isfile(filepath):
        print('\nFile is already saved:', filepath, end='\n\n')
        return filepath

    authinf = (username, password) if username and password else None

    try:

        response = get(url, stream=binf, timeout=3, auth=authinf)

        response.raise_for_status()

        if binf:
            with open(filepath, mode='wb') as f:
                f.write(response.content)

        else:
            with open(filepath, mode='wt', encoding=response.encoding) as f:
                f.write(response.text)

    except exceptions.Timeout:
        print('Cannot get:', url)
        print('Connection timeout')

    except (exceptions.ConnectionError, exceptions.HTTPError) as err:
        print(err)

    except (IOError, OSError) as err:
        print('Cannot save:', filepath)
        print(err.strerror if err.strerror else err)

    else:
        response.close()

        print('\nSuccessfully get:', url)
        print('-- Status code:', response.status_code)
        print('-- Encoding:', response.encoding if not binf else '---')

        print('\nFile saved:', filepath, end='\n\n')

        return filepath

    return ''
