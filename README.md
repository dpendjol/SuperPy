# Welcome to SuperPy

SuperPy is a command line program to keep track of transactions and inventory of a fictional supermarket.
SuperPy comes with some nifty features to help everthing get along nicely

* * *
Table of contents
- [Getting started](#getting-started)
- [Needed files and formats](#needed-files-and-formats)
- [Buying a product](#buying-a-product)
- [Selling a product](#selling-a-product)
- [Getting reports](#getting-reports)
  - [Inventory](#inventory)
  - [Revenue](#revenue)
  - [Profit](#profit)
  - [Expired](#expired)
  - [Overview](#overview)
  - [Transactions](#transactions)
- [Modifying date](#modifying-date)
  - [Advancing time](#advancing-time)
- [Thank you](#thank-you)

* * *

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

---
### Needed files and formats
---

date.txt
: The date of the system is stored in the `date.txt` file as a string conforming to the iso format `yyyy-mm-dd`.

sold.csv
: The `sold.csv` file keeps track of the sells made by the supermarket. The file is located in the data folder.  
Columns needed in the `sold.csv` file are in order:  
`> id,product_id,selling_count,selling_date,selling_price`

bought.csv
: The `bought.csv` file keepts track of the purchases made by the supermarket. The file is located in the data folder.  
Column needed in the `bought.csv` file are:  
`> id,product_name,purchase_count,purchase_price, expiration_date,purchase_date`

---
### Buying a product
---

With the following command you, as supermarkt owner, buy products for your supermarkt. 

`> usage: super.py buy [-h] -pn PRODUCT_NAME [-a AMOUNT] -p PRICE -ed EXPIRATION_DATE`  

Lets buy 15 apples for 50 cents a piece. The apples expiration dates is 22th of January 2021.

`> python super.py buy --product-name apples --price 0.5 --expiration-date 2021-01-22`

If you **do not pass** a `--amount [AMOUNT]` the system wil **buy** only **one** item. If you want to buy more, just pass in the argument.

If you pass a expiration-date in the past, then **the product will not be bought** since it allready expired.

---
### Selling a product
---
With the following command you, as supermarkt owner, can sell product to your customers and adjust the stock.

`> usage: super.py sell [-h] [-pn PRODUCT_NAME] [-a AMOUNT] [-p PRICE]`

Assume there is a customer that wants to buy 10 appels for 2 euro a piece. We can do that as follow:

`> python super.py sell --product-name apples --amount 10 --price 2`

Just as with the `buy` command you can leave out the amount. When you do that, the program will ask you if you want to sell all the apples in stock. Choose `y` and everthing wil be sold, choose `n` and the program will do nothing.

---
### Getting reports
---
#### **Inventory**

With the following command you can print reports:  

`> usage: super.py report [-h] {inventory,revenue,profit} [--now | --yesterday | --today | --date DATE]`  

Suppose we want to print out the inventory. Then we would use the following command:  

`> python super.py report inventory --now`  

The reports thats follows looks like this:  

````
┌──────────────┬────────┬────────────┬────────────┐  
│ Product Name │ Amount │ Bought for │ Expire on  │  
├──────────────┼────────┼────────────┼────────────┤  
│ orange       │ 100    │ 0.8        │ 2020-04-02 │  
│ wine         │ 686    │ 0.5        │ 2020-05-02 │  
│ apples       │ 196    │ 0.8        │ 2020-04-01 │  
│ wine         │ 1386   │ 0.5        │ 2020-03-02 │  
└──────────────┴────────┴────────────┴────────────┘  
````

We can also print the inventory report for yesterday or a specific date in de past.  

#### **Revenue**

As supermarkt owner we want to now how much money is comming in. So this program also has the ability to print out how much money has come in on a certain date. Or over a period of a month. 
Lets get the revenue for today:  

`> python super.py report revenue --today`

The output is as follows:  
```
Today's revenue so far:  14.0
```

Now lets see the the revenue for 23rd of January 2020. The command:  
`> python super.py report revenue --date 2020-01-23`  

And the output:
```
Revenue from 23 Jan 2020: 26.0
```

Now lets see the revenue for the month January 2020.

`> python super.py report revenue --date 2020-01`

As you can see we leave out the day section. Let see how the supermarkt did in January:

```
Revenue from Jan 2020: 184.0
```

#### **Profit**
Apart from the revenue it is also usefull to know if you can buy dinner today after a long hard day of work in the supermarket. So we can also get the profit.

`> python super.py report profit --today`

The output is simple yet effective:
```
29.4
```

As with the revenue you can also get the `profit` of yesterday, a specific date of a whole month.

#### **Expired**
If we want to know which product expired and what the loss is because we didn't sell the products we can use the following command

`> python super.py report expired --now`

The output is a table in which you can see which product expired, how many items per product and what the loss is.

```
┌──────────────┬────────────────────┬──────────────┬────────────┐
│ Product Name │ Number of products │ Loss in euro │ Expired on │
├──────────────┼────────────────────┼──────────────┼────────────┤
│ wine         │                679 │       339.50 │ 2021-01-02 │
├──────────────┼────────────────────┼──────────────┼────────────┤
│              │                    │       339.50 │            │
└──────────────┴────────────────────┴──────────────┴────────────┘
```

In the above example we didn't sell enough wine, so we have a loss of 339.50 euro.

We can also see which products go bad in de comming seven day's with the command:

`> python super.py report expired --nextweek`

The result looks the same, but now we can see which products are going bad in de comming week.

```
┌──────────────┬────────────────────┬──────────────┬────────────┐
│ Product Name │ Number of products │ Loss in euro │ Expired on │
├──────────────┼────────────────────┼──────────────┼────────────┤
│ wine         │               1383 │       691.50 │ 2021-02-02 │
│ apples       │                200 │       160.00 │ 2021-02-01 │
├──────────────┼────────────────────┼──────────────┼────────────┤
│              │                    │       851.50 │            │
└──────────────┴────────────────────┴──────────────┴────────────┘
```

### **Overview**

If we want to know wat we products we sold at a particular day, then we can use the command:

`usage: super.py report overview [--now | --yesterday | --today | --nextweek | --date DATE]`

*sidenote: the `--now` and the `--today` flag give the same results*

So we want to know what we sold on the following date 2021-02-05. We can do that with the command:

`> python super.py report overview --date 2021-02-05`

Below you can see the output of this command

```
Overview                                                  
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Product name ┃ Producs sold ┃ Revenue ┃ Costs ┃ Profit ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ orange       │            6 │   12.00 │  4.80 │   7.20 │
│ appels       │            1 │    2.00 │  0.80 │   1.20 │
│ wine         │            1 │    2.00 │  0.80 │   1.20 │
├──────────────┼──────────────┼─────────┼───────┼────────┤
│              │              │   16.00 │  6.40 │   9.60 │
└──────────────┴──────────────┴─────────┴───────┴────────┘
```

As you can see, we get a overview in and we can see wat we sold, and what the revenue, costs and profit per product and totals for the requested day.

#### **Transactions**

We can also evaluate the transaction. As supermarkt manager you can plot data concerning the average-amount spend bij customers per day per transactions. And we can also plot the number of transactions per day given a certain period. Both will be explaind below

```
usage: super.py transaction [-h] (--average-amount | --number-of-transactions) (--all | --current-month | --current-year | --previous-month | --previous-year)

optional arguments:
  -h, --help            show this help message and exit
  --average-amount
  --number-of-transactions
  --all                 get all the transactions
  --current-month       only get transactions for current month
  --current-year        only get transactions for current year
  --previous-month      only get transactions for previous month
  --previous-year       only get transactions for previous year
```

So wen we want to know the average amount spend per transaction over the current month we can use the command:

`> python super.py transaction --average-amount --current-month `

The result wil be a graph as you can see below (depending on the data in your files off-course):

![average spending](readme_img/average_amount_example_month.png)

We can also do this for all the data in de current year bij using the flag `--current-year` instead of `--current-month`.  
The `--all` flag ensures that all the sales in the datafile are taken into account wen creating the plot.  
Finally we can use the `--previous-month` or the `--previous-year` flag if we want to see the data of that time period.
When there is no data to display you will get a message in your terminal.

Next to the spending amount we can see if it was busy. We can plot the number of transactions bij issueing the command:

`> python super.py transaction --number-of-transactions --all`

That wil result in the following plot.

![Number of transactions](readme_img/number_of_transactions.png)

The periods over which this command can display the data are the same as with the `--average-amount` flag.

---
### Modifying date
---
#### **Advancing time**
For testing purposes we can advance the date. We do that with the following command:

`> usage: super.py [-h] [--advance-time ADVANCE_TIME]`

ADVANCE_TIME is in day's, so if we want to advance the time for 2 day's we can use the next command:

`> python super.py --advance-time 2`

If we want to reset the date to the system date we can pass any negative value. For example:

`> python super.py --advance-time -1`

---
### Thank you
---
Thank you for reading the manual. If you came across bugs or if you have feature requests please let me know. This is my first command-line program so any feedback is welcome.

