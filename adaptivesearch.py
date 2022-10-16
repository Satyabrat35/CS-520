import time
import minheap as mh
from maze import Maze
from visualize import Visualize


class Solution:

    @staticmethod
    def get_manhattan_distance(source, target):
        return abs(target[0] - source[0]) + abs(target[1] - source[1])

    @staticmethod
    def pretty_print(maze_output):
        for output in maze_output:
            print(f"{output[0]}   Time Taken : {output[1]} ,   Expanded nodes size:{output[2]} ")

    def get_path_for_maze(self, m, n, source, target, blocked_cells, h_cost_mat, use_adaptive_h_cost,
                          lower_g_cost=True):

        path_history = [[(-1, -1)] * n for i in range(m)]
        cost_history = [[0] * n for i in range(m)]
        if use_adaptive_h_cost:
            initial_h_cost = h_cost_mat[source[0]][source[1]]
        else:
            initial_h_cost = abs(target[0] - source[0]) + abs(target[1] - source[1])
        heap = [(initial_h_cost, 0, initial_h_cost, source, (-1, -1))]
        path_history[source[0]][source[1]] = (-2, -2)
        visited = set()

        while heap:

            total_cost, g_cost, h_cost, cell, parent = mh.pop(heap)
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
                        if use_adaptive_h_cost:
                            new_h_cost = h_cost_mat[updated_row][updated_col]
                        else:
                            new_h_cost = self.get_manhattan_distance((updated_row, updated_col), target)
                        new_g_cost = g_cost + 1

                        g_cost_comparator = new_g_cost
                        if not lower_g_cost:
                            g_cost_comparator = 0 - g_cost_comparator
                        mh.push(heap, (
                            new_h_cost + new_g_cost, g_cost_comparator, new_h_cost, (updated_row, updated_col), cell))

        path_to_traverse = []
        cell = target
        while cell != source:
            path_to_traverse.append(cell)
            cell = path_history[cell[0]][cell[1]]
            if cell == (-1, -1):
                return [], 0

        path_to_traverse.append(source)
        g_target = cost_history[target[0]][target[1]]

        for i in range(m):
            for j in range(n):
                if use_adaptive_h_cost and (i, j) in visited:
                    h_cost_mat[i][j] = g_target - cost_history[i][j]
                else:
                    h_cost_mat[i][j] = self.get_manhattan_distance((i, j), target)
        return path_to_traverse, len(visited)

    def solve_maze(self, m, n, source, target, physical_map_blocked_cells, mental_map_blocked_cells, h_cost_mat,
                   use_adaptive_h_cost=False,
                   forward=True, lower_g_cost=True, visited_paths=[], expanded_node_count=[]):

        transitions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for transition in transitions:
            updated_row = source[0] + transition[0]
            updated_col = source[1] + transition[1]
            if 0 <= updated_row < m and 0 <= updated_col < n and (
                    updated_row, updated_col) in physical_map_blocked_cells:
                mental_map_blocked_cells.add((updated_row, updated_col))

        if forward:
            path, visited_node_count = self.get_path_for_maze(m, n, source, target, mental_map_blocked_cells,
                                                              h_cost_mat,
                                                              use_adaptive_h_cost, lower_g_cost)
        else:
            path, visited_node_count = self.get_path_for_maze(m, n, target, source, mental_map_blocked_cells,
                                                              h_cost_mat,
                                                              use_adaptive_h_cost, lower_g_cost)
            path.reverse()
        visited_paths.append(path.copy())
        expanded_node_count.append(visited_node_count)
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
                                                                visited_paths, expanded_node_count)

            if is_solvable:
                path_till_blockage.pop()
                path_till_blockage.extend(path_from_new_source)
                return True, path_till_blockage
            return False, []

        return True, path_till_blockage


def run_search_for_given_algorithm(maze, source, target, use_adaptive, forward, lower_g_cost, algorithm):
    maze_output = []
    for blocked_cells_list in maze.blocked_sets:

        # precalculating the h_cost_matrix
        h_cost_matrix = [[0] * col for i in range(row)]
        for i in range(row):
            for j in range(col):
                h_cost_matrix[i][j] = Solution.get_manhattan_distance((i, j), target)

        blocked_cells_set = set()

        for cell in blocked_cells_list:
            blocked_cells_set.add(tuple(cell))

        if source in blocked_cells_set:
            blocked_cells_set.remove(source)
        if target in blocked_cells_set:
            blocked_cells_set.remove(target)

        visited_path = []
        expanded_node_count = []
        start = time.time()
        final_path = Solution().solve_maze(row, col, source, target, blocked_cells_set, set(), h_cost_matrix,
                                           use_adaptive, forward,
                                           lower_g_cost,

                                           visited_path, expanded_node_count)
        end = time.time()

        for arr in visited_path:
            arr.reverse()
        output = (
            algorithm + " maze " + str(len(maze_output) + 1) + " ", end - start, sum(expanded_node_count),
            blocked_cells_set, visited_path, final_path)

        maze_output.append(output)
    Solution.pretty_print(maze_output)

    # Visualizing the last maze output sample
    # sample_visualization = maze_output[-1]
    # blocked_cells_set = sample_visualization[-3]
    # path = sample_visualization[-2]
    # Visualize(blocked_cells_set, path)


def repeated_forward_a_star_lower_g_cost(maze, source, target):
    forward = True
    use_lower_g_cost = True
    use_adaptive = False
    run_search_for_given_algorithm(maze, source, target, use_adaptive, forward, use_lower_g_cost,
                                   "Repeated forward A star with lower g_cost as tie breaker")


def repeated_forward_a_star_higher_g_cost(maze, source, target):
    forward = True
    use_lower_g_cost = False
    use_adaptive = False
    run_search_for_given_algorithm(maze, source, target, use_adaptive, forward, use_lower_g_cost,
                                   "Repeated forward A star with higher g_cost as tie breaker")


def repeated_backward_a_star_higher_g_cost(maze, source, target):
    forward = False
    use_lower_g_cost = False
    use_adaptive = False
    run_search_for_given_algorithm(maze, source, target, use_adaptive, forward, use_lower_g_cost,
                                   "Repeated backward A star with higher g_cost as tie breaker")


def adaptive_a_star_higher_g_cost(maze, source, target):
    forward = True
    use_lower_g_cost = False
    use_adaptive = True
    run_search_for_given_algorithm(maze, source, target, use_adaptive, forward, use_lower_g_cost,
                                   "Adaptive A star with higher g_cost as tie breaker")


if __name__ == "__main__":
    # environment size
    environments = 2
    # Maze Dimension
    row = 101
    col = 101

    # setting the source and target
    source = (0, 0)
    target = (row - 1, col - 1)

    # Generates N number of grids of size row *
    maze = Maze(row, col, environments)

    repeated_forward_a_star_higher_g_cost(maze, source, target)
    repeated_forward_a_star_lower_g_cost(maze, source, target)
    repeated_backward_a_star_higher_g_cost(maze, source, target)
    adaptive_a_star_higher_g_cost(maze, source, target)
