#!/usr/bin/env python3


import numpy as np
import os
from itertools import product


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day9.csv")
    return np.array([
        [int(x) for x in line.strip('\n')] for line in open(filename, 'r').readlines()
    ])


def find_local_minima(data):
    maxx, maxy = data.shape
    local_minima = []
    for x, y in product(range(maxx), range(maxy)):
        nb = get_neighbors((x, y), maxx, maxy)
        if all(data[x, y] < data[nb]):
            local_minima.append((x, y))
    return local_minima


def get_risk_sum(data, local_minima):
    return sum([data[x, y] + 1 for x, y in local_minima])


def get_neighbors(idx, maxx=100, maxy=100):
    x, y = idx
    xs = x + np.array([-1, 0, 0, 1])
    ys = y + np.array([0, -1, 1, 0])
    keep_idx = (
        np.logical_and(0 <= xs, xs < maxx) *
        np.logical_and(0 <= ys, ys < maxy)
    ).astype(bool)
    return xs[keep_idx], ys[keep_idx]


def get_basin_size(local_minimum, data):
    size = 1
    maxx, maxy = data.shape
    contained, new_ones = [set(local_minimum) for _ in range(2)]
    proposals = [(x, y) for x, y in zip(*get_neighbors(local_minimum, maxx, maxy))]
    while len(new_ones):
        new_ones = set([x for x in proposals if not data[x] == 9])
        contained = contained | new_ones
        proposals = set()
        for x in new_ones:
            nb = set([(x, y) for x, y in zip(*get_neighbors(x, maxx, maxy))])
            proposals = proposals | nb
        proposals = proposals - contained
    return len(contained)


def prod_basin_sizes(local_minima, data):
    basin_sizes = [get_basin_size(lm, data) for lm in local_minima]
    return np.prod(sorted(basin_sizes)[-3:])


if __name__ == "__main__":
    data = read_data()
    local_minima = find_local_minima(data)
    rl_sum = get_risk_sum(data, local_minima)
    print(f'Sum of risk levels: {rl_sum}')
    result_size_prod = prod_basin_sizes(local_minima, data)
    print(f'Product of 3 largest basin sizes: {result_size_prod}')
