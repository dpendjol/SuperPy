from matplotlib import pyplot as plt
from supermarket import Supermarket


def make_bar_chart(data_x, *args, label_x="", label_y="", title=""):
    print(len(args))
    for data_y in args:
        plt.plot(data_x, data_y)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.show()


mysuper = Supermarket("bought.csv", "sold.csv")
data = mysuper.get_monthly_data("2020-01")
make_bar_chart(data['days'], data['costs'], data['revenue'], data['profit'])
