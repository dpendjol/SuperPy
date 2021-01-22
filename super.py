from supermarket import Supermarket
from cli import get_args
from supermarket import Supermarket
from rich.console import Console

mysuper = Supermarket()
myconsole = Console()

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

print('done')
