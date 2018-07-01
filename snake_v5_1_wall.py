#!/usr/bin/env python
'''     python version 3.6

        This module contains following Classes:
        - WallObject

        Functions:
        - init_walls
        - mouse_action_wall
        - plot_walls
        - set_color_wall
        - clear_wall_selection

        Author: Bruno Vermeulen
        bruno_vermeulen2001@yahoo.com
'''
from snake_v5_1_tools import (GREY, ORANGE, LIGHTGREY, BLACK, YELLOW, BLUE,
                              GREEN, LWIDTH, Setup, PlotObject, Tools)

''' initialise the configuration paramaters
'''
global walls, wall_is_selected
setup = Setup()  # window setup is default False
tools = Tools()
walls = []
wall_is_selected = False


class WallObject:
    '''   Definition of wall object with following methods:
          - __init__
          - build_bricks
          - remove_bricks
          - select_wall
          - delete_vertex
          - add_vertex
          - plot
          - __repr__
    '''
    def __init__(self, cell, vertices, color):
        '''  initialise a wall element
        '''
        self.color = color
        self.vertices = vertices
        self.bricks = []
        self.select = False
        self.build_bricks(cell)

    def build_bricks(self, cell):
        '''  method to build the bricks of the wall given vertices and set
             the cell environment
        '''
        if len(self.vertices) == 1:
            i, j = self.vertices[0][0], self.vertices[0][1]
            self.bricks.append((i, j))
            cell[i][j].content = 'wall'
            cell[i][j].plot = True

        else:
            for i, vertex in enumerate(self.vertices[:-1]):
                a_x = vertex[0]
                a_y = vertex[1]
                b_x = self.vertices[i+1][0]
                b_y = self.vertices[i+1][1]
                assert (a_x >= 0 and a_x <= setup.cells_x-1), \
                    "wall must be inside the action window - x violation"
                assert (a_y >= 0 and a_y <= setup.cells_y-1), \
                    "wall must be inside the action window - y violation"

                range_x, range_y = (b_x - a_x), (b_y - a_y)
                steps = max(abs(range_x), abs(range_y))
                for step in range(steps+1):
                    i = a_x + round(step / steps * range_x)
                    j = a_y + round(step / steps * range_y)
                    self.bricks.append((i, j))
                    cell[i][j].content = 'wall'
                    cell[i][j].plot = True

    def remove_bricks(self, cell):
        '''  method to delete the wall and clear the environment cell
        '''
        for brick in self.bricks:
            cell[brick[0]][brick[1]].content = 'empty'
            cell[brick[0]][brick[1]].plot = True
        self.bricks = []

    def select_wall(self, select_choice):
        '''  method to select or deselect wall, selection is boolean
        '''
        assert (type(select_choice) is bool), "select choice must be boolean"
        self.select = select_choice

        return self.select

    def delete_vertex(self, grid, cell):
        '''  method to delete vertex point "grid" and rebuild the wall
        '''
        self.remove_bricks(cell)
        del self.vertices[self.vertices.index(grid)]
        self.build_bricks(cell)

    def add_vertex(self, grid, cell):
        '''  method to add vertex point "grid" and rebuild the walls
        '''
        if grid not in self.vertices:
            dist_first = (self.vertices[0][0] - grid[0])**2 + \
                         (self.vertices[0][1] - grid[1])**2
            dist_last = (self.vertices[-1][0] - grid[0])**2 + \
                        (self.vertices[-1][1] - grid[1])**2

            if dist_first < dist_last:
                self.vertices.insert(0, grid)

            else:
                self.vertices.append(grid)
            self.build_bricks(cell)

        else:
            print('cannot create 2 vertices at the same place')

    def plot(self, plotlist, wall_setup):
        '''  method to plot the wall
        '''
        if wall_setup:
            if self.select:
                brick_color = YELLOW
                vertex_color = BLUE
            else:
                brick_color = GREY
                vertex_color = ORANGE
            shape = 'oval'

        else:
            brick_color = self.color
            shape = 'rectangle'

        for brick in self.bricks:
            plotlist.append(PlotObject(origin=setup.a_w_o,
                            i=brick[0], j=brick[1],
                            dimension=(setup.cell_dim_x, setup.cell_dim_y),
                            size=setup.brick_size,
                            fcolor=brick_color,
                            ocolor='',
                            owidth=0,
                            shape=shape))

        if wall_setup:
            for vertex in self.vertices:
                plotlist.append(PlotObject(origin=setup.a_w_o,
                                i=vertex[0], j=vertex[1],
                                dimension=(setup.cell_dim_x, setup.cell_dim_y),
                                size=setup.brick_size,
                                fcolor=vertex_color,
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
    # walls.append(WallObject(cell, setup.wall_v[0], GREY))
    walls.append(WallObject(cell, setup.wall_v[1], BLUE))
    return walls


def mouse_action_wall(mouse_event, double_click, cell):
    '''  defines the options to create and delete wall elements
    '''
    global wall_is_selected

    grid = (int((mouse_event.x - setup.a_w_o[0]) / setup.cell_dim_x),
            int((mouse_event.y - setup.a_w_o[1]) / setup.cell_dim_y))

    grid_inside = (grid[0] < setup.cells_x and grid[0] >= 0) and \
                  (grid[1] < setup.cells_y and grid[1] >= 0)

    for index, wall in enumerate(walls):
        if grid in wall.bricks and mouse_event.num == 1 \
           and double_click and not wall_is_selected:
            print('wall is selected ...', grid)
            wall_is_selected = wall.select_wall(True)

        elif mouse_event.num == 3 and wall.select:
            wall_is_selected = wall.select_wall(False)

        elif wall.select and grid in wall.vertices and double_click:
            wall.delete_vertex(grid, cell)
            if wall.vertices == []:
                del walls[index]
                wall_is_selected, double_click = False, False
                #  disable double_click so point is not created again below

        elif grid_inside and wall.select and mouse_event.num == 1 \
                and not double_click:
            wall.add_vertex(grid, cell)

    if grid_inside and not wall_is_selected and mouse_event.num == 1 \
            and double_click:
        _ = []
        _.append(grid)
        walls.append(WallObject(cell, _, GREEN))
        wall_is_selected, walls[-1].select_wall(True)


def plot_walls(aw, bcolor, wall_setup):
    '''  function to plot walls in either setup case or normal
    '''
    plotlist = []
    for wall in walls:
        wall.plot(plotlist, wall_setup)

    if wall_setup:
        bgcolor = LIGHTGREY

    else:
        bgcolor = BLACK

    w = tools.plot_window(canvas=aw, rectangle=setup.r_action_window,
                          background=bgcolor, border_color=bcolor,
                          border_width=LWIDTH, plotlist=plotlist)

    return w


def set_color_wall(color):
    '''  set the color of the wall
    '''
    for wall in walls:
        if wall.select:
            if color in setup.color_buttons:
                wall.color = color
            else:
                color = wall.color

    return color


def clear_wall_selection():
    '''  clears the wall snake_selection
    '''
    global wall_is_selected
    for wall in walls:
        wall_is_selected = wall.select_wall(False)
