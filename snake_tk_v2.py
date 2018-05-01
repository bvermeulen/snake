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

from snake_tk_tools_v2 import SnakeSetup

import snake_tk_mod_v2
from snake_tk_mod_v2 import (plot_grid_walls, init_walls, init_cells, 
                             move_randomly, display_text, plot_snakes, 
                             plot_monitor, plot_status, show_vision,
                             reset_snakes   
                            )
from snake_tk_control_v2 import Control


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
    debug_stats = [0, 0, 0, 0, 0]

    cntrl = Control()
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
            debug_stats = move_randomly(debug_stats)
        
        ''' clear screen, plot grid, display walls and snakes
        '''
        time_elapsed = int( 1000 * (time() - start_time))
        plot_status(setup.label_SMB, cntrl.pause)
        plot_grid_walls(setup.aw, cntrl.bcolor)
        plot_snakes(setup.aw)
        show_vision(setup.aw)
        display_text(setup.aw, time_elapsed)
    
        ''' update the screen and display at rate fps
        '''
        if cntrl.monitor:
            plot_monitor(setup.mw)
            margin = 2
        else:
            margin = 1
            setup.root.after(int(1000/setup.fps))

        setup.root.update()
        setup.mroot.update()
        setup.aw.delete("all")
        setup.mw.delete("all")
        display_text(setup.aw, time_elapsed)

    setup.root.destroy()
    setup.mroot.destroy()
    sys.exit
    debug_stats[4] = int(time_elapsed/ 1000)
    print('debug_stats:',debug_stats)

    return setup, cntrl, debug_stats

if __name__ == '__main__':
    setup, cntrldebug, debug_stats = main() 
