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


mysuper = Supermarket("bought.csv", "sold.csv")
data = mysuper.get_monthly_data("2020-01")
make_bar_chart(data['days'], data['costs'], data['revenue'], data['profit'],
               xlabel="xlabel", ylabel="ylabel", title="title")
