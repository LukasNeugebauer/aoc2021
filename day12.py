#!/usr/bin/env python3


import os
import numpy as np
from collections import defaultdict, Counter


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day12.csv")
    return [line.split('-') for line in open(filename, 'r').read().splitlines()]


def create_graph(data):
    graph = defaultdict(list)
    for x, y in data:
        if not x == "end" and not y == "start":
            graph[x].append(y)
        if not x == "start" and not y == "end":
            graph[y].append(x)
    return graph


def get_paths(paths, graph):
    finished = list(filter(lambda x: x[-1] == "end", paths))
    paths = list(filter(lambda x: not x[-1] == "end", paths))
    if len(paths) == 0:
        return len(finished)
    nextsteps = []
    for p in paths:
        node = p[-1]
        possible_next = graph[node]
        for pn in possible_next:
            if not (pn.islower() and pn in p):
                nextsteps.append(p + [pn])
    return len(finished) + get_paths(nextsteps, graph)


def check_condition_2(path):
    for key, value in Counter(path).items():
        if key.islower() and value == 2:
            return False
    return True


def get_valid_followups(path, graph):
    followups = []
    for node in graph[path[-1]]:
        if node not in path or node.isupper():
            followups.append(path + [node])
        elif check_condition_2(path):
            followups.append(path + [node])
    return followups


def get_paths_2(init_path, graph):
    """
    Recursion kills my computer. so sad :(
    Trying without
    """
    finished = 0
    paths = init_path
    while True:
        to_complete = []
        for p in paths:
            followups = get_valid_followups(p, graph)
            for f in followups:
                if f[-1] == "end":
                    finished += 1
                else:
                    to_complete.append(f)
        if len(to_complete) == 0:
            return finished
        paths = to_complete


if __name__ == "__main__":
    data = read_data()
    graph = create_graph(data)
    init_path = [["start"]]
    paths = get_paths(init_path, graph)
    print(f"There are {paths} paths through the caves.")
    init_path = [["start"]]
    paths_2 = get_paths_2(init_path, graph)
    print(f"There are {paths_2} other paths through the caves.")
