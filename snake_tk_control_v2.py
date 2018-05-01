#!/usr/bin/env python
''' module for the tkinter control
    Class: 
            - Control
'''
from tkinter import Button

from snake_tk_tools_v2 import BLUE, ORANGE, SnakeSetup, BWIDTH
from snake_tk_mod_v2 import mouse_pressed, reset_snakes, snake_select

setup   = SnakeSetup()

class Control:
    ''' control class with following functions:
        Escape      - leave program
        b           - change border color to blue
        o           - change border color to orange
        Space       - toggle between pause and run
        c           - clear all snakes
        m           - toggle between display and omit monitor
        s           - select snake - toggle through
        Left arrow  - not yet implemented
        Right arrow - not yet implemented

        When paused, if mouse is pressed in the action window a snake will be created, if mouse is pressed on 
        the head of an existing snake the snake will be deleted
        
        When Exit window is pressed leave program

        Functions:
        -   __init__
        -   key_action
        -   buttons
        -   in_button_area
        -   out_button_area
        -   pause_status
        -   clear_status
        -   select_status
        -   monitor_status
        -   mouse_action
        -   exit_program
        -   __repr__
    '''
    def __init__(self):
        self.run = True
        self.pause = True
        self.left = False
        self.right = False
        self.monitor = True
        self.bcolor = BLUE
        self.in_button = False

    def key_action(self, event):
        ''' function to determine action on key events
        '''
        print('event: ', event.keysym, event.char)
        if event.keysym == 'Escape':     # stop running when Quit event type is triggered
            self.run = False

        elif event.char == 'b':          # b - change border color to blue
            self.bcolor = BLUE
        
        elif event.char == 'o':          # o - change border color to orange
            self.bcolor = ORANGE
 
        elif event.keysym == 'space':    # Space - change pause status, pause is not pause
            self.pause_status()

        elif event.char == 'c':          # c - clear screen and pause
            self.clear_status()

        elif event.char == 'm':          # m - change monitor status
            self.monitor_status()

        elif event.char == 's':          # s - select a snake
            self.select_status()

        elif event.keysym == 'Left':     # LEFT arrow - move left
            self.left = True

        elif event.keysym == 'Right':    # RIGHT arrow - move right
            self.right = True

    def buttons(self, root):
        ''' definition of buttons: setup, pause, clear, select
        '''
        print('button called', setup.b_w_o)
        self.setup_button = Button(root, text='Setup', relief = 'raised', width = BWIDTH, state = 'disabled')
        self.setup_button.place( x = setup.b_w_o[0][0], y = setup.b_w_o[0][1])
        self.setup_button.bind("<Enter>", self.in_button_area)
        self.setup_button.bind("<Leave>", self.out_button_area)

        self.pause_button = Button(root, text='Pause', relief = 'sunken', width = BWIDTH, command = self.pause_status)
        self.pause_button.place( x = setup.b_w_o[1][0], y = setup.b_w_o[1][1])
        self.pause_button.bind("<Enter>", self.in_button_area)
        self.pause_button.bind("<Leave>", self.out_button_area)

        self.clear_button = Button(root, text='Clear', relief = 'raised', width = BWIDTH, command = self.clear_status)
        self.clear_button.place( x = setup.b_w_o[2][0], y = setup.b_w_o[2][1])
        self.clear_button.bind("<Enter>", self.in_button_area)
        self.clear_button.bind("<Leave>", self.out_button_area)

        self.monitor_button = Button(root, text='Monitor', relief = 'sunken', width = BWIDTH, command = self.monitor_status)
        self.monitor_button.place( x = setup.b_w_o[3][0], y = setup.b_w_o[3][1])
        self.monitor_button.bind("<Enter>", self.in_button_area)
        self.monitor_button.bind("<Leave>", self.out_button_area)

        self.select_button = Button(root, text='Select', relief = 'raised', width = BWIDTH, command = self.select_status)
        self.select_button.place( x = setup.b_w_o[4][0], y = setup.b_w_o[4][1])
        self.select_button.bind("<Enter>", self.in_button_area)
        self.select_button.bind("<Leave>", self.out_button_area)

        self.exit_button = Button(root, text='Exit', relief = 'raised', width = BWIDTH, command = self.exit_program)
        self.exit_button.place( x = setup.b_w_o[5][0], y = setup.b_w_o[5][1])
        self.exit_button.bind("<Enter>", self.in_button_area)
        self.exit_button.bind("<Leave>", self.out_button_area)

    def in_button_area(self, event):
        ''' set in_button to True, mouse pointer is in a button area
        '''
        self.in_button = True
    
    def out_button_area(self, event):
        ''' set in_button to False, mouse pointer has left a button area
        '''
        self.in_button = False

    def pause_status(self):
        '''
            Method to toggle between pause and run
        '''
        self.pause = not self.pause
       
        if self.pause:
            self.pause_button.config(relief = 'sunken')
 
        else:
            self.pause_button.config(relief = 'raised')

    def clear_status(self):
        ''' Method to clear the screen
        '''
        if not self.pause:
            self.pause_status()
        reset_snakes()

    def select_status(self):
        ''' Method to toggle selected snake
        '''
        snake_select()

    def monitor_status(self):
        ''' Method to toggle monitor window on and off
        '''
        self.monitor = not self.monitor

        if self.monitor:
            self.monitor_button.config(relief = 'sunken')
 
        else:
            self.monitor_button.config(relief = 'raised')
		
    def mouse_action(self, event):
        ''' if event is mouse clicked then determine the location through cell indices
            first check in mouse point is not on a button though
        '''
        if self.pause and not self.in_button:
            _m_pos = (int((event.x - setup.a_w_o[0]) / setup.cell_dim_x), \
                      int((event.y - setup.a_w_o[1])/ setup.cell_dim_y))

            if mouse_pressed(_m_pos):
                pass

    def exit_program(self):
        ''' exit program on pressing the X (close window)
        '''
        self.run = False

    def __repr__(self):
        ''' method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k,v in self.__dict__.items()) 
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.format(self=self))+s
        return s

