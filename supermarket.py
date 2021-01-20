import csv
from datetime import date
from main import print_report
from rich.console import Console
from rich.table import Table
from reports import print_report

class Supermarket:
    _BOUGHT = 'bought.csv'
    _SOLD = 'sold.csv'
    _CURR_date = date.today()
    
    def __init__(self):
        
        self._BOUGHT = 'bought.csv'
        self._SOLD = 'sold.csv'
        self._CURR_date = date.today()
        
        # Read data from file
        self.bought = self.read_file(Supermarket._BOUGHT)
        self.sold = self.read_file(Supermarket._SOLD)
        print_report(self.bought)
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
            return(list(reader))
            

    def buy_product(self, product_name, price, amount, expiration_date):
        '''
        Buy a product, but first check if it doesn't exist
        '''
        # Check if there is a product width the same price and experation date
        fieldnames = self.bought[0].keys()
        for item in self.bought:
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
        product_id = self.get_product_id(product_name)
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
    
    
    def get_report_inventory(self, asked_date:str):
        '''
        Display a table which contains every inventory item
        '''
        asked_date = date.fromisoformat(asked_date)
        
        products = {}
        
        table = Table(show_header=True, title='Inventory report')
        
        file_content = []
        for row in self.bought:
            try:
                check_date = date.fromisoformat(row['buy_date'])
            except:
                check_date = date.fromisoformat(row['sell_date'])
            if check_date <= asked_date:
                file_content.append(row)
        
        table.add_column('Product Name')
        table.add_column('Amount')
        table.add_column('Bought for')
        table.add_column('Expire on')
        
        for item in file_content:
            products[item['id']] = [
                item['product_name'],
                item['price'],
                item['expiration_date']
            ]

        for key, value in self.inventory.items():
            if not value == 0:
                # Only add roy if the key exists. Work-a-round for when we need a inventory from the past
                try:
                    product = products[key]
                    table.add_row(str(product[0]), str(value), str(product[1]), str(product[2]))
                except KeyError:
                    pass
            
        return table
               
#######################################################################
mysuper = Supermarket()
report = mysuper.get_report_inventory('2020-05-02')
myconsole = Console()
myconsole.print(report)

if __name__ == "__main__":
    pass