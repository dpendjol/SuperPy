import argparse
import csv
from datetime import date
# Getting the correct data from the CLI and calling the function including the arguments belonging to that function from the CLI
def main():
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest="command")

# Everthing that has to do with the report command
  report_parser = subparser.add_parser("report", help="report command")
  report_parser.add_argument("subcommand", choices=["inventory", "revenue", "profit"], help="Choose which report you want to see")
  time_group = report_parser.add_mutually_exclusive_group()
  time_group.add_argument("--yesterday", action="store_true", help="get data of yesterday")
  time_group.add_argument("--today", action="store_true", help="get data of today")
  time_group.add_argument("--date", type=str, help="get data of date provided in format yyyy-mm")

# Everthing that has to do with the sell command
  sell_parser = subparser.add_parser("sell", help="sell command")
  sell_parser.add_argument("--price", type=float, help="provide the price of the product")
  sell_parser.add_argument("--product-name")

# Everything that had to do with the buy command
  buy_parser = subparser.add_parser("buy", help="buy command")
  buy_parser.add_argument("--advance-time", type=int, help="advance time by x day's")
  buy_parser.add_argument("--price", type=float, help="provide the price of the product")
  buy_parser.add_argument("--product-name")
  buy_parser.add_argument("--expiration-date")

  args = parser.parse_args()

  return args

def select_function(args):
  if args.command == "buy":
    print("calling buy function")
    print(buy(args.product_name, args.price, args.expiration_date))
  elif args.command == "report":
    print("calling report function")
  elif args.command == "sell":
    print("calling sell function")
    print(sell(args.product_name, args.price))
  else:
    print(f"Sorry, I don't know what to do with the command {args.command}")
  pass

def sell(product_name:str, price:float):
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
    writer.writerow([last_id + 1, product_id, today.isoformat(), price])
  return 'ok'


def read_file(file_name) -> list:
    file_content = []
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            file_content.append(row)
    return file_content

def find_product_id(product_name:str) -> int:
  pass


def buy(product_name:str, price:float, expiration_date:str) -> bool:
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
        if row[0] == 'id':
          last_id = 0
        else:
          last_id = int(row[0])
      else:
        break
  return last_id


if __name__ == "__main__":
  args = main()
  print(args)
  select_function(args)
  # sell(args.product_name, args.price)
  pass