#!/usr/bin/env python
'''     python version 3.6

        Module snake_v4_snake contains following Classes:
        - SnakeObject

        Functions:
        - init_cells
        - mouse_pressed
        - move_randomly
        - create_snake
        - delete_snake
        - set_snake_environment
        - plot_snakes
        - reset_snakes
        - snake_selection
        - show_snake_vision

        Author: Bruno Vermeulen
        bruno_vermeulen2001@yahoo.com
'''
import random

from snake_v4_tools import (
                            RED, YELLOW, GREEN, SnakeSetup, eye, randomvector,
                            hex_color
                           )
'''  initialise the configuration paramaters
'''
setup = SnakeSetup()  # window setup is default False


class SnakeObject:
    '''  definition of snake object and following methods:
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
        self.head = pos
        self.vector = vect
        self.length = length
        self.color = snake_color
        x = self.head[0]
        y = self.head[1]
        print('head is:', self.head)

        # create tail of length (note we start at 0)
        self.tail = []
        for i in range(length):
            x = (pos[0] - vect[0]) % setup.cells_x
            y = (pos[1] - vect[1]) % setup.cells_y
            self.tail.append((x, y))
            print(i, vect, self.tail[i])
            vect = (vect[0] + self.vector[0], vect[1] + self.vector[1])

    def move(self, cell_p):
        '''  method to move snake straight and update cell status
        '''
        global cell
        cell = cell_p

        # set the new head position and check if this is a wall
        x = (self.head[0] + self.vector[0]) % setup.cells_x
        y = (self.head[1] + self.vector[1]) % setup.cells_y

        if cell[x][y].content == 'wall':
            print('unable to move - hit wall')
            move = False

        else:
            # update environment: previous last tail element to 'empty' unless
            # this  is a wall
            if cell[self.tail[self.length - 1][0]][self.tail[self.length - 1]
                                                   [1]].content != 'wall':

                cell[self.tail[self.length - 1][0]][self.tail[self.length - 1]
                                                    [1]].content = 'empty'
                cell[self.tail[self.length - 1][0]][self.tail[self.length - 1]
                                                    [1]].plot = True

            # move up the snake towards the head, start at the end
            for i in range(self.length - 1, 0, -1):
                self.tail[i] = self.tail[i - 1]

            self.tail[0] = self.head
            self.head = (x, y)

            # set the new head position
            cell[x][y].content = 'snake'
            cell[x][y].plot = True
            move = True

        return move

    def move_left(self):
        '''  depending on vector select next position (relative to head)
             steering left
        '''
        if self.vector == (1, 1):
            s = (1, 0)
        elif self.vector == (0, 1):
            s = (1, 1)
        elif self.vector == (-1, 1):
            s = (0, 1)
        elif self.vector == (-1, 0):
            s = (-1, 1)
        elif self.vector == (-1, -1):
            s = (-1, 0)
        elif self.vector == (0, -1):
            s = (-1, -1)
        elif self.vector == (1, -1):
            s = (0, -1)
        elif self.vector == (1, 0):
            s = (1, -1)
        self.vector = (s[0], s[1])

    def move_right(self):
        '''  depending on vector select next position (relative to head)
             steering right
        '''
        if self.vector == (1, 1):
            s = (0, 1)
        elif self.vector == (0, 1):
            s = (-1, 1)
        elif self.vector == (-1, 1):
            s = (-1, 0)
        elif self.vector == (-1, 0):
            s = (-1, -1)
        elif self.vector == (-1, -1):
            s = (0, -1)
        elif self.vector == (0, -1):
            s = (1, -1)
        elif self.vector == (1, -1):
            s = (1, 0)
        elif self.vector == (1, 0):
            s = (1, 1)
        self.vector = (s[0], s[1])

    def plot_snake(self, aw):
        '''  method to plot the snake
        '''
        _headcolor = RED
        # first plot the head
        pos_x = int(setup.a_w_o[0] + self.head[0] * setup.cell_dim_x)
        pos_y = int(setup.a_w_o[1] + self.head[1] * setup.cell_dim_y)
        aw.create_oval(pos_x, pos_y, pos_x + setup.cell_dim_x, pos_y + setup.
                       cell_dim_y, outline=hex_color(_headcolor), width=2)

        # then plot the tail
        for i in range(self.length):
            pos_x = int(setup.a_w_o[0] + self.tail[i][0] * setup.cell_dim_x)
            pos_y = int(setup.a_w_o[1] + self.tail[i][1] * setup.cell_dim_y)
            aw.create_oval(pos_x, pos_y, pos_x + setup.cell_dim_x, pos_y
                           + setup.cell_dim_y, fill=hex_color(self.color))

    def view(self, cell_p):
        '''  method to obtain view looking from the head in the vector direction
             obtaining: Left View (LV), Front View (FV) and Right View (RV) in
             case eye observes wall object it increases the value giving a 3
             component vector (LV, FV, RV)
        '''
        global cell
        cell = cell_p

        if self.vector == (1, 0):
            LV = eye(self.head, cell, setup.view_field[-1 % 8])
            FV = eye(self.head, cell, setup.view_field[0 % 8])
            RV = eye(self.head, cell, setup.view_field[1 % 8])
        elif self.vector == (1, 1):
            LV = eye(self.head, cell, setup.view_field[0 % 8])
            FV = eye(self.head, cell, setup.view_field[1 % 8])
            RV = eye(self.head, cell, setup.view_field[2 % 8])
        elif self.vector == (0, 1):
            LV = eye(self.head, cell, setup.view_field[1 % 8])
            FV = eye(self.head, cell, setup.view_field[2 % 8])
            RV = eye(self.head, cell, setup.view_field[3 % 8])
        elif self.vector == (-1, 1):
            LV = eye(self.head, cell, setup.view_field[2 % 8])
            FV = eye(self.head, cell, setup.view_field[3 % 8])
            RV = eye(self.head, cell, setup.view_field[4 % 8])
        elif self.vector == (-1, 0):
            LV = eye(self.head, cell, setup.view_field[3 % 8])
            FV = eye(self.head, cell, setup.view_field[4 % 8])
            RV = eye(self.head, cell, setup.view_field[5 % 8])
        elif self.vector == (-1, -1):
            LV = eye(self.head, cell, setup.view_field[4 % 8])
            FV = eye(self.head, cell, setup.view_field[5 % 8])
            RV = eye(self.head, cell, setup.view_field[6 % 8])
        elif self.vector == (0, -1):
            LV = eye(self.head, cell, setup.view_field[5 % 8])
            FV = eye(self.head, cell, setup.view_field[6 % 8])
            RV = eye(self.head, cell, setup.view_field[7 % 8])
        elif self.vector == (1, -1):
            LV = eye(self.head, cell, setup.view_field[6 % 8])
            FV = eye(self.head, cell, setup.view_field[7 % 8])
            RV = eye(self.head, cell, setup.view_field[8 % 8])
        else:
            assert False, "Something wrong here, check code"

        v = (LV, FV, RV)
        return v

    def __repr__(self):
        '''   method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self)) + s
        return s


def mouse_pressed(grid, cell_p):
    '''  if mouse is pressed in the action window then create a snake and plot
         it, or if the snake already exists then delete the snake
    '''
    global cell, snake_number  # explicitly tell the function to use the global
    cell = cell_p
    create = True
    mouse_action_done = False

    if grid[0] < setup.cells_x and grid[0] >= 0 and grid[1] < setup.cells_y \
       and grid[1] >= 0:
        i = 0
        while i in range(snake_number) and create:
            '''  check if snake already exist
            '''
            if grid[0] == snake[i].head[0] and grid[1] == snake[i].head[1]:
                delete_snake(i, cell)
                create = False
            i += 1

        if create:
            '''  if the snake does not exist then create a new one
            '''
            create_snake(grid, cell)

        mouse_action_done = True

    return mouse_action_done


def move_randomly(cell_p, debug_stats):
    '''  move the snakes randomly around but avoid the wall
    '''
    global cell
    cell = cell_p
    for i in range(snake_number):

        v = snake[i].view(cell)
        if v[0] == 0 and v[1] == 0 and v[2] == 0:
            turn = random.randint(0, 2)
        elif v[0] != 0 and v[1] == 0 and v[2] == 0:
            turn = random.randint(1, 2)
        elif v[0] == 0 and v[1] != 0 and v[2] == 0:
            turn = random.randint(0, 1)
            if turn == 1:
                turn = 2
        elif v[0] == 0 and v[1] == 0 and v[2] != 0:
            turn = random.randint(0, 1)

        else:
            mn, id = min((v[i], i) for i in range(len(v)))
            turn = id

        if turn == 0:
            # move left
            snake[i].move_left()
            debug_stats[0] += 1

        elif turn == 1:
            # when 1 move straight - keep same vector
            pass
            debug_stats[1] += 1

        elif turn == 2:
            # when 2 move right
            snake[i].move_right()
            debug_stats[2] += 1

        else:
            assert False, "something not right here"

        if not snake[i].move(cell):   # if snake is stuck at wall delete it
            debug_stats[3] += 1
            delete_snake(i, cell)
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


def create_snake(grid, cell_p):
    '''  create a snake
    '''
    global cell
    cell = cell_p
    global snake_number
    length = random.randint(1, setup.snake_length)
    vector = randomvector()
    snake.append(SnakeObject(grid, vector, length, YELLOW))
    snake_number += 1
    snake_selection(reset_selection=True)

    '''  set cell environment
    '''
    set_snake_environment(cell, snake_number - 1, 'snake')


def delete_snake(snake_index, cell_p):
    '''  delete a snake
    '''
    global cell
    cell = cell_p
    global snake_number  # make it explicit use global variables!
    assert snake != [], 'there should be at least one snake to delete it'
    print('delete snake', snake_index)

    '''  reset cell environment
    '''
    set_snake_environment(cell, snake_index, 'empty')

    del snake[snake_index]
    snake_number -= 1
    snake_selection(reset_selection=True)


def set_snake_environment(cell_p, snake_index, content):
    '''  set the snake environment for snake i
    '''
    global cell
    cell = cell_p
    assert content == 'snake' or content == 'empty', "only 'snake' or 'empty' \
        is allowed"

    head = snake[snake_index].head
    if cell[head[0]][head[1]].content != 'wall':
        cell[head[0]][head[1]].content = content
        cell[head[0]][head[1]].plot = True

    tail = snake[snake_index].tail

    for i in range(len(tail)):
        if cell[tail[i][0]][tail[i][1]].content != 'wall':
            cell[tail[i][0]][tail[i][1]].content = content
            cell[tail[i][0]][tail[i][1]].plot = True


def plot_snakes(aw):
    '''  plot all the snakes
    '''
    for i in range(snake_number):
        snake[i].plot_snake(aw)


def reset_snakes(cell_p):
    '''  delete all snakes and reset the variables snake_number and snake
    '''
    global cell
    cell = cell_p

    global snake_number, snake, snake_select  # global throughout this module

    try:
        while snake != []:
            delete_snake(0, cell)
            print('reset')
    except:
        pass

    snake_number = 0
    snake = []
    snake_select = 0


def snake_selection(reset_selection=False):
    '''  selection of snake
    '''
    global snake_select

    if reset_selection:
        for i in range(1, snake_number + 1):
            snake[i-1].color = YELLOW
        snake_select = 0

    else:
        if snake_select in range(1, snake_number + 1):  # normal switching
            snake[snake_select - 1].color = YELLOW

        snake_select = (snake_select + 1) % (snake_number + 1)

        if snake_select in range(1, snake_number + 1):
            snake[snake_select - 1].color = GREEN


def show_snake_vision(aw, cell_p):
    '''  show the vision of snake[snake_nr]
    '''
    global cell
    cell = cell_p

    if snake_select in range(1, snake_number + 1):
        vision = snake[snake_select-1].view(cell)

    else:
        vision = (0, 0, 0)

    delta_intensity = 255 / 6  # values typically range between 0 and 6

    l_v = max(int((6 - vision[0]) * delta_intensity), 0)
    color = (l_v, l_v, l_v)
    aw.create_rectangle(setup.r_v_w[0], fill=hex_color(color))

    f_v = max(int((6 - vision[1]) * delta_intensity), 0)
    color = (f_v, f_v, f_v)
    aw.create_rectangle(setup.r_v_w[1], fill=hex_color(color))

    r_v = max(int((6 - vision[2]) * delta_intensity), 0)
    color = (r_v, r_v, r_v)
    aw.create_rectangle(setup.r_v_w[2], fill=hex_color(color))
