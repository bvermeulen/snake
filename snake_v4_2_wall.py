#!/usr/bin/env python
'''     python version 3.6

        This module contains following Classes:
        - WallObject

        Functions:
        - init_walls
        - plotlist_walls

        Author: Bruno Vermeulen
        bruno_vermeulen2001@yahoo.com
'''
from snake_v4_2_tools import GREY, ORANGE, Setup, PlotObject

''' initialise the configuration paramaters
'''
setup = Setup()  # window setup is default False


class WallObject:
    '''   Definition of wall object with following methods:
          - __init__
          - plot_wall
          - __repr__
    '''
    def __init__(self, cell, vertices, color):
        self.color = color
        self.brick = []

        for i in range(len(vertices) - 1):
            a_x = vertices[i][0]
            a_y = vertices[i][1]
            b_x = vertices[i+1][0]
            b_y = vertices[i+1][1]
            assert (a_x >= 0 and a_x <= setup.cells_x-1), \
                "wall must be inside the action window - x violation"
            assert (a_y >= 0 and a_y <= setup.cells_y-1), \
                "wall must be inside the action window - y violation"

            range_x = b_x - a_x
            range_y = b_y - a_y
            steps = max(abs(range_x), abs(range_y))
            for step in range(steps):
                    i = a_x + round(step / steps * range_x)
                    j = a_y + round(step / steps * range_y)
                    self.brick.append((i, j))
                    cell[i][j].content = 'wall'
                    cell[i][j].plot = True

    def plot(self, plotlist):
        '''  method to plot the wall
        '''
        for i in range(len(self.brick)):
            plotlist.append(PlotObject(origin=setup.a_w_o,
                            i=self.brick[i][0], j=self.brick[i][1],
                            dimension=(setup.cell_dim_x, setup.cell_dim_y),
                            size=setup.brick_size,
                            fcolor=self.color,
                            ocolor='',
                            owidth=0,
                            shape='rectangle'))

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


def init_walls(cell):
    '''  initialise the wall objects
    '''
    global wall
    wall = []
    wall.append(WallObject(cell, setup.wall_v[0], GREY))
    wall.append(WallObject(cell, setup.wall_v[1], ORANGE))

    return wall


def plotlist_walls(plotlist):
    '''  set the list of plot points for all init_walls
    '''
    for i in range(len(wall)):
        wall[i].plot(plotlist)
