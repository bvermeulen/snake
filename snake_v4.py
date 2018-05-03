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
from time import time

# import snake_v4_tools
from snake_v4_tools import ( SnakeSetup, init_cells, plot_grid_walls, 
                             plot_monitor, plot_status, display_text
                           )
# import snake_v4_wall
from snake_v4_wall import  ( init_walls )

import snake_v4_control
from snake_v4_control import Control

import snake_v4_snake as sm
from snake_v4_snake import ( move_randomly, plot_snakes, show_snake_vision, 
                             reset_snakes
                           )
def main():
    ''' Main program of snake
    '''
    global setup, cntrl, debug_stats, cell, wall, elapsed_time # set to global to have access at interrupt
    ''' initialise the global snake set up paramaters
    '''
    setup = SnakeSetup(set_window = True)
    print(repr(setup))

    ''' initialise the local variables
    '''
    cell = init_cells()
    wall = init_walls(cell)
    reset_snakes(cell)
    debug_stats = [0, 0, 0, 0, 0]

    cntrl = Control(cell)
    cntrl.buttons(setup.root)
    setup.root.bind_all('<Key>', cntrl.key_action)
    setup.root.bind_all( "<Button-1>", cntrl.mouse_action)
    setup.root.protocol('WM_DELETE_WINDOW', cntrl.exit_program)
    setup.mroot.protocol('WM_DELETE_WINDOW', cntrl.exit_program)
    margin = 1
    start_time = time()

    '''run indefinetaly while run is true
    '''
    while cntrl.run:
        ''' when program is paused you can create new snakes or delete existing ones by clicking the mouse on the action window
            if the program is not paused the snakes move around randomly
        '''
        if cntrl.pause:
            ''' wait on user input 
            '''
            pass

        else:
            ''' move all the snakes randomly snakes randomly
            '''
            debug_stats = move_randomly(cell, debug_stats)
        
        ''' clear screen, plot grid, display walls and snakes
        '''
        time_elapsed = int( 1000 * (time() - start_time))
        plot_status(setup.label_SMB, cntrl.pause)
        plot_grid_walls(setup.aw, wall, cntrl.bcolor)
        plot_snakes(setup.aw)
        show_snake_vision(setup.aw, cell)
#       display_text(setup.aw, time_elapsed, _snake_number, _snake_select)
        display_text(setup.aw, time_elapsed, sm.snake_number, sm.snake_select)
    
        # update the screen and display at rate fps
        if cntrl.monitor:
            plot_monitor(setup.mw, cell)
        else:
            setup.root.after(int(1000/setup.fps))

        setup.root.update()
        setup.mroot.update()
        setup.aw.delete("all")
        setup.mw.delete("all")

    setup.root.destroy()
    setup.mroot.destroy()
    sys.exit
    debug_stats[4] = int(time_elapsed/ 1000)
    print('debug_stats:', debug_stats)

    return setup, cntrl, debug_stats, cell, wall, time_elapsed

if __name__ == '__main__':

    setup, cntrl, debug_stats, cell, wall, time_elapsed = main() 
