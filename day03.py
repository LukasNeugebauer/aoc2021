#!/usr/bin/env python3


import numpy as np
import os


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day3.csv")
    with open(filename, "r") as f:
        data = np.array([[int(x) for x in l] for l in f.read().split()])
    return data


def get_power_consumption(data):
    gamma = data.sum(axis=0) > data.shape[0] / 2
    epsilon = np.logical_not(gamma)
    gamma = bin2dec(gamma.astype(int))
    epsilon = bin2dec(epsilon.astype(int))
    return gamma * epsilon


def bin2dec(array):
    string = "".join([str(x) for x in array])
    return int(string, 2)


def get_oxy_gen_rating(data):
    data = data.copy()
    n_col = data.shape[1]
    for i in range(n_col):
        _, (count0, count1) = np.unique(data[:, i], return_counts=True)
        keep = 1 if count0 == count1 else int(count1 > count0)
        data = data[np.where(data[:, i] == keep)]
        if data.shape[0] == 1:
            break
    return bin2dec(data.squeeze())


def get_co2_scrub_rating(data):
    data = data.copy()
    n_col = data.shape[1]
    for i in range(n_col):
        _, (count0, count1) = np.unique(data[:, i], return_counts=True)
        keep = 0 if count0 == count1 else int(count1 < count0)
        data = data[np.where(data[:, i] == keep)]
        if data.shape[0] == 1:
            break
    return bin2dec(data.squeeze())


def get_life_support_rating(data):
    return get_oxy_gen_rating(data) * get_co2_scrub_rating(data)


if __name__ == "__main__":
    data = read_data()
    print(f"Power consumption: {get_power_consumption(data)}")
    print(f"Life support rating: {get_life_support_rating(data)}")
