#!/usr/bin/env python
'''  module snake_v5_2_control has the following class:
     - Control
         - MouseControl
'''
from tkinter import Button

from snake_v5_1_tools import BLUE, ORANGE, NOCOLOR, BWIDTH, Setup, Tools
from snake_v5_1_snake import mouse_action_snake, reset_snakes, snake_selection
from snake_v5_1_wall import (mouse_action_wall, set_color_wall,
                             clear_wall_selection)

setup = Setup()
tools = Tools()


class ButtonControl:
    '''   class to define button control, which are self explantory
          Button actions are equivalent to Space, (s, S), (w, W), (c, C),
          (m, M) and Escape. When the Exit window is pressed program is ended.
          Methods:
          - buttons
          - in_button_area
          - out_button_area
          - color_buttons
          - remove_color_buttons
          - _repr__
    '''
    def buttons(self):
        ''' definition and display of buttons
        '''
        print('button called', setup.b_w_o)

        self.setup_button = Button(self.root, text='Setup', relief='raised',
                                   width=BWIDTH, command=self.setup_status)
        self.setup_button.place(x=setup.b_w_o[0][0], y=setup.b_w_o[0][1])
        self.setup_button.bind('<Enter>', self.in_button_area)
        self.setup_button.bind('<Leave>', self.out_button_area)
        self.default_button_bg = self.setup_button.cget('background')

        self.pause_button = Button(self.root, text='Pause', relief='sunken',
                                   width=BWIDTH, command=self.pause_status,
                                   bg=self.select_color)
        self.pause_button.place(x=setup.b_w_o[1][0], y=setup.b_w_o[1][1])
        self.pause_button.bind('<Enter>', self.in_button_area)
        self.pause_button.bind('<Leave>', self.out_button_area)

        self.clear_button = Button(self.root, text='Clear', relief='raised',
                                   width=BWIDTH, command=self.clear_status)
        self.clear_button.place(x=setup.b_w_o[2][0], y=setup.b_w_o[2][1])
        self.clear_button.bind('<Enter>', self.in_button_area)
        self.clear_button.bind('<Leave>', self.out_button_area)

        self.monitor_button = Button(self.root, text='Monitor',
                                     relief='sunken', width=BWIDTH,
                                     command=self.monitor_status,
                                     bg=self.select_color)
        self.monitor_button.place(x=setup.b_w_o[3][0], y=setup.b_w_o[3][1])
        self.monitor_button.bind('<Enter>', self.in_button_area)
        self.monitor_button.bind('<Leave>', self.out_button_area)

        self.select_button = Button(self.root, text='Select', relief='raised',
                                    width=BWIDTH, command=self.select_status)
        self.select_button.place(x=setup.b_w_o[4][0], y=setup.b_w_o[4][1])
        self.select_button.bind('<Enter>', self.in_button_area)
        self.select_button.bind('<Leave>', self.out_button_area)

        self.exit_button = Button(self.root, text='Exit', relief='raised',
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

    def color_buttons(self):
        '''  Method to define and display the color buttons
        '''
        self.color_button = {}
        for color in setup.color_buttons:
            self.color_button[color] =\
                 Button(self.root,
                        bg=tools.hex_color(color),
                        activebackground=tools.hex_color(color),
                        borderwidth=2,
                        relief='raised',
                        width=1,
                        command=lambda x=color: self.color_select(x))
            self.color_button[color].place(x=setup.color_buttons[color][0],
                                           y=setup.color_buttons[color][1])
            self.color_button[color].bind('<Enter>', self.in_button_area)
            self.color_button[color].bind('<Leave>', self.out_button_area)

    def remove_color_buttons(self):
        '''  Methond to remove the color buttons
        '''
        for color in setup.color_buttons:
            self.color_button[color].destroy()

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


class MouseControl:
    '''  class to control the various mouse actions, such as click, double
         click and mouse moving. When in wall setup mode following mouse
         actions are defined in the module _walls:
          - Doubleclick on empty space: create new wall and vertex
          - Doubleclick on existing wall: select the wall for editing
          - Rightclick anywhere: deselect the wall
          - Singleclick in empty space: if a wall is selected create a
            new vertex
          - Doubleclicked on an existing vertex point and wall is selected:
            delete the vertex point
          (in module _walls)

          When in normal running mode. The following mouse actions are defined
          in the module _snake`:
          if mouse is pressed in the action window a snake will be created,
          if mouse is pressed on the head of an existing snake the snake will
          be deleted

          Methods:
          - __init__
          - mouse_click
          - mouse_double_click
          - mouse_action
          - __repr__
    '''
    def __init__(self):
        self.double_click = False
        self.aw.bind('<Button>', self.mouse_click)
        self.aw.bind('<Double-Button>', self.mouse_double_click)

    def mouse_click(self, event):
        '''  Method to delay mouse action to allow for a double click to occur
        '''
        self.aw.after(250, self.mouse_action, event)

    def mouse_double_click(self, event):
        '''  Method to set double_click flag
        '''
        self.double_click = True

    def mouse_action(self, event):
        '''  Method to action mouse event
        '''
        #   if not self.in_button:  # check if mouse position is not on a
        #   button. I am no longer sure why a check had to be made for this
        if self.setup:
            mouse_action_wall(event, self.double_click, self.cell)
            #  if a wall is selected in module wall, self.color will be set
            #  to the color of the selected wall otherwise it stay NOCOLOR
            self.color = NOCOLOR
            self.color = set_color_wall(self.color)
            self.color_select(self.color)

        elif self.pause and not self.double_click:
            mouse_action_snake(event, self.cell)

        #  else:
        #  print('mouse position is on button')

        self.double_click = False

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


class KeyControl:
    ''' class to control to key stroke entries, following are defined:
        Escape      - leave program
        b, B        - change border color to blue
        o, O        - change border color to orange
        Space       - toggle between pause and run
        c, C        - clear all snakes
        m, M        - select or desect monitor display
        s, S        - select snake - toggle through
        w, W        - select or deselect wall setup mode
        Left arrow  - not yet implemented
        Right arrow - not yet implemented

        Methods:
        - __init__
        - key_action
        - __repr__
    '''
    def __init__(self):
        self.root.bind('<Key>', self.key_action)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_program)
        self.mroot.protocol('WM_DELETE_WINDOW', self.exit_program)

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

    def __repr__(self):
        '''  method to represent the contents of this class
        '''
        s = ''.join('{} = {}\n'.format(k, v) for k, v in self.__dict__.items())
        s = ('\n{self.__module__}/{self.__class__.__name__}:\n'.
             format(self=self))+s
        return s


class Control(MouseControl, ButtonControl, KeyControl):
    '''  class Control supported by classes MouseControl, ButtonControl and
         KeyControl

         Methods:
         -   __init__
         -   setup_status
         -   pause_status
         -   clear_status
         -   select_status
         -   monitor_status
         -   color_select
         -   exit_program
         -   __repr__
    '''
    def __init__(self, root, mroot, aw, mw, cell):
        self.run = True
        self.pause = True
        self.left = False
        self.right = False
        self.monitor = True
        self.bcolor = BLUE
        self.in_button = False
        self.select_color = 'yellow'
        self.setup = False
        self.root = root
        self.mroot = mroot
        self.aw = aw
        self.mw = mw
        self.cell = cell
        self.color = NOCOLOR
        MouseControl.__init__(self)
        KeyControl.__init__(self)

    def setup_status(self):
        ''' Method to switch on or off setup_wall
        '''
        self.setup = not self.setup

        if self.setup:
            self.setup_button.config(relief='sunken', bg=self.select_color)
            self.pause_status()
            reset_snakes(self.cell)
            self.color_buttons()
            self.color = NOCOLOR
            self.color_select(self.color)

        else:
            self.setup_button.config(relief='raised',
                                     bg=self.default_button_bg)
            clear_wall_selection()
            self.remove_color_buttons()

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

        if self.monitor:
            self.monitor_button.config(relief='sunken', bg=self.select_color)

        else:
            self.monitor_button.config(relief='raised',
                                       bg=self.default_button_bg)

    def color_select(self, color):
        '''  Method to select color, if self.color is NOCOLOR then pressing
             a color buttons has no effect
        '''
        for _ in setup.color_buttons:
            self.color_button[_].config(relief='raised')

        if self.color in setup.color_buttons:
            assert (color in setup.color_buttons), "assert on valid colors"
            self.color_button[color].config(borderwidth=2, relief='solid')
            self.color = set_color_wall(color)

        else:
            pass

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
