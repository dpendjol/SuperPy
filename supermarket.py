import csv
from datetime import date

class Supermarket:

    _BOUGHT = 'bought.csv'
    _SOLD = 'sold.csv'
    _CURR_date = date.today()
    
    def __init__(self):
        self.bought = self.read_file(Supermarket._BOUGHT)
        self.sold = self.read_file(Supermarket._SOLD)
        self.id_names = {}
        self.bought_id_quantity = {}
        self.bought_id_costs = {}
        self.sold_id_quantity = {}
        self.sold_id_price = {}
        self.inventory = {}
        self.expired = {}
        
        for item in self.bought:
            self.bought_id_quantity[item['id']] = int(item['count'])
            if date.fromisoformat(item['expiration_date']) < Supermarket._CURR_date:
                self.expired[item['id']] = float(item['price'])
            self.bought_id_costs[item['id']] = float(item['price'])

        for item in self.sold:
            self.sold_id_price[item['id']] = float(item['sell_price'])
            try:
                self.sold_id_quantity[item['product_id']] += int(item['count'])
            except KeyError:
                self.sold_id_quantity[item['product_id']] = int(item['count'])
            
        for key, value in self.bought_id_quantity.items():
            try:
                self.inventory[key] = value - self.sold_id_quantity[key]
            except KeyError:
                self.inventory[key] = value
                
        #print('Expired:', self.expired)
        #print('Inventory:', self.inventory)
        #print('Sold:', self.sold_id_quantity)
        #print('Sold-price:', self.sold_id_price)
        #print('Bought-amount:', self.bought_id_quantity)
        #print('Bought-price:', self.bought_id_costs)
        
        #print('Total costs expired:', self._get_costs_expired())
        #print('Total cost sold:', self._get_costs_sold())
        #print('Total revenue:', self._get_revenue_sold())
        #print('Total still in inventory:', self._get_money_in_stock())
        #a = self.get_product_id('apple')
        #print('Number apples present:', self.check_inventory(a))
        
        #print(self.get_latest_id('bought'))
        
        #buy_fieldnames = self.buy_product('Vegetables', 2, 5, '2021-05-12')
        #print('Buy fieldnames:', buy_fieldnames)
        #self.write_file(Supermarket._BOUGHT, buy_fieldnames, self.bought)
        #sell_fieldnames = self.sell_product('Vegetables', 5, 5)
        #print('Sell fieldnames:', sell_fieldnames)
        #self.write_file(Supermarket._SOLD, sell_fieldnames, self.sold)
        

    def _get_costs_expired(self):
        '''
        Get the cost of the expired products
        '''
        total_costs = 0
        for key, value in self.expired.items():
            total_costs += self.inventory[key] * value
        return total_costs
    
    def _get_costs_sold(self):
        '''
        Get the cost of the sold products
        '''
        total_costs = 0
        for key, value in self.sold_id_quantity.items():
            total_costs += self.bought_id_costs[key] * value
        return total_costs
    
    def _get_revenue_sold(self):
        '''
        Get the revenue of the sold products
        '''
        total_revenue = 0
        for key, value in self.sold_id_quantity.items():
            total_revenue += self.sold_id_price[key] * value
        return total_revenue
    
    def _get_money_in_stock(self):
        '''
        Get the money still tied up in stock
        '''
        total_costs_inventory = 0
        for key, value in self.inventory.items():
            total_costs_inventory += self.bought_id_costs[key] * value
        return total_costs_inventory
        
    def get_product_id(self, product_name):
        '''
        Get the product id when a product name is given
        '''
        found_products = []
        for item in self.bought:
            if item['product_name'] == product_name:
                found_products.append(item['id'])
        return found_products
                
    
    def check_inventory(self, products):
        '''
        Check how many of the asked product is in stock
        @products: list of product id codes
        '''
        number_present = 0
        for key, value in self.inventory.items():
            if key in products:
                number_present += value
        return number_present
    
    
    def get_latest_id(self, infile='sold'):
        '''
        Get the latest id code
        '''
        if infile == 'sold':
            return max(self.sold_id_price.keys())
        elif infile == 'bought':
            return max(self.bought_id_costs.keys())
                

    def read_file(self, file_name) -> list:
        '''
        Reads the csv file and exports its in a dict.
        Each line becomes a dict in a list
        '''
        with open(file_name, newline='') as f:
            reader = csv.DictReader(f)
            return (list(reader))

    def buy_product(self, product_name, price, amount, expiration_date):
        '''
        Buy a product, but first check if it doesn't exist
        '''
        # Check if there is a product width the same price and experation date
        fieldnames = self.bought[0].keys()
        for item in self.bought:
            print(item)
            if item['product_name'] == product_name and float(item['price']) == price and item['expiration_date'] == expiration_date:
                item['count'] = int(item['count']) + amount
                return fieldnames
            
        new_id = int(self.get_latest_id('bought')) + 1
        new_row = {'id': new_id,
                    'product_name': product_name,
                    'count': amount,
                    'price': price,
                    'expiration_date': expiration_date
                    }
        self.bought.append(new_row)
        return fieldnames
    
    def sell_product(self, product_name, amount, price):
        fieldnames = self.sold[0].keys()
        #check if there is enough in inventory
        #check if multiple experation dates are in inventory, in other words. are there multiple product id's in the inventory with the same name
        
        #if spread over multiple experiation date, split the sell-assignments
        print('sell product')
        product_id = self.get_product_id(product_name)
        print(self.check_inventory(product_id))
        if amount <= self.check_inventory(product_id):
            print('there is enough')
            new_id = int(self.get_latest_id('sold')) + 1
            new_row = {'id': new_id,
                    'product_id': product_id[0],
                    'count': amount,
                    'sell_date': Supermarket._CURR_date,
                    'sell_price': price
                    }
            self.sold.append(new_row)
        return fieldnames
                
    
    def write_file(self, file_name, fieldnames, data):
      '''
      Write data to the file, rewrite the whole file for now
      '''
        with open(file_name, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for line in data:
                writer.writerow(line)
        return
    
               
########################################################################


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
    
if __name__ == "__main__":
    pass