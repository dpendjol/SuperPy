import argparse


def getArguments() -> dict:
  '''
  Get the arguments from the command line
  '''

  parser = argparse.ArgumentParser(description="test")
  
  # argument can assume values 'buy' 'report' 'sell'
  parser.add_argument("argument", nargs="?")

  # argument can assume value 'inventory' 'revenue' 'profit'
  # needs only be read when argument = report
  parser.add_argument("report-type", nargs="?")


  #producet name needs to be read when argument = 'buy' 'sell'
  parser.add_argument("--product-name", help=" Provide the product name", default=None, type=str)

  # product price needs to be read when argument = buy and sell
  parser.add_argument("--price", help="Set the price", default=0, type=float)

  # optional argument
  parser.add_argument("-a", "--advance-time", help="Move x days in the future", default=0, type=int)
  # needs to be read when argument = buy
  parser.add_argument("--experation-date", help="time")
  # needs to be read when argument = report
  parser.add_argument("--now", help="Get report for current time", default=False, action="store_true")
  # OPTIONAL needs to be read when argument = report
  parser.add_argument("--yesterday", help="Get report for yesterday", action="store_true")
  parser.add_argument("--today", help="Get report for today", action="store_true")
  
  args = parser.parse_args()
  print("Argument: ", args.argument)
  return args

if __name__ == "__main__":
  getArguments()