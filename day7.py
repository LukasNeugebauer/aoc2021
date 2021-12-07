#!/usr/bin/env python3


import numpy as np
import os


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, '..', 'data']))
    filename = os.path.join(direc, 'day7.csv')
    return np.genfromtxt(filename, delimiter=',').astype(int)


def get_fuel_cost(data):
    """
    Median is the value that minimizes non-squared distance
    """
    target = np.median(data)
    return np.abs(target - data).sum().astype(int)


def get_fuel_cost_2(data):
    """
    There's probably some weird central tendency measure that minimizes the distance
    or you can do something with a log transform, but I didn't find it
    Brute force it is ]:->
    """
    minx, maxx = min(data), max(data)
    best_pos, best_cost = None, np.inf
    return min([
        sum([np.arange(np.abs(x - i) + 1).sum() for x in data]) for i in range(minx, maxx + 1)
    ])


if __name__ == "__main__":
    data = read_data()
    cost = get_fuel_cost(data)
    print(f'Crabs need a total of {cost} fuel')
    cost = get_fuel_cost_2(data)
    print(f'Crabs need a total of {cost} fuel')
