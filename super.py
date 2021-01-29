from supermarket import Supermarket
from cli import get_args
from rich.console import Console
from datetime import timedelta, date
from dates import get_current_date, shift_date, is_valid_date, set_date, \
                  get_dates_month

mysuper = Supermarket()
myconsole = Console()

inventory = mysuper.get_inventory(date(2021, 1, 1))
expired_items = mysuper.get_expired_items('2021-01-01', inventory)
mysuper.print_expired_items(expired_items)

mysuper.print_sold_products()

args = get_args()

if args.command == 'buy':
    try:
        mydate = is_valid_date(args.expiration_date)
        if mydate <= mysuper._CURR_date:
            print('ERROR: product is already expired')
            exit()
    except ValueError as e:
        print(e)
    else:
        amount = args.amount if args.amount else 1
        mysuper.buy_product(args.product_name, args.price, amount,
                            args.expiration_date)
        mysuper.write_file(mysuper.bought_file, mysuper.bought)
        print('OK')

if args.command == 'sell':
    try:
        mysuper.sell_product(args.product_name, args.amount, args.price)
    except Exception as e:
        print(e)
    else:
        mysuper.write_file(mysuper.sold_file, mysuper.sold)
        print('OK')

if args.command == 'report' and args.subcommand == 'inventory':
    mydate = get_current_date(mysuper.date_file)
    if args.now:
        pass
    if args.yesterday:
        mydate += timedelta(days=-1)
    if args.date is not None:
        mydate = is_valid_date(args.date)
    mysuper.get_report_inventory(mydate)

if args.command == 'report' and args.subcommand == 'revenue':
    report = 0
    if args.today:
        curr_date = get_current_date(mysuper.date_file)
        report = mysuper.get_revenue_sold(curr_date, curr_date)
        print("Today's revenue so far: ", report)
    if args.yesterday:
        asked_date = shift_date(mysuper.date_filedate_file, -1)
        report = mysuper.get_revenue_sold(asked_date, asked_date)
        print("Yesterday's revenue: ", report)
    if args.date:
        if len(args.date) == 7:
            first_day, last_day = get_dates_month(args.date)
            report = mysuper.get_revenue_sold(first_day, last_day)
            print('Revenue from ' + first_day.strftime("%b %Y") + ":", report)
        else:
            try:
                message = is_valid_date(args.date)
            except ValueError as e:
                print(e)
            else:
                new_date = message
                report = mysuper.get_revenue_sold(new_date, new_date)
                print('Revenue from ' + new_date.strftime("%d %b %Y") + ":",
                      report)

if args.command == "report" and args.subcommand == "expired":
    inventory = mysuper.get_inventory(date(2021, 1, 1))
    expired_items = mysuper.get_expired_items('2021-01-01', inventory)
    mysuper.print_expired_items(expired_items)
    if args.mode == "table":
        pass
    
if args.command == "report" and args.subcommand == "profit":
    curr_date = get_current_date(mysuper.date_file)
    first_day = None
    last_day = None
    try:
        if args.today:
            first_day = curr_date
        if args.yesterday:
            first_day = curr_date + timedelta(days=-1)
        if args.date:
            if len(args.date) == 7:
                first_day, last_day = get_dates_month(args.date)
            else:
                first_day = is_valid_date(args.date)
        if not last_day:
            last_day = first_day
        cost_sold = mysuper.get_costs_sold(first_day, last_day)
    except NameError:
        print("Please use the --yesterday/--yesterday/--date \
              [yyyy-mm-dd] arguments")
    else:
        # Function get_costs_expired not working correctly yet
        # cost_expired = mysuper.get_costs_expired(date_one, date_one)
        cost_expired = 0
        revenue = mysuper.get_revenue_sold(first_day, last_day)
        # print(revenue, cost_expired, cost_sold)
        print(revenue - cost_expired - cost_sold)

if args.advance_time:
    shifted = shift_date(mysuper.date_file, args.advance_time)
    set_date(mysuper.date_file, shifted)
