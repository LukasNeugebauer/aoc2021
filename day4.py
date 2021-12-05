#!/usr/bin/env python3

import os
import numpy as np
from copy import deepcopy


class Board:

    def __init__(self, values):
        self.board = np.array(values)
        self.marked = np.zeros(self.board.shape).astype(bool)
        self.complete = False

    def update(self, value):
        self.marked[np.where(self.board == value)] = True

    def check_completion(self):
        if self.complete:
            return False
        complete = self.marked.all(axis=0).any() or self.marked.all(axis=1).any()
        self.complete = complete
        return complete

    def reset(self):
        self.marked = np.zeros(self.board.shape).astype(bool)
        self.complete = False


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, '..', 'data']))
    filename = os.path.join(direc, 'day4.csv')
    draws, boards, rows = [], [], []
    with open(filename, 'r') as f:
        lines = f.readlines()
    draws = [int(x) for x in lines.pop(0).strip('\n').split(',')]
    for l in lines[1:]:
        l = l.strip('\n')
        if len(l) == 0:
            boards.append(rows)
            rows = []
            continue
        rows.append([int(x) for x in l.split()])
    boards.append(rows)
    boards = [Board(b) for b in boards]
    return draws, boards


def get_winner(draws, boards):
    for d in draws:
        for b in boards:
            b.update(d)
            if b.check_completion():
                return b, d


def get_last_winner(draws, boards):
    winner, draw = None, None
    for d in draws:
        for b in boards:
            b.update(d)
            if b.check_completion():
                winner = deepcopy(b)
                draw = d
    return winner, draw


def get_score(board, draw):
    unmarked_sum = board.board[np.logical_not(board.marked)].sum()
    return unmarked_sum * draw


if __name__ == '__main__':
    draws, boards = read_data()
    board, draw = get_winner(draws, boards)
    final_score = get_score(board, draw)
    print(f'Final score of winning board: {final_score}.')
    for b in boards:
        b.reset()
    board, draw = get_last_winner(draws, boards)
    final_score = get_score(board, draw)
    print(f'Final score of last winning board: {final_score}.')
