#!/usr/bin/env python
'''     python version 3.6                      

        This module contains following Classes:
        - WallObject

        Functions:
        - init_walls
                                               
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
'''
from tkinter import Label

from snake_v4_tools import (BLACK, WHITE, RED, GREY, YELLOW, BLUE, ORANGE, GREEN, LWIDTH, 
                            SnakeSetup, randomvector, hex_color
                           )

''' initialise the configuration paramaters
'''
setup = SnakeSetup() # window setup is default False

class WallObject:
    ''' Definition of wall object with following methods:
        - __init__
        - plot_wall
        - __repr__
    '''
    def __init__(self, cell_p, vertices, color):
        global cell
        cell = cell_p
        self.color    = color
        self.brick    = []

        for i in range(len(vertices)-1):
            a_x = vertices[i][0]
            a_y = vertices[i][1]
            b_x = vertices[i+1][0]
            b_y = vertices[i+1][1]
            assert (a_x >= 0 and a_x <= setup.cells_x-1), "wall must be inside the action window - x violation"
            assert (a_y >= 0 and a_y <= setup.cells_y-1), "wall must be inside the action window - y violation"
            
            range_x = b_x - a_x
            range_y = b_y - a_y
            steps = max(abs(range_x), abs(range_y))
            for step in range(steps):
                    x = a_x + round(step/ steps * range_x)
                    y = a_y + round(step/ steps * range_y)
                    self.brick.append((int(x), int(y)))
                    cell[int(x)][int(y)].content = 'wall'

    def plot_wall(self, aw):
        ''' method to plot the wall
        '''
        for i in range(len(self.brick)):
            pos_x = int(setup.a_w_o[0] + self.brick[i][0]*setup.cell_dim_x)
            pos_y = int(setup.a_w_o[1] + self.brick[i][1]*setup.cell_dim_y)
            aw.create_rectangle( pos_x, pos_y, pos_x + setup.brick_size[0], pos_y + setup.brick_size[1], \
                                 fill = hex_color(self.color), width = 0 )

    def __repr__(self):
        ''' method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k,v in self.__dict__.items()) 
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
        return s

def init_walls(cell_p):
    ''' initialise the wall objects
    '''
    global cell
    cell = cell_p
    wall = []
    wall.append(WallObject(cell, setup.wall_v[0], GREY))
    wall.append(WallObject(cell, setup.wall_v[1], ORANGE))

    return wall

