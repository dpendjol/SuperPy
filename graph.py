from matplotlib import pyplot as plt
from supermarket import Supermarket

''' Availible styles plot

['Solarize_Light2',
'_classic_test_patch',
'bmh', 'classic',
'dark_background',
'fast',
'fivethirtyeight',
'ggplot', 'grayscale',
'seaborn', 'seaborn-bright',
'seaborn-colorblind', 'seaborn-dark',
'seaborn-dark-palette',
'seaborn-darkgrid',
'seaborn-deep',
'seaborn-muted',
'seaborn-notebook',
'seaborn-paper',
'seaborn-pastel',
'seaborn-poster',
'seaborn-talk',
'seaborn-ticks',
'seaborn-white',
'seaborn-whitegrid',
'tableau-colorblind10']

'''

# choose to make use of another name voor args to make it more clear
# what information it contains


def make_bar_chart(data_x, *data_y, **kwargs):

    ''' Create and show a lineplot

    Arguments:
    data_x -- list of dates
    data_y -- multiple lists of data

    Also possible to use arguments used in matplotlib

    '''
    for data in data_y:
        print(data)
        plt.plot(data_x, data, label="blablabla")

    i = 0
    labels = []
    for item in data_x:
        if i % 5 == 0:
            labels.append(i+1)
        else:
            labels.append("")
        i += 1
    plt.xticks(ticks=data_x, labels=labels)
    plt.xlabel(kwargs['xlabel'])
    plt.ylabel(kwargs['ylabel'])
    plt.title(kwargs['title'])
    plt.legend()
    plt.show()


def get_transactions_per_day(asked_date):
    output = filter(lambda item: item[1]['selling_date'] ==
                    asked_date, sold_file.items())
    return dict(output)


def get_number_of_transactions_per_day(asked_date: str):
    '''Gets the number of transactions per day'''
    output = get_transactions_per_day(asked_date)
    number_of_transactions = len(list(output))
    return number_of_transactions


def get_average_transaction_per_day(asked_date):
    output = get_transactions_per_day(asked_date)
    total_revenue = 0
    for item in output.values():
        total_revenue += (item['selling_count'] * item['selling_price'])
    try:
        average = total_revenue / len(output)
    except ZeroDivisionError:
        average = 0
    return average


def _get_cost_per_day(asked_date):
    output = filter(lambda item: item[1]['purchase_date'] ==
                    asked_date, bought_file)
    return dict(output)


myconsole = Console()
output = get_number_of_transactions_per_day('2021-01-01')
output = get_expired_items('2021-01-01')
output = get_average_transaction_per_day('2021-01-01')
myconsole.print(output, style='')

# bought_items = {k: v for k, v in sorted(self.bought.items(),
#                key=lambda item: item[1]['expiration_date'])}


mysuper = Supermarket("bought.csv", "sold.csv")
data = mysuper.get_monthly_data("2020-01")
make_bar_chart(data['days'], data['costs'], data['revenue'], data['profit'],
               xlabel="xlabel", ylabel="ylabel", title="title")
