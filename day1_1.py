#!/usr/bin/env python3

import numpy as np
import os


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, '..', 'data']))
    filename = os.path.join(direc, 'day1.csv')
    return np.genfromtxt(filename)


def get_increases_1(data):
    diffs = np.diff(data)
    return (diffs > 0).sum()


def get_increases_2(data):
    stack = np.stack([data[:-2], data[1:-1], data[2:]], axis=1)
    sums = stack.sum(axis=1)
    diffs = np.diff(sums)
    return (diffs > 0).sum()



if __name__ == '__main__':
    data = read_data()
    increases = get_increases_1(data)
    print(f'There are {increases} simple increases.')
    sum_increases = get_increases_2(data)
    print(f'There are {sum_increases} summed increases.')
