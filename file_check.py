from os import path, makedirs
from csv import DictWriter
from datetime import date


def check_files(cwd, folder, **kwargs):
    '''Check is the nesseary files are there where they are supposed to be,
    if not, then create them

    Arguments:
    cwd -- current working directory
    folder -- folder in which the data
    **kwargs -- pass data=, bought=, sold= and the title of the filename

    Returns:
    None
    '''
    full_path = path.join(cwd, folder)
    dir_exists = path.isdir(full_path)
    if not dir_exists:
        makedirs(full_path)

    try:
        bought_file = kwargs['bought']
        sold_file = kwargs['sold']
    except KeyError as e:
        print(e)
    else:
        boughtfile = path.join(full_path, bought_file)
        bought_file_exists = path.isfile(boughtfile)
        if not bought_file_exists:
            with open(boughtfile, 'w', newline='') as filehandle:
                headers = ['id', 'product_name', 'purchase_count',
                           'purchase_price', 'expiration_date',
                           'purchase_date']
                writer = DictWriter(filehandle, fieldnames=headers)
                writer.writeheader()
        soldfile = path.join(full_path, sold_file)
        sold_file_exists = path.isfile(soldfile)
        if not sold_file_exists:
            with open(soldfile, 'w', newline='') as filehandle:
                headers = ['id', 'product_id', 'selling_count', 'selling_date',
                           'selling_price']
                writer = DictWriter(filehandle, headers)
                writer.writeheader()
    return None
