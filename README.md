# Welcome to SuperPy

SuperPy is a command line program to keep track of tranactions and inventory of a fictional supermarket.
SuperPy comes with some nifty features to help everthing get along nicely

### Getting started
We can use SuperPy with the following command from the command line

>```
> usage: super.py [-h] [--advance-time ADVANCE_TIME]  {report,sell,buy} ...
>
> positional arguments:
>  {report,sell,buy}
>    report              report command
>    sell                sell command
>    buy                 buy command
> 
> optional arguments:
>  -h, --help            show this help message and exit
>  --advance-time ADVANCE_TIME
>                        specify how many day's you want to shift time, use the
>                        minus sign (-) for days to the past
>```

### Needed files and formats
date.txt
: The date of the system is stored in the `date.txt` file as a string conforming to the iso format `yyyy-mm-dd`.

sold.csv
: The `sold.csv` file keeps track of the sells made by the supermarket. The file is located in the data folder. 

bought.csv
: The `bought.csv` file keepts track of the purchases made by the supermarket. The file is located in the data folder.  






