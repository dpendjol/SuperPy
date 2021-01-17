import csv
from datetime import date

def main():
    file_content = read_file('./sold.csv')
    revenue = get_revenue(file_content, date.fromisoformat('2021-02-03'), 'month')
    print(revenue)
    


def read_file(file_name) -> list:
    with open(file_name, newline='') as f:
        reader = csv.DictReader(f)
        return (list(reader))


def get_revenue(data:list, filter_date:date, period:str='day') -> float:
    '''
    Get the rows of data within a specifiec date
    @param data list of dicts with data
    @filter_date date to filter
    @period does it had to be month, day or year
    @returns a float containing the revenue of the day or a month
    '''
    found_rows = []
    total_revenue = 0
    
    if period == 'month':
        myfilter = filter_date.isoformat()[0:7]
        end = 7
    elif period == 'day':
        myfilter = filter_date.isoformat()
        end = None
    
    for item in data:
        if item['sell_date'][0:end] == myfilter:
            found_rows.append(item)
            
            total_revenue += int(item['count']) * float(item['sell_price'])
    
    return total_revenue
            

if __name__ == "__main__":
    main()