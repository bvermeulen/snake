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

import snake_tk_mod_v1
from snake_tk_mod_v1 import (SnakeObject, WallObject, Cell, Control, plot_grid_walls, init_walls, init_cells, mouse_pressed, 
                             move_randomly, reset_snakes, display_text, plot_snakes, plot_monitor, plot_status, show_vision,
                             randomvector, hex_color
                            )
from snake_tk_conf import SnakeSetup

def main():
    ''' Main program of snake
    '''
    global setup, cntrl, debug_stats # set to global to have access at interrupt
    ''' initialise the global snake set up paramaters
    '''
    setup = SnakeSetup(set_window = True)
    print(repr(setup))

    ''' initialise the local variables
    '''
    reset_snakes()
    init_cells()
    init_walls()
    debug_stats = [0, 0, 0, 0]

    cntrl = Control()

    setup.root.bind_all('<Key>', cntrl.key_action)
    setup.root.bind_all( "<Button-1>", cntrl.mouse_action)
    setup.root.protocol('WM_DELETE_WINDOW', cntrl.exit_program)

    '''run indefinetaly while run is true
    '''
    start_time = time()
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
            debug_stats = move_randomly(debug_stats)
        
        ''' clear screen, plot grid, display walls and snakes
        '''
        plot_status(setup.label_SMB, cntrl.pause)
        plot_grid_walls(setup.aw, cntrl.bcolor)
        plot_snakes(setup.aw)
        show_vision(setup.aw, cntrl.snake_select)
        display_text(setup.aw, 1000 * (time()- start_time))
    
        ''' update the screen and display at rate fps
        '''
        if cntrl.monitor:
            plot_monitor(setup.aw)

        else:
            setup.root.after(int(1000/setup.fps))

        setup.root.update()
        setup.aw.delete("all")

    setup.root.destroy()
    sys.exit
    print('debug_stats:',debug_stats)

    return setup, cntrl, debug_stats

if __name__ == '__main__':
    setup, cntrldebug, debug_stats = main() 
