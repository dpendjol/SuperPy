# Report

## Technical implementation 

During the implementation of this program we ran into some challenges, I will enlighten three of them:

### **The first one:**
---

For the plots where I wanted to display the number of transactions that occured on a specific day I needed to get al the lines of in de sold records where the selling date equals a specific date.
Python has the filter function built in. And I used it, together with the map function alot in Javascript, but nog yet in Python. Together with the use of a anonymous funcion, or lambda, it's a simple way to filter out data without a lot of code and is nice and readable. But most importantly, I didn't had to think how I had to write the filter function myself.

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

I wanted to minimize the read/write actions to the files containing the bought and sold products. So I thought of the following. 
When the class initalizes I read the files into a variable. And just before we are done and exiting, we write the data back into a file. And to be as quick as possible with the lookups I converted it into a dict for quick lookup of data when possible. 
When using lists you have to loop though the list untill you find what you where looking for. A dict is faster. I will take up more memory, but in most user systems nowaday's that's not a big problem. When the system feels laggy it's a bad user experience.


### **The third one:**
---

With my implementation of the sell command, it was possible to pass in how much you sold. Suppose we bought 100 appels and a customer buy's 50, then we pass that by the `--amount` flag. But in the examples command given in the excercise, no `--amount` is passed in.
So I solved it by checking if the everything needs to be sold, simply bij asking the user.
```
if amount is None:
    check = None
    while not (check == "n" or check == "y"):
        check = input("Do you want to sell all the {}? [y/n] "
                        .format(self.bought[product_id]['product_name']))
        if check == 'n':
            return
```

We can also buy 50 appels with a for 50 cents a piece, and a couple of days later where at the wholesale and the appels are in sale, so we buy 100 extra for 10 cents a piece. 
When a customer wants to buy 60 appels, this is possible. I solved this check with the code as seen below.

```
total_amount = 0
    for product_id in product_ids:
        if self.bought[product_id]['expiration_date'] > self.current_date:
            total_amount += inventory[product_id]

    if total_amount == 0:
        raise Exception('Error: Product no longer in stock')
```

Then I realised that a user can request to buy 500 appels. But that isn't possible in the example. So another check was added below, so we know how much we have in stock.

```
if total_amount < amount:
    if total_amount == 0:
        print("All out")
    else:
        print("Sorry, just got " + str(total_amount) + " left")
```
