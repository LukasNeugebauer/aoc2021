#!/usr/bin/env python3


import os
import numpy as np
from collections import defaultdict, Counter


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day5.csv")
    with open(filename, "r") as f:
        lines = [l.strip("\n").replace("-> ", "") for l in f.readlines()]
    data = []
    return [[tuple(map(int, ll.split(","))) for ll in l.split()] for l in lines]


def check_straight(pos1, pos2):
    return any([x == y for x, y in zip(pos1, pos2)])


def get_straight_trajectory(pos1, pos2):
    if not check_straight(pos1, pos2):
        return []
    fixed = 0 if pos1[0] == pos2[0] else 1
    free = 1 - fixed
    bounds = pos1[free], pos2[free]
    path = np.arange(min(bounds), max(bounds) + 1)
    static = np.ones(path.shape) * pos1[fixed]
    trajectory = np.stack([path, static], axis=1)
    if fixed == 0:
        trajectory = trajectory[:, ::-1]
    return trajectory.astype(int)


def get_diagonal_trajectory(pos1, pos2):
    bounds1 = sorted([pos1[0], pos2[0]])
    bounds2 = sorted([pos1[1], pos2[1]])
    traj1 = np.arange(bounds1[0], bounds1[1] + 1)
    traj2 = np.arange(bounds2[0], bounds2[1] + 1)
    if pos1[0] > pos2[0]:
        traj1 = traj1[::-1]
    if pos1[1] > pos2[1]:
        traj2 = traj2[::-1]
    return np.stack([traj1, traj2], axis=1)


def get_all_trajectory(pos1, pos2):
    if check_straight(pos1, pos2):
        return get_straight_trajectory(pos1, pos2)
    return get_diagonal_trajectory(pos1, pos2)


def get_straight_visits(data):
    counts = defaultdict(int)
    for pos1, pos2 in data:
        trajectory = get_straight_trajectory(pos1, pos2)
        for t in trajectory:
            counts[tuple(t)] += 1
    return counts


def get_all_visits(data):
    counts = defaultdict(int)
    for pos1, pos2 in data:
        trajectory = get_all_trajectory(pos1, pos2)
        for t in trajectory:
            counts[tuple(t)] += 1
    return counts


def count_lt_2(counts):
    counter = Counter(counts.values())
    return sum([v for k, v in counter.items() if k >= 2])


if __name__ == "__main__":
    data = read_data()
    counts = get_straight_visits(data)
    print(
        f"There are at least two overlapping straight lines at {count_lt_2(counts)} points."
    )
    counts = get_all_visits(data)
    print(f"There are at least two overlapping lines at {count_lt_2(counts)} points.")
