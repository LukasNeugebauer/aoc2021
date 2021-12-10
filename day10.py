#!/usr/bin/env python3


import os
from statistics import median


# mapping of closing to corresponding opening characters and reverse
close_to_open = {")": "(", "]": "[", "}": "{", ">": "<"}
open_to_close = {value: key for key, value in close_to_open.items()}


syntax_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
completion_points = {")": 1, "]": 2, "}": 3, ">": 4}


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day10.csv")
    return [[x for x in line.strip("\n")] for line in open(filename, "r").readlines()]


def get_invalid_closing(line):
    openings = []
    for char in line:
        if char in close_to_open.values():
            openings.append(char)
        else:
            if (this_open := close_to_open[char]) == openings[-1]:
                openings = openings[:-1]
            else:
                return char
    return None


def discard_corrupted_lines(data):
    return [line for line in data if get_invalid_closing(line) is None]


def get_line_completion(line):
    openings = []
    for char in line:
        if char in close_to_open.values():
            openings.append(char)
        else:
            if (this_open := close_to_open[char]) == openings[-1]:
                openings = openings[:-1]
    return [open_to_close[o] for o in openings[::-1]]


def get_line_points(endings):
    highscore = 0
    for e in endings:
        highscore *= 5
        highscore += completion_points[e]
    return highscore


def get_syntax_highscore(data):
    highscore = 0
    for line in data:
        char = get_invalid_closing(line)
        if char is not None:
            highscore += syntax_points[char]
    return highscore


def get_completion_highscore(data):
    incomplete = discard_corrupted_lines(data)
    line_points = []
    for line in incomplete:
        endings = get_line_completion(line)
        line_points.append(get_line_points(endings))
    return median(line_points)


if __name__ == "__main__":
    data = read_data()
    syntax_highscore = get_syntax_highscore(data)
    print(f"Syntax highscore: {syntax_highscore}")
    completion_highscore = get_completion_highscore(data)
    print(f"Completion highscore: {completion_highscore}")
