import random
import numpy as np
import numpy.random as rand

class Maze:

    # env_row_dimension = 3
    # env_col_dimension = 3
    # n_runs = 2
    transitions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    blocked_sets = []
    environments = []

    global visited_set
    global blocked_set
    global node_stack

    def is_valid(self,row_index, col_index , visited_set):
        return not (row_index < 0 or col_index < 0 or row_index >= self.env_row_dimension or col_index >= self.env_col_dimension or self.is_visited(row_index, col_index , visited_set))

    def is_visited(self , row_index, col_index, visited_set):
        return [row_index, col_index] in visited_set

    def block( self , row_index, col_index , environment , blocked_set):
        blocked_set.append([row_index, col_index])
        environment[row_index, col_index] = 1
        return

    def block_define(self,row_index, col_index , visited_set , node_stack , blocked_set , environment):
        if rand.randint(0, 9) >= 7:
            self.block(row_index, col_index , environment , blocked_set )
        visited_set.append([row_index, col_index])
        node_stack.append([row_index, col_index])
        return

    def DFS_maze_search(self ,row_index, col_index , visited_set , blocked_set , environment):

        node_stack = [[row_index, col_index]]

        while len(node_stack) > 0:
            curr_row_index, curr_col_index = node_stack[len(node_stack) - 1]
            node_stack.remove(node_stack[len(node_stack) - 1])

            if self.is_valid(curr_row_index, curr_col_index , visited_set):
                self.block_define(curr_row_index, curr_col_index , visited_set , node_stack , blocked_set , environment)
                rand_list = []
                while len(rand_list)!=4:
                    rand_n = rand.randint(0, 4)
                    if rand_n not in rand_list:
                        rand_list.append(rand_n)
                        neig_row, neig_col = np.array([curr_row_index, curr_col_index]) + np.array(self.transitions[rand_n])
                        if self.is_valid(neig_row, neig_col , visited_set):
                            node_stack.append([neig_row, neig_col])

    def __init__(self,env_row_dimension , env_col_dimension, n_runs):
        self.env_row_dimension = env_row_dimension
        self.env_col_dimension = env_col_dimension
        self.n_runs = n_runs

        for i in range(0,n_runs):
            visited_set = []
            blocked_set = []
            environment = np.zeros((env_row_dimension, env_col_dimension), dtype=int)

            start_row_index, start_col_index = random.randint(0, env_row_dimension - 1), random.randint(0, env_col_dimension - 1)
            self.DFS_maze_search(start_row_index, start_col_index , visited_set , blocked_set , environment)

            self.blocked_sets.append(blocked_set)
            self.environments.append(environment)
        return

# s1 = Maze(5,5,1)
# print(s1.blocked_sets)
