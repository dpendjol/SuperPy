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
    parser.add_argument("--advance-time", type=int,
                        help="specify how many day's you want to shift time, \
                        use the minus sign (-) for days to the past"
                        )
    parser.add_argument("--date-to-sysdate",
                        action="store_true", help="reset the date to the \
                        systemdate")
    parser.add_argument("--tell-current-date",
                        action="store_true", help="print the date the \
                        the supermarket sees as today")
# Everything that has to do with the report command
    report_parser = subparser.add_parser("report", help="report command")
    report_parser.add_argument("subcommand",
                               choices=["inventory", "revenue", "profit",
                                        "expired", "overview"],
                               help="Choose which report you want to see")
# Choose to create a group, only one of the arguments can be used at one time
    time_group = report_parser.add_mutually_exclusive_group(required=True)
    time_group.add_argument("--now", action="store_true",
                            help="get current inventory")
    time_group.add_argument("--yesterday", action="store_true",
                            help="get data of yesterday")
    time_group.add_argument("--today", action="store_true",
                            help="get data of today")
    time_group.add_argument("--nextweek", action="store_true",
                            help="get the items that will expire in de coming\
                            seven days")
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
# Everthing that has to do with plot
    transaction_parser = subparser.add_parser("transaction",
                                              help=("Plot transaction data "
                                                    "per day"))
    transaction_parser.add_argument("--save", action="store_true",
                                    help="saving plot in directory 'plots'")
    type_group = transaction_parser.add_mutually_exclusive_group(required=True)
    type_group.add_argument("--average-amount",
                            action="store_true")
    type_group.add_argument("--number-of-transactions",
                            action="store_true")

    selection_group = transaction_parser.add_mutually_exclusive_group(required=True)
    selection_group.add_argument("--all",
                                 action="store_true",
                                 help="get all the transactions")
    selection_group.add_argument("--current-month",
                                 action="store_true",
                                 help=("only get transactions "
                                       "for current month"))
    selection_group.add_argument("--current-year",
                                 action="store_true",
                                 help=("only get transactions "
                                       "for current year"))
    selection_group.add_argument("--previous-month",
                                 action="store_true",
                                 help=("only get transactions "
                                       "for previous month"))
    selection_group.add_argument("--previous-year",
                                 action="store_true",
                                 help=("only get transactions "
                                       "for previous year"))

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
