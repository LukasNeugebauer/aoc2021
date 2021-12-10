#!/usr/bin/env python3

import numpy as np
import os


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day2.csv")
    ints, strs = [], []
    with open(filename, "r") as f:
        for line in f.readlines():
            s, i = line.split()
            strs.append(s)
            ints.append(int(i))
    return strs, ints


def get_position(strs, ints):
    x, y = 0, 0
    for s, i in zip(strs, ints):
        if s == "forward":
            x += i
        elif s == "down":
            y += i
        elif s == "up":
            y -= i
        else:
            raise ValueError("No known direction: " + s)
    return x, y


def get_position_aim(strs, ints):
    x, y, aim = 0, 0, 0
    for s, i in zip(strs, ints):
        if s == "down":
            aim += i
        elif s == "up":
            aim -= i
        elif s == "forward":
            x += i
            y += i * aim
        else:
            raise ValueError("No known direction: " + s)
    return x, y


if __name__ == "__main__":
    strs, ints = read_data()
    x, y = get_position(strs, ints)
    print("First one:")
    print(f"\thorizontal: {x}")
    print(f"\tdepth: {y}")
    print(f"\tProduct: {x * y}")
    x, y = get_position_aim(strs, ints)
    print("Second one:")
    print(f"\thorizontal: {x}")
    print(f"\tdepth: {y}")
    print(f"\tProduct: {x * y}")
