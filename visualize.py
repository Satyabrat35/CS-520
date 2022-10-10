import pandas as pd
import pygame as pygame
import numpy as np

GRID_LENGTH = 808
GRID_WIDTH = 808
GRID_ROWS = 4
GRID_COLS = 4
GRID_NODE_LENGTH = GRID_LENGTH/GRID_ROWS
GRID_NODE_WIDTH = GRID_WIDTH/GRID_COLS

SURFACE_COLOR = (0, 200, 200)
GREY = (211, 211, 211)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

gridDisplay = pygame.display.set_mode((GRID_LENGTH, GRID_WIDTH))
pygame.display.get_surface().fill(SURFACE_COLOR)
pygame.display.set_caption("Path Traversal Grid")

matrix = np.random.randint(0, 2, (GRID_ROWS, GRID_COLS), dtype=int)

clock = pygame.time.Clock()
run = True


def createSquare(x, y, color):
    pygame.draw.rect(gridDisplay, color, [x, y, GRID_NODE_LENGTH, GRID_NODE_WIDTH])


def rescale_to_grid(path):
    print(path)
    print("")
    path = np.array(path)*int(GRID_NODE_LENGTH)
    print(path)
    print("")
    add_value = int(int(GRID_NODE_LENGTH)/2)
    path = path + add_value
    print(pd.DataFrame(path))
    return path


def plotlines(path_followed):
    for i in range(len(path_followed)):
        path_followed[i] = rescale_to_grid(path_followed[i])
        if i != len(path_followed) - 1:
            # pygame.draw.lines(gridDisplay, BLUE, False, path_followed[i], int(GRID_NODE_LENGTH/5))
            pygame.draw.aalines(gridDisplay, BLUE, False, path_followed[i], 1)
        else:
            # pygame.draw.lines(gridDisplay, GREEN, False, path_followed[i], int(GRID_NODE_LENGTH/3))
            pygame.draw.aalines(gridDisplay, GREEN, False, path_followed[i], 1)
    pygame.display.update()


def visualizeGrid():
    y = 0  # we start at the top of the screen
    for row in matrix:
        x = 0  # for every row we start at the left of the screen again
        for item in row:
            if item == 0:
                createSquare(x, y, (255, 255, 255))
            else:
                createSquare(x, y, (0, 0, 0))

            x += GRID_NODE_LENGTH  # for ever item/number in that row we move one "step" to the right
        y += GRID_NODE_WIDTH  # for every new row we move one "step" downwards

    plotlines(path_followed)

    pygame.display.update()
    return

path_followed = [[[0,0],[0,1],[0,2]],
    [[0,0],[1,0],[2,0]],
    [[0,0],[1,0],[1,1],[2,1],[2,2],[2,3],[3,3]]]

visualizeGrid()

while run:

    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pass
# ps = pygameSetup()
# ps.createDisplay()
# ps.vis
