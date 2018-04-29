#!/usr/bin/env python
''' module snake_configuration to read configuration file
    and to set all variables
    Class: SnakeSetup
    Function: read_config 
'''
import re
import sys
import os
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Label, BOTH, YES

''' set the constants
'''
BLACK	    = (0, 0, 0)
WHITE       = (255, 255, 255)
BLUE        = (0, 128, 255)
ORANGE      = (255, 100, 0)
RED         = (255, 0, 0)
YELLOW      = (255, 255, 0)
GREY        = (128, 128, 128)
GREEN       = (  0, 128, 0)
PADDING     = 5
LWIDTH      = 1
STATUS_X    = 60
STATUS_Y    = 60

def read_config():
    ''' read config file in 1st argument (otherwise default is data/config.txt). Optionally 2nd argument is 
        pattern file otherwise defined in config file
        returns values for: pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y
    '''
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

    cfile.close()
    return pattern_file, fps, cells_x, cells_y, cell_dim_x, cell_dim_y

class SnakeSetup:
    ''' Setup of variables environment for the program
        Input are the parameters from the configuration file
    '''
    def __init__(self, set_window = False):
        ''' set the parameters for windows, font, time
        '''
        self.set_window = set_window

        # read the configuration file
        _pattern_file, _fps, _cells_x, _cells_y, _cell_dim_x, _cell_dim_y = read_config()

        # set the variable from the configuration file
        self.pattern_file = _pattern_file
        self.fps = _fps
        self.cells_x = _cells_x
        self.cells_y = _cells_y
        self.cell_dim_x = _cell_dim_x
        self.cell_dim_y = _cell_dim_y
 
        # set window boundaries - abbrevations stand for: a_ [action], m_ [monitor], s_ [status]
        self.a_w_o = (PADDING , PADDING )
        a_w_x = self.cells_x * self.cell_dim_x 
        a_w_y = self.cells_y * self.cell_dim_y 

        s_w_o                 = (self.a_w_o[0] + a_w_x - STATUS_X, self.a_w_o[1] + a_w_y + PADDING)
        self.r_action_window  = (self.a_w_o[0], self.a_w_o[1], self.a_w_o[0] + a_w_x, self.a_w_o[1] + a_w_y)
        self.r_status_window  = (s_w_o[0], s_w_o[1])
        self.r_text_window    = (self.a_w_o[0], self.a_w_o[1] + a_w_y + PADDING)
        self.m_dim_x = 2
        self.m_dim_y = 2
        m_w_x = self.cells_x * self.m_dim_x
        m_w_y = self.cells_y * self.m_dim_y
        status_y   = max(STATUS_Y, m_w_y)
        self.m_w_o = (s_w_o[0] - PADDING - m_w_x, \
                      s_w_o[1] ) 

        v_dim_x = 30
        v_dim_y = 30 
        v_w_o = (self.m_w_o[0] - 3 * (PADDING + v_dim_x), \
                      self.m_w_o[1] )
        self.r_v_w = []
        self.r_v_w.append((v_w_o[0], v_w_o[1], \
                           v_w_o[0] + v_dim_x, v_w_o[1] + v_dim_y))

        self.r_v_w.append((self.r_v_w[0][0] + PADDING + v_dim_x, v_w_o[1], \
                           self.r_v_w[0][0] + PADDING + 2 * v_dim_x, v_w_o[1] + v_dim_y))
        
        self.r_v_w.append((self.r_v_w[1][0] + PADDING + v_dim_x, v_w_o[1], \
                           self.r_v_w[1][0] + PADDING + 2 * v_dim_x, v_w_o[1] + v_dim_y))

        self.text_x = a_w_x - STATUS_X - m_w_x - 2 *PADDING - 3 * (v_dim_x + PADDING)

        main_x = PADDING * 2 + a_w_x
        main_y = PADDING * 3 + a_w_y + status_y

        # set windows and root parameters; only do this once controlled by set_window
        if self.set_window:
            self.root = Tk()
            self.root.title("Snakes ...")
            self.root.geometry(f"{main_x}x{main_y}")
            self.root.configure(background = 'white')

            self.aw = Canvas(self.root, width = a_w_x, height = a_w_y, bg = 'grey')
            self.aw.pack(fill = BOTH, expand = YES)
            
            self.label_SMB = []
            pause_SMB = ImageTk.PhotoImage(file = 'data/Pause.png')
            self.label_SMB.append(Label(self.aw, image = pause_SMB, bg = 'grey'))
            self.label_SMB[0].image = pause_SMB

            run_SMB = ImageTk.PhotoImage(file = 'data/Triangle.png')
            self.label_SMB.append(Label(self.aw, image = run_SMB, bg = 'grey'))
            self.label_SMB[1].image = run_SMB

        # set some other parameters
        self.snake_length = 10 # this is the maximum snake length
        self.wall_v = []
        self.wall_v.append([(int(0.10*self.cells_x), int(0.10*self.cells_y)), \
                            (int(0.10*self.cells_x), int(0.90*self.cells_y)), \
                            (int(0.80*self.cells_x), int(0.90*self.cells_y)), \
                            (int(0.80*self.cells_x), int(0.40*self.cells_y))])
        self.wall_v.append([(int(0.25*self.cells_x), int(0.25*self.cells_y)), \
                            (int(0.65*self.cells_x), int(0.25*self.cells_y))])
        self.brick_size = (int(0.8 * self.cell_dim_x), int(0.8 * self.cell_dim_y))
        self.myfont = "Calibri 12"

        # setup view_field
        self.view_field = []
        self.view_field.append((( 1, 0), ( 1, 1), ( 1,-1), ( 2, 0), ( 2, 1), ( 2,-1)))  # -> E
        self.view_field.append((( 1, 1), ( 1, 0), ( 0, 1), ( 2, 2), ( 2, 1), ( 1, 2)))  # -> SE
        self.view_field.append((( 0, 1), (-1, 1), ( 1, 1), ( 0, 2), (-1, 2), ( 1, 2)))  # -> S
        self.view_field.append(((-1, 1), ( 0, 1), (-1, 0), (-2, 2), (-1, 2), (-2, 1)))  # -> SW
        self.view_field.append(((-1, 0), (-1, 1), (-1,-1), (-2, 0), (-2, 1), (-2,-1)))  # -> W
        self.view_field.append(((-1,-1), (-1, 0), ( 0,-1), (-2,-2), (-2,-1), (-1,-2)))  # -> NW
        self.view_field.append((( 0,-1), ( 1,-1), (-1,-1), ( 0,-2), ( 1,-2), (-1,-2)))  # -> N
        self.view_field.append((( 1,-1), ( 0,-1), ( 1, 0), ( 2,-2), ( 1,-2), ( 2,-1)))  # -> NE

    def __repr__(self):
        ''' method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k,v in self.__dict__.items()) 
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
        return s

