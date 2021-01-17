import csv
from datetime import date

boughtfile = 'bought.csv'
soldfile = 'sold.csv'
currentdate = "2020-01-14"

def main():
    file_content = get_file_content(boughtfile)
    print_report(file_content)
    file_content = get_file_content(soldfile)
    print_report(file_content)

    #get_unique_sold_items()

def get_file_content(file_name):
    with open(file_name, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def conv_date(d):
    return date.fromisoformat(d)

def get_expired():
    #read the boughtfile and print a list of everthing that is expired
    content = get_file_content(boughtfile)
    expired = ''
    for record in content:
        if conv_date(currentdate) > conv_date(record['expiration_date']):
            expired += '\nEXPIRED - ' + record['product_name'] + '  ' + record['expiration_date']
    print(expired)


def print_report(file_content):
    print(file_content)
    '''
    Get report as seen in assignment.
    '''
    # Set a empty array to store the width of each column
    width = []
    # Set variable to keep track of the line
    line_number = 0
    # Check each row for all items
    # Check the length of each item in the line and compare to same item
    # index to find out which is longer for good formatting
    for row in file_content:
        if line_number == 0:
            for key in row:
                width.append(len(key))
        elif line_number > 0:
            i = 0
            for key in row:
                if width[i] < len(key):
                    width[i] = len(key)
                i += 1
        line_number += 1
    # Make the row divider

    row_seperator = "+"
    for item in width:
        row_seperator += (item + 2) * "-" + "+"
    # Walk through each row to print out the information it contains

    row_number = 0
    
    #print header
    line = "|"
    i=0
    print(file_content[0])
    print(row_seperator)
    
    for item in file_content[0].keys():
        line += f" {item}{' ' * (width[i] - len(item))} |"
        i+=1
    print(line)

    #print content
    for row in file_content: 
        # Assuming first row contains headers. After header want a simulation of
        #  a double line
        if row_number == 0:
            print(row_seperator.replace("-","="))
        else:        
            print(row_seperator)
        line = "|"
        i = 0
        for item in row.values():
            line += f" {item}{' ' * (width[i] - len(item))} |"
            i += 1
        print(line)
        row_number += 1
    print(row_seperator)


if __name__ == "__main__":
    main()

