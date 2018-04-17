#!/usr/bin/env python
''' module "cfg" containing all shared variables
    and the functions:
        - read_config
        - set_parameter
'''
import re
import sys
import os
import pygame
from pygame.locals import *

''' set the constants
'''
BLACK	    = (0,0,0)
BLUE        = (0,128,255)
ORANGE      = (255,100,0)
RED         = (255,0,0)
YELLOW      = (255,255,0)
GREY        = (128,128,128)
PADDING     = 5
LWIDTH      = 1
STATUS_X    = 50
STATUS_Y    = 38

''' Functions to read the main paramters from the config file and set the parameters
        - read_config
        - set_parameters
'''

def read_config():
    ''' read config file in 1st argument (otherwise default is data/config.txt). Optionally 2nd argument is 
        pattern file otherwise defined in config file
    '''
    global pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        config_file = os.path.join("data","config.txt")

    cfile = open(config_file)

    pattern_file = cfile.readline()[17:]
    fps          = int(cfile.readline()[17:])
    cells_x      = int(cfile.readline()[17:])
    cells_y      = int(cfile.readline()[17:])
    cell_dim_x   = int(cfile.readline()[17:])
    cell_dim_y   = int(cfile.readline()[17:])

    if len(sys.argv) == 3:
        pattern_file= sys.argv[2]

    # remove return /r, new line /n or spaces /s from pattern_file
    pattern_file = re.sub(r'[\r\n\s]','',pattern_file)
    print (pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y)

    cfile.close()

def set_parameters():
    ''' set the parameters for time, font and windows
    '''
    # set some variables not defined in config file
    global fpsClock, myfont, radius
    pygame.init()
    fpsClock = pygame.time.Clock()
    myfont = pygame.font.Font(None,22)
    radius = int(cell_dim_x/2)

    # set window boundaries
    global a_w_o, a_w_x, a_w_y, a_tl, a_tr, a_br, a_bl, text_x, text_y
    a_w_o = (PADDING , PADDING )
    a_w_x = cells_x * cell_dim_x 
    a_w_y = cells_y * cell_dim_y 

    a_tl = a_w_o
    a_tr = (a_w_o[0] + a_w_x, a_w_o[1])
    a_br = (a_w_o[0] + a_w_x, a_w_o[1] + a_w_y)
    a_bl = (a_w_o[0], a_w_o[1] + a_w_y)

    text_x      = a_w_x - STATUS_X
    text_y      = STATUS_Y

    # action_window = (a_tl,a_tr,a_br,a_bl)
    global r_action_window, r_status_window, r_text_window, status_pos, main_x, main_y
    r_action_window = (a_tl, (a_w_x, a_w_y))
    r_status_window = ((a_br[0] - STATUS_X, a_br[1] + PADDING),(STATUS_X, STATUS_Y))
    r_text_window   = ((a_bl[0], a_bl[1] + PADDING), ( text_x, text_y))
    status_pos      = (int(a_br[0] - STATUS_X), int(a_br[1] + PADDING-10))
    main_x          = PADDING*2 + a_w_x
    main_y          = PADDING + a_w_y + STATUS_Y

    # set the screen, set caption of the main window and load icons for pause and run
    global screen, pause_SMB, run_SMB
    screen = pygame.display.set_mode((main_x, main_y))
    pygame.display.set_caption('Snakes ...')
    pause_SMB = pygame.image.load('data/Pause.png').convert_alpha()
    run_SMB   = pygame.image.load('data/Triangle.png').convert_alpha()

    #set some other parameter
    global snake_length, bcolor, wall_v, brick_size
    snake_length = 10 # this is the maximum snake length
    bcolor = BLUE
    wall_v = []
    wall_v.append([(int(0.05*cells_x), int(0.05*cells_y)), (int(0.05*cells_x), int(0.95*cells_y)), (int(0.8*cells_x), int(0.95*cells_y)), (int(0.8*cells_x), int(0.4*cells_y))])
    wall_v.append([(int(0.3*cells_x), int(0.3*cells_y)), (int(0.6*cells_x), int(0.3*cells_y))])
    brick_size = (0.8 * cell_dim_x, 0.8 * cell_dim_y)


