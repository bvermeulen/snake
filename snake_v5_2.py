#!/usr/bin/env python
'''     Snake around

        python version 3.6
        version: snake_5_2

        snake movement on a surface

        For more information read the
        readme.txt!

        Author: Bruno Vermeulen
        bruno_vermeulen2001@yahoo.com
'''
from time import time
import snake_v5_2_tools    # noqa F401 - required for debugging
from snake_v5_2_tools import Setup, Monitor, Tools
import snake_v5_2_wall     # noqa F401 - required for debugging
from snake_v5_2_wall import init_walls, plot_walls, wall_pass_logger

import snake_v5_2_control  # noqa F401 - required for debugging
from snake_v5_2_control import Control

import snake_v5_2_snake as sm
from snake_v5_2_snake import (move_randomly, show_snake_vision,
                              plot_snakes, reset_snakes, snake_pass_logger)


def main():
    '''  Main program of snake
    '''
    global setup, cntrl, monitor, debug_stats, cell, elapsed_time
    # set to global to have access at interrupt
    '''  initialise the snake set up paramaters
    '''
    setup = Setup(set_window=True)
    setup.logger.info('-'*70)
    setup.logger.info(repr(setup))
    snake_pass_logger(setup.logger)
    wall_pass_logger(setup.logger)

    '''  initialise the local variables
    '''
    tools = Tools()
    cell = tools.init_cells()
    reset_snakes(cell)

    debug_stats = [0, 0, 0, 0, 0]
    cntrl = Control(setup.root, setup.mroot, setup.aw, setup.mw,
                    cell, setup.logger)
    monitor = Monitor(setup.mroot, setup.mw, cell)
    cntrl.buttons()
    init_walls(cell)
    m_counter = 0
    monitor_clear = 200
    start_time = time()

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
            m_counter = monitor.clear(m_counter, monitor_clear)

        #  update the screen and display at rate fps
        # setup.root.after(int(1000 / setup.fps))
        setup.root.update()
        setup.aw.delete("all")

    setup.root.destroy()
    setup.mroot.destroy()
    debug_stats[4] = int(time_elapsed / 1000)
    setup.logger.info(f'==> debug_stats: {debug_stats}')

    return setup, cntrl, monitor, debug_stats, cell, time_elapsed


if __name__ == '__main__':
    setup, cntrl, monitor, debug_stats, cell, time_elapsed = main()
