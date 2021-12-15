#!/usr/bin/env python3
"""
Probably a stupid idea, but I'll solve this using reinforcement learning
Optional dependency on tqdm
"""


import os
import numpy as np
try:
    from tqdm import tqdm
except:
    tqdm = lambda x: x


def get_valid_actions(y, x, maxx, maxy):
    y_offset = [-1, 1, 0, 0]
    x_offset = [0, 0, -1, 1]
    return [
        (yo, xo) for xo, yo in zip(y_offset, x_offset) if 0 <= x + xo < maxx and 0 <= y + yo < maxy
    ]


def read_data():
    file = __file__
    direc = os.path.dirname(os.path.abspath(file))
    direc = os.path.abspath(os.sep.join([direc, "..", "data"]))
    filename = os.path.join(direc, "day15.csv")
    lines = open(filename, 'r').read().splitlines()
    rewards = np.array([
        [-int(x) for x in line] for line in open(filename, 'r').read().splitlines()
    ])
    maxy, maxx = rewards.shape
    actions = {}
    for i, line in enumerate(lines):
        for j, _ in enumerate(line):
            actions[(i, j)] = get_valid_actions(i, j, maxx, maxy)
    return rewards, actions


def transition(y, x, action):
    return (y + action[0], x + action[1])


def choose_action(qv, epsilon):
    """
    epsilon-greedy policy with respect to current value function
    """
    if np.random.rand() > epsilon:
        return np.argmax(qv)
    else:
        return np.random.choice(np.arange(len(qv)))


def rl_episode(Q, rewards, actions, alpha, epsilon):
    pos = (0, 0)
    end_pos = list(Q.keys())[-1]
    while True:
        old_pos = pos
        act_idx = choose_action(Q[old_pos], epsilon)
        action = actions[old_pos][act_idx]
        pos = transition(*old_pos, action)
        reward = rewards[pos[0], pos[1]]
        Q[old_pos][act_idx] += alpha * (reward + max(Q[pos]) - Q[old_pos][act_idx])
        if  pos == end_pos:
            break
    return Q


def learn_action_value_function(
    rewards,
    actions,
    alpha=.2,
    epsilon=.2,
    iterations=20000
):
    """
    Epsilon-greedy Q-Learning, i.e. off-policy learning for the optimal policy
    """
    Q = {key: [0 for _ in range(len(value))] for key, value in actions.items()}
    print(f'Training agent for {iterations} iterations. 20k should take like 3 minutes.')
    for _ in tqdm(range(iterations)):
        Q = rl_episode(Q, rewards, actions, alpha, epsilon)
    return Q


def get_optimal_path_cost(Q):
    return - round(max(Q[(0, 0)])) #we didn't count the last penalty


if __name__ == "__main__":
    rewards, actions = read_data()
    Q = learn_action_value_function(rewards, actions)
    print(f'Cost of shortest path should be somewhere around {get_optimal_path_cost(Q)}')
    #full_rewards, full_actions = construct_full_space(rewards)
    #full_Q = learn_action_value_function(full_rewards, full_actions)
