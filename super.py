from supermarket import Supermarket
from cli import get_args
from supermarket import Supermarket
from rich.console import Console

mysuper = Supermarket()
args = get_args()
print('Arguments', args)

if args.command == 'buy':
    fieldnames = mysuper.buy_product(args.product_name, args.price, args.amount, args.expiration_date)
    mysuper.write_file(mysuper._BOUGHT, fieldnames, mysuper.bought)

if args.command == 'sell':
    fieldnames = mysuper.sell_product(args.product_name, args.amount, args.price)
    mysuper.write_file(mysuper._SOLD, fieldnames, mysuper.sold)

mysuper = Supermarket()
myconsole = Console()

mysuper.sell_product('milk', 60, 2)
    
print('done')

