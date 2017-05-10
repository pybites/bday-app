import csv
import os
import random

names_csv = os.path.join('data', 'CSV_Database_of_First_Names.csv')
used = set()  # could use class

with open(names_csv) as f:
    # get unique names
    names = list(set(row[0] for row in csv.reader(f)))


def get_random_name():
    while True:
        name = random.choice(names)
        if len(names) == len(used):
            print('No more new names')
            break
        if name in used:
            continue
        used.add(name)
        return name


if __name__ == '__main__':
    for i in range(1, 11):
        print('Random name {}:'.format(i), end=' ')
        print(get_random_name())
