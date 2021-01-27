
import csv
from datetime import date, timedelta
from dates import get_current_date, get_dates_month
from rich.table import Table
from rich.console import Console


class Supermarket:
    '''Create a instance of a supermarket
    Provide 2 files, one for bought products, one for sold products
    '''
    _CURR_date = get_current_date('date.txt')

    def __init__(self, bought_file: str, sold_file: str):

        self._CURR_date = get_current_date('date.txt')
        self.bought_file = bought_file
        self.sold_file = sold_file

        self.bought = self.read_file(self.bought_file)
        self.sold = self.read_file(self.sold_file)

    def read_file(self, file_name) -> list:
        '''Reads the csv file and exports its in a dictionary.

        Arguments:
        file_name -- name of the file that needs to be read. Path relative to
        main directory.

        Returns:
        dict -- id is the key. remainder of fields are saved in value
        '''
        with open(file_name, newline='') as f:
            reader = csv.DictReader(f)
            output = {}

            if file_name == self.bought_file:
                for line in reader:
                    output[line['id']] = {
                        'product_name': line['product_name'],
                        'purchase_count': int(line['purchase_count']),
                        'purchase_price': float(line['purchase_price']),
                        'expiration_date': date.fromisoformat(
                                                        line['expiration_date']
                                                        ),
                        'purchase_date': date.fromisoformat(
                            line['purchase_date'])
                    }

            if file_name == self.sold_file:
                for line in reader:
                    output[line['id']] = {
                        'product_id': line['product_id'],
                        'selling_count': int(line['selling_count']),
                        'selling_price': float(line['selling_price']),
                        'selling_date': date.fromisoformat(
                            line['selling_date'])
                    }

            return output

    def get_report_inventory(self, asked_date):
        '''Display a table which contains every inventory item

        Arguments:
        asked_date -- datetime object

        Returns:
        None

        Dependancies:
        rich package -- install trough pip install rich
            Needs rich.table and rich.console
        '''
        table = Table(show_header=True, title='Inventory report')
        table.add_column('Product Name')
        table.add_column('Amount')
        table.add_column('Bought for')
        table.add_column('Expire on')

        inventory = self.get_inventory(asked_date)

        for key, value in inventory.items():
            if not value == 0 and \
                   asked_date < self.bought[key]['expiration_date']:

                # Only add roy if the key exists. Work-a-round for when we
                # need a inventory from the past
                try:
                    product = self.bought[key]
                    try:
                        check_date = product['purchase_date']
                    except KeyError:
                        check_date = product['selling_date']
                    if check_date <= asked_date:
                        table.add_row(
                            product['product_name'],
                            str(value),
                            str(product['purchase_price']),
                            date.isoformat(product['expiration_date'])
                        )
                except KeyError:  # if pro
                    pass

        myconsole = Console()
        myconsole.print(table)

        return None

    def get_inventory(self, asked_date=date(2200, 1, 1)):
        '''Get the total inventory

        Arguments:
        None

        Returns:
        dict -- dictionary, key = product id, value = amount not sold yet
        '''
        inventory = {}
        sold_products = self.sold.values()
        sold_product_ids = []
        sold_products_info = {}

        for item in sold_products:
            if item['selling_date'] <= asked_date:
                sold_product_ids.append(item['product_id'])
                try:
                    sold_products_info[item['product_id']] = \
                        sold_products_info[item['product_id']] \
                        + item['selling_count']
                except KeyError:  # when product is not yet in sold_products
                    sold_products_info[item['product_id']] = \
                        item['selling_count']

        for key, value in self.bought.items():
            if key in sold_product_ids:
                inventory[key] = value['purchase_count'] \
                    - sold_products_info[key]
            else:
                inventory[key] = value['purchase_count']

        return inventory

    def get_costs_sold(self, start_date, end_date):
        '''Get the sum of the cost of the sold products

        Arguments:
        start_date -- datetime object with the start of the period
        end_date -- datetime object with the end date of the period
            When needed one specifiek date, start_date as to equal end_date

        Returns:
        int -- Integer containing the sum of the costs
        '''

        total_costs = 0
        for value in self.sold.values():
            check_date = value['selling_date']
            if start_date <= check_date <= end_date:
                total_costs += \
                    self.bought[value['product_id']]['purchase_price'] \
                    * value['selling_count']

        return total_costs

    def get_revenue_sold(self, start_date, end_date):
        '''Get the revenue of the sold products

        Arguments:
        start_date -- datetime object with the start of the period
        end_date -- datetime object with the end date of the period
            When needed one specifiek date, start_date as to equal end_date

        Returns:
        int -- Integer containing the sum of the revenue
        '''
        total_revenue = 0
        for value in self.sold.values():
            check_date = value['selling_date']
            if start_date <= check_date <= end_date:
                total_revenue += (value['selling_count']
                                  * value['selling_price'])
        return total_revenue

    def buy_product(self, product_name: str, price: float,
                    amount: int, expiration_date) -> bool:
        '''Buy a product

        Arguments:
        product_name -- name of the product bought
        price -- price of the product bought
        amount -- number of products bought
        expiration_date -- string representation of the date yyyy-mm-dd

        Returns:
        boolean
        '''
        # Check if there is a product width the same price and experation date

        expiration_date = date.fromisoformat(expiration_date)

        for key, value in self.bought.items():
            if value['product_name'] == product_name and \
               value['purchase_price'] == price and \
               value['expiration_date'] == expiration_date:
                value['purchase_count'] += amount
                return key

        new_id = int(self.get_latest_id('bought')) + 1
        self.bought[new_id] = {
            'product_name': product_name,
            'purchase_count': amount,
            'purchase_price': price,
            'expiration_date': expiration_date,
            'purchase_date': Supermarket._CURR_date
        }

        return True, 'Ok'

    def get_product_id(self, product_name):
        '''Get the product id when a product name is given

        Arguments:
        product_name -- name of the product

        Returns:
        int -- representing product ID if exists, else returns -1
        '''
        product_ids = []
        for key, value in self.bought.items():
            if value['product_name'] == product_name:
                product_ids.append(key)
        if len(product_ids) > 0:
            return product_ids
        return -1

    def sell_product(self, product_name, amount, price):
        '''Selling products

        Arguments:
        product_name -- name of the product
        amount -- amount sold
        price -- price for which it is sold

        Returns:
        boolean, message
            True, 'Ok' on succes
            False, error message on failure
        '''

        product_ids = self.get_product_id(product_name)
        inventory = self.get_inventory()
        # bought_items = {k: v for k, v in sorted(self.bought.items(),
        #                key=lambda item: item[1]['expiration_date'])}

        if product_ids == -1:
            raise Exception('Error: Product not in stock')

        total_amount = 0
        for product_id in product_ids:
            if self.bought[product_id]['expiration_date'] > self._CURR_date:
                total_amount += inventory[product_id]

        if total_amount == 0:
            raise Exception('Error: Product no longer in stock')

        # If the --amount argument is not used
        # we want to sell all the products
        # that equals the --product-name argument
        if amount is None:
            check = None
            while not (check == 'n' or check == 'y'):
                check = input('Do you want to sell all the {}? [y/n] '
                              .format(self.bought[product_id]['product_name']))
                if check == 'n':
                    return
            for product_id in product_ids:
                new_id = int(self.get_latest_id('sold')) + 1
                if inventory[product_id] > 0:
                    self.sold[str(new_id)] = {
                        'product_id': product_id,
                        'selling_count': inventory[product_id],
                        'selling_date': Supermarket._CURR_date,
                        'selling_price': price
                        }
            return True, 'OK, product sold out now'

        if total_amount < amount:
            if total_amount == 0:
                print("All out")
            else:
                print("Sorry, just got " + str(total_amount) + " left")
            return 'Not enough in stock'

        for product_id in product_ids:
            if self.bought[product_id]['expiration_date'] > self._CURR_date:
                if inventory[product_id] >= amount:
                    new_id = int(self.get_latest_id('sold')) + 1
                    self.sold[str(new_id)] = {
                        'product_id': product_id,
                        'selling_count': amount,
                        'selling_date': Supermarket._CURR_date,
                        'selling_price': price
                        }
                    break
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
        return True, 'Ok'

    # Did not need to be rewritten
    def get_latest_id(self, infile='sold'):
        '''Get the latest id

        Arguments:
        infile -- which file needs to be searched for the string

        Returns:
        int -- biggest integer used as key
        '''
        try:
            if infile == 'sold':
                return max(self.sold.keys())
            elif infile == 'bought':
                return max(self.bought.keys())
        except ValueError:
            return 0

    # Not working correctly yet
    def get_costs_expired(self, start_date, end_date):
        '''Get the cost of the expired products

        Arguments:
        start_date -- datetime object with the start of the period
        end_date -- datetime object with the end date of the period
            When needed one specifiek date, start_date as to equal end_date

        Returns:
        int -- Integer containing the sum of the costs of expired products
        '''
        total_costs = 0

        inventory = self.get_inventory()

        for product in inventory.keys():
            if start_date < self.bought[product]['expiration_date'] < end_date:
                total_costs += (inventory[product]
                                * self.bought[product]['purchase_price'])
        return total_costs

    def write_file(self, file_name, data):
        '''Write data to the file, rewrite the whole file for now

        Arguments:
        file_name -- name of the file needs to be written
        data --

        Returns:
        boolean
            True, 'Ok' on succes
            False, error message on failure
        '''

        with open(file_name, 'r') as f:
            headers = f.readline().strip().split(',')

        with open(file_name, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            if file_name == self.bought_file:
                for key, value in data.items():
                    output = {
                        headers[0]: key,
                        headers[1]: value['product_name'],
                        headers[2]: value['purchase_count'],
                        headers[3]: value['purchase_price'],
                        headers[4]: value['expiration_date'],
                        headers[5]: value['purchase_date']
                        }
                    writer.writerow(output)
            if file_name == self.sold_file:
                for key, value in data.items():
                    output = {
                        headers[0]: key,
                        headers[1]: value['product_id'],
                        headers[2]: value['selling_count'],
                        headers[3]: value['selling_date'],
                        headers[4]: value['selling_price']
                        }
                    writer.writerow(output)
        return

    def get_monthly_data(self, asked_date: str):
        '''returns arrays of data for plotting graphs'''
        day, last_day = get_dates_month(asked_date)
        days = []
        costs = []
        revenues = []
        profits = []
        while not day > last_day:
            days.append(day.strftime("%Y-%b-%d"))
            cost = self.get_costs_sold(day, day)
            revenue = self.get_revenue_sold(day, day)
            costs.append(cost)
            revenues.append(revenue)
            profits.append(revenue - cost)
            day = day + timedelta(days=1)
        return {'days': days,
                'costs': costs,
                'revenue': revenues,
                'profit': profits
                }

    def get_revenu_date_month(self, asked_date):
        pass


if __name__ == "__main__":
    pass
