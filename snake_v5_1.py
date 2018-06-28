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

import snake_v5_1_tools    # noqa F401 - required for debugging
from snake_v5_1_tools import (Setup, Monitor, Tools,)
import snake_v5_1_wall     # noqa F401 - required for debugging
from snake_v5_1_wall import init_walls, plot_walls

import snake_v5_1_control  # noqa F401 - required for debugging
from snake_v5_1_control import Control

import snake_v5_1_snake as sm
from snake_v5_1_snake import (move_randomly, show_snake_vision,
                              plot_snakes, reset_snakes)


def main():
    '''  Main program of snake
    '''
    global setup, cntrl, monitor, debug_stats, cell, wall, elapsed_time
    # set to global to have access at interrupt
    '''  initialise the snake set up paramaters
    '''
    setup = Setup(set_window=True)
    print(repr(setup))

    '''  initialise the local variables
    '''
    tools = Tools()
    cell = tools.init_cells()
    reset_snakes(cell)

    debug_stats = [0, 0, 0, 0, 0]
    cntrl = Control(setup.aw, setup.mw, cell)
    cntrl.buttons(setup.root)
    setup.root.bind('<Key>', cntrl.key_action)
    setup.aw.bind('<Button>', cntrl.mouse_click)
    setup.aw.bind('<Double-Button>', cntrl.mouse_double_click)
    setup.root.protocol('WM_DELETE_WINDOW', cntrl.exit_program)
    setup.mroot.protocol('WM_DELETE_WINDOW', cntrl.exit_program)
    start_time = time()
    wall = init_walls(cell)
    monitor = Monitor(setup.mroot, setup.mw, cell)
    m_counter = 0
    monitor_clear = 200

    '''  run indefinetaly while run is true
    '''
    while cntrl.run:
        '''  when program is paused you can create new snakes or delete
             existing ones by clicking the mouse on the action window
             if the program is not paused the snakes move around randomly
        '''
        plot_walls(setup.aw, cntrl.bcolor, cntrl.setup)

        if cntrl.setup:
            '''  if setup wait on user input to setup the walls
            '''
            pass

        else:
            '''  otherwise handle the snake ...
            '''
            if cntrl.pause:
                '''  wait on user input and create/ delete snakes
                '''
                pass

            else:
                '''  move all the snakes randomly snakes randomly
                '''
                debug_stats = move_randomly(cell, debug_stats)

            plot_snakes(setup.aw, cntrl.bcolor)
            show_snake_vision(setup.aw, cell)
            if sm.snake_number == 0 and not cntrl.pause:
                cntrl.pause_status()

        '''  update status and text and show the screen
        '''
        time_elapsed = int(1000 * (time() - start_time))
        tools.plot_status(setup.label_SMB, cntrl.pause)
        tools.display_text(setup.aw, time_elapsed, sm.snake_number,
                           sm.snake_select)

        if cntrl.monitor:
            monitor.plot()
            print('m_counter is: ', m_counter, end='\r')
            m_counter = monitor.clear(m_counter, monitor_clear)

        #  update the screen and display at rate fps
        # setup.root.after(int(1000 / setup.fps))
        setup.root.update()
        setup.aw.delete("all")

    setup.root.destroy()
    setup.mroot.destroy()
    debug_stats[4] = int(time_elapsed / 1000)
    print('debug_stats:', debug_stats)

    return setup, cntrl, monitor, debug_stats, cell, wall, time_elapsed


if __name__ == '__main__':
    setup, cntrl, monitor, debug_stats, cell, wall, time_elapsed = main()
