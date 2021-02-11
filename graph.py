from matplotlib import pyplot as plt
from datetime import datetime
from os import path as ospath, getcwd, makedirs


def make_bar_chart(data_x, *data_y, **kwargs):

    ''' Create and show a lineplot

    Arguments:
    data_x -- list of dates
    data_y -- multiple lists of data

    Also possible to use arguments used in matplotlib

    Return:
    None
    '''

    save = kwargs['save']
    
    full_path = ospath.join(getcwd(), 'plots')
    dir_exists = ospath.isdir(full_path)
    if not dir_exists:
        makedirs(full_path)
        
    for data in data_y:
        plt.plot(data_x, data)
    number_of_items = len(data_x)
    to_calculate_ticks = round(number_of_items / 25)
    number_of_ticks = to_calculate_ticks if to_calculate_ticks > 0 else 1

    i = 0
    labels = []
    ticks = []
    for item in data_x:
        if i % number_of_ticks == 0:
            mydate = datetime.strptime(item, "%Y-%m-%d")
            labels.append(mydate.strftime("%d-%m"))
            ticks.append(item)
        i += 1
    plt.xticks(ticks=ticks, labels=labels, fontsize=8, rotation=-90)
    plt.xlabel(kwargs['xlabel'])
    plt.ylabel(kwargs['ylabel'])
    plt.title(kwargs['title'])
    if save:
        fname = datetime.now().strftime("%Y%m%d%H%M%S%f.png")
        relpath = ospath.join(getcwd(), "plots", fname)
        plt.savefig(relpath)
        print(f"file saved to {relpath}")
    plt.show()

    return None


def get_transactions_per_day(asked_date: str, sold_file):
    '''Get the transactions per day'''
    output = filter(lambda item: item[1]['selling_date'] ==
                    asked_date, sold_file.items())
    return dict(output)


def get_number_of_transactions_per_day(asked_date: str):
    '''Gets the number of transactions per day'''
    output = get_transactions_per_day(asked_date)
    number_of_transactions = len(list(output))
    return number_of_transactions


def get_average_transaction_per_day(asked_date):
    '''Get the average amount spend per transactions per day '''
    output = get_transactions_per_day(asked_date)
    total_revenue = 0
    for item in output.values():
        total_revenue += (item['selling_count'] * item['selling_price'])
    try:
        average = total_revenue / len(output)
    except ZeroDivisionError:
        average = 0
    return average


# Redundant?
# def plot_average_transactions(month: str):
#     day, last_day = get_dates_month(month)
#     transactions = []
#     while day < last_day:
#         transactions.append((day.strftime("%Y-%m-%d"),
#                             get_average_transaction_per_day(day)))
#         day += timedelta(days=1)
#     print(transactions)


if __name__ == "__main__":
    pass
