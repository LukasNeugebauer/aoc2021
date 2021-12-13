#!/usr/bin/env python3


import os
import re


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day13.csv")
    points, folds = [], []
    for line in open(filename, "r").read().splitlines():
        if len(line) == 0:
            continue
        elif line.startswith("fold"):
            direction, fold = re.search(r"[x,y]=[0-9]+", line).group(0).split("=")
            folds.append((direction, int(fold)))
        else:
            points.append(tuple(int(x) for x in line.split(",")))
    return {"points": set(points), "folds": folds}


def fold(points, direction, line):
    idx = 1 if direction == "y" else 0
    new_points = set()
    for p in points:
        pl = list(p)  # tuples are immutable
        if p[idx] < line:
            new_points.add(p)
        else:
            pl[idx] = 2 * line - p[idx]
            new_points.add(tuple(pl))
    return new_points


def get_points_fold_1(points, folds):
    direction, line = folds[0]
    new_points = fold(points, direction, line)
    return len(new_points)


def full_fold(points, folds):
    for direction, line in folds:
        points = fold(points, direction, line)
    return points


def print_solution(points):
    maxx, maxy = [max(x[i] for x in points) for i in [0, 1]]
    myprint = lambda x: print(x, end="")
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) in points:
                myprint("#")
            else:
                myprint(" ")
        myprint("\n")


if __name__ == "__main__":
    data = read_data()
    n_points_1 = get_points_fold_1(**data)
    print(f"There are {n_points_1} visible points after one fold.")
    end_points = full_fold(**data)
    print(f"The solution is:")
    print_solution(end_points)
