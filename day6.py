#!/usr/bin/env python3


import numpy as np
import os
from collections import Counter, defaultdict


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, '..', 'data']))
    filename = os.path.join(direc, 'day6.csv')
    return np.genfromtxt(filename, delimiter=',')


def simulate(data, days, init=8, reset=6):
    data = data.copy()
    for _ in range(days):
        data -= 1
        creators = np.where(data < 0)[0]
        new_fish = np.ones(creators.shape) * init
        data[creators] = reset
        data = np.r_[data, new_fish]
    return data


def simulate_without_overflow(data, days, init=8, reset=6):
    """
    Instead of keeping track of all fish, we'll just keep track of their number
    to avoid RAM overflow
    """
    init_counts = Counter(data)
    tracker = defaultdict(int)
    tracker.update(init_counts)
    for _ in range(days):
        tracker = defaultdict(int, {k - 1: v for k, v in tracker.items()})
        creators = tracker[-1]
        tracker[-1] = 0
        tracker[reset] += creators
        tracker[init] += creators
    return sum(tracker.values())


if __name__ == "__main__":
    data = read_data()
    after80 = simulate(data, 80)
    print(f'After 80 days there would be {len(after80)} fish.')
    after256 = simulate_without_overflow(data, 256)
    print(f'After 256 days there would be {after256} fish.')
