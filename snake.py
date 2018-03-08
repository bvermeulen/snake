#!/usr/bin/env python
'''
     
        Snake around                   
                                               
        python version 3.6                      
                                               
        snake movement on a surface                 
                                                
        For more information read the           
        readme.txt!                             
                                                
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
    
'''
import re
import sys, os
import random
import pygame
from pygame.locals import *

# definition of snake object and methods
class Snake_object():

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
            x = (pos[0]-vect[0])%cells_x
            y = (pos[1]-vect[1])%cells_y
            self.tail.append((x,y))
            print (i, vect, self.tail[i])
            vect = (vect[0] + self.vector[0], vect[1] + self.vector[1])   

    def move_straight(self):
        x   = (self.head[0] + self.vector[0])%cells_x
        y   = (self.head[1] + self.vector[1])%cells_y
        for i in range(self.length-1,0,-1):
            self.tail[i] = self.tail[i-1]
#            print(i, self.tail[i])
        self.tail[0] = self.head
#        print(0,self.tail[0])
        self.head    = (x,y)
#        print("new head:",self.head)
            
    def move_left(self):
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

#    def delete(self):


    def plot_snake(self):
        _headcolor = red
        # first plot the head        
        pos_x = int(a_w_o[0] + (self.head[0]+0.5)*cell_dim_x)
        pos_y = int(a_w_o[1] + (self.head[1]+0.5)*cell_dim_y)
        pygame.draw.circle(screen,_headcolor,(pos_x,pos_y),radius,2)

        # then plot the tail
        for i in range(self.length):
           pos_x = int(a_w_o[0] + (self.tail[i][0]+0.5)*cell_dim_x)
           pos_y = int(a_w_o[1] + (self.tail[i][1]+0.5)*cell_dim_y)
           pygame.draw.circle(screen,self.color,(pos_x,pos_y),radius,0)

def plot_grid():
    '''
    # draw vertical grid lines
    for x in range(a_tl[0]+cell_dim_x,a_tr[0],cell_dim_x):
        pygame.draw.lines(screen,grey,False,((x,a_tl[1]+1),(x,a_bl[1]-1)),lwidth)

    # draw horizontal grid lines
    for y in range(a_tl[1]+cell_dim_y,a_bl[1],cell_dim_y):
        pygame.draw.lines(screen,grey,False,((a_tl[0]+1,y),(a_tr[0]-1,y)),lwidth)
    '''
    # draw action window border - there are two color (blue and organge)
    pygame.draw.rect(screen, bcolor, pygame.Rect(r_action_window), 2*lwidth)

# if mouse is pressed in the action window then create a snake and plot it
def mouse_pressed(grid):
    global snake, snake_number
    
    if grid[0] < cells_x and grid[0] >= 0 and grid[1] < cells_y and grid[1] >= 0:
        snake_length = random.randint(1,8)
        vector = randomvector()        
        print(snake_number+1, vector)
        snake.append(Snake_object(grid, vector, snake_length, yellow))
        snake[snake_number].plot_snake()
        snake_number = snake_number + 1
    grid = (999999,99999)
    return grid

# display number snakes and time passed in seconds in status window left	
def display_text(n, t):
	
    # display text only once a second
    if t%1000 < 100:
		
        tpos = (a_bl[0], int(a_bl[1] + text_y*0.25))

        text ='Number of snakes: ' + str(int(n)) + ' and elapsed time is ' + str(int(t/1000)) + ' seconds.'
        text_display = myfont.render(text, False, yellow)
		
        #clear the text surface
        pygame.draw.rect(screen, black, pygame.Rect(r_text_window), 0)

        #display text on surface
        screen.blit(text_display,tpos)

# calculate a random vector ([-1,0-1],[-1,0,-1]) but not (0,0))
def randomvector():
    vector = (0,0)
    while vector == (0,0):
        x = random.randint(-1,1)
        y = random.randint(-1,1)
        vector = (x, y)    
    return vector

# save and load pattern file

# read config file in 1st argument (otherwise default is data/config.txt). Optionally 2nd argument is 
# pattern file otherwise defined in config file
def read_config():
    global pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y, survival, birth	
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        config_file = os.path.join("data","config.txt")

    cfile = open(config_file)

    pattern_file= cfile.readline()[17:]
    fps         = int(cfile.readline()[17:])
    cells_x     = int(cfile.readline()[17:])
    cells_y     = int(cfile.readline()[17:])
    cell_dim_x  = int(cfile.readline()[17:])
    cell_dim_y  = int(cfile.readline()[17:])

    if len(sys.argv) == 3:
        pattern_file= sys.argv[2]

    # remove return /r, new line /n or spaces /s from pattern_file
    pattern_file = re.sub(r'[\r\n\s]','',pattern_file)
    print (pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y)

    cfile.close()

# main program
def main():

    # initialize and set parameters
    global myfont
    pygame.init()
    fpsClock = pygame.time.Clock()
    myfont = pygame.font.Font(None,22)

    read_config()
	
    # set some variables not defined in config file
    global black, blue, orange, red, yellow, grey, padding, lwidth, radius
    black	= (0,0,0)
    blue        = (0,128,255)
    orange      = (255,100,0)
    red         = (255,0,0)
    yellow      = (255,255,0)
    grey        = (128,128,128)
    padding     = 5
    lwidth      = 1
    radius      = int(cell_dim_x/2)

    # set window boundaries
    global a_w_o, a_w_x, a_w_y, a_tl, a_tr, a_br, a_bl, r_action_window, r_text_window, text_x, text_y
    a_w_o = (padding , padding )
    a_w_x = cells_x*cell_dim_x 
    a_w_y = cells_y*cell_dim_y 

    a_tl = a_w_o
    a_tr = (a_w_o[0]+a_w_x,a_w_o[1])
    a_br = (a_w_o[0]+a_w_x,a_w_o[1]+a_w_y)
    a_bl = (a_w_o[0],a_w_o[1] + a_w_y)

    status_x    = 50
    status_y    = 38
    text_x      = a_w_x - status_x
    text_y      = status_x

    # action_window = (a_tl,a_tr,a_br,a_bl)
    r_action_window = (a_tl,(a_w_x,a_w_y))
    r_status_window = ((a_br[0]-status_x,a_br[1]+padding),(status_x,status_y))
    r_text_window   = ((a_bl[0], a_bl[1]+padding),(text_x, text_y))
    status_pos      = (int(a_br[0]-status_x),int(a_br[1]+padding-10))
    main_x          = padding*2 + a_w_x
    main_y          = padding + a_w_y + status_y

    global bcolor, snake_number, snake_length, snake
    bcolor           = blue
    run              = True
    pause            = True
    dummy            = 0
    m                = (99999,99999)
    snake_number     = 0
    snake_length     = 6
    time_counter     = 0
    snake            = []
    Left             = False
    Right            = False
    snake_select     = 0

    # set the screen, set caption of the main window and load icons for pause and run
    global screen
    screen = pygame.display.set_mode((main_x, main_y))
    pygame.display.set_caption('Snakes ...')
    pause_SMB = pygame.image.load('data/Pause.png').convert_alpha()
    run_SMB   = pygame.image.load('data/Triangle.png').convert_alpha()

    # run indefinetaly while run is true
    display_text(0, 0)
    while run:
        if pause:
            # update status symbol to pause
            pygame.draw.rect(screen, black, pygame.Rect(r_status_window), 0)
            screen.blit(pause_SMB, status_pos)
	
            # if mouse is pressed inside action window create a snake
            m = mouse_pressed(m)

            #plot grid
            plot_grid()

        else:
            #update status symbol to run
            pygame.draw.rect(screen, black, pygame.Rect(r_status_window), 0)
            screen.blit(run_SMB, status_pos)		

            # clear the screen and plot grid
            pygame.draw.rect(screen, black, pygame.Rect(r_action_window), 0)
            plot_grid()
			
            #move snakes randomly
#           snake_select = random.randint(0,snake_number-1)
#           turn = random.randint(0,2)
#           if turn == 1:
#               # move right when 1
#               snake[snake_select].move_right()
#           elif turn == 2:
#               # else left when 2
#               snake[snake_select].move_left()
#           else:
#               # moving straight

            for i in range(snake_number):
                turn = random.randint(0,2)
                if turn == 1:
                    # move right when 1
                    snake[i].move_right()
                elif turn == 2:
                    # else left when 2
                    snake[i].move_left()

                snake[i].move_straight()
                snake[i].plot_snake()            
     
        # there are three events to be considered: QUIT (click on exit window icon), KEYDOWN, MOUSEBUTTONUP 
        for event in pygame.event.get():
            if event.type == QUIT:            # stop running when Quit event type is triggered
                run = False

            # for key press there are below options:	
            elif event.type == KEYDOWN:
                if event.key == K_b:          # b - change border color to blue
                    bcolor = blue
                elif event.key == K_o:        # o - change border color to orange
                    bcolor = orange
                elif event.key == K_ESCAPE:   # Escape - leave program
                    run = False
                elif event.key == K_SPACE:    # Space - change pause status, pause is not pause
                    pause = not pause
                elif event.key == K_l:        # l - load pattern
                    load_pattern()
                elif event.key == K_s:        # s - save pattern, note this overwrites the file
                    save_pattern()
                elif event.key == K_c:        # c - clear screen and pause
                    pause = True
                    snake = []
                    snake_number = 0
                    pygame.draw.rect(screen, black, pygame.Rect(r_action_window), 0)
                    plot_grid
                elif event.key == K_LEFT:     # LEFT arrow - move left
                    Left = True
                elif event.key == K_RIGHT:    # RIGHT arrow - move right
                    Right = True
								
            elif event.type == MOUSEBUTTONUP: # if mouse if pressed calculated the cell indices
                m = pygame.mouse.get_pos()
                m = [int((m[0]-a_w_o[0])/cell_dim_x),int((m[1]-a_w_o[1])/cell_dim_y)]

        pygame.display.flip()
        fpsClock.tick(fps)
	        
        time = pygame.time.get_ticks()
        display_text(snake_number, time)

    pygame.quit()
    sys.exit

if __name__ == "__main__" :
    main()
