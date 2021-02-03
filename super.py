from supermarket import Supermarket
from cli import get_args
from rich.console import Console
from datetime import timedelta
from dates import get_current_date, shift_date, is_valid_date, set_date, \
                  get_dates_month
from graph import make_bar_chart

mysuper = Supermarket()
myconsole = Console()

stl_error = "bold red on white"
stl_reg = "bold green"

args = get_args()

# Documented
if args.command == 'buy':
    try:
        mydate = is_valid_date(args.expiration_date)
        if mydate <= mysuper.current_date:
            myconsole.print('ERROR: product is already expired',
                            style=stl_error)
            exit()
    except ValueError as e:
        myconsole.print(e, style=stl_error)
    else:
        amount = args.amount if args.amount else 1
        mysuper.buy_product(args.product_name, args.price, amount,
                            args.expiration_date)
        mysuper.write_file(mysuper.bought_file, mysuper.bought)
        myconsole.print('OK', style=stl_reg)

# Documented
if args.command == 'sell':
    try:
        mysuper.sell_product(args.product_name, args.amount, args.price)
    except Exception as e:
        myconsole.print(e, style=stl_error)
    else:
        mysuper.write_file(mysuper.sold_file, mysuper.sold)
        myconsole.print('OK', style=stl_reg)

# Documented
if args.command == 'report' and args.subcommand == 'inventory':
    mydate = get_current_date(mysuper.date_file)
    if args.now:
        pass
    if args.yesterday:
        mydate += timedelta(days=-1)
    if args.date is not None:
        mydate = is_valid_date(args.date)
    mysuper.print_inventory_table(mydate)

# Documented
if args.command == 'report' and args.subcommand == 'revenue':
    report = 0
    if args.today:
        curr_date = get_current_date(mysuper.date_file)
        report = mysuper.get_revenue_sold(curr_date, curr_date)
        myconsole.print(f"Today's revenue so far: {report}", style=stl_reg)
    if args.yesterday:
        asked_date = shift_date(mysuper.date_file, -1)
        report = mysuper.get_revenue_sold(asked_date, asked_date)
        myconsole.print(f"Yesterday's revenue: {report}", style=stl_reg)
    if args.date:
        if len(args.date) == 7:
            first_day, last_day = get_dates_month(args.date)
            report = mysuper.get_revenue_sold(first_day, last_day)
            myconsole.print(f"Revenue from {first_day.strftime('%b %Y')}: \
                {report}", style=stl_reg)
        else:
            try:
                message = is_valid_date(args.date)
            except ValueError as e:
                myconsole.print(e, style="bold red on white")
            else:
                new_date = message
                report = mysuper.get_revenue_sold(new_date, new_date)
                myconsole.print(f"Revenue from {new_date.strftime('%d %b %Y')}: {report}",
                                style=stl_reg)

# Documented
if args.command == "report" and args.subcommand == "expired":
    if args.now:
        mydate = get_current_date(mysuper.date_file)
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
        myconsole.print("Please use a --now or the --nextweek flag, see --help", style=stl_error)

# Documented
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
        myconsole.print("Please use the --yesterday/--yesterday/--date \
              [yyyy-mm-dd] arguments", style=stl_error)
    else:
        # Function get_costs_expired not working correctly yet
        # cost_expired = mysuper.get_costs_expired(date_one, date_one)
        cost_expired = 0
        revenue = mysuper.get_revenue_sold(first_day, last_day)
        # print(revenue, cost_expired, cost_sold)
        myconsole.print(revenue - cost_expired - cost_sold, style=stl_reg)

if args.advance_time:
    if args.advance_time >= 0:
        shifted = shift_date(mysuper.date_file, args.advance_time)
        set_date(mysuper.date_file, shifted)

    if args.advance_time < 0:
        shifted = shift_date(mysuper.date_file, args.advance_time)
        set_date(mysuper.date_file, shifted)

if args.command == "transaction" and args.average_amount:
    '''Plots average transaction revenue per day'''
    dates, average = mysuper.plot_average_transactions()
    make_bar_chart(dates, average, xlabel="date", ylabel="Average (EUR)",
                   title="Average transaction")
