import argparse
import csv
from datetime import date


def main():
  args = get_args()
  print("Arguments: \n", args, "\n", 20 * r"\_/", "\n")
  


# Getting the correct data from the CLI and calling the function including the arguments belonging to that function from the CLI
def get_args() -> dict:
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest="command")
# Everything that has to do with the report command
  report_parser = subparser.add_parser("report", help="report command")
  report_parser.add_argument("subcommand", choices=["inventory", "revenue", "profit"], help="Choose which report you want to see")
# Choose to create a group, only one of the arguments can be used at one time
  time_group = report_parser.add_mutually_exclusive_group()
  time_group.add_argument("--yesterday", action="store_true", help="get data of yesterday")
  time_group.add_argument("--today", action="store_true", help="get data of today")
  time_group.add_argument("--date", type=str, help="get data of date provided in format yyyy-mm")
# Everything that has to do with the sell command
  sell_parser = subparser.add_parser("sell", help="sell command")
  sell_parser.add_argument("-pn", "--product-name")
  sell_parser.add_argument("-a", "--amount", type=int, help="number of productitems sold")
  sell_parser.add_argument("-p", "--price", type=float, help="provide the price of the product")
# Everything that had to do with the buy command
  buy_parser = subparser.add_parser("buy", help="buy command")
  buy_parser.add_argument("-pn", "--product-name", type=str, help="provide name of the product")
  buy_parser.add_argument("-a", "--amount", type=int, help="how many items dit you bought")
  buy_parser.add_argument("-p", "--price", type=float, help="provide bought price per item")
  buy_parser.add_argument("-ed", "--expiration-date")
  #buy_parser.add_argument("--advance-time", type=int, help="advance time by x day's")

  args = parser.parse_args()

  return args

def select_function(args):
  '''
  Check which command is given and execute the associated functions
  '''
  if args.command == "buy":
    print("calling buy function")
    print(buy(args.product_name, args.amount, args.price, args.expiration_date))
  elif args.command == "report":
    print("calling report function")
  elif args.command == "sell":
    print("calling sell function")
    print(sell(args.product_name, args.price, args.amount))
  else:
    print(f"Sorry, I don't know what to do with the command {args.command}")
  pass

def sell(product_name:str, price:float, amount:int=1, ):
  '''
  Process a sell action from the user

  Args:
    product_name: name of the product sold
    price: price of the product sold

  Returns:
    None
  '''
  #find the key of the product
  product_id = -1
  file_content = read_file("./bought.csv")
  for row in file_content:
    if row[1] == product_name:
      product_id = row[0]
      break
  if product_id == -1:
    print('product not found')
    return
  last_id = find_last_id('./sold.csv')
  today = date.today()
  with open('./sold.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([last_id + 1, product_id, amount, today.isoformat(), price])
  return 'ok'


def find_product_id(product_name:str) -> int:
  pass


def buy(product_name:str, amount:int, price:float, expiration_date:str) -> bool:
  last_id = find_last_id('./bought.csv')
  ### Write info to file
  with open('./bought.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([last_id + 1, product_name, price, expiration_date])
  return True


def find_last_id(file:str):
  last_id = -1 #containing last id used in file
  ### Get last_id used in file
  with open(file, newline='') as f:
    reader = csv.reader(f)
    for row in reversed(list(reader)):
      if last_id == -1:
        try:
          if row[0] == 'id':
            last_id = 0
          else:
            last_id = int(row[0])
        except IndexError:
          last_id = 0
      else:
        break
  return last_id


if __name__ == "__main__":
  main()