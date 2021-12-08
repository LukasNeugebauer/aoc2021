#!/usr/bin/env python3


import numpy as np
import os


n_segments = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6
}


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, '..', 'data']))
    filename = os.path.join(direc, 'day8.csv')
    lines = [line.strip('\n') for line in open(filename, 'r').readlines()]
    return [
        [l.split() for l in line.split(' | ')] for line in lines
    ]


def count_1478(data, n_segments):
    valid_length = [n_segments[x] for x in [1, 4, 7, 8]]
    outputs = [line[1] for line in data]
    count_per_line = [
        sum(list(map(lambda x: len(x) in valid_length, line))) for line in outputs
    ]
    return sum(count_per_line)


def check_all_in(str1, str2):
    return all([x in str2 for x in str1])


def determine_mapping(input_, n_segments):
    input_ = [''.join(sorted(inp)) for inp in input_]
    unique_mapping = {
        1: 2,
        4: 4,
        7: 3,
        8: 7
    }
    #find known length element
    mapping = {
        key: filter(lambda x: len(x) == value, input_).__next__() \
            for key, value in unique_mapping.items()
    }
    #determine len 5 and 6 elements respectively
    len5 = list(filter(lambda x: len(x) == 5, input_))
    len6 = list(filter(lambda x: len(x) == 6, input_))
    #3 is the one where all elements of 7 are present
    mapping[3] = filter(lambda x: check_all_in(mapping[7], x), len5).__next__()
    len5.remove(mapping[3])
    #9 is the only len6 one that contains all elements of 3
    mapping[9] = filter(lambda x: check_all_in(mapping[3], x), len6).__next__()
    len6.remove(mapping[9])
    #0 is the only len6 remaining that contains all of 1s elements
    mapping[0] = filter(lambda x: check_all_in(mapping[1], x), len6).__next__()
    len6.remove(mapping[0])
    #6 is the remaining on
    mapping[6] = len6[0]
    #all of 5s elements are contained in 9
    mapping[5] = filter(lambda x: check_all_in(x, mapping[9]), len5).__next__()
    len5.remove(mapping[5])
    #and 2 remains
    mapping[2] = len5[0]
    return {value: key for key, value in mapping.items()}



def get_final_output(data, n_segments):
    total_sum = 0
    for input_, output in data:
        mapping = determine_mapping(input_, n_segments)
        total_sum += get_row_value(output, mapping)
    return total_sum


def get_row_value(output, mapping):
    output = [''.join(sorted(o)) for o in output]
    value_string = ''.join([str(mapping[x]) for x in output])
    return int(value_string)


if __name__ == '__main__':
    data = read_data()
    unique_count = count_1478(data, n_segments)
    print(f'Found {unique_count} elements of length [2, 4, 3, 7].')
    final_output = get_final_output(data, n_segments)
    print(f'Final output is  {final_output} and boy wtf was that')
