#!/usr/bin/env python
'''     Snake around                   
                                               
        python version 3.6                      
                                               
        snake movement on a surface                 
                                                
        For more information read the           
        readme.txt!                             
                                                
        Author: Bruno Vermeulen                 
        bruno_vermeulen2001@yahoo.com           
'''
import sys
import tkinter
from time import time
from tkinter import Tk, Canvas, BOTH, YES, Label
from PIL import Image, ImageTk

import snake_tk_mod_v1
from snake_tk_mod_v1 import (SnakeObject, WallObject, Cell, Control, plot_grid_walls, init_walls, init_cells, mouse_pressed, 
                             move_randomly, reset_snakes, display_text, plot_snakes, plot_monitor, plot_status,
                             randomvector, hex_color
                            )
from snake_tk_conf import SnakeSetup

def main():
    ''' Main program of snake
    '''
    global setup, debug_stats # set to global to have access at interrupt
    ''' initialise the global snake set up paramaters
    '''

    setup = SnakeSetup()
    print(repr(setup))

    root = Tk()
    root.title("Snakes ...")
    root.geometry(f"{setup.main_x}x{setup.main_y}")
    root.configure(background = 'white')

    setup = SnakeSetup()
    print(repr(setup))

    ''' initialise the local variables
    '''
    reset_snakes()
    init_cells()
    init_walls()
    debug_stats = [0, 0, 0, 0]

    aw = Canvas(root, width = setup.a_w_x, height = setup.a_w_y, bg = 'grey')
    aw.pack(fill = BOTH, expand = YES)
    cntrl = Control()

    root.bind_all('<Key>', cntrl.key_action)
    root.bind_all( "<Button-1>", cntrl.mouse_action)
    plot_monitor(aw)
#   plot_status(aw, cntrl.pause)
    display_text(aw, 0)

    '''run indefinetaly while run is true
    '''
    start = time()

    while cntrl.run:
        ''' when program is paused you can create new snakes or delete existing ones by clicking the mouse on the action window
            if the program is not paused the snakes move around randomly
        '''
        if cntrl.pause:
            ''' set status to pause
            '''
            SMB = ImageTk.PhotoImage(setup.pause_png)
            label = Label(aw, image = SMB, bg = 'grey')
            label.place(x = setup.r_status_window[0] , y = setup.r_status_window[1])

        else:
            ''' set status to run
            '''
            SMB = ImageTk.PhotoImage(setup.run_png)
            label = Label(aw, image = SMB, bg = 'grey')
            label.place(x = setup.r_status_window[0] , y = setup.r_status_window[1])

            ''' move all the snakes randomly snakes randomly
            '''
            debug_stats = move_randomly(debug_stats)
#           print(debug_stats)
        
        ''' clear screen, plot grid, display walls and snakes
        '''
#       plot_status(aw, cntrl.pause)
        plot_grid_walls(aw, cntrl.bcolor)
        plot_snakes(aw)
        plot_monitor(aw)
        display_text(aw, 1000 * (time()- start))
    
        ''' update the screen and display at rate fps
        '''
        root.update()
#       root.after(int(1000/setup.fps))
        aw.delete("all")

    root.destroy()
    sys.exit
    print('debug_stats:',debug_stats)

    return

if __name__ == '__main__':
    main() 
