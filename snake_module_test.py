#!/usr/bin/env python
'''     python version 3.6                      

        This module contains following Classes:
        - SnakeObject
        - WallObject
        - Tools
        
        Functions:
        - init_walls
        - init_cells
        - plot_grid_wall
        - mouse_pressed
        - move_randomly
        - delete_snake
        - plot_snakes
        - reset_snakes
        - plot_monitor
        - display_text
        - drawText
        - random_vector
        - dist
        - eye
                                               
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
'''
import re
import sys 
import os
import random
import pygame

from snake_configuration_test import BLACK, WHITE, RED, GREY, YELLOW, BLUE, ORANGE, LWIDTH, read_config, SnakeSetup

''' initialise the configuration paramaters
'''
setup = SnakeSetup()

class SnakeObject:
    ''' definition of snake object and following methods:
        - __init__
        - move()
        - move_left()
        - move_right()
        - plot_snake()
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

            # set the new head position 
            self.head    = (x , y)
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

    def plot_snake(self):
        ''' method to plot the snake
        '''
        _headcolor = RED
        # first plot the head        
        pos_x = int(setup.a_w_o[0] + (self.head[0] + 0.5) * setup.cell_dim_x)
        pos_y = int(setup.a_w_o[1] + (self.head[1] + 0.5) * setup.cell_dim_y)
        pygame.draw.circle(setup.screen, _headcolor, (pos_x, pos_y), setup.radius,2)

        # then plot the tail
        for i in range(self.length):
           pos_x = int(setup.a_w_o[0] + (self.tail[i][0] + 0.5) * setup.cell_dim_x)
           pos_y = int(setup.a_w_o[1] + (self.tail[i][1] + 0.5) * setup.cell_dim_y)
           pygame.draw.circle(setup.screen, self.color, (pos_x, pos_y), setup.radius, 0)
       
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
        s = ('{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
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

    def plot_wall(self):
        ''' method to plot the wall
        '''
        for i in range(len(self.brick)):
            pos_x = int(setup.a_w_o[0] + self.brick[i][0]*setup.cell_dim_x)
            pos_y = int(setup.a_w_o[1] + self.brick[i][1]*setup.cell_dim_y)
            pygame.draw.rect(setup.screen, self.color, (pos_x, pos_y, setup.brick_size[0], setup.brick_size[1]), 4)

    def __repr__(self):
        ''' method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k,v in self.__dict__.items()) 
        s = ('{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
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
        s = ('{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
        return s

def init_walls():
    ''' initialise the wall objects
    '''
    wall = []
    wall.append(WallObject(setup.wall_v[0], GREY))
    wall.append(WallObject(setup.wall_v[1], ORANGE))
    return wall

def init_cells():
    ''' initialise the cells to capture status of the field
        Cell. cell.x and cell.y are the monitor cell positions
    '''
    global cell
    cell = [[Cell( \
                  int( setup.m_w_o[0] + x * setup.m_dim_x), \
                  int( setup.m_w_o[1] + y * setup.m_dim_y), \
                  'empty') for y in range(setup.cells_y)] for x in range(setup.cells_x)]
    return cell

def plot_grid_walls(border_color, wall):
    ''' draw action window border - there are two color (blue and organge)
        and the walls
    '''
    pygame.draw.rect(setup.screen, border_color, pygame.Rect(setup.r_action_window), 2*LWIDTH)
    for i in range(len(wall)):
        wall[i].plot_wall()

def mouse_pressed(grid):
    ''' if mouse is pressed in the action window then create a snake and plot it, or if the snake
        already exists then delete the snake
    '''
    global snake_number # explicitly tell the function to use the global variable snake_number!
    create = True
    if grid[0] < setup.cells_x and grid[0] >= 0 and grid[1] < setup.cells_y and grid[1] >= 0:
        i = 0
        while i < snake_number and create == True:
            ''' check if snake already exist 
            '''
            if grid[0] == snake[i].head[0] and grid[1] == snake[i].head[1]:
                create = delete_snake(i)
            i += 1
        if create:
            ''' if the snake does not exist then create a new one
            '''
            length = random.randint(1,setup.snake_length)
            vector = randomvector()
            snake.append(SnakeObject(grid, vector, length, YELLOW))
            snake_number += 1

    grid = (999999,99999), snake
    return grid

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

#        if i == 0:     # debug print for snake[0]
#            print("{:.3f},{:.3f},{:.3f}: turn taken: ".format(v[0],v[1], v[2]),turn)

        if   turn == 0:
            debug_stats[0] += 1
        elif turn == 1:
            debug_stats[1] += 1
        elif turn == 2:
            debug_stats[2] += 1

        if snake[i].move() == False:  # try to sneak a way out
            debug_stats[3] += 1
            turn = random.randint(0,1)
            if turn == 1:
                turn = 2
            if turn == 0:
                snake[i].move_left()
            elif turn == 2:
                snake[i].move_right()

    return debug_stats

def delete_snake(snake_nr):
    ''' delete a snake
    '''
    global snake_number # explicitly tell the function to use the global variable snake_number!
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
    return False

def plot_snakes():
    ''' plot all the snakes
    '''
    for i in range(snake_number):
        snake[i].plot_snake()

def reset_snakes():
    ''' reset the variables snake_number and snake
    '''
    global snake_number, snake # these variables are global throughout this module
    snake_number = 0
    snake = []

def plot_monitor():
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
 
            pygame.draw.rect(setup.screen, color, (cell[i][j].x, cell[i][j].y, setup.m_dim_x, setup.m_dim_y), 0)

def display_text(t):
    ''' display number snakes and time passed in seconds in status window left	
    '''
    # display text only once a second
    if t%1000 < 100:
		
        text ='Number of snakes: ' + str(int(snake_number)) + ' and elapsed time is ' + str(int(t/1000)) + ' seconds.'

        # clear the test surface and draw the text
        pygame.draw.rect(setup.screen, BLACK, pygame.Rect(setup.r_text_window), 0)#
        drawText(setup.screen, text, YELLOW, setup.r_text_window, setup.myfont, aa=False, bkg=None)

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    ''' draw some text into an area of a surface (reference: https://www.pygame.org/wiki/TextWrap)
        automatically wraps words
        returns any text that didn't get blitted
    '''
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def randomvector():
    ''' calculate a random vector ([-1,0-1],[-1,0,-1]) but not (0,0))
    '''
    vector = (0,0)
    while vector == (0,0):
        x = random.randint(-1,1)
        y = random.randint(-1,1)
        vector = (x, y)    
    return vector

def dist(a, b):
    ''' calculate the distance between vectors 
    '''
    v = ((b[1] - a[1])**2 + (b[0] - a[0])**2)**0.5
    return v 

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


# save and load pattern file


