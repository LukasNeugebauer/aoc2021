#!/usr/bin/env python3


import os
import numpy as np


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day11.csv")
    return np.array(
        [[int(x) for x in line.strip()] for line in open(filename, "r").readlines()]
    )


def get_neighbors(idx, maxx, maxy):
    """
    Produce all neighboring indices that are in the grid
    """
    x, y = idx
    ys = y + np.array([-1, -1, -1, 0, 0, 1, 1, 1])
    xs = x + np.array([-1, 0, 1, -1, 1, -1, 0, 1])
    return [(x, y) for x, y in zip(xs, ys) if (0 <= x < maxx) and (0 <= y < maxy)]


get_idx_9 = lambda x: set(zip(*np.where(x > 9)))


def simulate_1_day(data):
    maxx, maxy = data.shape
    grid = data.copy() + 1
    flashed_idx = get_idx_9(grid)
    flashed_already = flashed_idx.copy()
    while flashed_idx:
        for x, y in flashed_idx:
            nb = get_neighbors((x, y), maxx, maxy)
            grid[tuple(zip(*nb))] += 1
        flashed_idx = get_idx_9(grid)
        flashed_idx = flashed_idx - flashed_already
        flashed_already = flashed_already | flashed_idx
    grid[np.where(grid > 9)] = 0
    return grid, len(flashed_already)


def simulate_n_days(data, n_days):
    flash_counter = 0
    grid = data.copy()
    for _ in range(n_days):
        grid, flashes = simulate_1_day(grid)
        flash_counter += flashes
    return flash_counter


def find_sync(data):
    grid = data.copy()
    target = np.prod(data.shape)
    day, flashes = 0, 0
    while flashes < target:
        day += 1
        grid, flashes = simulate_1_day(grid)
    return day


if __name__ == "__main__":
    data = read_data()
    flashes100 = simulate_n_days(data, 100)
    print(f"Flashes after 100 days: {flashes100}")
    sync_day = find_sync(data)
    print(f"Synchronized after {sync_day} days")
