import time
import pandas as pd
import pygame as pygame
import numpy as np


class Visualize:
    # Grid boundaries
    GRID_LENGTH = 808
    GRID_WIDTH = 808
    GRID_ROWS = 101
    GRID_COLS = 101
    GRID_NODE_LENGTH = GRID_LENGTH / GRID_ROWS
    GRID_NODE_WIDTH = GRID_WIDTH / GRID_COLS

    # grid Colors
    SURFACE_COLOR = (0, 200, 200)
    GREY = (211, 211, 211)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # SLEEP
    SLEEP_TIME = 0.1

    # Grid Display Setup
    gridDisplay = pygame.display.set_mode((GRID_LENGTH, GRID_WIDTH))
    pygame.display.get_surface().fill(SURFACE_COLOR)
    pygame.display.set_caption("Path Traversal Grid")

    # initializing the matrix with blocked cells
    matrix = np.zeros((GRID_ROWS, GRID_COLS), dtype=int)
    # or you can get the environment passed

    clock = pygame.time.Clock()

    def create_square(self, x, y, color):
        pygame.draw.rect(self.gridDisplay, color, [x, y, self.GRID_NODE_LENGTH, self.GRID_NODE_WIDTH])

    def rescale_to_grid(self, path):
        if len(path) > 0:
            path = np.array(path) * int(self.GRID_NODE_LENGTH)
            add_value = int(int(self.GRID_NODE_LENGTH) / 2)
            path = path + add_value
            return path

    def flipp_path(self, path):
        if len(path) > 0:
            for x in path:
                temp = x[0]
                x[0] = x[1]
                x[1] = temp
            return path

    def plotlines(self, path_followed):
        point_of_recalibration = []
        final_path = []
        for i in range(len(path_followed)):
            path = path_followed[i]
            rescaled_path = self.rescale_to_grid(path)

            if i != len(path_followed) - 1:
                # path respective code
                recab_point = path_followed[i + 1][0]
                point_of_recalibration.append(recab_point)

                # visualization respective code
                flipped_path = self.flipp_path(rescaled_path)
                # drawing aalines flips path, so we are pre flipping the path, so we get the correct path on the graph
                # pygame.draw.lines(gridDisplay, BLUE, False, path_followed[i], int(GRID_NODE_LENGTH/5))
                pygame.draw.aalines(self.gridDisplay, self.BLUE, False, flipped_path, 1)

            else:
                # path respective code
                recab_point = (-9, -9)

                # visualization respective code
                # flipped_path = flipp_path(rescaled_path)
                # drawing aalines flips path, so we are pre flipping the path so we get the correct path on the graph
                # pygame.draw.lines(gridDisplay, GREEN, False, path_followed[i], int(GRID_NODE_LENGTH/3))
                # pygame.draw.aalines(gridDisplay, GREEN, False, flipped_path, 1)

            for j in path_followed[i]:
                if not (j == path_followed[i][0] and len(final_path) > 0):
                    if j == recab_point:
                        final_path.append(j)
                        break
                    else:
                        final_path.append(j)

            if len(final_path) > 0:
                final_rescaled_path = self.rescale_to_grid(final_path)
                final_flipped_path = self.flipp_path(final_rescaled_path)
                pygame.draw.aalines(self.gridDisplay, self.GREEN, False, final_flipped_path, 1)

            if len(point_of_recalibration) > 0:
                recab_rescaled = self.rescale_to_grid(point_of_recalibration)
                recab_flipped = self.flipp_path(recab_rescaled)
                for x in recab_flipped:
                    pygame.draw.circle(self.gridDisplay, self.RED, x, 2)

            pygame.display.update()
            time.sleep(self.SLEEP_TIME)
            if ((i % 10 == 0) and (i != len(path_followed) - 1)):
                self.visualize_grid()
            if i == len(path_followed) - 2:
                self.visualize_grid()

        return

    def visualize_grid(self):
        y = 0  # we start at the top of the screen
        for row in self.matrix:
            x = 0  # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.create_square(x, y, self.WHITE)
                else:
                    self.create_square(x, y, self.BLACK)
                x += self.GRID_NODE_LENGTH  # forever item/number in that row we move one "step" to the right
            y += self.GRID_NODE_WIDTH  # for every new row we move one "step" downwards
        pygame.display.update()

    def __init__(self, blocked_cells, path_followed, source = None, target = None):

        for x in blocked_cells:
            self.matrix[x[0], x[1]] = 1

        self.visualize_grid()
        self.plotlines(path_followed)

        run = True
        while run:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pass
        return


blocked_cells = {(0, 4), (3, 1), (1, 4), (4, 2), (1, 0)}
path_followed = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
                 [(0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)], [(1, 3), (2, 3), (2, 4), (3, 4), (4, 4)]]
# S1 = Visualize(blocked_cells , path_followed)