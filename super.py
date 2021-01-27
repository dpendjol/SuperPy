from supermarket import Supermarket
from cli import get_args
from supermarket import Supermarket
from rich.console import Console
from datetime import date, timedelta
from dates import get_current_date, shift_date, is_valid_date, set_date

bought_file = 'bought.csv'
sold_file = 'sold.csv'

mysuper = Supermarket('bought.csv', 'sold.csv')
myconsole = Console()

date_file = 'date.txt'

args = get_args()

myconsole.print('#' * 50)
myconsole.print('# Arguments', args)
myconsole.print('#' * 50)

if args.command == 'buy':
    check, message = is_valid_date(args.expiration_date)
    if check:
        mysuper.buy_product(args.product_name, args.price, args.amount, args.expiration_date)
        mysuper.write_file(bought_file, mysuper.bought)
    else:
        print(message)

if args.command == 'sell':
    mysuper.sell_product(args.product_name, args.amount, args.price)
    mysuper.write_file(sold_file, mysuper.sold)

if args.command == 'report' and args.subcommand == 'inventory':
    mydate = get_current_date(date_file)
    if args.yesterday:
        mydate += timedelta(days=-1)
    if args.date is not None:
        check, message = is_valid_date(args.date)
        if check:
            mydate = message
        else:
            print(message)
    print(mydate)
    mysuper.get_report_inventory(mydate)
    
if args.command == 'report' and args.subcommand == 'revenue':
    report = 0
    if args.today:
        curr_date = get_current_date(date_file)
        report = mysuper.get_revenue_sold(curr_date, curr_date)
        print("Today's revenue so far: ", report)
    if args.yesterday:
        asked_date = shift_date(date_file, -1)
        print(asked_date)
        report = mysuper.get_revenue_sold(asked_date, asked_date)
        print("Yesterday's revenue: ", report)
    if args.date:
        if len(args.date) == 7:
            year = int(args.date.split("-")[0])
            month = int(args.date.split("-")[1])
            max_days = (date(year, month + 1, 1) - date(year, month, 1)).days
            check, first_day = is_valid_date(args.date + "-01")
            check, last_day = is_valid_date(args.date + "-" + str(max_days))
            report = mysuper.get_revenue_sold(first_day, last_day)
            print('Revenue from', args.date, report)
        else:   
            check, message = is_valid_date(args.date)
            if check:
                new_date = message
                report = mysuper.get_revenue_sold(new_date, new_date)
                print('Revenue from ', new_date, report)
            else:
                print(message)
    
if args.command == "report" and args.subcommand == "profit":
    print('calculated profit')
    curr_date = get_current_date(date_file)
    if args.today:
        date_one = curr_date
        cost_sold = mysuper.get_costs_sold(date_one, date_one)
        cost_expired = mysuper.get_costs_expired(date_one, date_one)
        revenue = mysuper.get_revenue_sold(date_one, date_one)
        print(revenue, cost_expired,cost_sold)
        print(revenue - cost_expired - cost_sold)
    
if args.advance_time:
    shifted = shift_date(date_file, args.advance_time)
    set_date(date_file, shifted)

print('done')
