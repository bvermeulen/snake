#!/usr/bin/env python
'''     Snake around

        python version 3.6

        snake movement on a surface

        For more information read the
        readme.txt!

        Author: Bruno Vermeulen
        bruno_vermeulen2001@yahoo.com
'''
from time import time

import snake_v4_2_tools    # noqa F401 - required for debugging
from snake_v4_2_tools import (BLACK, Setup, init_cells, plot_window,
                              plot_monitor, plot_status, display_text)
import snake_v4_2_wall     # noqa F401 - required for debugging
from snake_v4_2_wall import init_walls, plotlist_walls

import snake_v4_2_control  # noqa F401 - required for debugging
from snake_v4_2_control import Control

import snake_v4_2_snake as sm
from snake_v4_2_snake import (move_randomly, show_snake_vision,
                              plotlist_snakes, reset_snakes)


def main():
    '''  Main program of snake
    '''
    global setup, cntrl, debug_stats, cell, wall, elapsed_time, plotlist, p, vw
    # set to global to have access at interrupt
    '''  initialise the snake set up paramaters
    '''
    setup = Setup(set_window=True)
    print(repr(setup))

    '''  initialise the local variables
    '''
    cell = init_cells()
    wall = init_walls(cell)
    reset_snakes(cell)

    debug_stats = [0, 0, 0, 0, 0]
    cntrl = Control(setup.mw, cell)
    cntrl.buttons(setup.root)
    setup.root.bind_all('<Key>', cntrl.key_action)
    setup.root.bind_all('<Button-1>', cntrl.mouse_action)
    setup.root.protocol('WM_DELETE_WINDOW', cntrl.exit_program)
    setup.mroot.protocol('WM_DELETE_WINDOW', cntrl.exit_program)
    start_time = time()

    '''  get the plotlist for wall
    '''
    plotlist = []
    plotlist_walls(plotlist)
    plot_window(canvas=setup.aw, rectangle=setup.r_action_window,
                background=BLACK, border_color=cntrl.bcolor,
                plotlist=plotlist)

    '''  run indefinetaly while run is true
    '''
    while cntrl.run:
        '''  when program is paused you can create new snakes or delete
             existing ones by clicking the mouse on the action window
             if the program is not paused the snakes move around randomly
        '''
        if cntrl.pause:
            '''  wait on user input
            '''
            pass

        else:
            '''  move all the snakes randomly snakes randomly
            '''
            debug_stats = move_randomly(cell, debug_stats)

        '''  update the screens
        '''
        time_elapsed = int(1000 * (time() - start_time))
        # to change color of border plot_evironment must be placed in loop
        plotlist = []
        plotlist_snakes(plotlist)
        p = plot_window(canvas=setup.aw, rectangle=setup.r_action_window,
                        background='', border_color=cntrl.bcolor,
                        plotlist=plotlist)

        plot_status(setup.label_SMB, cntrl.pause)
        vw = show_snake_vision(setup.aw, cell)
        display_text(setup.aw, time_elapsed, sm.snake_number, sm.snake_select)

        if cntrl.monitor:
            plot_monitor(setup.mroot, setup.mw, cell)

        #  update the screen and display at rate fps
        setup.root.after(int(1000 / setup.fps))
        setup.root.update()
        setup.aw.delete(*p, *vw)

    setup.root.destroy()
    setup.mroot.destroy()
    debug_stats[4] = int(time_elapsed / 1000)
    print('debug_stats:', debug_stats)

    return setup, cntrl, debug_stats, cell, wall, time_elapsed, plotlist


if __name__ == '__main__':
    setup, cntrl, debug_stats, cell, wall, time_elapsed, plotlist = main()
