#!/usr/bin/env python
'''     python version 3.6                      

        This module contains following Classes:
        - SnakeObject
        - WallObject
        - Tools
        
        Functions:
        - plot_grid
        - mouse_pressed
        - move_randomly
        - delete_snake
        - plot_snakes
        - reset_snakes
        - display_text
        - random_vector
                                               
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
'''
import re
import sys 
import os
import random
import pygame
from pygame.locals import *

import cfg
from cfg import BLACK, RED, YELLOW, LWIDTH

class SnakeObject:
    ''' definition of snake object and following methods:
        - move_straight()
        - move_left()
        - move_right()
        - plot_snake()
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

        # create tail of length (note we start at 0)
        self.tail = []
        for i in range(length):
            x = (pos[0]-vect[0])%cfg.cells_x
            y = (pos[1]-vect[1])%cfg.cells_y
            self.tail.append((x,y))
            print (i, vect, self.tail[i])
            vect = (vect[0] + self.vector[0], vect[1] + self.vector[1])   

    def move_straight(self):
        ''' method to move snake straight
        '''
        x   = (self.head[0] + self.vector[0]) % cfg.cells_x
        y   = (self.head[1] + self.vector[1]) % cfg.cells_y
        for i in range(self.length-1,0,-1):
            self.tail[i] = self.tail[i-1]
#           print(i, self.tail[i])
        self.tail[0] = self.head
#       print(0,self.tail[0])
        self.head    = (x , y)
#       print("new head:",self.head)
            
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
#        print('vector is:', self.vector)

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
        pos_x = int(cfg.a_w_o[0] + (self.head[0] + 0.5) * cfg.cell_dim_x)
        pos_y = int(cfg.a_w_o[1] + (self.head[1] + 0.5) * cfg.cell_dim_y)
        pygame.draw.circle(cfg.screen, _headcolor, (pos_x, pos_y), cfg.radius,2)

        # then plot the tail
        for i in range(self.length):
           pos_x = int(cfg.a_w_o[0] + (self.tail[i][0] + 0.5) * cfg.cell_dim_x)
           pos_y = int(cfg.a_w_o[1] + (self.tail[i][1] + 0.5) * cfg.cell_dim_y)
           pygame.draw.circle(cfg.screen, self.color, (pos_x, pos_y), cfg.radius, 0)

class WallObject:
    ''' Definition of wall object
    '''
    def __init__(self, vertices, color):
#       self.vertices = vertices
        self.color    = color
        self.brick    = []

        for i in range(len(vertices)-1):
            a_x = vertices[i][0]
            a_y = vertices[i][1]
            b_x = vertices[i+1][0]
            b_y = vertices[i+1][1]
            assert (a_x >= 0 and a_x <= cfg.cells_x-1), "wall must be inside the action window - x violation"
            assert (a_y >= 0 and a_y <= cfg.cells_y-1), "wall must be inside the action window - y violation"
            
            range_x = b_x - a_x
            range_y = b_y - a_y
            steps = max(abs(range_x), abs(range_y))
            for step in range(steps):
                    x = a_x + round(step/ steps * range_x)
                    y = a_y + round(step/ steps * range_y)
                    self.brick.append((int(x), int(y)))
    
    def plot_wall(self):
        ''' method to plot the wall
        '''
        for i in range(len(self.brick)):
            pos_x = int(cfg.a_w_o[0] + self.brick[i][0]*cfg.cell_dim_x)
            pos_y = int(cfg.a_w_o[1] + self.brick[i][1]*cfg.cell_dim_y)
            
            pygame.draw.rect(cfg.screen, self.color, (pos_x, pos_y, cfg.brick_size[0], cfg.brick_size[1]), 4)

def plot_grid():
    ''' draw action window border - there are two color (blue and organge)
    '''
    ''' do not plot grid lines commented out below
    '''
    #for x in range(a_tl[0]+cell_dim_x,a_tr[0],cell_dim_x):
    #    pygame.draw.lines(screen,grey,False,((x,a_tl[1]+1),(x,a_bl[1]-1)),LWIDTH)
    #
    # draw horizontal grid lines
    # for y in range(a_tl[1]+cell_dim_y,a_bl[1],cell_dim_y):
    #    pygame.draw.lines(screen,grey,False,((a_tl[0]+1,y),(a_tr[0]-1,y)),LWIDTH)
    pygame.draw.rect(cfg.screen, cfg.bcolor, pygame.Rect(cfg.r_action_window), 2*cfg.LWIDTH)

def mouse_pressed(grid):
    ''' if mouse is pressed in the action window then create a snake and plot it, or if the snake
        already exists then delete the snake
    '''
    global snake_number # explicitly tell the function to use the global variable snake_number!
    create = True
    if grid[0] < cfg.cells_x and grid[0] >= 0 and grid[1] < cfg.cells_y and grid[1] >= 0:
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
            length = random.randint(1,cfg.snake_length)
            vector = randomvector()
            snake.append(SnakeObject(grid, vector, length, YELLOW))
            snake_number += 1
    grid = (999999,99999)
    return grid

def move_randomly():
    ''' move the snakes randomly around
    '''
    for i in range(snake_number):
        turn = random.randint(0,2)
        if turn == 1:
        # move right when 1
            snake[i].move_right()
        elif turn == 2:
        # else left when 2
            snake[i].move_left()

        snake[i].move_straight()

def delete_snake(i):
    ''' delete a snake
    '''
    global snake_number # explicitly tell the function to use the global variable snake_number!
    assert snake != [], 'there should be at least one snake to delete it'
    del snake[i]
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

def display_text(t):
    ''' display number snakes and time passed in seconds in status window left	
    '''
    # display text only once a second
    if t%1000 < 100:
		
        tpos = (cfg.a_bl[0], int(cfg.a_bl[1] + cfg.text_y*0.25))
        text ='Number of snakes: ' + str(int(snake_number)) + ' and elapsed time is ' + str(int(t/1000)) + ' seconds.'
        text_display = cfg.myfont.render(text, False, YELLOW)
	
        #clear the text surface
        pygame.draw.rect(cfg.screen, BLACK, pygame.Rect(cfg.r_text_window), 0)

        #display text on surface
        cfg.screen.blit(text_display,tpos)

def randomvector():
    ''' calculate a random vector ([-1,0-1],[-1,0,-1]) but not (0,0))
    '''
    vector = (0,0)
    while vector == (0,0):
        x = random.randint(-1,1)
        y = random.randint(-1,1)
        vector = (x, y)    
    return vector

# save and load pattern file


