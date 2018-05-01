#!/usr/bin/env python
'''     python version 3.6                      

        This module contains following Classes:
        - SnakeObject
        - WallObject

        Functions:
        - init_walls
        - init_cells
        - plot_grid_wall
        - mouse_pressed
        - move_randomly
        - delete_snake
        - plot_snakes
        - reset_snakes
        - snake_select
        - plot_monitor
        - plot_status 
        - display_text
        - show_vision
        - eye
                                               
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
'''
import re
import sys 
import os
import random
from tkinter import Label
from PIL import Image, ImageTk

from snake_tk_tools_v2 import (BLACK, WHITE, RED, GREY, YELLOW, BLUE, ORANGE, GREEN, LWIDTH, 
                               SnakeSetup, randomvector, hex_color
                              )

''' initialise the configuration paramaters
'''
setup = SnakeSetup() # window setup is default False
snake_number = 0
snake = []
snake_select = 1
        
class SnakeObject:
    ''' definition of snake object and following methods:
        - __init__
        - move()
        - move_left()
        - move_right()
        - plot_snake()
        - view() out vision
        - __repr__ 
    '''
    def __init__(self, pos, vect, length, snake_color):
        # set the position of head
        self.head   = pos
        self.vector = vect
        self.length = length
        self.color  = snake_color
        x   = self.head[0]
        y   = self.head[1]        
        print ('head is:',self.head)
        if cell[x][y].content != 'wall':
            cell[x][y].content = 'snake'

        # create tail of length (note we start at 0)
        self.tail = []
        for i in range(length):
            x = (pos[0]-vect[0])%setup.cells_x
            y = (pos[1]-vect[1])%setup.cells_y
            self.tail.append((x,y))
            if cell[x][y].content != 'wall':
                cell[x][y].content = 'snake'
            print (i, vect, self.tail[i])
            vect = (vect[0] + self.vector[0], vect[1] + self.vector[1])   

    def move(self):
        ''' method to move snake straight and update cell status
        '''
        # set the new head position and check if this is a wall
        x   = (self.head[0] + self.vector[0]) % setup.cells_x
        y   = (self.head[1] + self.vector[1]) % setup.cells_y

        if cell[x][y].content == 'wall':
            print('unable to move - hit wall')
            move = False

        else:
            # update environment: previous last tail element to 'empty' unless this  is a wall
            if cell[self.tail[self.length-1][0]][self.tail[self.length-1][1]].content != 'wall':    
                cell[self.tail[self.length-1][0]][self.tail[self.length-1][1]].content = 'empty' 

            # move up the snake towards the head, start at the end        
            for i in range(self.length-1, 0,-1):
                self.tail[i] = self.tail[i-1]
            self.tail[0] = self.head
            self.head = (x, y)

            # set the new head position 
            cell[x][y].content = 'snake'
            move = True

        return move
            
    def move_left(self):
        ''' depending on vector select next position (relative to head) steering left
        '''
        if   self.vector == ( 1, 1):
           s = ( 1, 0)
        elif self.vector == ( 0, 1):
           s = ( 1, 1)
        elif self.vector == (-1, 1):
           s = ( 0, 1)
        elif self.vector == (-1, 0):
           s = (-1, 1)
        elif self.vector == (-1,-1):
           s = (-1, 0)
        elif self.vector == ( 0,-1):
           s = (-1,-1)
        elif self.vector == ( 1,-1):
           s = ( 0,-1)
        elif self.vector == ( 1, 0):
           s = ( 1,-1)
        self.vector = (s[0], s[1])

    def move_right(self):
        ''' depending on vector select next position (relative to head) steering right
        '''
        if   self.vector == ( 1, 1):
           s = ( 0, 1)
        elif self.vector == ( 0, 1):
           s = (-1, 1)
        elif self.vector == (-1, 1):
           s = (-1, 0)
        elif self.vector == (-1, 0):
           s = (-1,-1)
        elif self.vector == (-1,-1):
           s = ( 0,-1)
        elif self.vector == ( 0,-1):
           s = ( 1,-1)
        elif self.vector == ( 1,-1):
           s = ( 1, 0)
        elif self.vector == ( 1, 0):
           s = ( 1, 1)
        self.vector = (s[0], s[1])

    def plot_snake(self, aw):
        ''' method to plot the snake
        '''
        _headcolor = RED
        # first plot the head        
        pos_x = int(setup.a_w_o[0] + self.head[0] * setup.cell_dim_x)
        pos_y = int(setup.a_w_o[1] + self.head[1] * setup.cell_dim_y)
        aw.create_oval(pos_x, pos_y, pos_x + setup.cell_dim_x,  \
                       pos_y + setup.cell_dim_y, outline = hex_color(_headcolor), width = 2)

        # then plot the tail
        for i in range(self.length):
           pos_x = int(setup.a_w_o[0] + self.tail[i][0] * setup.cell_dim_x)
           pos_y = int(setup.a_w_o[1] + self.tail[i][1] * setup.cell_dim_y)
           aw.create_oval(pos_x, pos_y, pos_x + setup.cell_dim_x, pos_y + setup.cell_dim_y, \
                          fill = hex_color(self.color))
      
    def view(self):
        ''' method to obtain view looking from the head in the vector direction obtaining: Left View (LV), 
            Front View (FV) and Right View (RV) in case eye observes wall object it increases the value 
            giving a 3 component vector (LV, FV, RV)
        '''
        if   self.vector == ( 1, 0):
            LV = eye(self.head, setup.view_field[-1 % 8])
            FV = eye(self.head, setup.view_field[ 0 % 8])
            RV = eye(self.head, setup.view_field[ 1 % 8])
        elif self.vector == ( 1, 1):
            LV = eye(self.head, setup.view_field[ 0 % 8])
            FV = eye(self.head, setup.view_field[ 1 % 8])
            RV = eye(self.head, setup.view_field[ 2 % 8])
        elif self.vector == ( 0, 1):
            LV = eye(self.head, setup.view_field[ 1 % 8])
            FV = eye(self.head, setup.view_field[ 2 % 8])
            RV = eye(self.head, setup.view_field[ 3 % 8])
        elif self.vector == (-1, 1):
            LV = eye(self.head, setup.view_field[ 2 % 8])
            FV = eye(self.head, setup.view_field[ 3 % 8])
            RV = eye(self.head, setup.view_field[ 4 % 8])
        elif self.vector == (-1, 0):
            LV = eye(self.head, setup.view_field[ 3 % 8])
            FV = eye(self.head, setup.view_field[ 4 % 8])
            RV = eye(self.head, setup.view_field[ 5 % 8])
        elif self.vector == (-1,-1):
            LV = eye(self.head, setup.view_field[ 4 % 8])
            FV = eye(self.head, setup.view_field[ 5 % 8])
            RV = eye(self.head, setup.view_field[ 6 % 8])
        elif self.vector == ( 0,-1):
            LV = eye(self.head, setup.view_field[ 5 % 8])
            FV = eye(self.head, setup.view_field[ 6 % 8])
            RV = eye(self.head, setup.view_field[ 7 % 8])
        elif self.vector == ( 1,-1):
            LV = eye(self.head, setup.view_field[ 6 % 8])
            FV = eye(self.head, setup.view_field[ 7 % 8])
            RV = eye(self.head, setup.view_field[ 8 % 8])
        else:
            assert False, "Something wrong here, check code"
        
        v = (LV, FV, RV)
        return v
 
    def __repr__(self):
        ''' method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k,v in self.__dict__.items()) 
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
        return s

class WallObject:
    ''' Definition of wall object with following methods:
        - __init__
        - plot_wall
        - __repr__
    '''
    def __init__(self, vertices, color):
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

class Cell:
    ''' class Cell to represent the play environment and status with following methods: 
        - __init__
        - __repr__
    '''
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content
        assert self.content in ['empty', 'wall', 'snake'], "content is limited to empty, wall or snake"

    def __repr__(self):
        ''' method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k,v in self.__dict__.items()) 
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
        return s

def init_walls():
    ''' initialise the wall objects
    '''
    global wall
    wall = []
    wall.append(WallObject(setup.wall_v[0], GREY))
    wall.append(WallObject(setup.wall_v[1], ORANGE))

def init_cells():
    ''' initialise the cells to capture status of the field
        Cell. cell.x and cell.y are the monitor cell positions
    '''
    global cell
    cell = [[Cell( \
                  int( setup.m_w_o[0] + x * setup.m_dim_x), \
                  int( setup.m_w_o[1] + y * setup.m_dim_y), \
                  'empty') for y in range(setup.cells_y)] for x in range(setup.cells_x)]
    return

def plot_grid_walls(aw, border_color):
    ''' draw action window border - there are two color (blue and organge)
        and the walls
    '''
    aw.create_rectangle( setup.r_action_window, outline = hex_color(border_color), \
                         fill = 'black', width = LWIDTH)
    for i in range(len(wall)):
        wall[i].plot_wall(aw)

def mouse_pressed(grid):
    ''' if mouse is pressed in the action window then create a snake and plot it, or if the snake
        already exists then delete the snake
    '''
    global snake_number, snake_select # explicitly tell the function to use the global variables!
    create = True
    mouse_action_done = False

    if grid[0] < setup.cells_x and grid[0] >= 0 and grid[1] < setup.cells_y and grid[1] >= 0:
        i = 0
        while i < snake_number and create == True:
            ''' check if snake already exist 
            '''
            if grid[0] == snake[i].head[0] and grid[1] == snake[i].head[1]:
                delete_snake(i)
                create = False
            i += 1

        if create:
            ''' if the snake does not exist then create a new one
            '''
            length = random.randint(1,setup.snake_length)
            vector = randomvector()
            snake.append(SnakeObject(grid, vector, length, YELLOW))
            snake_number += 1

        for i in range(1, snake_number + 1):
            snake[i-1].color = YELLOW
        snake_select = 0
        mouse_action_done = True

    return mouse_action_done
        
def move_randomly(debug_stats):
    ''' move the snakes randomly around but avoid the wall
    '''
    for i in range(snake_number):
        
        v = snake[i].view()
        if   v[0] == 0 and v[1] == 0 and v[2] == 0:
            turn = random.randint(0,2)
        elif v[0] != 0 and v[1] == 0 and v[2] == 0:
            turn = random.randint(1,2)
        elif v[0] == 0 and v[1] != 0 and v[2] == 0:
            turn = random.randint(0,1)
            if turn == 1:
                turn = 2
        elif v[0] == 0 and v[1] == 0 and v[2] != 0:
            turn = random.randint(0,1)

        else:
            mn, id = min( (v[i],i) for i in range(len(v)) )
            turn = id

        if   turn == 0:
            # move left
            snake[i].move_left()
        elif turn == 1:
            # when 1 move straight - keep same vector
            pass
        elif turn == 2:
            # when 2 move right
            snake[i].move_right()
        else:
            assert False, "something not right here"

        if   turn == 0:
            debug_stats[0] += 1
        elif turn == 1:
            debug_stats[1] += 1
        elif turn == 2:
            debug_stats[2] += 1

        if not snake[i].move():   # if snake is stuck in the wall delete the snake
            debug_stats[3] += 1
            delete_snake(i)
            break

#        if snake[i].move() == False:  # try to sneak a way out
#            debug_stats[3] += 1
#            turn = random.randint(0,1)
#            if turn == 1:
#                turn = 2
#            if turn == 0:
#                snake[i].move_left()
#            elif turn == 2:
#                snake[i].move_right()

    return debug_stats

def delete_snake(snake_nr):
    ''' delete a snake
    '''
    global snake_number, snake_select, snake # explicitly tell the function to use the global variables!
    assert snake != [], 'there should be at least one snake to delete it'
    # reset the environment
    head = snake[snake_nr].head
    if cell[head[0]][head[1]].content != 'wall':
        cell[head[0]][head[1]].content = 'empty'

    tail = snake[snake_nr].tail

    for i in range(len(tail)):
        if cell[tail[i][0]][tail[i][1]].content != 'wall':
            cell[tail[i][0]][tail[i][1]].content = 'empty'
        
    
    del snake[snake_nr]
    snake_number -= 1
    for i in range(1, snake_number + 1):
        snake[i-1].color = YELLOW
    snake_select = 0    

def plot_snakes(aw):
    ''' plot all the snakes
    '''
    for i in range(snake_number):
        snake[i].plot_snake(aw)

def reset_snakes():
    ''' delete all snakes and reset the variables snake_number and snake
    '''
    global snake_number, snake, snake_select # these variables are global throughout this module
    
    while snake != []:
            delete_snake(0)

    snake_number = 0
    snake = []
    snake_select = 0

def snake_select():
    ''' selection of snake
    '''
    global snake_select

    if snake_select in range(1, snake_number + 1): # normal switching in selection
        snake[snake_select - 1].color = YELLOW
                
    snake_select = (snake_select + 1) % (snake_number + 1)

    if snake_select in range(1, snake_number + 1):
        snake[snake_select - 1].color = GREEN

def plot_monitor(mw):
    ''' plot the cell status in the monitor window
    '''
    for i in range(setup.cells_x):
        for j in range(setup.cells_y):
            if cell[i][j].content == 'empty':
                color = WHITE
            elif cell[i][j].content == 'snake':
                color = RED
            elif cell[i][j].content == 'wall':
                color = BLACK
            else:
                assert False, "this option can not be possible, check code"
            
            mw.create_rectangle( cell[i][j].x, cell[i][j].y, cell[i][j].x + setup.m_dim_x, \
                                 cell[i][j].y + setup.m_dim_y, fill = hex_color(color), width = 0 )

def plot_status(label_SMB, pause_status):
    ''' display status pause or run
    '''
    if pause_status == True:
       label_SMB[0].lift()
       label_SMB[0].place(x = setup.s_w_o[0], y = setup.s_w_o[1])

    else:
       label_SMB[1].lift()
       label_SMB[1].place(x = setup.s_w_o[0], y = setup.s_w_o[1])

def display_text(aw, t_elapsed):
    ''' display number snakes and time passed in seconds in status window left every 1 s
        and refresh the windows according to refresh_rate
    '''
    # display text only once a second
    if t_elapsed % 1000 < 80:
        text ='Number of snakes: ' + str(int(snake_number)) + ' and elapsed time is ' + str(int(t_elapsed/1000)) + ' seconds.'
        label = Label(aw, text=text, wraplength = setup.text_x, bg = 'grey', font = setup.myfont)
        label.place(x = setup.t_w_o[0], y = setup.t_w_o[1])

def show_vision(aw):
    ''' show the vision of snake[snake_nr]
    '''
    if snake_select in range(1, snake_number + 1):
        vision = snake[snake_select-1].view()
            
    else:
        vision = (0, 0, 0)

    delta_intensity = 255 / 6 # values typically range between 0 and 6

    l_v = max( int((6 - vision[0]) * delta_intensity), 0 )
    color = (l_v, l_v, l_v)
    aw.create_rectangle(setup.r_v_w[0], fill = hex_color(color))

    f_v = max( int((6 - vision[1]) * delta_intensity), 0 )
    color = (f_v, f_v, f_v)
    aw.create_rectangle(setup.r_v_w[1], fill = hex_color(color))

    r_v = max( int((6 - vision[2]) * delta_intensity), 0 )
    color = (r_v, r_v, r_v)
    aw.create_rectangle(setup.r_v_w[2], fill = hex_color(color))

#   print('color: {:02x}, {:02x}, {:02x}'.format(l_v, f_v, r_v))

def eye(head, a):
    ''' captures a value of the view depending on looking vector a
    '''
    v = 0
    for i in range(len(a)):
        if cell[(head[0] + a[i][0]) % setup.cells_x][(head[1] + a[i][1]) % setup.cells_y].content != 'empty':
            if i == 0:
                v = v + 4
            else:
                v = v + 1
    return v
