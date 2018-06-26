#!/usr/bin/env python
'''  module snake_v5_1_control has the following class:
     - Control
'''
from time import time

from tkinter import Button

from snake_v5_1_tools import BLUE, ORANGE, BWIDTH, Setup
from snake_v5_1_snake import mouse_action_snake, reset_snakes, snake_selection
from snake_v5_1_wall import mouse_action_wall

setup = Setup()


class Control:
    '''  control class with following functions:
         Escape      - leave program
         b           - change border color to blue
         o           - change border color to orange
         Space       - toggle between pause and run
         c           - clear all snakes
         m           - toggle between display and omit monitor
         s           - select snake - toggle through
         Left arrow  - not yet implemented
         Right arrow - not yet implemented

         When paused, if mouse is pressed in the action window a snake will be
         created, if mouse is pressed on the head of an existing snake the
         snake will be deleted

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
    def __init__(self, aw, mw, cell):
        self.run = True
        self.pause = True
        self.left = False
        self.right = False
        self.monitor = True
        self.bcolor = BLUE
        self.in_button = False
        self.select_color = 'yellow'
        self.setup = False
        self.aw = aw
        self.mw = mw
        self.cell = cell
        self.double_click = False
        self.n = 0

    def key_action(self, event):
        '''  function to determine action on key events
        '''
        if event.keysym == 'Escape':    # stop running when Escase pressed
            self.run = False

        elif event.keysym == 'space':   # Space - toggle pause and run
            self.pause_status()

        elif event.keysym == 'Left':    # LEFT arrow - move left
            self.left = True

        elif event.keysym == 'Right':   # RIGHT arrow - move right
            self.right = True

        elif event.char in ('b', 'B'):  # b - change border color to blue
            self.bcolor = BLUE

        elif event.char in ('o', 'O'):  # o - change border color to orange
            self.bcolor = ORANGE

        elif event.char in ('w', 'W'):  # w = setup walles
            self.setup_status()

        elif event.char in ('c', 'C'):  # c - clear screen and pause
            self.clear_status()

        elif event.char in ('m', 'M'):  # m - change monitor status
            self.monitor_status()

        elif event.char in ('s', 'S'):  # s - select a snake
            self.select_status()

    def buttons(self, root):
        ''' definition of buttons: setup, pause, clear, select
        '''
        print('button called', setup.b_w_o)

        self.setup_button = Button(root, text='Setup', relief='raised',
                                   width=BWIDTH, command=self.setup_status)
        self.setup_button.place(x=setup.b_w_o[0][0], y=setup.b_w_o[0][1])
        self.setup_button.bind('<Enter>', self.in_button_area)
        self.setup_button.bind('<Leave>', self.out_button_area)
        self.default_button_bg = self.setup_button.cget('background')

        self.pause_button = Button(root, text='Pause', relief='sunken',
                                   width=BWIDTH, command=self.pause_status,
                                   bg=self.select_color)
        self.pause_button.place(x=setup.b_w_o[1][0], y=setup.b_w_o[1][1])
        self.pause_button.bind('<Enter>', self.in_button_area)
        self.pause_button.bind('<Leave>', self.out_button_area)

        self.clear_button = Button(root, text='Clear', relief='raised',
                                   width=BWIDTH, command=self.clear_status)
        self.clear_button.place(x=setup.b_w_o[2][0], y=setup.b_w_o[2][1])
        self.clear_button.bind('<Enter>', self.in_button_area)
        self.clear_button.bind('<Leave>', self.out_button_area)

        self.monitor_button = Button(root, text='Monitor', relief='sunken',
                                     width=BWIDTH, command=self.monitor_status)
        self.monitor_button.place(x=setup.b_w_o[3][0], y=setup.b_w_o[3][1])
        self.monitor_button.bind('<Enter>', self.in_button_area)
        self.monitor_button.bind('<Leave>', self.out_button_area)

        self.select_button = Button(root, text='Select', relief='raised',
                                    width=BWIDTH, command=self.select_status)
        self.select_button.place(x=setup.b_w_o[4][0], y=setup.b_w_o[4][1])
        self.select_button.bind('<Enter>', self.in_button_area)
        self.select_button.bind('<Leave>', self.out_button_area)

        self.exit_button = Button(root, text='Exit', relief='raised',
                                  width=BWIDTH, command=self.exit_program)
        self.exit_button.place(x=setup.b_w_o[5][0], y=setup.b_w_o[5][1])
        self.exit_button.bind('<Enter>', self.in_button_area)
        self.exit_button.bind('<Leave>', self.out_button_area)

    def in_button_area(self, event):
        '''  set in_button to True, mouse pointer is in a button area
        '''
        self.in_button = True

    def out_button_area(self, event):
        '''  set in_button to False, mouse pointer has left a button area
        '''
        self.in_button = False

    def setup_status(self):
        ''' Method to switch on or off setup_wall
        '''
        self.setup = not self.setup

        if self.setup:
            self.setup_button.config(relief='sunken', bg=self.select_color)
            self.pause_status()
            reset_snakes(self.cell)

        else:
            self.setup_button.config(relief='raised',
                                     bg=self.default_button_bg)

    def pause_status(self):
        '''  Method to toggle between pause and run
        '''
        if self.setup:
            self.pause = False
        else:
            self.pause = not self.pause

        if self.pause:
            self.pause_button.config(relief='sunken', bg=self.select_color)

        else:
            self.pause_button.config(relief='raised',
                                     bg=self.default_button_bg)

    def clear_status(self):
        '''  Method to clear the screen
        '''
        if not self.pause:
            self.pause_status()
        reset_snakes(self.cell)

    def select_status(self):
        '''  Method to toggle selected snake
        '''
        snake_selection()

    def monitor_status(self):
        '''  Method to toggle monitor window on and off
        '''
        self.monitor = not self.monitor
        self.mw.delete("all")

        if self.monitor:
            self.monitor_button.config(relief='sunken')
            for i in range(setup.cells_x):
                for j in range(setup.cells_y):
                    self.cell[i][j].plot = True

        else:
            self.monitor_button.config(relief='raised')

    def mouse_action(self, event):
        '''  Method to action mouse event
        '''
        if not self.in_button:  # check if mouse position is not on a button

            if self.setup:
                mouse_action_wall(event, self.double_click, self.cell)

            elif self.pause and not self.double_click:
                mouse_action_snake(event, self.cell)

        else:
            print('mouse position is on button')

        self.double_click = False


    def mouse_click(self, event):
        '''  Method to delay mouse action to allow for a double click to occur
        '''
        self.aw.after(250, self.mouse_action, event)


    def mouse_double_click(self, event):
        '''  Method to set double_click flag
        '''
        self.double_click = True


    def exit_program(self):
        '''  exit program on pressing the X (close window)
        '''
        self.run = False

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s
