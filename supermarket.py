
import csv
from datetime import datetime, timedelta
from rich.table import Table
from rich.console import Console
from os import path, getcwd
from file_check import check_files


class Supermarket:
    '''Create a instance of a supermarket
    Provide 3 files, one for bought products, one for sold products,
    one for a date file
    '''
    
    std_datestrformat = "%Y-%m-%d"

    def __init__(self, data_folder, bought_file, sold_file, current_date):

        working_directory = getcwd()

        # Check if the nessesary files exist, if not, then create them
        check_files(working_directory, data_folder,
                    sold=sold_file, bought=bought_file)

        self.current_date = current_date

        self.bought_file = path.join(data_folder, bought_file)
        self.sold_file = path.join(data_folder, sold_file)

        self.bought = self.read_file(self.bought_file)
        self.sold = self.read_file(self.sold_file)

    def read_file(self, file_name):
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
                        'expiration_date': datetime.strptime(
                                                        line['expiration_date'],
                                                        Supermarket.std_datestrformat),
                        'purchase_date': datetime.strptime(
                            line['purchase_date'],
                            Supermarket.std_datestrformat)
                    }

            if file_name == self.sold_file:
                for line in reader:
                    output[line['id']] = {
                        'product_id': line['product_id'],
                        'selling_count': int(line['selling_count']),
                        'selling_price': float(line['selling_price']),
                        'selling_date': datetime.strptime(
                                            line['selling_date'], self.std_dateformat)
                    }

            return output

    def get_inventory(self, first_day: datetime, last_day: datetime):
        '''Get the total inventory

        Arguments:
        first_day -- records from and including this date will be found
        last_day -- record till and including this date will be found

        Returns:
        dict -- dictionary, key = product id, value = amount not sold yet
        '''
        inventory = {}
        sold_products = self.sold.values()
        sold_product_ids = []
        sold_products_info = {}

        for product in sold_products:
            if first_day <= product['selling_date'] <= last_day:
                sold_product_ids.append(product['product_id'])
                try:
                    sold_products_info[product['product_id']] = \
                        sold_products_info[product['product_id']] \
                        + product['selling_count']
                except KeyError:  # when product is not yet in sold_products
                    sold_products_info[product['product_id']] = \
                        product['selling_count']

        for product_id, product_specs in self.bought.items():
            if product_id in sold_product_ids:
                inventory[product_id] = product_specs['purchase_count'] \
                    - sold_products_info[product_id]
            else:
                inventory[product_id] = product_specs['purchase_count']
        return inventory

# Maybe do some work here
    def print_inventory_table(self, asked_date: datetime):
        '''Display a table which contains every inventory item

        Arguments:
        asked_date -- datetime object

        Returns:
        None

        Dependancies:
        rich package -- install trough pip install rich
            Needs rich.table and rich.console
        '''
        table = Table(show_header=True, header_style="bold green",
                      title='Inventory report', title_style="bold blue",
                      title_justify="left")
        table.add_column('Product Name')
        table.add_column('Amount')
        table.add_column('Bought for')
        table.add_column('Expire on')

        inventory = self.get_inventory(datetime(1970, 1, 1),
                                       last_day=asked_date)

        for product_id, amount in inventory.items():
            if not amount == 0 and \
                   asked_date < self.bought[product_id]['expiration_date']:

                # Only add row if the key exists. Work-a-round for when we
                # need a inventory from the past
                try:
                    product = self.bought[product_id]
                    try:
                        check_date = product['purchase_date']
                    except KeyError:
                        check_date = product['selling_date']
                    if check_date <= asked_date:
                        table.add_row(
                            product['product_name'],
                            str(amount),
                            str(product['purchase_price']),
                            product['expiration_date'].strftime(Supermarket.std_datestrformat)
                        )
                except KeyError:
                    pass

        myconsole = Console()
        myconsole.print(table)

        return None

    def get_expired_items(self, asked_date, inventory, to_expire):
        '''Get the experied items

        Arguments:
        asked_date -- # TODO
        inventory -- inventory list from self.get_inventory
        to_expire -- boolean, true for future expire, false for listing 
                     already expired
        
        Returns:
        dict -- {product_id: amount_that_expired}

        '''
        if to_expire:
            start_date = self.current_date
        else:
            start_date = datetime.strptime("1970-01-01",
                                           Supermarket.std_datestrformat)
        product_expired = filter(lambda item: start_date
                                 <= item[1]['expiration_date']
                                 <= asked_date, self.bought.items()
                                 )
        product_expired = dict(product_expired)
        output = {}
        for k, v in inventory.items():
            if k in product_expired.keys():
                output[k] = v

        return output

    def get_expired_costs(self, dict_expired_items):
        '''Get the costs of the items that where expired

        Arguments:
        dict_expired_items -- a dictionary of the expired items

        Returns:
        float -- total costs of the products in the experied items
        '''
        total_costs = 0
        for product_id, amount in dict_expired_items.items():
            total_costs += (self.bought[product_id]['purchase_price'] * amount)
        return total_costs

    def print_expired_table(self, dict_expired_items):
        '''Print a table which list a overview of all expired items

        Arguments:
        dict_expired_items -- return from get_expired_items()

        Returns:
        None
        '''
        total_costs = self.get_expired_costs(dict_expired_items)

        table = Table(show_header=True, header_style="green",
                      show_footer=True, footer_style="bold red on white",
                      title='Expired report', title_style="frame bold blue",
                      title_justify="left")
        table.add_column('Product Name')
        table.add_column('Number of products', justify="right")
        table.add_column('Loss in euro', str(format(total_costs, ".2f")),
                         justify="right")
        table.add_column("Expired on", justify="right")

        for k, v in dict_expired_items.items():
            product_costs = round(self.bought[k]['purchase_price'] * v, 2)
            table.add_row(self.bought[k]['product_name'],
                          str(v),
                          str(format(product_costs, ".2f")),
                          self.bought[k]['expiration_date'].strftime(Supermarket.std_datestrformat))
        myconsole = Console()
        myconsole.print(table)

        return None

    def get_sold_products_by_name(self, first_day,
                                  last_day):
        '''
        Get the sold product items sold between first_day till and including
        last_day

        Arguments:
        first_day -- the selling date from which data has to be taken into
                     account. Date is included in the selection
                     Default is 1st January 1970
        last_day -- the selling date till which data has to be taken into
                    account. Date is included in the selection
                    Default is 1st January 2500

        Return:
        dict -- {productname: {number sold, revenue, costs}}
        '''
        output = {}
        sold = filter(lambda x: first_day <= x[1]['selling_date'] <= last_day,
                      self.sold.items())
        for product in dict(sold).values():
            id = product['product_id']
            product_name = self.bought[id]['product_name']
            product_revenue = product['selling_count'] \
                * product['selling_price']
            product_costs = product['selling_count'] \
                * self.bought[id]['purchase_price']
            try:
                output[product_name]['selling_count'] += \
                    product['selling_count']
                output[product_name]['revenue'] += product_revenue
                output[product_name]['costs'] += product_costs
            except KeyError:
                output[product_name] = {
                                    'selling_count': product['selling_count'],
                                    'revenue': product_revenue,
                                    'costs': product_costs
                                    }
        return output

    def print_selling_overview(self, day: datetime, last_day: datetime):
        '''Print a overview of the sold product. Tabel contains
        the cost, revenue and profit per product and totals.

        Arguments:
        day -- start day of selection period
        last_day -- end day of the selection

        Returns:
        None

        '''
        sold_items = self.get_sold_products_by_name(day, last_day)
        table = Table(show_header=True, header_style="green",
                      show_footer=True, footer_style="bold red on white",
                      title="Overview", title_style="bold blue",
                      title_justify="left")

        total_revenue = 0
        total_costs = 0

        for item in sold_items.values():
            total_revenue += item['revenue']
            total_costs += item['costs']

        total_profit = total_revenue - total_costs

        table.add_column("Product name")
        table.add_column("Producs sold", justify="right")
        table.add_column("Revenue", f"{format(total_revenue, '.2f')}",
                         justify="right")
        table.add_column("Costs", f"{format(total_costs, '.2f')}",
                         justify="right")
        table.add_column("Profit", f"{format(total_profit, '.2f')}",
                         justify="right")

        for product_name, product_specs in sold_items.items():
            table.add_row(product_name,
                          str(product_specs['selling_count']),
                          str(format(product_specs['revenue'], ".2f")),
                          str(format(product_specs['costs'], ".2f")),
                          str(format(product_specs['revenue']
                                     - product_specs['costs'], ".2f"))
                          )
        console = Console()
        console.print(table)

        return None

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
                    amount: int, expiration_date: datetime):
        '''Buy a product

        Arguments:
        product_name -- name of the product bought
        price -- price of the product bought
        amount -- number of products bought
        expiration_date -- string representation of the date yyyy-mm-dd

        Returns:
        tuple -- (boolean, 'OK') on succes
        '''
        # Check if there is a product width the same price and experation date

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
            'purchase_date': self.current_date
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

    def sell_product(self, product_name: str, amount: int, price: float):
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
        inventory = self.get_inventory(datetime(1970, 1, 1),
                                       datetime(2200, 1, 1))

        if product_ids == -1:
            raise Exception('Error: Product not in stock')

        total_amount = 0
        for product_id in product_ids:
            if self.bought[product_id]['expiration_date'] > self.current_date:
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
                        'selling_date': self.current_date,
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
            if self.bought[product_id]['expiration_date'] > self.current_date:
                if inventory[product_id] >= amount:
                    new_id = int(self.get_latest_id('sold')) + 1
                    self.sold[str(new_id)] = {
                        'product_id': product_id,
                        'selling_count': amount,
                        'selling_date': self.current_date,
                        'selling_price': price
                        }
                    break
                elif inventory[product_id] > 0:
                    sell_out_amount = inventory[product_id]
                    new_id = int(self.get_latest_id('sold')) + 1
                    self.sold[str(new_id)] = {
                        'product_id': product_id,
                        'selling_count': sell_out_amount,
                        'selling_date': Supermarket.current_date,
                        'selling_price': price
                        }
                    inventory[product_id] = 0
                    amount -= sell_out_amount
        return True, 'Ok'

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
                    expiration = datetime.strftime(value['expiration_date'],
                                                   Supermarket.std_datestrformat)
                    purchase = datetime.strftime(value['purchase_date'],
                                                 Supermarket.std_datestrformat
                    output = {
                        headers[0]: key,
                        headers[1]: value['product_name'],
                        headers[2]: value['purchase_count'],
                        headers[3]: value['purchase_price'],
                        headers[4]: expiration,
                        headers[5]: purchase
                        }
                    writer.writerow(output)
            if file_name == self.sold_file:
                for key, value in data.items():
                    selling_date = datetime.strftime(value['selling_date'],
                                                    Supermarket.std_datestrformat)
                    output = {
                        headers[0]: key,
                        headers[1]: value['product_id'],
                        headers[2]: value['selling_count'],
                        headers[3]: selling_date,
                        headers[4]: value['selling_price']
                        }
                    writer.writerow(output)
        return True, 'Ok'

# Redundant ?
    def get_monthly_data(self, day, last_day):
        '''returns arrays of data for plotting graphs

        Arguments:
        asked_date -- give a year and a month in the format yyyy-mm

        Returns:
        dict -- {days, costs, revenue, profit}
        '''
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

    def get_transactions_per_day(self, asked_date):
        output = filter(lambda item: item[1]['selling_date'] ==
                        asked_date, self.sold.items())
        return dict(output)

    def get_number_of_transactions_per_day(self, asked_date: str):
        '''Gets the number of transactions per day'''
        output = self.get_transactions_per_day(asked_date)
        number_of_transactions = len(list(output))
        return number_of_transactions

    def get_average_transaction_per_day(self, asked_date):
        output = self.get_transactions_per_day(asked_date)
        total_revenue = 0
        for item in output.values():
            total_revenue += (item['selling_count'] * item['selling_price'])
        try:
            average = total_revenue / len(output)
        except ZeroDivisionError:
            average = 0
        return average

    def plot_average_transactions(self, day, last_day):
        dates = []
        average = []
        while day < last_day:
            dates.append(day.strftime(Supermarket.std_datestrformat))
            average.append(self.get_average_transaction_per_day(day))
            day += timedelta(days=1)
        return dates, average

    def plot_number_of_transactions(self, day, last_day):
        dates = []
        average = []
        while day < last_day:
            dates.append(day.strftime(Supermarket.std_datestrformat))
            average.append(self.get_number_of_transactions_per_day(day))
            day += timedelta(days=1)
        return dates, average


if __name__ == "__main__":
    pass
