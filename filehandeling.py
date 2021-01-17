import csv
from datetime import date

def main():
    file_content = read_file('./sold.csv')
    selection = get_selection(file_content, date.fromisoformat('2021-01-03'), 'month')
    revenue = get_numbers(selection)
    print(revenue)    


def read_file(file_name) -> list:
    '''
    Reads the csv file and exports its in a dict.
    Each line becomes a dict in a list
    '''
    with open(file_name, newline='') as f:
        reader = csv.DictReader(f)
        return (list(reader))


def get_selection(data:list, filter_date:date, period:str='day') -> float:
    '''
    Get the rows of data within a specifiec date
    @param data list of dicts with data
    @filter_date date to filter
    @period does it had to be month, day or year
    @returns a float containing the revenue of the day or a month
    '''
    found_rows = []
    
    if period == 'month':
        myfilter = filter_date.isoformat()[0:7]
        end = 7
    elif period == 'day':
        myfilter = filter_date.isoformat()
        end = None
    
    for item in data:
        if item['sell_date'][0:end] == myfilter:
            found_rows.append(item)
    return found_rows
            

def get_numbers(data:list):
    total_revenue = 0
    total_costs = 0
    for item in data:
        total_costs += get_costs(read_file('bought.csv'), 
                                item['bought_id'],
                                item['count'])
        total_revenue += int(item['count']) * float(item['sell_price'])
    return {'revenue': total_revenue, 'costs': total_costs}

def get_costs(data:list, product_id:str, number_sold:int):
    for item in data:
        if item['id'] == product_id:
            costs = int(item['count']) * float(item['price'])
            print(f'Costs of {item["product_name"]}: ', costs)
    return costs            
    
if __name__ == "__main__":
    main()