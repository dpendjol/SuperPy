import csv
from datetime import date

class Supermarket:

    _BOUGHT = 'bought.csv'
    _SOLD = 'sold.csv'

    def __init__(self):
        self.bought = self.read_file(Supermarket._BOUGHT)
        self.sold = self.read_file(Supermarket._SOLD)
        self.id_names = {}
        self.bought_id_quantity = {}
        for item in self.bought:
            self.bought_id_quantity[item['id']] = item['product_name']
        print(self.bought_id_quantity)

    def doit(self):
        for item in self.bought:
            self.bought_id_quantity[item.id] = item.name

    def get_inventory(self):
        for item in self.bought:
            pass
        for item in self.sold:
            pass

    def read_file(self, file_name) -> list:
        '''
        Reads the csv file and exports its in a dict.
        Each line becomes a dict in a list
        '''
        with open(file_name, newline='') as f:
            reader = csv.DictReader(f)
            return (list(reader))


    def get_selection(self, data:list, filter_date:date, period:str='day') -> float:
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
                

    def get_numbers(self, data:list):
        total_revenue = 0
        total_costs = 0
        for item in data:
            total_costs += get_costs(read_file('bought.csv'), 
                                    item['product_id'],
                                    item['count'])
            total_revenue += int(item['count']) * float(item['sell_price'])
        return {'revenue': total_revenue, 'costs': total_costs}

    def get_costs(self, data:list, product_id:str, number_sold:int):
        for item in data:
            if item['id'] == product_id:
                costs = int(item['count']) * float(item['price'])
        return costs            

supermarkt = Supermarket()
    
if __name__ == "__main__":
    pass