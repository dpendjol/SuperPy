# Report

## Technical implementation

During the implementation of this program we ran into some challenges, I will enlighten three of them:

### **The first one:**
---

For the plots where I wanted to display the number of transactions that occurred on a specific day I needed to get all the lines in the sold records where the selling date equals a specific date.  
Python has the filter function built in. Together with the use of a lambda function, it's a simple way to filter out data without a lot of code and is nice and readable.

```
def get_transactions_per_day(self, asked_date):
    '''Get the transactions by a date requested in asked_date

    Arguments:
    asked_date -- the of which the transactions has to be returnt
   
    Returns:
    dict -- {transaction_id: {details of transaction}}
    '''
    output = filter(lambda item: item[1]['selling_date'] ==
                    asked_date, self.sold.items())
    return dict(output)
```

### **The second one:**
---

I wanted to minimize the read/write actions to the files containing the bought and sold products. 
When the class initializes I read the files into a variable. And just before the program is done and exiting, it writes the date back into a file. And to be as quick as possible with the lookups I converted it into a dictionary for quick lookup of data when possible.  
When using lists you have to loop through the list until you find what you where looking for. A dictionary is faster. 

### **The third one:**
---

When entering the arguments in the command line, it was possible to add arguments to specify for example `--today` and `--yesterday`. However, if one is used, the other can’t be.  
This can be solved by a check after reading the arguments, however, I found a more simple solution with the use of the `.add_mutually_exclusive_group` that’s available when you use the argparse module. It was implemented with the following snippet:

```
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
```

So now you can use one one of the arguments in this group. When you specify more, the program reminds you how it was supposed to be used. Furthermore, there is no need for long `if... and... elif ... and ...` statements.

### Finally

The report has a little bit more then 300 words (not including the code snippets). Hope that’s ok.

