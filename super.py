import sys
from supermarket import Supermarket
from os import path
from cli import get_args
from rich.console import Console
from datetime import timedelta, date
from graph import make_bar_chart
from mydate import ShopDate

# Create a console for rich printing
myconsole = Console()
datefile = path.join('data', 'date.txt')
mydateobj = ShopDate(datefile)
# Create a Supermarkt
mysuper = Supermarket(data_folder='data',
                      bought_file='bought.csv',
                      sold_file='sold.csv',
                      current_date=mydateobj.today
                      )

stl_error = "bold red on white"
stl_reg = "bold green"

args = get_args()

if args.command == "buy":
    try:
        mydate = mydateobj.convert_str_to_datetime(args.expiration_date)
        if mydate <= mysuper.current_date:
            myconsole.print("ERROR: product is already expired",
                            style=stl_error)
            sys.exit()
    except ValueError as e:
        myconsole.print(e, style=stl_error)
    else:
        amount = args.amount if args.amount else 1
        expiriation_date = mydateobj.convert_str_to_datetime(args.expiration_date)
        print(expiriation_date)
        mysuper.buy_product(args.product_name, args.price, amount,
                            expiriation_date)
        mysuper.write_file(mysuper.bought_file, mysuper.bought)
        myconsole.print("OK", style=stl_reg)

if args.command == "sell":
    try:
        mysuper.sell_product(args.product_name, args.amount, args.price)
    except Exception as e:
        myconsole.print(e, style=stl_error)
    else:
        mysuper.write_file(mysuper.sold_file, mysuper.sold)
        myconsole.print("OK", style=stl_reg)

if args.command == "report" and args.subcommand == "inventory":
    mydate = mydateobj.today
    if args.now:
        pass
    if args.yesterday:
        mydate = mydateobj.yesterday
    if args.date is not None:
        mydate = mydateobj.convert_str_to_datetime(args.date)
    mysuper.print_inventory_table(mydate)

if args.command == "report" and args.subcommand == "revenue":
    report = 0
    if args.today:
        curr_date = mydateobj.today
        report = mysuper.get_revenue_sold(curr_date, curr_date)
        myconsole.print(f"Today's revenue so far: {report}", style=stl_reg)
    if args.yesterday:
        asked_date = mydate.yesterday
        report = mysuper.get_revenue_sold(asked_date, asked_date)
        myconsole.print(f"Yesterday's revenue: {report}", style=stl_reg)
    if args.date:
        first_day, last_day = mydateobj.get_range_month(args.date)
        report = mysuper.get_revenue_sold(first_day, last_day)
        myconsole.print(f"Revenue from {first_day.strftime('%b %Y')}: "
            f"{report}", style=stl_reg)

if args.command == "report" and args.subcommand == "expired":
    if args.now:
        mydate = mydateobj.today
        inventory = mysuper.get_inventory(mydate)
        expired_items = mysuper.get_expired_items(mydate, inventory,
                                                  to_expire=False)
    if args.nextweek:
        mydate = mydate + timedelta(days=7)
        inventory = mysuper.get_inventory(mydate)
        expired_items = mysuper.get_expired_items(mydate, inventory,
                                                  to_expire=True)
    try:
        mysuper.print_expired_table(expired_items)
    except NameError:
        myconsole.print(("Please use a --now or the --nextweek flag, see "
                         "--help"), style=stl_error)

if args.command == "report" and args.subcommand == "overview":
    mydate = mydateobj.today
    if args.now:
        pass
    if args.yesterday:
        mydate += timedelta(days=-1)
    if args.date:
        mydate = mydateobj.convert_str_to_datetime(args.date)
    mysuper.print_selling_overview(mydate, mydate)

if args.command == "report" and args.subcommand == "profit":
    curr_date = mydateobj.today
    first_day = None
    last_day = None
    try:
        if args.today:
            first_day = curr_date
        if args.yesterday:
            first_day = curr_date + timedelta(days=-1)
        if args.date:
            if len(args.date) == 7:
                first_day, last_day = mydateobj.get_range_month(args.date)
            else:
                first_day = mydateobj.convert_str_to_datetime(args.date)
        if not last_day:
            last_day = first_day
        cost_sold = mysuper.get_costs_sold(first_day, last_day)
    except NameError:
        myconsole.print(("Please use the --yesterday/--yesterday/--date "
                        "[yyyy-mm-dd] arguments"), style=stl_error)
    else:
        cost_expired = 0
        revenue = mysuper.get_revenue_sold(first_day, last_day)
        myconsole.print(revenue - cost_expired - cost_sold, style=stl_reg)

if args.advance_time:
    if args.advance_time >= 0:
        shifted = mydateobj.shift(args.advance_time)

    if args.advance_time < 0:
        shifted = mydateobj.shift(args.advance_time)

# Setting the date variables for the transactions reports
try:
    if args.all:
        day = date(2021, 1, 1)
        last_day = mysuper.current_date + timedelta(days=1)
    if args.current_month:
        day, last_day = mydateobj.current_month_range()
    if args.current_year:
        day = date(mysuper.current_date.year, 1, 1)
        last_day = date(mysuper.current_date.year, 12, 31)
    if args.previous_month:
        curr_year = mysuper.current_date.year
        curr_month = mysuper.current_date.month
        prev_month = curr_month - 1
        if prev_month < 1:
            prev_month = 12
            curr_year -= 1
        prevdate = date(curr_year, prev_month, 1)
        day, last_day = mydateobj.get_range_month(prevdate.strftime("%Y-%m"))
    if args.previous_year:
        prev_year = mysuper.current_date.year - 1
        day = date(prev_year, 1, 1)
        last_day = date(prev_year, 12, 31)
except AttributeError:
    pass

if args.command == "transaction" and args.average_amount:
    '''Plots average transaction revenue per day'''
    daystr = day.strftime("%B %d, %Y")
    last_daystr = last_day.strftime("%B %d, %Y")
    dates, average = mysuper.plot_average_transactions(day, last_day)
    number_of_not_zero = [x for x in average if x > 0]
    if len(number_of_not_zero) < 1:
        myconsole.print("No data found", style=stl_error)
        sys.exit()
    make_bar_chart(dates, average, xlabel="Date", ylabel="Average (EUR)",
                   title=("Average amount spend per transaction per day \n"
                          "{} - {}").format(daystr, last_daystr))

if args.command == "transaction" and args.number_of_transactions:
    dates, average = mysuper.plot_number_of_transactions(day, last_day)
    daystr = day.strftime("%B %d, %Y")
    last_daystr = last_day.strftime("%b %d, %Y")
    number_of_not_zero = [x for x in average if x > 0]
    if len(number_of_not_zero) < 1:
        myconsole.print("No data found", style=stl_error)
        sys.exit()
    make_bar_chart(dates, average, xlabel="date", ylabel="Transactions",
                   title=("Average number of transactions per day \n"
                          "{} - {}").format(daystr, last_daystr))
