import heapq
import time

from maze import Maze


class Solution:

    def get_manhattan_distance(self, source, target):
        return abs(target[0] - source[0]) + abs(target[1] - source[1])

    def get_path_for_maze(self, m, n, source, target, blocked_cells, h_cost_mat, use_adaptive_h_cost,
                          lower_g_cost=True):
        maze_start_time = time.time()
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
                            updated_row, updated_col) not in blocked_cells and (
                            updated_row, updated_col) not in visited:
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
        maze_end_time = time.time()

        print(f"time taken to solve maze for {len(visited)} is {maze_end_time - maze_start_time}")

        adaptive_time_start = time.time()
        for i in range(row):
            for j in range(col):
                if use_adaptive_h_cost and (i, j) in visited:
                    h_cost_matrix[i][j] = g_target - cost_history[i][j]
                else:
                    h_cost_matrix[i][j] = abs(target[0] - i) + abs(target[1] - j)

        adaptive_time_end = time.time()
        print(f"time taken for adaptive update is {adaptive_time_end - adaptive_time_start}")
        return path_to_traverse

    def solve_maze(self, m, n, source, target, physical_map_blocked_cells, mental_map_blocked_cells, h_cost_mat,
                   use_adaptive_h_cost=False,
                   forward=True, lower_g_cost=True, visited_paths=[]):

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
        visited_paths.append(path.copy())
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
            # print("Unsolvable path", path)
            is_solvable, path_from_new_source = self.solve_maze(m, n, updated_source, target,
                                                                physical_map_blocked_cells, mental_map_blocked_cells,
                                                                h_cost_mat, use_adaptive_h_cost, forward, lower_g_cost,
                                                                visited_paths)

            if is_solvable:
                path_till_blockage.pop()
                path_till_blockage.extend(path_from_new_source)
                return True, path_till_blockage
            return False, []

        return True, path_till_blockage


if __name__ == "__main__":
    # row = 5
    # col = 5
    #
    # source = (4, 2)
    # target = (row - 1, col - 1)
    #
    # h_cost_matrix = [[0] * col for i in range(row)]
    # for i in range(row):
    #     for j in range(col):
    #         h_cost_matrix[i][j] = abs(target[0] - i) + abs(target[1] - j)
    #
    # visited_path = []
    #
    # blocked_cells_set = {(1, 2), (2, 2), (2, 3), (3, 2), (3, 3), (4,3)}
    #
    # print(Solution().solve_maze(row, col, source, target, blocked_cells_set, set(), h_cost_matrix, True, True, True, visited_path))
    # print(visited_path)

    row = 101
    col = 101

    source = (0, 0)
    target = (row - 1, col - 1)

    h_cost_matrix = [[0] * col for i in range(row)]
    for i in range(row):
        for j in range(col):
            h_cost_matrix[i][j] = abs(target[0] - i) + abs(target[1] - j)

    blocked_cells_set = set()

    for cell in Maze(row, col, 1).blocked_sets[0]:
        blocked_cells_set.add(tuple(cell))

    if source in blocked_cells_set:
        blocked_cells_set.remove(source)
    if target in blocked_cells_set:
        blocked_cells_set.remove(target)

    visited_path = []
    # print("blocked path", len(blocked_cells_set), blocked_cells_set)
    # blocked_cells_set = {(1, 2), (2, 2), (2, 3), (3, 2), (3, 3), (4,3)}
    # source = (4, 2)

    start = time.time()
    Solution().solve_maze(row, col, source, target, blocked_cells_set, set(), h_cost_matrix, False, True, False,
                          visited_path)
    end = time.time()
    print(" Forward Repeated A star time", end - start)
    # print(visited_path)
    # for arr in visited_path:
    #     arr.reverse()
    # print(visited_path)

    h_cost_matrix = [[0] * col for i in range(row)]
    for i in range(row):
        for j in range(col):
            h_cost_matrix[i][j] = abs(target[0] - i) + abs(target[1] - j)

    start = time.time()
    Solution().solve_maze(row, col, source, target, blocked_cells_set, set(), h_cost_matrix, True, True, False,
                          visited_path)
    end = time.time()
    print(" Adaptive A star time", end - start)
