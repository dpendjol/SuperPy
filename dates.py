from datetime import date, timedelta

def main():
    pass

def is_valid_date(input_date:str) -> bool:
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
        return (True, date_format)
    except ValueError as e:
        return (False, e)

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
        is_valid, message = is_valid_date(read_date)
        if is_valid == True:
            return message
        else:
            print(message)
            return
        
        
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

def shift_date(file_name:str, num_days:int):
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