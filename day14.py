#!/usr/bin/env python3


import os
import re
from collections import Counter, defaultdict


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day14.csv")
    mapping = {}
    stringlist = []
    for line in open(filename, "r").read().splitlines():
        if len(line) == 0:
            continue
        elif "->" in line:
            dummy = line.split(" -> ")
            mapping[dummy[0]] = dummy[1]
        else:
            stringlist += [x for x in line]
    return {"stringlist": stringlist, "mapping": mapping}


def add_matches(matches, letters, mapping):
    """
    Since the number of new matches depends on the old ones, this should be enough
    """
    matches = matches.copy()
    for m, v in list(matches.items()):
        addition = mapping[m]
        letters[addition] += v
        # we destroy old ones
        if (new_match := m[0] + addition) in mapping:
            matches[new_match] += v
        if (new_match := addition + m[1]) in mapping:
            matches[new_match] += v
        matches[m] -= v
    return matches, letters


def solution(stringlist, mapping, N):
    """
    Only keeping track of matches should be fine
    """
    letter_counter = defaultdict(int, Counter(stringlist))
    pattern = f"(?=({'|'.join(mapping.keys())}))"
    matches = defaultdict(
        int, Counter([x.groups()[0] for x in re.finditer(pattern, "".join(stringlist))])
    )
    for _ in range(N):
        matches, letter_counter = add_matches(matches, letter_counter, mapping)
    counts = letter_counter.values()
    return max(counts) - min(counts)


if __name__ == "__main__":
    data = read_data()
    part1_solution = solution(**data, N=10)
    print(f"The solution to part 1 is {part1_solution}.")
    part2_solution = solution(**data, N=40)
    print(f"The solution to part 2 is {part2_solution}.")
