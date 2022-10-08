import random
import numpy as np
import numpy.random as rand

# defining the start row and col
transitions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

blocked_sets = []

global env_row_dimension
global env_col_dimension
global visited_set
global blocked_set
global node_stack

def is_valid(row_index, col_index):
    global env_row_dimension
    global env_col_dimension
    return not (row_index < 0 or col_index < 0 or row_index >= env_row_dimension or col_index >= env_col_dimension or is_visited(row_index, col_index))

def is_visited(row_index, col_index):
    return [row_index, col_index] in visited_set

def block(row_index, col_index):
    global environment

    blocked_set.append([row_index, col_index])
    environment[row_index, col_index] = 1
    return

def block_define(row_index, col_index):
    global node_stack
    global visited_set

    if rand.randint(0, 9) >= 7:
        block(row_index, col_index)
    visited_set.append([row_index, col_index])
    node_stack.append([row_index, col_index])
    return

def DFS_maze_search(row_index, col_index):
    global env_row_dimension
    global env_col_dimension
    global environment

    node_stack = [[row_index, col_index]]

    while len(node_stack) > 0:
        curr_row_index, curr_col_index = node_stack[len(node_stack) - 1]
        node_stack.remove(node_stack[len(node_stack) - 1])

        if is_valid(curr_row_index, curr_col_index):
            block_define(curr_row_index, curr_col_index)
            rand_list = []
            while len(rand_list)!=4:
                rand_n = rand.randint(0, 4)
                if rand_n not in rand_list:
                    rand_list.append(rand_n)
                    neig_row, neig_col = np.array([curr_row_index, curr_col_index]) + np.array(transitions[rand_n])
                    if is_valid(neig_row, neig_col):
                        node_stack.append([neig_row, neig_col])

def generation_map(row_dimension , col_dimension , n_runs = 1):
    env_row_dimension = row_dimension
    env_col_dimension = col_dimension
    n_runs = n_runs

    for i in range(0,n_runs):
        visited_set = []
        blocked_set = []
        node_stack = []
        environment = np.zeros((env_row_dimension, env_col_dimension), dtype=int)

        start_row_index, start_col_index = random.randint(0, env_row_dimension - 1), random.randint(0, env_col_dimension - 1)
        DFS_maze_search(start_row_index, start_col_index)

        blocked_sets.append(blocked_set)

    return blocked_sets

generation_map(3,3,1)