''' python 3.6
    test of vission mechanism
    
    author: Bruno Vermeulen
    email : bruno_vermeulen2001@yahoo.com
'''
import pygame

from pygame.locals import (QUIT, KEYDOWN,MOUSEBUTTONUP, 
                           K_o, K_b, K_l, K_s, K_c, 
                           K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN)

from snake_configuration_test import SnakeSetup

import snake_module_test
from snake_module_test import (Cell, 
                              )
class TestSnake:

    def __init__(self, pos, vect):
        self.head = pos
        self.vector = vect
        self.tail = []   
        x = self.head[0]
        y = self.head[1]
        if tcell[x][y].content != 'wall':
            tcell[x][y].content = 'snake'

        x = (pos[0]-vect[0]) % CELLS_X
        y = (pos[1]-vect[1]) % CELLS_Y
        self.tail.append((x,y))
        if tcell[x][y].content != 'wall':
           tcell[x][y].content = 'snake'

    def plot_snake(self):
        pos_x = int((self.head[0] + 0.5) * X_DIM)
        pos_y = int((self.head[1] + 0.5) * Y_DIM)
        pygame.draw.circle(screen, RED, (pos_x, pos_y), int(X_DIM/2), 2)
        pos_x = int((self.tail[0][0] + 0.5) * X_DIM)
        pos_y = int((self.tail[0][1] + 0.5) * Y_DIM)
        pygame.draw.circle(screen, YELLOW, (pos_x, pos_y), int(X_DIM/2), 0)
        

    def move(self, forward = True):
        if forward:
            x   = (self.head[0] + self.vector[0]) % CELLS_X
            y   = (self.head[1] + self.vector[1]) % CELLS_Y

            # update environment: previous last tail element to 'empty' unless this  is a wall
            if tcell[self.tail[0][0]][self.tail[0][1]].content != 'wall':    
                tcell[self.tail[0][0]][self.tail[0][1]].content = 'empty' 

            self.tail[0] = self.head
        
            # set the new head position 
            self.head    = (x , y)

            if tcell[x][y].content != 'wall':
               tcell[x][y].content = 'snake'

        else: # reverse
            x   = (self.tail[0][0] - self.vector[0]) % CELLS_X
            y   = (self.tail[0][1] - self.vector[1]) % CELLS_Y

            # update environment: in reverse head position goes to 'empty'
            if tcell[self.head[0]][self.head[1]].content != 'wall':    
                tcell[self.head[0]][self.head[1]].content = 'empty' 

            self.head = self.tail[0]
        
            # and tail becomes the new position
            self.tail[0] = (x , y)

            if tcell[x][y].content != 'wall':
               tcell[x][y].content = 'snake'

        return True
            
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

class WallTest:

    def __init__(self,vertices):
        self.color = BLACK
        self.brick = []

        for i in range(len(vertices)-1):
            a_x = vertices[i][0]
            a_y = vertices[i][1]
            b_x = vertices[i+1][0]
            b_y = vertices[i+1][1]
            assert (a_x >= 0 and a_x <= CELLS_X - 1), "wall must be inside the action window - x violation"
            assert (a_y >= 0 and a_y <= CELLS_Y - 1), "wall must be inside the action window - y violation"
            
            range_x = b_x - a_x
            range_y = b_y - a_y
            steps = max(abs(range_x), abs(range_y))
            for step in range(steps):
                    x = round(a_x + step/ steps * range_x)
                    y = round(a_y + step/ steps * range_y)
                    self.brick.append((x, y))
                    tcell[x][y].content = 'wall'

    def plot_wall(self):
        ''' method to plot the wall
        '''
        for i in range(len(self.brick)):
            pos_x = int(self.brick[i][0] * X_DIM)
            pos_y = int(self.brick[i][1] * Y_DIM)
            pygame.draw.rect(screen, self.color, (pos_x, pos_y, X_DIM-2, Y_DIM-2), 0)

def eye(head, a):
    ''' captures a value of the view depending on looking vector a
    '''
    v = 0
    for i in range(len(a)):
        if tcell[(head[0] + a[i][0]) % CELLS_X][(head[1] + a[i][1]) % CELLS_Y].content != 'empty':
            if i == 0:
                v = v + 4 # first element of view vector is the closest center cell of the vision
            else:
                v = v + 1
    return v

def show_vision(vision):
    delta_intensity = 255 / 6 # values typically range between 0 and 6

    l_v = max( int( (6 - vision[0]) * delta_intensity), 0 )
    color = (l_v, l_v, l_v)
    pygame.draw.rect( screen, color, (10, 210, 30, 30), 0)

    f_v = max( int( (6 - vision[1]) * delta_intensity), 0 )
    color = (f_v, f_v, f_v)
    pygame.draw.rect( screen, color, (50, 210, 30, 30), 0)

    r_v = max( int( (6 - vision[2]) * delta_intensity), 0 )
    color = (r_v, r_v, r_v)
    pygame.draw.rect( screen, color, (90, 210, 30, 30), 0)

    print('color: ', l_v, f_v, r_v)

setup = SnakeSetup()
X_DIM = 20
Y_DIM = 20
CELLS_X = 10
CELLS_Y = 10
MAIN_X = X_DIM * CELLS_X
MAIN_Y = Y_DIM * CELLS_Y + 50
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
PINKISH = (255, 200, 200)
BLACK = (0, 0, 0)
R_ACTION = ((0, 0), (MAIN_X, CELLS_Y * Y_DIM))

screen = pygame.display.set_mode((MAIN_X, MAIN_Y))
run = True
Left = False
Right = False
Forward = False
Reverse = False

pygame.init()
pygame.display.set_caption('Snakes ...')
screen = pygame.display.set_mode((MAIN_X, MAIN_Y))

tcell = [[Cell( \
               x, \
               y, \
               'empty') for y in range(CELLS_Y)] for x in range(CELLS_X)]

wall_vertices = [(2, 2), (8, 2), (8, 7)]
test_wall = []
test_wall.append(WallTest(wall_vertices))

test_snake = []
test_snake.append(TestSnake((4, 7), (0,-1)))

pygame.draw.rect( screen, PINKISH, (0, 200, 200, 60), 0)
show_vision( (0, 0, 0) )

while run:
    move = False
    pygame.draw.rect(screen, GREY, pygame.Rect(R_ACTION), 0)
    test_wall[0].plot_wall()
    test_snake[0].plot_snake()
    pygame.display.flip()

    if Left:
        test_snake[0].move_left()
        move =test_snake[0].move()
        Left = False

    elif Right:
        test_snake[0].move_right()
        move = test_snake[0].move()
        Right = False

    elif Forward:
        move = test_snake[0].move()
        Forward = False

    elif Reverse:
        move = test_snake[0].move(forward = False)
        Reverse = False

    if move:
        v = test_snake[0].view()
        print(test_snake[0].vector, test_snake[0].head, test_snake[0].tail[0])
        print('view: ', v)
        show_vision(v)

    for event in pygame.event.get():
        if event.type == QUIT:            # stop running when Quit event type is triggered
            run = False

        elif event.type == KEYDOWN:
            ''' if event is key press (KEYDOWN) then check if following option occur
            '''
            if   event.key == K_ESCAPE:   # Escape - leave program
                run = False
            elif event.key == K_LEFT:     # LEFT arrow - move left
                Left = True
            elif event.key == K_RIGHT:    # RIGHT arrow - move right
                Right = True
            elif event.key == K_UP:       # UP arrow - move forward
                Forward = True
            elif event.key == K_DOWN:     # DOWN arrow - undo the move
                Reverse = True

pygame.quit()



