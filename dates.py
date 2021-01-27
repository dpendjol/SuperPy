from datetime import date, timedelta


def main():
    pass


def is_valid_date(input_date: str) -> bool:
    '''
    Check if the inputed date is of the proper format
    We expect a format by yyyy-mm-dd

    Keyword arguments:
    datum -- input the datum string

    Returns:
    Tuple -- [0] bool
             [1] When true datetime object
             [1] When false errormessage
    '''
    try:
        date_format = date.fromisoformat(input_date)
        return date_format
    except ValueError as e:
        if "Invalid isoformat string:" in e.args[0]:
            raise ValueError('ERROR: input date as follow yyyy-mm-dd')
        if "month must be in" in e.args[0]:
            raise ValueError('ERROR: ' + e.args[0])
        if "day is out of range" in e.args[0]:
            raise ValueError('ERROR: ' + e.args[0])
        raise ValueError


def get_dates_month(mydate: str):
    '''get first and last day of month'''
    year = int(mydate.split("-")[0])
    month = int(mydate.split("-")[1])
    max_days = (date(year, month + 1, 1) - date(year, month, 1)).days
    first_day = is_valid_date(mydate + "-01")
    last_day = is_valid_date(mydate + "-" + str(max_days))
    return first_day, last_day


def get_current_date(file_name):
    '''
    Get the current date from a file

    Arguments:
    file_name -- relative path to the file containing the date

    Returns:
    datetime object of the date saved in file_name
    '''
    with open(file_name, 'r') as f:
        read_date = f.readline().strip()
        try:
            message = is_valid_date(read_date)
        except ValueError as e:
            print(e)
        return message


def set_date(file_name, datestring):
    '''
    Write date to file.

    Arguments:
    file_name: filename to which the date is written with relative path
    datestring: datetime object

    Returns:
    None
    '''
    with open(file_name, 'w') as f:
        f.write(datestring.isoformat())
    return


def shift_date(file_name: str, num_days: int):
    '''
    Shift the date by number of days, Use minus when turning back time
    Example: two day's ago will be achived bij numdays=-2

    Arguments:
    filename -- filename to which the date is written with relative path
    num_days -- integer to shift the day's

    Returns:
    datetime object of shift day
    '''
    curr_date = get_current_date(file_name)
    new_date = 0
    shift = timedelta(days=num_days)
    new_date = curr_date + shift
    return new_date


if __name__ == "__main__":
    main()
