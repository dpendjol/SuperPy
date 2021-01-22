from supermarket import Supermarket
from cli import get_args
from supermarket import Supermarket
from rich.console import Console
from datetime import date
from dates import get_current_date, shift_date, is_valid_date

mysuper = Supermarket()
myconsole = Console()

date_file = 'date.txt'

args = get_args()

myconsole.print('#' * 50)
myconsole.print('# Arguments', args)
myconsole.print('#' * 50)

if args.command == 'buy':
    mysuper.buy_product(args.product_name, args.price, args.amount, args.expiration_date)
    mysuper.write_file(mysuper._BOUGHT, mysuper.bought)

if args.command == 'sell':
    mysuper.sell_product(args.product_name, args.amount, args.price)
    mysuper.write_file(mysuper._SOLD, mysuper.sold)

if args.command == 'report' and args.subcommand == 'inventory':
    report = mysuper.get_report_inventory('2020-06-06')
    myconsole.print(report)

if args.command == 'report' and args.subcommand == 'revenue':
    report = 0
    if args.today:
        curr_date = get_current_date(date_file)
        new_date = curr_date.isoformat()
        report = mysuper.get_revenue_sold(new_date, new_date)
        print("Today's revenue so far: ", report)
    if args.yesterday:
        asked_date = shift_date(date_file, -1)
        new_date = asked_date.isoformat()
        report = mysuper.get_revenue_sold(new_date, new_date)
        print("Yesterday's revenue: ", report)
    if args.date:
        if len(args.date) == 7:
            year = int(args.date.split("-")[0])
            month = int(args.date.split("-")[1])
            max_days = (date(year, month + 1, 1) - date(year, month, 1)).days
            report = mysuper.get_revenue_sold(args.date + "-01", args.date + "-" + str(max_days))
            print('Revenue from', args.date, report)
        else:   
            check, message = is_valid_date(args.date)
            if check:
                new_date = message.isoformat()
                report = mysuper.get_revenue_sold(new_date, new_date)
                print('Revenue from ', newdate, report)
            else:
                print(message)
    
if args.command == "report" and args.subcommand == "profit":
    print('calculated profit')
    if args.today:
        curr_date = get_current_date(date_file)
        date_one = curr_date.isoformat()
        cost_sold = mysuper.get_costs_sold(date_one, date_one)
        cost_expired = mysuper.get_costs_expired(date_one, date_one)
        revenue = mysuper.get_revenue_sold(date_one, date_one)
        print(revenue,cost_expired,cost_sold)
        print(revenue - cost_expired - cost_sold)
    
if args.advance_time:
    shift_date(date_file, args.advance_time)

print('done')
