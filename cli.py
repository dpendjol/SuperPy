import argparse


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

if __name__ == "__main__":
  main()