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
        # print_report(self.bought)
        self.id_names = {}
        self.bought_id_quantity = {}
        self.bought_id_costs = {}
        self.sold_id_quantity = {}
        self.sold_id_price = {}
        self.inventory = {}
        self.expired = {}

    ############ DONE
    def read_file(self, file_name) -> list:
        '''
        Reads the csv file and exports its in a dict.
        @returns dict with key id, remaining column values in nested dict
        @param filename in string with relative path
        '''        
        with open(file_name, newline='') as f:
            reader = csv.DictReader(f)
            output = {}
            
            if file_name == Supermarket._BOUGHT:
                for line in reader:
                    output[line['id']] = {
                        'product_name': line['product_name'],
                        'purchase_count': int(line['count']),
                        'purchase_price': float(line['price']),
                        'expiration_date': date.fromisoformat(line['expiration_date']),
                        'purchase_date': date.fromisoformat(line['buy_date'])
                    }
                
            if file_name == Supermarket._SOLD:
                for line in reader:
                    output[line['id']] = {
                        'product_id': line['product_id'],
                        'selling_count': int(line['count']),
                        'selling_price': float(line['sell_price']),
                        'selling_date': date.fromisoformat(line['sell_date'])
                    }
                    
            return output
        
    #Done rewritten
    def get_report_inventory(self, asked_date:str):
        '''
        Display a table which contains every inventory item
        '''
        asked_date = date.fromisoformat(asked_date)
        
        table = Table(show_header=True, title='Inventory report')
        table.add_column('Product Name')
        table.add_column('Amount')
        table.add_column('Bought for')
        table.add_column('Expire on')
        
        inventory = self.get_inventory()
        
        for key, value in inventory.items():
            if not value == 0:
                # Only add roy if the key exists. Work-a-round for when we need a inventory from the past
                try:
                    product = self.bought[key]
                    try:
                        check_date = product['purchase_date']
                    except:
                        check_date = product['selling_date']
                    if check_date <= asked_date:
                        table.add_row(
                            product['product_name'],
                            str(value),
                            str(product['purchase_price']),
                            date.isoformat(check_date)
                        )
                except KeyError:
                    pass
                  
        return table
    
    #Done rewritten
    def get_inventory(self):
        #returns dict {product_id: product_count_in_inventory}
        inventory = {}
        sold_products = self.sold.values()
        sold_product_ids = []
        sold_products_info = {}
        
        for item in sold_products:
            sold_product_ids.append(item['product_id'])
            sold_products_info[item['product_id']] = item['selling_count']
            
        for key, value in self.bought.items():
            if key in sold_product_ids:
                inventory[key] = value['purchase_count'] - sold_products_info[key]
            else:
                inventory[key] = value['purchase_count']
        return inventory
    
    #Done rewritten
    def get_costs_sold(self, start_date='1970-01-01', end_date='2200-12-12'):
        '''
        Get the cost of the sold products
        returns a integer
        '''
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
        
        total_costs = 0
        for key, value in self.sold.items():
            check_date = value['selling_date']
            if start_date <= check_date <= end_date:
                total_costs += (self.bought[value['product_id']]['purchase_price'] * value['selling_count'])
                
        return total_costs

    # Done rewritten
    def get_revenue_sold(self, start_date='1970-01-01', end_date='2022-12-12'):
        '''
        Get the revenue of the sold products
        '''
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
        
        total_revenue = 0
        for key, value in self.sold.items():
            check_date = value['selling_date']
            if start_date <= check_date <= end_date:
                total_revenue += (value['selling_count'] * value['selling_price'])
        return total_revenue

    ##################################
    # Rewritten
    ##################################
    def buy_product(self, product_name, price, amount, expiration_date):
        '''
        Buy a product, but first check if it doesn't exist
        '''
        # Check if there is a product width the same price and experation date
        for key, value in self.bought.items():
            if value['product_name'] == product_name and value['purchase_price'] == price and value['expiration_date'] == expiration_date:
                value['purchase_count'] += amount
                return key
            
        new_id = int(self.get_latest_id('bought')) + 1
        self.bought[new_id] = {
            'product_name': product_name,
            'count': amount,
            'price': price,
            'expiration_date': expiration_date,
            'buy_date': Supermarket._CURR_date
        }
   
        return True

    #Rewritten this function
    def get_product_id(self, product_name):
        '''
        Get the product id when a product name is given
        @returns a list with product id's that have the product_name
        '''
        product_ids = []
        for key, value in self.bought.items():
            if value['product_name'] == product_name:
                product_ids.append(key)
        if len(product_ids) > 0:
            return product_ids
        return 'no key found'

    ##################################
    # Has been rewritten
    ##################################
    def sell_product(self, product_name, amount, price):
        #check if there is enough in inventory
        #check if multiple experation dates are in inventory, in other words. are there multiple product id's in the inventory with the same name
        
        #if spread over multiple experiation date, split the sell-assignments
        
        product_ids = self.get_product_id(product_name)
        
        inventory = self.get_inventory()
        
        #is there enough
        total_amount = 0
        for product_id in product_ids:
            total_amount += inventory[product_id]
        
        if total_amount < amount:
            return 'Not enough in stock'
        
        for product_id in product_ids:
            if inventory[product_id] >= amount:
                new_id = int(self.get_latest_id('sold')) + 1
                self.sold[str(new_id)] = {
                    'product_id': product_id,
                    'selling_count': amount,
                    'selling_date': Supermarket._CURR_date,
                    'selling_price': price
                    }
            elif inventory[product_id] > 0:
                sell_out_amount = inventory[product_id]                
                new_id = int(self.get_latest_id('sold')) + 1
                self.sold[str(new_id)] = {
                    'product_id': product_id,
                    'selling_count': sell_out_amount,
                    'selling_date': Supermarket._CURR_date,
                    'selling_price': price
                    }
                inventory[product_id] = 0
                amount -= sell_out_amount
        return True

    # Did not need to be rewritten
    def get_latest_id(self, infile='sold'):
        '''
        Get the latest id code
        '''
        if infile == 'sold':
            return max(self.sold.keys())
        elif infile == 'bought':
            return max(self.bought.keys())
    

##############################################################################
#Currently working here
    def get_costs_expired(self, start_date='1970-01-01', end_date='2200-01-01'):
        '''
        Get the cost of the expired products
        '''
        total_costs = 0
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
        
        products_bought = self.bought
        # for product in self.bought:
        #     products_bought[product['id']] = [
        #         product['price'],
        #         product['count'],
        #         product['expiration_date']
        #     ]
        
        products_sold = {}
        for key, value in self.sold.items():
            products_sold[value['product_id']] = value['selling_count']
        
        expired = {}
        for key, value in products_bought.items():
            check_date = value['expiration_date']
            
            if key in products_sold.keys():
                products_bought[key][1] = int(products_bought[key][1]) - int(products_sold[key])
            if not products_bought[key][1] == 0 and start_date <= check_date <= end_date:
                expired[key] = value

        return total_costs
                
   
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
               
if __name__ == "__main__":
    pass