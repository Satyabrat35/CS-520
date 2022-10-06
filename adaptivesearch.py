import math
import heapq


class Solution:
    def networkDelayTime(self, times, n: int, k: int) -> int:

        #
        times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
        n = 4
        k = 2

        adj = {}

        time_taken = [math.inf] * (n + 1)
        time_taken[k] = 0
        time_taken[0] = 0

        for time in times:
            node = time[0]
            if node not in adj:
                adj[node] = []
            adj[node].append((time[1], time[2]))

        parent = [-1] * (n + 1)
        heap = [(0, k, -1)]
        visited = set()

        # print(adj)
        while heap:

            node = heapq.heappop(heap)
            if node[1] not in visited:
                visited.add(node[1])
                parent[node[1]] = node[2]
                time_taken[node[1]] = node[0]

                if node[1] in adj:
                    for neighbour in adj[node[1]]:
                        heapq.heappush(heap, (node[0] + neighbour[1], neighbour[0], node[1]))

        max_time_taken = 0

        for val in time_taken:
            if val == math.inf:
                return -1
            else:
                max_time_taken = max(max_time_taken, val)

        return max_time_taken

    def get_path_for_maze(self, m, n, source, target, blocked_cells, h_cost_mat, use_adaptive_h_cost,
                          lower_g_cost=False):

        path_history = [[(-1, -1)] * n for i in range(m)]
        cost_history = [[0] * n for i in range(m)]
        initial_h_cost = h_cost_mat[source[0]][source[1]]
        heap = [(initial_h_cost, 0, initial_h_cost, source, (-1, -1))]
        path_history[source[0]][source[1]] = (-2, -2)
        visited = set()

        # print(adj)
        # should exit when we find the target?
        while heap:

            total_cost, g_cost, h_cost, cell, parent = heapq.heappop(heap)
            # going to introduce negative g_cost to make heap behave differently in ties
            g_cost = abs(g_cost)
            if cell not in visited:
                visited.add(cell)
                path_history[cell[0]][cell[1]] = parent
                cost_history[cell[0]][cell[1]] = g_cost

                if cell == target:
                    break

                transitions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
                for transition in transitions:
                    updated_row = cell[0] + transition[0]
                    updated_col = cell[1] + transition[1]
                    if 0 <= updated_row < m and 0 <= updated_col < n and (
                            updated_row, updated_col) not in blocked_cells:
                        new_h_cost = h_cost_mat[updated_row][updated_col]
                        # new_h_cost = abs(target[0] - updated_row) + abs(target[1] - updated_col)
                        new_g_cost = g_cost + 1

                        g_cost_comparator = new_g_cost
                        if not lower_g_cost:
                            g_cost_comparator = 0 - g_cost_comparator
                        heapq.heappush(heap, (
                            new_h_cost + new_g_cost, g_cost_comparator, new_h_cost, (updated_row, updated_col), cell))

        path_to_traverse = []
        cell = target
        while cell != source:
            path_to_traverse.append(cell)
            cell = path_history[cell[0]][cell[1]]
            if cell == (-1, -1):
                return []

        path_to_traverse.append(source)

        # print(path_to_traverse)

        # updating the h_mat for visited nodes
        g_target = cost_history[target[0]][target[1]]

        if use_adaptive_h_cost:
            for i in range(row):
                for j in range(col):
                    if (i, j) in visited:
                        h_cost_matrix[i][j] = g_target - cost_history[i][j]

        return path_to_traverse

    def solve_maze(self, m, n, source, target, physical_map_blocked_cells, mental_map_blocked_cells, h_cost_mat,
                   use_adaptive_h_cost=False,
                   forward=True, lower_g_cost=True):

        transitions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for transition in transitions:
            updated_row = source[0] + transition[0]
            updated_col = source[1] + transition[1]
            if 0 <= updated_row < m and 0 <= updated_col < n and (
                    updated_row, updated_col) in physical_map_blocked_cells:
                mental_map_blocked_cells.add((updated_row, updated_col))

        if forward:
            path = self.get_path_for_maze(m, n, source, target, mental_map_blocked_cells, h_cost_mat,
                                          use_adaptive_h_cost, lower_g_cost)
        else:
            path = self.get_path_for_maze(m, n, target, source, mental_map_blocked_cells, h_cost_mat,
                                          use_adaptive_h_cost, lower_g_cost)
            path.reverse()

        path_successfully_traversed_in_physical_map = True
        updated_source = source
        path_till_blockage = []
        if not path:
            return False, []
        else:
            #                 Traverse the actual pysical_map
            parent = source
            for cell in reversed(path):
                if cell in physical_map_blocked_cells:
                    path_successfully_traversed_in_physical_map = False
                    mental_map_blocked_cells.add(cell)
                    updated_source = parent
                    break

                path_till_blockage.append(cell)
                parent = cell
        if not path_successfully_traversed_in_physical_map:
            print("Unsolvable path", path)
            is_solvable, path_from_new_source = self.solve_maze(m, n, updated_source, target,
                                                                physical_map_blocked_cells, mental_map_blocked_cells,
                                                                h_cost_mat, use_adaptive_h_cost, lower_g_cost)

            if is_solvable:
                path_till_blockage.pop()
                path_till_blockage.extend(path_from_new_source)
                return True, path_till_blockage
            return False, []

        return True, path_till_blockage


blocked_cells = set()
blocked_cells.add((0, 2))
blocked_cells.add((1, 1))
# Solution().get_path_for_maze(3, 3, (0, 1), (2, 2), ())
# Solution().get_path_for_maze(3, 3, (0, 1), (2, 2), blocked_cells)
source = (0, 0)
target = (2, 2)
row = 3
col = 3

h_cost_matrix = [[0] * col for i in range(row)]
for i in range(row):
    for j in range(col):
        h_cost_matrix[i][j] = abs(target[0] - i) + abs(target[1] - j)

print(Solution().solve_maze(row, col, source, target, blocked_cells, set(), h_cost_matrix, True, False))

# import numpy as np
# import matplotlib.pyplot as plt
#
# plt.imshow(np.random.random((50,50)))
# plt.colorbar()
# plt.show()
