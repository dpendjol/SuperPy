import argparse


def main():
    args = get_args()
    print(args)


def get_args():
    '''
    Get de arguments given by the user on the command line

    Returns:
    Arguments namespace
    '''
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
# Everthing that had to do with shifting time
    parser.add_argument(
        "--advance-time",
        type=int,
        help="specify how many day's you want to shift time, \
        use the minus sign (-) for days to the past"
        )
# Everything that has to do with the report command
    report_parser = subparser.add_parser("report", help="report command")
    report_parser.add_argument("subcommand",
                               choices=["inventory", "revenue", "profit"],
                               help="Choose which report you want to see")
# Choose to create a group, only one of the arguments can be used at one time
    time_group = report_parser.add_mutually_exclusive_group()
    time_group.add_argument("--now", action="store_true",
                            help="get current inventory")
    time_group.add_argument("--yesterday", action="store_true",
                            help="get data of yesterday")
    time_group.add_argument("--today", action="store_true",
                            help="get data of today")
    time_group.add_argument("--date", type=str,
                            help="get data of date provided in format yyyy-mm")
# Everything that has to do with the sell command
    sell_parser = subparser.add_parser("sell", help="sell command")
    sell_parser.add_argument("--product-name", type=str, required=True,
                             help="provide name of the product")
    sell_parser.add_argument("--price", type=float, required=True,
                             help="provide the price of the product")
    sell_parser.add_argument("--amount", type=int,
                             help="number of productitems sold")
# Everything that had to do with the buy command
    buy_parser = subparser.add_parser("buy", help="buy command")
    buy_parser.add_argument("--product-name", type=str, required=True,
                            help="provide name of the product")
    buy_parser.add_argument("--price", type=float, required=True,
                            help="provide bought price per item")
    buy_parser.add_argument("--expiration-date", required=True,
                            help="provide expiration date as yyyy-mm-dd")
    buy_parser.add_argument("--amount", type=int,
                            help="how many items dit you bought")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
