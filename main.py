# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.

# Imports
import argparse
import csv
from datetime import date
import sys

def create_datefile():
    today = date.today()
    try:
        with open("./date.txt", "w+") as f:
            f.write(today.isoformat())
            print(f"File {str(f)} created")
    except FileExistsError:
        print("File bestaat niet")

    
def main():
    with open("./bought.csv", newline="") as f:
      reader = csv.DictReader(f)
      for row in reader:
        print(row)
    
    with open("./sold.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['schrijf', 'dit', 'naar', 'file'])


def buy_product():
    # read sold file
    # append given arguments in command line
    # return 'OK'
    pass
 
def read_commandline():
    pass

def read_file(file_name):
    file_content = []
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            file_content.append(row)
    return file_content

def print_report(file_content):
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
    for row in file_content: 
        # Assuming first row contains headers. After header want a simulation of
        #  a double line
        if row_number == 1:
            print(row_seperator.replace("-","="))
        else:        
            print(row_seperator)
        line = "|"
        i = 0
        for item in row:
            line += f" {item}{' ' * (width[i] - len(item))} |"
            i += 1
        print(line)
        row_number += 1
    print(row_seperator)

if __name__ == '__main__':
    #main()
    print_report(read_file("bought.csv"))
    print_report(read_file("sold.csv"))
    argparse

