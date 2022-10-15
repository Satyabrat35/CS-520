import time

import pandas as pd
import pygame as pygame
import numpy as np

# Grid boundaries
GRID_LENGTH = 800
GRID_WIDTH = 800
GRID_ROWS = 5
GRID_COLS = 5
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

#SLEEP
SLEEP_TIME = 1

# Grid Display Setup
gridDisplay = pygame.display.set_mode((GRID_LENGTH, GRID_WIDTH))
pygame.display.get_surface().fill(SURFACE_COLOR)
pygame.display.set_caption("Path Traversal Grid")

#  Global set parameters that needs to be updated
blocked_cells = {(0, 4), (3, 1), (1, 4), (4, 2), (1, 0)}  # get this info from the passed values
path_followed = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
                 [(0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)], [(1, 3), (2, 3), (2, 4), (3, 4), (4, 4)]]

# initializing the matrix with blocked cells
matrix = np.zeros(((GRID_ROWS, GRID_COLS)), dtype=int)
for x in blocked_cells:
    matrix[x[0], x[1]] = 1
# or you can get the environment passed

clock = pygame.time.Clock()
run = True


def createSquare(x, y, color):
    pygame.draw.rect(gridDisplay, color, [x, y, GRID_NODE_LENGTH, GRID_NODE_WIDTH])


def rescale_to_grid(path):
    if len(path) > 0:
        path = np.array(path) * int(GRID_NODE_LENGTH)
        add_value = int(int(GRID_NODE_LENGTH) / 2)
        path = path + add_value
        return path


def flipp_path(path):
    if len(path) > 0:
        for x in path:
            temp = x[0]
            x[0] = x[1]
            x[1] = temp
        return path


def plotlines(path_followed):
    point_of_recalibration = []
    final_path = []
    for i in range(len(path_followed)):
        path = path_followed[i]
        rescaled_path = rescale_to_grid(path)

        if i != len(path_followed) - 1:
            # path respective code
            recab_point = path_followed[i + 1][0]
            point_of_recalibration.append(recab_point)

            # visualization respective code
            flipped_path = flipp_path(rescaled_path)
            # drawing aalines flips path so we are pre flipping the path so we get the correct path on the graph
            # pygame.draw.lines(gridDisplay, BLUE, False, path_followed[i], int(GRID_NODE_LENGTH/5))
            pygame.draw.aalines(gridDisplay, BLUE, False, flipped_path, 1)

            if len(point_of_recalibration) > 0:
                recab_rescaled = rescale_to_grid(point_of_recalibration)
                recab_flipped = flipp_path(recab_rescaled)
                for x in recab_flipped:
                    pygame.draw.circle(gridDisplay, RED, x, 2)

        else:
            # path respective code
            recab_point = (-9, -9)

            # visualization respective code
            # flipped_path = flipp_path(rescaled_path)
            # drawing aalines flips path so we are pre flipping the path so we get the correct path on the graph
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
            final_rescaled_path = rescale_to_grid(final_path)
            final_flipped_path = flipp_path(final_rescaled_path)
            pygame.draw.aalines(gridDisplay, GREEN, False, final_flipped_path, 1)

        pygame.display.update()
        time.sleep(SLEEP_TIME)
        if ((i % GRID_ROWS == 0) and (i != len(path_followed)-1)):
            visualizeGrid()
        if i == len(path_followed) - 2:
            visualizeGrid()

def visualizeGrid():
    y = 0  # we start at the top of the screen
    for row in matrix:
        x = 0  # for every row we start at the left of the screen again
        for item in row:
            if item == 0:
                createSquare(x, y, WHITE)
            else:
                createSquare(x, y, BLACK)
            x += GRID_NODE_LENGTH  # for ever item/number in that row we move one "step" to the right
        y += GRID_NODE_WIDTH  # for every new row we move one "step" downwards
    pygame.display.update()
    return


visualizeGrid()
plotlines(path_followed)

while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pass

"""
blocked_cells = {(0, 4), (3, 1), (1, 4), (4, 2), (1, 0)}
source = (0,0)
target = (4,4)
solution = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)], [(0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)], [(1, 3), (2, 3), (2, 4), (3, 4), (4, 4)]]

"""
